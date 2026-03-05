#!/usr/bin/env python3
"""Standalone QIRRunner helper executed as a subprocess.

Reads QIR (.ll) code from stdin, runs it with qirrunner, prints JSON
bitstring distribution to stdout.

Running in a separate process avoids the shared-LLVM segfault that occurs
when qirrunner._native and catalyst/JAX (XLA) are both loaded in the same
Python process.

Usage:
    python _qir_subprocess_runner.py <shots> < circuit.ll
"""

import json
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple


def qubit_ptr(i: int) -> str:
    return "null" if i == 0 else f"inttoptr (i64 {i} to %Qubit*)"


def result_ptr(i: int) -> str:
    return "null" if i == 0 else f"inttoptr (i64 {i} to %Result*)"


def _ensure_measurements(qir_code: str) -> Tuple[str, int]:
    """Inject terminal mz+record_output calls if the QIR has none."""
    m = re.search(r'"required_num_results"="(\d+)"', qir_code)
    num_results = int(m.group(1)) if m else 0
    if num_results > 0:
        return qir_code, num_results

    m = re.search(r'"required_num_qubits"="(\d+)"', qir_code)
    num_qubits = int(m.group(1)) if m else 0
    if num_qubits == 0:
        return qir_code, 0

    mz_lines = [
        f"  call void @__quantum__qis__mz__body(%Qubit* {qubit_ptr(i)}, %Result* {result_ptr(i)})"
        for i in range(num_qubits)
    ]
    record_lines = [
        f"  call void @__quantum__rt__array_record_output(i64 {num_qubits}, i8* null)"
    ] + [
        f"  call void @__quantum__rt__result_record_output(%Result* {result_ptr(i)}, i8* null)"
        for i in range(num_qubits)
    ]
    injected = "\n".join(mz_lines + record_lines) + "\n"

    if "  ret void" in qir_code:
        last = qir_code.rfind("  ret void")
        modified = qir_code[:last] + injected + qir_code[last:]
    else:
        modified = qir_code + "\n" + injected

    modified = re.sub(
        r'"required_num_results"="\d+"',
        f'"required_num_results"="{num_qubits}"',
        modified,
    )
    return modified, num_qubits


def _parse_outputs(outputs: List, num_results: int) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for out_obj in outputs:
        msg = str(out_obj)
        if "OUTPUT\tARRAY\t" not in msg:
            continue
        bits: List[str] = re.findall(r"OUTPUT\tRESULT\t([01])", msg)
        if len(bits) == num_results:
            bs = "".join(bits)
            dist[bs] = dist.get(bs, 0) + 1
    return dist


if __name__ == "__main__":
    shots = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    qir_code = sys.stdin.read()

    import qirrunner  # noqa: E402 — isolated in subprocess

    runnable, num_results = _ensure_measurements(qir_code)
    if num_results == 0:
        print(json.dumps({}))
        sys.exit(1)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".ll", delete=False) as f:
        f.write(runnable)
        path = f.name

    try:
        outputs: List = []
        qirrunner.run(path, shots=shots, output_fn=outputs.append)
        dist = _parse_outputs(outputs, num_results)
        print(json.dumps(dist))
    finally:
        Path(path).unlink(missing_ok=True)
