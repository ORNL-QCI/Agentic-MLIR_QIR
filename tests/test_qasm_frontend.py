"""Tests for the OpenQASM -> Quake MLIR frontend.

The frontend parses OpenQASM 2.0/3.0 with Qiskit, rebuilds the circuit as a
CUDA-Q kernel, and emits Quake-dialect MLIR that the existing deterministic
``MLIRParser`` + ``QIRGenerator`` pipeline already consumes.

These tests require the optional ``qasm`` extra (qiskit, qiskit-qasm3-import,
cuda-quantum). They are skipped if those backends are unavailable.
"""

from __future__ import annotations

import pytest

qasm_frontend = pytest.importorskip("agentic_mlir_qir.frontends.qasm_frontend")

is_qasm = qasm_frontend.is_qasm
detect_qasm_version = qasm_frontend.detect_qasm_version
qasm_to_circuit = qasm_frontend.qasm_to_circuit
circuit_to_quake_mlir = qasm_frontend.circuit_to_quake_mlir
qasm_to_mlir = qasm_frontend.qasm_to_mlir
UnsupportedQASMGateError = qasm_frontend.UnsupportedQASMGateError


BELL_V2 = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0]->c[0];
measure q[1]->c[1];
"""

BELL_V3 = """OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
h q[0];
cx q[0], q[1];
c[0] = measure q[0];
c[1] = measure q[1];
"""

MLIR_SAMPLE = """module @run {
  func.func public @jit_run() -> () { return }
}
"""


# --- is_qasm ---------------------------------------------------------------

def test_is_qasm_detects_v2_header():
    assert is_qasm(BELL_V2) is True


def test_is_qasm_detects_v3_header():
    assert is_qasm(BELL_V3) is True


def test_is_qasm_detects_header_after_comments_and_blank_lines():
    src = "// a comment\n\n   OPENQASM 2.0;\nqreg q[1];\n"
    assert is_qasm(src) is True


def test_is_qasm_rejects_mlir():
    assert is_qasm(MLIR_SAMPLE) is False


def test_is_qasm_rejects_empty():
    assert is_qasm("") is False
    assert is_qasm("   \n  ") is False


# --- detect_qasm_version ---------------------------------------------------

def test_detect_version_v2():
    assert detect_qasm_version(BELL_V2) == "2"


def test_detect_version_v3():
    assert detect_qasm_version(BELL_V3) == "3"


def test_detect_version_rejects_non_qasm():
    with pytest.raises(ValueError):
        detect_qasm_version(MLIR_SAMPLE)


# --- qasm_to_circuit -------------------------------------------------------

def test_qasm_to_circuit_v2_bell():
    qc = qasm_to_circuit(BELL_V2)
    assert qc.num_qubits == 2
    names = [inst.operation.name for inst in qc.data]
    assert "h" in names and "cx" in names


def test_qasm_to_circuit_v3_bell():
    qc = qasm_to_circuit(BELL_V3)
    assert qc.num_qubits == 2


# --- circuit_to_quake_mlir -------------------------------------------------

def test_circuit_to_quake_mlir_has_quake_markers():
    qc = qasm_to_circuit(BELL_V2)
    mlir = circuit_to_quake_mlir(qc)
    assert "quake.alloca" in mlir
    assert "!quake.veq" in mlir
    assert "quake.h" in mlir
    assert "quake.x" in mlir  # cx lowers to controlled-x


# --- qasm_to_mlir (end to end of the frontend) -----------------------------

def test_qasm_to_mlir_v2():
    mlir = qasm_to_mlir(BELL_V2)
    assert "quake.alloca" in mlir and "quake.h" in mlir


def test_qasm_to_mlir_v3():
    mlir = qasm_to_mlir(BELL_V3)
    assert "quake.alloca" in mlir and "quake.h" in mlir


def test_qasm_to_mlir_parametric_gate():
    src = (
        'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\n'
        "rx(0.7853981633974483) q[0];\n"
    )
    mlir = qasm_to_mlir(src)
    assert "quake.rx" in mlir


# --- error handling --------------------------------------------------------

def test_unsupported_gate_raises_with_gate_name():
    # 'u2' is a valid qelib1 gate (so Qiskit parses it) but has no CUDA-Q
    # kernel-builder mapping, so the frontend must reject it by name.
    src = (
        'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\n'
        "u2(0.1,0.2) q[0];\n"
    )
    with pytest.raises(UnsupportedQASMGateError) as exc:
        qasm_to_mlir(src)
    assert "u2" in str(exc.value)
