"""OpenQASM (2.0 / 3.0) -> Quake MLIR frontend.

This frontend lets the translator accept OpenQASM input without adding a new
MLIR dialect or a hand-written QASM parser. It reuses two existing tools:

1. **Qiskit** parses the OpenQASM text into a ``QuantumCircuit``
   (``qiskit.qasm2`` for 2.0, ``qiskit.qasm3`` for 3.0).
2. **CUDA-Q** (``cudaq.make_kernel``) rebuilds the circuit gate-by-gate and
   emits **Quake-dialect MLIR** (``str(kernel)``).

The resulting Quake MLIR is exactly the dialect the existing
``MLIRParser`` (Quake) + ``QIRGenerator`` already translate to QIR, so the
QASM path flows through the same downstream framework as native MLIR input.

The heavy backends (qiskit, qiskit-qasm3-import, cuda-quantum) are imported
lazily so importing this module never pulls them in until a conversion runs.
Install them with the optional ``qasm`` extra::

    pip install 'agentic-mlir-qir[qasm]'
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, Dict, List

if TYPE_CHECKING:  # pragma: no cover - typing only
    from qiskit import QuantumCircuit


class UnsupportedQASMGateError(ValueError):
    """Raised when a QASM gate has no CUDA-Q kernel-builder mapping."""


_OPENQASM_RE = re.compile(r"^\s*OPENQASM\s+(\d+)(?:\.\d+)?\s*;", re.MULTILINE)


def _first_significant_line(source: str) -> str:
    """Return the first non-blank, non-comment line (lowercased markers kept)."""
    for raw in source.splitlines():
        line = raw.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        return line
    return ""


def is_qasm(source: str) -> bool:
    """Return ``True`` if ``source`` looks like an OpenQASM program.

    Detection is based on the ``OPENQASM <version>;`` header being the first
    significant (non-blank, non-comment) line.
    """
    if not source or not source.strip():
        return False
    return _first_significant_line(source).upper().startswith("OPENQASM")


def detect_qasm_version(source: str) -> str:
    """Return the OpenQASM major version as ``"2"`` or ``"3"``.

    Raises
    ------
    ValueError
        If ``source`` has no recognisable ``OPENQASM`` header.
    """
    match = _OPENQASM_RE.search(source or "")
    if not match:
        raise ValueError("Not an OpenQASM program: missing 'OPENQASM <version>;' header")
    return match.group(1)


def qasm_to_circuit(source: str) -> "QuantumCircuit":
    """Parse OpenQASM source into a Qiskit ``QuantumCircuit``.

    Uses ``qiskit.qasm2`` for 2.x and ``qiskit.qasm3`` for 3.x. The latter
    needs the optional ``qiskit-qasm3-import`` package.
    """
    version = detect_qasm_version(source)
    if version == "2":
        try:
            import qiskit.qasm2 as qasm2
        except ImportError as exc:  # pragma: no cover - depends on extra
            raise RuntimeError(
                "OpenQASM 2 support requires qiskit. "
                "Install with: pip install 'agentic-mlir-qir[qasm]'"
            ) from exc
        return qasm2.loads(source)

    if version == "3":
        try:
            import qiskit.qasm3 as qasm3
        except ImportError as exc:  # pragma: no cover - depends on extra
            raise RuntimeError(
                "OpenQASM 3 support requires qiskit and qiskit-qasm3-import. "
                "Install with: pip install 'agentic-mlir-qir[qasm]'"
            ) from exc
        try:
            return qasm3.loads(source)
        except Exception as exc:  # qiskit raises MissingOptionalLibraryError
            if "qiskit_qasm3_import" in str(exc) or "qiskit-qasm3-import" in str(exc):
                raise RuntimeError(
                    "OpenQASM 3 loading requires the 'qiskit-qasm3-import' package. "
                    "Install with: pip install 'agentic-mlir-qir[qasm]'"
                ) from exc
            raise

    raise ValueError(f"Unsupported OpenQASM version: {version}")


# ---------------------------------------------------------------------------
# Qiskit gate name -> CUDA-Q kernel-builder action.
#
# Each handler receives (kernel, qubit_refs, wires, params) and applies the
# corresponding op. ``wires`` are integer qubit indices into ``qubit_refs``.
# ---------------------------------------------------------------------------

# Single-qubit, no parameters.
_SINGLE: Dict[str, str] = {
    "h": "h", "x": "x", "y": "y", "z": "z",
    "s": "s", "t": "t", "sdg": "sdg", "tdg": "tdg",
}
# Single-qubit, one rotation parameter.
_SINGLE_PARAM: Dict[str, str] = {
    "rx": "rx", "ry": "ry", "rz": "rz",
    "p": "r1", "u1": "r1",  # phase gate == r1 up to global phase
}
# Two-qubit controlled, no parameters: (control, target).
_CONTROLLED: Dict[str, str] = {
    "cx": "cx", "cnot": "cx", "cy": "cy", "cz": "cz", "ch": "ch",
}
# Two-qubit controlled, one rotation parameter: (angle, control, target).
_CONTROLLED_PARAM: Dict[str, str] = {
    "crx": "crx", "cry": "cry", "crz": "crz",
    "cp": "cr1", "cu1": "cr1",
}
# Gates we silently skip (no effect on the Quake program / handled elsewhere).
_SKIP = {"measure", "barrier", "id", "delay"}


def _apply_gate(kernel, qubit_refs, name: str, wires: List[int], params: List[float]) -> None:
    """Apply a single Qiskit-named gate to the CUDA-Q kernel builder."""
    if name in _SKIP:
        return

    if name in _SINGLE:
        getattr(kernel, _SINGLE[name])(qubit_refs[wires[0]])
        return

    if name in _SINGLE_PARAM:
        getattr(kernel, _SINGLE_PARAM[name])(params[0], qubit_refs[wires[0]])
        return

    if name in _CONTROLLED:
        getattr(kernel, _CONTROLLED[name])(qubit_refs[wires[0]], qubit_refs[wires[1]])
        return

    if name in _CONTROLLED_PARAM:
        getattr(kernel, _CONTROLLED_PARAM[name])(
            params[0], qubit_refs[wires[0]], qubit_refs[wires[1]]
        )
        return

    if name == "swap":
        kernel.swap(qubit_refs[wires[0]], qubit_refs[wires[1]])
        return

    if name in ("ccx", "toffoli"):
        # Multi-controlled X: controls list + target.
        kernel.x([qubit_refs[wires[0]], qubit_refs[wires[1]]], qubit_refs[wires[2]])
        return

    if name in ("cswap", "fredkin"):
        kernel.cswap(qubit_refs[wires[0]], qubit_refs[wires[1]], qubit_refs[wires[2]])
        return

    if name == "u3":
        kernel.u3(params[0], params[1], params[2], qubit_refs[wires[0]])
        return

    raise UnsupportedQASMGateError(
        f"OpenQASM gate '{name}' is not supported by the QASM->Quake frontend. "
        f"Supported gates: {sorted(supported_gates())}."
    )


def supported_gates() -> set:
    """Return the set of Qiskit gate names the frontend can lower to Quake."""
    return (
        set(_SINGLE) | set(_SINGLE_PARAM) | set(_CONTROLLED)
        | set(_CONTROLLED_PARAM)
        | {"swap", "ccx", "toffoli", "cswap", "fredkin", "u3"}
        | _SKIP
    )


def circuit_to_quake_mlir(circuit: "QuantumCircuit") -> str:
    """Rebuild ``circuit`` as a CUDA-Q kernel and return its Quake MLIR text.

    All qubits are measured (``mz``) at the end, matching the existing
    all-wire measurement convention used elsewhere in the verification path.
    """
    try:
        import cudaq
    except ImportError as exc:  # pragma: no cover - depends on extra
        raise RuntimeError(
            "QASM->Quake conversion requires CUDA-Q (cuda-quantum). "
            "Install with: pip install 'agentic-mlir-qir[qasm]'"
        ) from exc

    n = circuit.num_qubits
    kernel = cudaq.make_kernel()
    qubits = kernel.qalloc(n)

    for inst in circuit.data:
        op = inst.operation
        name = op.name.lower()
        wires = [circuit.find_bit(q).index for q in inst.qubits]
        params = [float(p) for p in op.params]
        _apply_gate(kernel, qubits, name, wires, params)

    kernel.mz(qubits)
    return str(kernel)


def qasm_to_mlir(source: str) -> str:
    """Convert OpenQASM 2.0/3.0 source to Quake-dialect MLIR text.

    This is the single entry point used by the CLI, the package API, and the
    Streamlit UI. The returned MLIR is consumed unchanged by the existing
    deterministic ``MLIRParser`` (Quake) + ``QIRGenerator`` pipeline.
    """
    circuit = qasm_to_circuit(source)
    return circuit_to_quake_mlir(circuit)
