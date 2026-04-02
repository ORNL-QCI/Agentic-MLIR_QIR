#!/usr/bin/env python3
"""E4 — QIR Mutation Injection for Verification Pipeline Testing.

Injects deliberate errors into correct QIR (.ll) files to test whether
the verification pipeline (TVD + gate counting) detects them.

5 mutation types:
  1. gate_sub    — Gate substitution (h → x)
  2. qubit_swap  — Swap control/target on CNOT
  3. gate_del    — Delete one gate call
  4. param_perturb — Change rotation angle
  5. gate_insert — Insert a spurious gate

Usage:
  # Apply a single mutation and print mutated QIR to stdout
  python experiments/inject_mutations.py <QIR_FILE> <MUTATION_TYPE>

  # Run all mutations on a file and verify each
  python experiments/inject_mutations.py <QIR_FILE> --all --mlir <MLIR_FILE> [--mode shots|probs]

  # Batch: run all mutations on all circuits, output JSONL
  python experiments/inject_mutations.py --batch --mode probs
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Add project root to path
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))


def mutate_gate_substitution(qir: str) -> str:
    """Replace first h__body call with x__body."""
    return qir.replace(
        "@__quantum__qis__h__body",
        "@__quantum__qis__x__body",
        1,  # only first occurrence
    )


def mutate_qubit_swap(qir: str) -> str:
    """Swap control and target qubits on the first CNOT."""
    # Match: cnot__body(%Qubit* <ctrl>, %Qubit* <tgt>)
    pattern = (
        r'(call void @__quantum__qis__cnot__body\()'
        r'(%Qubit\* [^,]+), (%Qubit\* [^)]+)\)'
    )
    m = re.search(pattern, qir)
    if not m:
        return qir  # no CNOT found
    original = m.group(0)
    swapped = f"{m.group(1)}{m.group(3)}, {m.group(2)})"
    return qir.replace(original, swapped, 1)


def mutate_gate_deletion(qir: str) -> str:
    """Delete one CNOT call (the last one, to avoid breaking the first entanglement)."""
    lines = qir.split('\n')
    # Find last cnot line and remove it
    last_cnot_idx = None
    for i, line in enumerate(lines):
        if '__quantum__qis__cnot__body' in line:
            last_cnot_idx = i
    if last_cnot_idx is not None:
        lines.pop(last_cnot_idx)
    return '\n'.join(lines)


def mutate_param_perturbation(qir: str) -> str:
    """Change a rotation angle: find first rx/ry/rz call and alter the parameter.

    QIR rotation gates look like:
      call void @__quantum__qis__rx__body(double 0x3FE921FB54442D18, %Qubit* ...)
    We replace the double value with a different one.
    """
    pattern = r'(call void @__quantum__qis__r[xyz]__body\(double )(0x[0-9A-Fa-f]+|[\d.e+-]+)'
    m = re.search(pattern, qir)
    if not m:
        # No parametric gate — fall back to inserting a phase shift
        return mutate_gate_insertion(qir)
    original_val = m.group(2)
    # Replace with a clearly wrong value (pi instead of original)
    new_val = "0x400921FB54442D18"  # pi ≈ 3.14159
    return qir.replace(
        m.group(0),
        f"{m.group(1)}{new_val}",
        1,
    )


def mutate_gate_insertion(qir: str) -> str:
    """Insert a spurious Z gate before the first measurement."""
    lines = qir.split('\n')
    for i, line in enumerate(lines):
        if '__quantum__qis__mz__body' in line:
            # Insert Z gate on qubit 0 before this measurement
            z_call = '  call void @__quantum__qis__z__body(%Qubit* null)'
            lines.insert(i, z_call)
            break
    return '\n'.join(lines)


MUTATIONS = {
    'gate_sub': mutate_gate_substitution,
    'qubit_swap': mutate_qubit_swap,
    'gate_del': mutate_gate_deletion,
    'param_perturb': mutate_param_perturbation,
    'gate_insert': mutate_gate_insertion,
}

# Default circuits for batch mode
BATCH_CIRCUITS = [
    # (mlir_path, qir_will_be_generated)
    ("examples/mlir/bell_state.mlir", "Bell"),
    ("examples/mlir/ghz_state.mlir", "GHZ-3"),
    ("example/catalyst_mlir/code_ghz_5.mlir", "GHZ-5"),
    ("example/catalyst_mlir/code_ghz_10.mlir", "GHZ-10"),
    ("examples/mlir/parametric_rotation.mlir", "Parametric"),
    ("example/catalyst_mlir/code_random_circuit_658.mlir", "Random-658"),
    ("example/catalyst_mlir/code_random_circuit_3990.mlir", "Random-3990"),
]


def translate_to_qir(mlir_path: str) -> str:
    """Deterministic translation of MLIR to QIR."""
    from src.parsers.mlir_parser import MLIRParser
    from src.generators.qir_generator import QIRGenerator

    mlir_code = Path(mlir_path).read_text()
    circuit = MLIRParser().parse(mlir_code)
    return QIRGenerator().generate(circuit)


def verify_mutation(mlir_path: str, mutated_qir: str,
                    mode: str = "shots", shots: int = 1000) -> dict:
    """Run verification pipeline on mutated QIR."""
    import src.verification  # noqa — triggers runner registration via __init__
    from src.verification.pipeline import run_verification_pipeline

    mlir_code = Path(mlir_path).read_text()
    return run_verification_pipeline(mlir_code, mutated_qir,
                                     shots=shots, mode=mode)


def run_batch(mode: str = "shots", shots: int = 1000) -> list:
    """Run all mutations on all batch circuits, return results as dicts."""
    results = []

    for mlir_path, label in BATCH_CIRCUITS:
        if not Path(mlir_path).exists():
            print(f"  SKIP: {mlir_path} not found", file=sys.stderr)
            continue

        # Get correct QIR
        try:
            correct_qir = translate_to_qir(mlir_path)
        except Exception as e:
            print(f"  SKIP: {label} — translation failed: {e}", file=sys.stderr)
            continue

        # Verify correct QIR (baseline)
        print(f"  {label}: baseline ...", file=sys.stderr)
        vr = verify_mutation(mlir_path, correct_qir, mode=mode, shots=shots)
        results.append({
            "circuit": label,
            "mlir_file": mlir_path,
            "mutation": "none",
            "similarity": vr.get("similarity", -1),
            "gate_match": vr.get("gate_comparison", {}).get("matches", False),
            "detected": False,  # correct QIR should not be "detected" as wrong
            "mode": vr.get("verification_mode", mode),
        })

        # Apply each mutation
        for mut_name, mut_fn in MUTATIONS.items():
            print(f"  {label}: {mut_name} ...", file=sys.stderr)
            try:
                mutated = mut_fn(correct_qir)
                if mutated == correct_qir:
                    # Mutation had no effect (e.g., no parametric gate to perturb)
                    results.append({
                        "circuit": label,
                        "mlir_file": mlir_path,
                        "mutation": mut_name,
                        "similarity": -1,
                        "gate_match": True,
                        "detected": False,
                        "note": "mutation had no effect",
                        "mode": mode,
                    })
                    continue

                vr = verify_mutation(mlir_path, mutated, mode=mode, shots=shots)
                sim = vr.get("similarity", -1)
                gate_ok = vr.get("gate_comparison", {}).get("matches", False)
                # "Detected" = either TVD fails OR gate count mismatches
                detected = (sim < 0.95) or (not gate_ok)

                results.append({
                    "circuit": label,
                    "mlir_file": mlir_path,
                    "mutation": mut_name,
                    "similarity": sim,
                    "gate_match": gate_ok,
                    "detected": detected,
                    "mode": vr.get("verification_mode", mode),
                })
            except Exception as e:
                results.append({
                    "circuit": label,
                    "mlir_file": mlir_path,
                    "mutation": mut_name,
                    "error": str(e),
                    "detected": True,  # crash = detected
                    "mode": mode,
                })

    return results


def main():
    parser = argparse.ArgumentParser(description="QIR mutation injection for E4")
    parser.add_argument("qir_file", nargs="?", help="QIR .ll file to mutate")
    parser.add_argument("mutation", nargs="?", choices=list(MUTATIONS.keys()),
                        help="Mutation type to apply")
    parser.add_argument("--all", action="store_true",
                        help="Apply all mutations and verify each")
    parser.add_argument("--mlir", help="MLIR file (needed for --all verification)")
    parser.add_argument("--batch", action="store_true",
                        help="Run all mutations on all default circuits")
    parser.add_argument("--mode", choices=["shots", "probs"], default="shots")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--output", "-o", help="Output JSONL file")

    args = parser.parse_args()

    if args.batch:
        print("=== E4 Batch: Mutation Verification ===", file=sys.stderr)
        results = run_batch(mode=args.mode, shots=args.shots)

        out = open(args.output, "w") if args.output else sys.stdout
        for r in results:
            out.write(json.dumps(r) + "\n")
        if args.output:
            out.close()
            print(f"\nResults written to {args.output}", file=sys.stderr)

        # Print summary
        total = len([r for r in results if r["mutation"] != "none"])
        detected = len([r for r in results if r["mutation"] != "none" and r.get("detected")])
        print(f"\n=== Detection rate: {detected}/{total} "
              f"({100*detected/total:.1f}%) ===", file=sys.stderr)
        return

    if args.qir_file and args.all:
        if not args.mlir:
            parser.error("--all requires --mlir <MLIR_FILE>")
        qir = Path(args.qir_file).read_text()
        for mut_name, mut_fn in MUTATIONS.items():
            mutated = mut_fn(qir)
            changed = mutated != qir
            vr = verify_mutation(args.mlir, mutated, mode=args.mode, shots=args.shots)
            sim = vr.get("similarity", -1)
            gate_ok = vr.get("gate_comparison", {}).get("matches", False)
            detected = (sim < 0.95) or (not gate_ok)
            status = "DETECTED" if detected else "MISSED"
            print(f"  {mut_name:20s}  TVD={sim:.4f}  gates={gate_ok}  "
                  f"changed={changed}  [{status}]")
        return

    if args.qir_file and args.mutation:
        qir = Path(args.qir_file).read_text()
        mutated = MUTATIONS[args.mutation](qir)
        print(mutated)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
