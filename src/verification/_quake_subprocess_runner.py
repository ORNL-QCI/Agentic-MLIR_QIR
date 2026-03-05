#!/usr/bin/env python3
"""Standalone QuakeRunner helper executed as a subprocess.

Reads Quake MLIR from stdin, samples with cudaq, prints JSON to stdout.
Running in a separate process avoids the shared-LLVM conflict between
cudaq and qirrunner when they are loaded in the same Python process.

Usage:
    python _quake_subprocess_runner.py <shots>  < circuit.mlir
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import cudaq  # noqa: E402 — must come after sys.path tweak
from src.dialects.quake_dialect import QuakeDialect  # noqa: E402


def build_and_sample(mlir_code: str, shots: int) -> dict:
    d = QuakeDialect()
    circuit = d.parse_circuit(mlir_code)

    kernel = cudaq.make_kernel()
    q = kernel.qalloc(circuit.num_qubits)

    one_q = {
        "h":   kernel.h,   "x":   kernel.x,
        "y":   kernel.y,   "z":   kernel.z,
        "s":   kernel.s,   "t":   kernel.t,
        "sdg": kernel.sdg, "tdg": kernel.tdg,
    }
    param_q = {
        "rx": kernel.rx, "ry": kernel.ry,
        "rz": kernel.rz, "r1": kernel.r1,
    }

    def apply_gate(gate):
        name, qs, ps = gate.name, gate.qubits, gate.params
        if name in one_q:
            one_q[name](q[qs[0]])
        elif name in param_q:
            param_q[name](ps[0], q[qs[0]])
        elif name in ("cnot", "cx"):
            kernel.cx(q[qs[0]], q[qs[1]])
        elif name == "cz":
            kernel.cz(q[qs[0]], q[qs[1]])
        elif name == "swap":
            kernel.swap(q[qs[0]], q[qs[1]])
        elif name == "r1" and len(qs) == 2:
            kernel.cr1(ps[0], q[qs[0]], q[qs[1]])

    meas_values: dict = {}
    meas_count = 0
    has_meas = any(t == "measurement" for t, _ in circuit.ordered_ops)

    for op_type, op in circuit.ordered_ops:
        if op_type == "gate":
            apply_gate(op)
        elif op_type == "measurement":
            mv = kernel.mz(q[op.qubit])
            meas_values[meas_count] = mv
            meas_count += 1
        elif op_type == "conditional":
            mv = meas_values.get(op.condition_measurement_idx)
            if mv is not None and op.then_gates:
                def _make_body(gates):
                    def body():
                        for g in gates:
                            apply_gate(g)
                    return body
                kernel.c_if(mv, _make_body(op.then_gates))

    if not has_meas:
        kernel.mz(q)

    sr = cudaq.sample(kernel, shots_count=shots)
    return {bs: sr[bs] for bs in sr}


if __name__ == "__main__":
    shots = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    mlir_code = sys.stdin.read()
    dist = build_and_sample(mlir_code, shots)
    print(json.dumps(dist))
