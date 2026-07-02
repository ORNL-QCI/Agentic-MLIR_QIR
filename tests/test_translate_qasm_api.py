"""Tests for the high-level ``translate_qasm`` package API.

End-to-end: OpenQASM source -> Quake MLIR (frontend) -> existing deterministic
MLIRParser + QIRGenerator -> QIR. Requires the ``qasm`` extra (qiskit,
qiskit-qasm3-import, cuda-quantum).
"""

from __future__ import annotations

import pytest

pytest.importorskip("agentic_mlir_qir.frontends.qasm_frontend")
import agentic_mlir_qir as amq

translate_qasm = amq.translate_qasm
TranslateResult = amq.TranslateResult


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


def test_translate_qasm_v2_produces_qir():
    res = translate_qasm(BELL_V2)
    assert isinstance(res, TranslateResult)
    assert res.success is True
    assert res.dialect == "quake"
    assert res.qir and "__quantum__" in res.qir
    assert res.source_format == "openqasm2"


def test_translate_qasm_v3_produces_qir():
    res = translate_qasm(BELL_V3)
    assert res.success is True
    assert res.dialect == "quake"
    assert res.source_format == "openqasm3"


def test_translate_qasm_rejects_non_qasm():
    with pytest.raises(ValueError):
        translate_qasm("module @run { func.func @f() { return } }")


def test_translate_qasm_empty_raises():
    with pytest.raises(ValueError):
        translate_qasm("   ")
