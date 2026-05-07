"""Deterministic QIR assembler: operation list -> valid LLVM IR.

Takes gate operations (extracted from LLM JSON output) and assembles
complete, syntactically valid QIR using the existing QIRTemplates.
"""

import logging
import re
from typing import Optional

from .templates import QIRTemplates

logger = logging.getLogger(__name__)

# Gate name normalisation: common LLM variants -> canonical QIR function suffix
_GATE_ALIASES = {
    "h": "h",
    "hadamard": "h",
    "x": "x",
    "paulix": "x",
    "pauli_x": "x",
    "y": "y",
    "pauliy": "y",
    "pauli_y": "y",
    "z": "z",
    "pauliz": "z",
    "pauli_z": "z",
    "cx": "cnot",
    "cnot": "cnot",
    "cz": "cz",
    "swap": "swap",
    "s": "s",
    "t": "t",
    "rx": "rx",
    "ry": "ry",
    "rz": "rz",
    "mz": "mz",
    "measure": "mz",
}

# Regex for LLVM call form: call void @__quantum__qis__<gate>__body(...)
# Uses greedy .* to handle nested parens in inttoptr(i64 N to %Qubit*).
# Allows an optional trailing LLVM attribute group (e.g. " #1") and optional
# trailing comment — models sometimes emit these without breaking semantics.
_CALL_RE = re.compile(
    r"call\s+void\s+@__quantum__qis__(\w+?)__body\((.+?)\)\s*(?:#\d+\s*)?(?:;.*)?$",
    re.IGNORECASE | re.MULTILINE,
)

# Regex for extracting qubit / result pointers from call arguments.
# Accepts any integer width (i32, i64, i8, ...) since smaller models sometimes
# emit i32 indices; QIR convention is i64 but the semantics are equivalent.
_QUBIT_PTR_RE = re.compile(
    r"%Qubit\*\s*(null|inttoptr\s*\(i\d+\s+(\d+)\s+to\s+%Qubit\*\))"
)
_RESULT_PTR_RE = re.compile(
    r"%Result\*\s*(null|inttoptr\s*\(i\d+\s+(\d+)\s+to\s+%Result\*\))"
)

# Regex for double param in call
_DOUBLE_PARAM_RE = re.compile(r"double\s+([\d.eE+\-]+)")

# Parameterised gates (take a double before the qubit)
_PARAM_GATES = {"rx", "ry", "rz"}


class ParsedOp:
    """A single parsed gate operation."""

    __slots__ = ("gate", "qubits", "param")

    def __init__(self, gate: str, qubits: list[int], param: Optional[float] = None):
        self.gate = gate      # canonical QIR suffix (e.g. "h", "cnot")
        self.qubits = qubits  # qubit indices
        self.param = param    # rotation angle (for rx/ry/rz)

    def __repr__(self) -> str:
        p = f", param={self.param}" if self.param is not None else ""
        return f"ParsedOp({self.gate}, qubits={self.qubits}{p})"


def _parse_call_form(line: str) -> Optional[ParsedOp]:
    """Parse an LLVM IR call statement into a ParsedOp."""
    m = _CALL_RE.search(line)
    if not m:
        return None

    gate_suffix = m.group(1).lower()
    args_str = m.group(2)

    # Skip measurement calls (handled separately)
    if gate_suffix == "mz":
        return None

    # Extract qubit indices from pointer arguments
    qubits = []
    for qm in _QUBIT_PTR_RE.finditer(args_str):
        if qm.group(1) == "null":
            qubits.append(0)
        else:
            qubits.append(int(qm.group(2)))

    # Extract parameter if present
    param = None
    pm = _DOUBLE_PARAM_RE.search(args_str)
    if pm and gate_suffix in _PARAM_GATES:
        param = float(pm.group(1))

    return ParsedOp(gate_suffix, qubits, param)


def _parse_short_form(line: str) -> Optional[ParsedOp]:
    """Parse short-form operation like 'h 0', 'cnot 0 1', 'rx 1.5708 0'."""
    parts = line.strip().split()
    if not parts:
        return None

    gate_raw = parts[0].lower().strip("_")
    gate = _GATE_ALIASES.get(gate_raw, gate_raw)

    # Skip measurements
    if gate in ("mz", "measure"):
        return None

    if gate in _PARAM_GATES and len(parts) >= 3:
        try:
            param = float(parts[1])
            qubits = [int(q) for q in parts[2:]]
            return ParsedOp(gate, qubits, param)
        except ValueError:
            return None
    else:
        try:
            qubits = [int(q) for q in parts[1:]]
            return ParsedOp(gate, qubits)
        except ValueError:
            return None


def parse_operations(operations: list[str]) -> list[ParsedOp]:
    """Parse a list of operation strings (either LLVM call form or short form).

    Returns a list of ParsedOp, skipping measurement ops (those are added
    automatically for all qubits).
    """
    parsed = []
    for op_str in operations:
        op_str = op_str.strip()
        if not op_str:
            continue
        # Try LLVM call form first
        op = _parse_call_form(op_str)
        if op is None and not op_str.startswith("call "):
            # Try short form
            op = _parse_short_form(op_str)
        if op is not None:
            parsed.append(op)
    return parsed


def assemble_qir_from_operations(
    operations: list[str],
    module_name: str = "quantum_module",
    num_qubits: Optional[int] = None,
) -> str:
    """Assemble valid QIR LLVM IR from a list of gate operation strings.

    Args:
        operations: List of operation strings in either:
            - LLVM call form: "call void @__quantum__qis__h__body(%Qubit* null)"
            - Short form: "h 0", "cnot 0 1", "rx 1.5708 0"
        module_name: Module ID for the QIR header.
        num_qubits: Override qubit count. If None, inferred from operations.

    Returns:
        Complete, valid QIR LLVM IR string.
    """
    t = QIRTemplates()

    # Parse all operations
    ops = parse_operations(operations)
    if not ops:
        logger.warning("No gate operations found to assemble")
        return ""

    # Infer qubit count from operations
    max_qubit = 0
    for op in ops:
        if op.qubits:
            max_qubit = max(max_qubit, max(op.qubits))
    inferred_qubits = max_qubit + 1
    n_qubits = num_qubits if num_qubits is not None else inferred_qubits
    n_results = n_qubits  # measure all qubits

    # ── Header ──
    header = t.HEADER.format(module_id=module_name, source_filename=module_name)

    # ── Gate operations ──
    gate_lines = []
    gate_declarations = {}  # func_name -> (num_qubits, has_param)

    for op in ops:
        func_name = f"__quantum__qis__{op.gate}__body"

        if op.param is not None and len(op.qubits) == 1:
            # Parameterised single-qubit gate
            qubit_ptr = t.get_qubit_pointer(op.qubits[0])
            gate_lines.append(
                t.PARAM_GATE.format(
                    function_name=func_name,
                    param=f"{op.param:.6e}",
                    qubit_ptr=qubit_ptr,
                )
            )
            gate_declarations[func_name] = (1, True)
        elif len(op.qubits) == 1:
            qubit_ptr = t.get_qubit_pointer(op.qubits[0])
            gate_lines.append(
                t.SINGLE_QUBIT_GATE.format(
                    function_name=func_name,
                    qubit_ptr=qubit_ptr,
                )
            )
            gate_declarations[func_name] = (1, False)
        elif len(op.qubits) == 2:
            control_ptr = t.get_qubit_pointer(op.qubits[0])
            target_ptr = t.get_qubit_pointer(op.qubits[1])
            gate_lines.append(
                t.TWO_QUBIT_GATE.format(
                    function_name=func_name,
                    control_ptr=control_ptr,
                    target_ptr=target_ptr,
                )
            )
            gate_declarations[func_name] = (2, False)
        else:
            logger.warning("Skipping %d-qubit gate %s (unsupported)", len(op.qubits), op.gate)

    # ── Measurements (all qubits) ──
    meas_lines = []
    for i in range(n_results):
        qubit_ptr = t.get_qubit_pointer(i)
        result_ptr = t.get_result_pointer(i)
        meas_lines.append(
            t.MEASUREMENT.format(qubit_ptr=qubit_ptr, result_ptr=result_ptr)
        )

    # ── Output recording ──
    output_lines = [
        f"  call void @__quantum__rt__array_record_output(i64 {n_results}, i8* null)"
    ]
    for i in range(n_results):
        result_ptr = t.get_result_pointer(i)
        output_lines.append(
            t.RESULT_OUTPUT.format(result_ptr=result_ptr)
        )

    # ── Entry function ──
    body = "\n".join(
        ["  call void @__quantum__rt__initialize(i8* null)"]
        + gate_lines
        + meas_lines
        + output_lines
        + ["  ret void"]
    )
    entry = f"define void @main() #0 {{\nentry:\n{body}\n}}\n"

    # ── Declarations ──
    gate_decl_lines = []
    for func_name, (nq, has_param) in gate_declarations.items():
        param_sig = t.get_gate_param_signature(func_name, nq, has_param)
        gate_decl_lines.append(
            t.GATE_DECLARATION.format(function_name=func_name, params=param_sig)
        )
    gate_decls_str = "\n".join(gate_decl_lines)

    declarations = t.DECLARATIONS.format(
        gate_declarations=gate_decls_str,
        conditional_declarations="",
    )

    # ── Attributes ──
    attributes = t.ATTRIBUTES.format(num_qubits=n_qubits, num_results=n_results)

    # ── Metadata ──
    metadata = t.METADATA

    return f"{header}\n{entry}\n{declarations}\n{attributes}\n{metadata}"
