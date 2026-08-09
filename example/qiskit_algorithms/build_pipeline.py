#!/usr/bin/env python3
"""Build Grover's and Shor's algorithm circuits from IBM Quantum's own
Qiskit tutorials, and push them through the full

    Qiskit circuit -> QASM -> Quake MLIR -> QIR

pipeline, keeping every intermediate artifact on disk. Both conversion
steps go through this project's own existing tooling, not any ad-hoc
or hand-written conversion:

  * QASM -> Quake MLIR uses ``agentic_mlir_qir.frontends.qasm_frontend
    .qasm_to_mlir`` (the same frontend the CLI/UI already expose).
  * Quake MLIR -> QIR uses ``translate.py``'s deterministic pass,
    invoked exactly as a user would from the command line.

Sources (circuit-building logic reproduced faithfully from the
tutorials; hardware/runtime-service/plotting cells are omitted since
they need IBM Quantum hardware access and are irrelevant to
translation testing):
  - Grover: https://quantum.cloud.ibm.com/docs/en/tutorials/grovers-algorithm
  - Shor:   https://quantum.cloud.ibm.com/docs/en/tutorials/shors-algorithm

Note: the installed Qiskit is 0.46.3, older than the tutorials'
target version, so ``MCMTGate`` (Qiskit >=1.0) is used here as
``MCMT`` (0.46.3), identical constructor signature.

Usage:
    python3 example/qiskit_algorithms/build_pipeline.py
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from math import floor, log
from pathlib import Path
from typing import List

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
import qiskit.qasm2 as qasm2
import qiskit.qpy as qpy

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = Path(__file__).resolve().parent
TRANSLATE_PY = REPO_ROOT / "translate.py"

# Deliberately restricted to a subset of the gate vocabulary the paper's
# existing 68-circuit benchmark already validates end-to-end (Table II:
# Hadamard, PauliX/Y/Z, S, T, RX, RY, RZ, CNOT, CZ, SWAP). Three broader
# bases were tried first and each surfaced a real, pre-existing bug in
# shared project infrastructure, not anything specific to these two
# circuits:
#   1. ccx/cswap: the installed CUDA-Q 0.13.0 kernel-builder's .x()/
#      .cswap() only accept a single control, not the Python list of
#      controls agentic_mlir_qir's QASM->Quake frontend passes for
#      Toffoli/CSWAP (`AttributeError: 'list' object has no attribute
#      'mlirValue'`).
#   2. r1/u1/p/sdg/tdg: gate *counts* matched perfectly (35/35) end to
#      end, but the measured distributions diverged badly between the
#      QIR-side and MLIR-side simulators (TVD similarity 0.251, far
#      below the 95% threshold) -- a phase-convention bug somewhere in
#      how one of the two backends executes these gates, invisible to
#      gate-count comparison alone.
#   3. swap: the installed qiskit.qasm2's bundled qelib1.inc definition
#      does not actually define "swap", so re-parsing our own emitted
#      QASM fails with `'swap' is not defined in this scope`, even
#      though the QASM text includes "qelib1.inc" and uses the gate
#      exactly as OpenQASM 2.0 specifies it.
# All three are out of scope for adding benchmark circuits; staying
# within the remaining proven gate set sidesteps them without touching
# that code. (SWAP still appears in the deterministic-path benchmark
# via the hand-written Catalyst/Quake circuits, which construct MLIR
# directly and never round-trip through qiskit.qasm2.)
BASIS_GATES = ["h", "x", "y", "z", "s", "t", "rx", "ry", "rz", "cx", "cz"]


def build_grover_circuit() -> QuantumCircuit:
    """Grover's algorithm, 3 qubits, marked states {011, 100}.

    Reproduces the tutorial's "Simulator Example" cell verbatim
    (oracle, grover_operator, optimal iteration count, H + power +
    measure_all); the IBM Runtime hardware/sampler cells are omitted.
    """
    from qiskit.circuit.library import MCMT, ZGate, GroverOperator

    def grover_oracle(marked_states):
        if not isinstance(marked_states, list):
            marked_states = [marked_states]
        num_qubits = len(marked_states[0])
        qc = QuantumCircuit(num_qubits)
        for target in marked_states:
            rev_target = target[::-1]
            zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
            if zero_inds:
                qc.x(zero_inds)
            qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
            if zero_inds:
                qc.x(zero_inds)
        return qc

    marked_states = ["011", "100"]
    oracle = grover_oracle(marked_states)
    # GroverOperator is the 0.46.3 class-based equivalent of the
    # >=1.0 functional grover_operator() used by the tutorial.
    grover_op = GroverOperator(oracle)

    optimal_num_iterations = math.floor(
        math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2 ** grover_op.num_qubits)))
    )

    qc = QuantumCircuit(grover_op.num_qubits)
    qc.h(range(grover_op.num_qubits))
    qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
    qc.measure_all()
    return qc


def build_shor_circuit() -> QuantumCircuit:
    """Shor's algorithm order-finding circuit, N=15, a=2.

    Reproduces the tutorial's circuit-building cell verbatim (the
    M2mod15/M4mod15 SWAP-based compiled modular-multiplication gates,
    the control/target register setup, and the inverse QFT). The
    classical continued-fractions post-processing and the tutorial's
    own illustrative example counts are intentionally NOT reproduced
    here -- this script obtains its own real measurement statistics by
    actually running the circuit through this project's pipeline.
    """
    from qiskit.circuit.library import QFT

    def M2mod15():
        b = 2
        U = QuantumCircuit(4)
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
        U = U.to_gate()
        U.name = f"M_{b}"
        return U

    def M4mod15():
        b = 4
        U = QuantumCircuit(4)
        U.swap(1, 3)
        U.swap(0, 2)
        U = U.to_gate()
        U.name = f"M_{b}"
        return U

    def a2kmodN(a, k, N):
        for _ in range(k):
            a = int(pow(a, 2, N))
        return a

    N, a = 15, 2
    num_target = floor(log(N - 1, 2)) + 1  # 4
    num_control = 2 * num_target  # 8

    b_list = [a2kmodN(2, k, 15) for k in range(num_control)]

    control = QuantumRegister(num_control, name="C")
    target = QuantumRegister(num_target, name="T")
    output = ClassicalRegister(num_control, name="out")
    circuit = QuantumCircuit(control, target, output)

    circuit.x(num_control)  # target register -> |1>

    for k, qubit in enumerate(control):
        circuit.h(k)
        b = b_list[k]
        if b == 2:
            circuit.compose(M2mod15().control(), qubits=[qubit] + list(target), inplace=True)
        elif b == 4:
            circuit.compose(M4mod15().control(), qubits=[qubit] + list(target), inplace=True)
        # else: b == 1 -> identity, skip (matches tutorial's "continue")

    circuit.compose(QFT(num_control, inverse=True), qubits=control, inplace=True)
    circuit.measure(control, output)
    return circuit


def run_pipeline(name: str, build_fn, translate_args: List[str]) -> dict:
    out_dir = OUT_ROOT / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Stage 1: Qiskit circuit object.
    qc = build_fn()
    (out_dir / "01_circuit.txt").write_text(str(qc.draw(output="text")))
    with open(out_dir / "01_circuit.qpy", "wb") as fh:
        qpy.dump(qc, fh)

    # Transpile to the gate basis the QASM->Quake frontend accepts.
    transpiled = transpile(qc, basis_gates=BASIS_GATES, optimization_level=1)

    # Stage 2: QASM 2 text.
    qasm_text = qasm2.dumps(transpiled)
    (out_dir / "02_circuit.qasm").write_text(qasm_text)

    # Stage 3: QASM -> Quake MLIR, via this project's own frontend.
    sys.path.insert(0, str(REPO_ROOT))
    from agentic_mlir_qir.frontends.qasm_frontend import qasm_to_mlir

    mlir_text = qasm_to_mlir(qasm_text)
    (out_dir / "03_quake.mlir").write_text(mlir_text)

    # Stage 4: Quake MLIR -> QIR + gate/TVD test, via translate.py's
    # deterministic pass -- the same CLI a user would invoke by hand.
    proc = subprocess.run(
        [sys.executable, str(TRANSLATE_PY), str(out_dir / "03_quake.mlir"),
         *translate_args, "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=900,
    )
    if proc.returncode not in (0, 1):  # 1 = translated but verification failed
        raise RuntimeError(f"translate.py crashed for {name}:\n{proc.stderr}")
    result = json.loads(proc.stdout)
    (out_dir / "04_result.json").write_text(json.dumps(result, indent=2))
    (out_dir / "04_qir.ll").write_text(result.get("qir", ""))

    return result


def main():
    # Grover (3 qubits, 53 gates) comfortably fits the qir-runner
    # subprocess's 120s timeout even at probs mode's 100K QIR-side
    # shots, so it gets the exact/near-noise-free comparison.
    #
    # Shor (12 qubits, 390 gates) does not: probs mode's 100K shots
    # exceeded the 120s timeout, silently falling back to a mock QIR
    # result (`qir_is_mock: True`) that trivially disagreed with the
    # real MLIR-side simulation. Default shots mode (1024) avoided the
    # timeout but 1024 shots spread over the circuit's real ~16-outcome
    # support was noisy enough to dip below the 95% threshold (91.8%);
    # 8000 shots reliably clears it (97.2%, both sides converging on
    # the same 16 outcomes) while still finishing in well under 120s.
    plan = [
        ("grover", build_grover_circuit, ["--mode", "probs"]),
        ("shor", build_shor_circuit, ["--shots", "8000"]),
    ]
    for name, build_fn, translate_args in plan:
        print(f"=== {name} ===")
        result = run_pipeline(name, build_fn, translate_args)
        gc = result.get("gate_comparison", {})
        ver = result.get("verification", {})
        print(f"  success: {result.get('success')}")
        print(f"  gate match: {gc.get('matches')}  ({gc.get('mlir_total')}/{gc.get('qir_total')} gates)")
        print(f"  TVD similarity: {ver.get('similarity')}")
        print(f"  passes threshold: {ver.get('similarity_passes')}")
        print()


if __name__ == "__main__":
    main()
