"""CLI integration tests for OpenQASM input auto-routing.

The CLI should detect ``.qasm`` files (and stdin starting with ``OPENQASM``),
convert them to Quake MLIR via the frontend, and then run the normal
deterministic translation path. Requires the ``qasm`` extra.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("agentic_mlir_qir.frontends.qasm_frontend")

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSLATE = REPO_ROOT / "translate.py"

BELL_V2 = (
    'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];\n'
    "h q[0];\ncx q[0],q[1];\nmeasure q[0]->c[0];\nmeasure q[1]->c[1];\n"
)
BELL_V3 = (
    'OPENQASM 3.0;\ninclude "stdgates.inc";\nqubit[2] q;\nbit[2] c;\n'
    "h q[0];\ncx q[0], q[1];\nc[0] = measure q[0];\nc[1] = measure q[1];\n"
)


def _run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(TRANSLATE), *args],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def test_cli_qasm2_file_produces_qir(tmp_path):
    f = tmp_path / "bell.qasm"
    f.write_text(BELL_V2)
    res = _run([str(f), "--no-verify", "--quiet"])
    assert res.returncode == 0, res.stderr
    assert "__quantum__" in res.stdout


def test_cli_qasm3_file_produces_qir(tmp_path):
    f = tmp_path / "bell3.qasm"
    f.write_text(BELL_V3)
    res = _run([str(f), "--no-verify", "--quiet"])
    assert res.returncode == 0, res.stderr
    assert "__quantum__" in res.stdout


def test_cli_qasm_via_stdin(tmp_path):
    res = _run(["-", "--no-verify", "--quiet"], stdin=BELL_V2)
    assert res.returncode == 0, res.stderr
    assert "__quantum__" in res.stdout
