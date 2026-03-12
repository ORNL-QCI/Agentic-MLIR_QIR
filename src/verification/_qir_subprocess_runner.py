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
    """Ensure ALL qubits are measured, matching qml.sample() all-wire behaviour.

    Even when the QIR already has some mz calls (e.g. mid-circuit measurements),
    we inject additional mz calls for any unmeasured qubits so that every shot
    produces a bitstring of length == num_qubits, consistent with the Catalyst
    runner which calls qml.sample() over all wires.
    """
    m = re.search(r'"required_num_qubits"="(\d+)"', qir_code)
    num_qubits = int(m.group(1)) if m else 0
    if num_qubits == 0:
        return qir_code, 0

    # Build qubit→result-slot map from existing mz calls
    result_of_qubit: dict = {}
    for mz_m in re.finditer(
        r'call void @__quantum__qis__mz__body\(%Qubit\*\s*([^,]+),\s*%Result\*\s*([^)]+)\)',
        qir_code,
    ):
        q_ptr = mz_m.group(1).strip()
        r_ptr = mz_m.group(2).strip()
        qi = 0 if q_ptr == 'null' else int(re.search(r'i64 (\d+)', q_ptr).group(1))
        ri = 0 if r_ptr == 'null' else int(re.search(r'i64 (\d+)', r_ptr).group(1))
        result_of_qubit[qi] = ri

    # Assign new result slots for any unmeasured qubits
    next_slot = max(result_of_qubit.values(), default=-1) + 1
    extra_mz = []
    for qi in range(num_qubits):
        if qi not in result_of_qubit:
            result_of_qubit[qi] = next_slot
            extra_mz.append(
                f"  call void @__quantum__qis__mz__body("
                f"%Qubit* {qubit_ptr(qi)}, %Result* {result_ptr(next_slot)})"
            )
            next_slot += 1

    total = next_slot  # == num_qubits

    # Record outputs in qubit-index order (matches qml.sample() wire order)
    record = [f"  call void @__quantum__rt__array_record_output(i64 {total}, i8* null)"] + [
        f"  call void @__quantum__rt__result_record_output(%Result* {result_ptr(result_of_qubit[i])}, i8* null)"
        for i in range(num_qubits)
    ]
    injected = "\n".join(extra_mz + record) + "\n"

    # Strip existing record_output calls (replaced by the full set above)
    modified = re.sub(
        r'[ \t]*call void @__quantum__rt__(?:array_record_output|result_record_output)\([^\n]*\)\n?',
        '',
        qir_code,
    )

    # Inject before the last ret void
    if "  ret void" in modified:
        last = modified.rfind("  ret void")
        modified = modified[:last] + injected + modified[last:]
    else:
        modified += "\n" + injected

    # Update required_num_results in the temporary copy
    modified = re.sub(
        r'"required_num_results"="\d+"',
        f'"required_num_results"="{total}"',
        modified,
    )

    return modified, total


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
