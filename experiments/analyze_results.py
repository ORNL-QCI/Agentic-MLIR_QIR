#!/usr/bin/env python3
"""Analyze experiment results and generate summary tables for the paper.

Usage:
  python experiments/analyze_results.py e1     # E1 correctness table
  python experiments/analyze_results.py e2     # E2 scalability table
  python experiments/analyze_results.py e3     # E3 cross-dialect table
  python experiments/analyze_results.py e4     # E4 unseen dialect (FTQC)
  python experiments/analyze_results.py all    # All four
"""

import json
import sys
from pathlib import Path

RESULTS_BASE = Path(__file__).parent / "results"


def load_jsonl(path: Path) -> list:
    """Load a JSONL file into a list of dicts.

    Handles both single-line JSONL and multi-line pretty-printed JSON
    objects concatenated in one file.
    """
    if not path.exists():
        print(f"  WARNING: {path} not found")
        return []
    text = path.read_text()
    results = []

    lines = text.splitlines()
    if lines and lines[0].strip().startswith('{') and lines[0].strip().endswith('}'):
        for line in lines:
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        if results:
            return results

    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        while idx < len(text) and text[idx] in ' \t\n\r':
            idx += 1
        if idx >= len(text):
            break
        try:
            obj, end_idx = decoder.raw_decode(text, idx)
            results.append(obj)
            idx = end_idx
        except json.JSONDecodeError:
            idx += 1

    return results


def analyze_e1():
    """E1: Translation Correctness — generate summary table."""
    print("\n" + "=" * 70)
    print("E1: Translation Correctness Across Dialects")
    print("=" * 70)

    for mode in ["shots", "probs"]:
        for dialect in ["catalyst", "quake"]:
            path = RESULTS_BASE / "e1" / f"{dialect}_{mode}.jsonl"
            data = load_jsonl(path)
            if not data:
                continue

            print(f"\n--- {dialect.title()} ({mode} mode) ---")
            print(f"{'Circuit':<35} {'Gate Match':<12} {'TVD':>8} {'Path':<15}")
            print("-" * 70)

            for d in data:
                if "error" in d and "dialect" not in d:
                    print(f"{'?':<35} {'ERROR':<12}")
                    continue

                name = d.get("dialect", "?") + "/" + Path(d.get("file", "?")).stem \
                    if "file" in d else d.get("dialect", "?")
                gc = d.get("gate_comparison", {})
                gate_match = "YES" if gc.get("matches") else "NO"
                vr = d.get("verification", {})
                tvd = vr.get("similarity", -1) if vr else -1
                tvd_str = f"{tvd:.4f}" if tvd >= 0 else "N/A"
                path_str = d.get("translation_path", "?")
                print(f"{name:<35} {gate_match:<12} {tvd_str:>8} {path_str:<15}")

    total, passed = 0, 0
    for mode in ["shots", "probs"]:
        for dialect in ["catalyst", "quake"]:
            path = RESULTS_BASE / "e1" / f"{dialect}_{mode}.jsonl"
            for d in load_jsonl(path):
                total += 1
                gc = d.get("gate_comparison", {})
                vr = d.get("verification", {})
                if gc.get("matches") and (vr.get("similarity_passes", False)
                                          if vr else True):
                    passed += 1

    if total > 0:
        print(f"\nOverall: {passed}/{total} passed ({100*passed/total:.1f}%)")


def analyze_e2():
    """E2: Scalability — print scaling data."""
    print("\n" + "=" * 70)
    print("E2: Scalability (GHZ Scaling Ladder)")
    print("=" * 70)

    for mode in ["shots", "probs"]:
        path = RESULTS_BASE / "e2" / f"deterministic_{mode}.jsonl"
        data = load_jsonl(path)
        if not data:
            continue

        print(f"\n--- Deterministic ({mode}) ---")
        print(f"{'Circuit':<30} {'Qubits':>6} {'Time (ms)':>10} {'TVD':>8} {'Gates':>6}")
        print("-" * 65)

        for d in data:
            name = Path(d.get("file", "?")).stem if "file" in d else "?"
            vr = d.get("verification", {})
            tvd = vr.get("similarity", -1) if vr else -1
            time_ms = d.get("translation_time_s", 0) * 1000
            gc = d.get("gate_comparison", {})
            gates = "MATCH" if gc.get("matches") else "DIFF"

            import re
            m = re.search(r'ghz_?(\d+)', name)
            qubits = int(m.group(1)) if m else "?"

            print(f"{name:<30} {str(qubits):>6} {time_ms:>10.1f} "
                  f"{tvd:>8.4f} {gates:>6}")


def analyze_e3():
    """E3: Cross-dialect portability."""
    print("\n" + "=" * 70)
    print("E3: Cross-Dialect Portability")
    print("=" * 70)

    path = RESULTS_BASE / "e3" / "cross_dialect.jsonl"
    data = load_jsonl(path)
    if not data:
        return

    print(f"\n{'Circuit':<20} {'Cat TVD':>8} {'Quake TVD':>9} {'Cat Gates':>10} "
          f"{'Q Gates':>8} {'Cat Time':>9} {'Q Time':>9}")
    print("-" * 75)

    for d in data:
        c_tvd = d.get("catalyst_tvd", -1)
        q_tvd = d.get("quake_tvd", -1)
        c_tvd_s = f"{c_tvd:.4f}" if c_tvd >= 0 else "N/A"
        q_tvd_s = f"{q_tvd:.4f}" if q_tvd >= 0 else "N/A"
        c_gates = "MATCH" if d.get("catalyst_gate_match") else "DIFF"
        q_gates = "MATCH" if d.get("quake_gate_match") else "DIFF"
        c_time = d.get("catalyst_time_s", -1)
        q_time = d.get("quake_time_s", -1)
        c_time_s = f"{c_time*1000:.1f}ms" if c_time >= 0 else "N/A"
        q_time_s = f"{q_time*1000:.1f}ms" if q_time >= 0 else "N/A"

        print(f"{d['circuit']:<20} {c_tvd_s:>8} {q_tvd_s:>9} {c_gates:>10} "
              f"{q_gates:>8} {c_time_s:>9} {q_time_s:>9}")

    both_match = sum(1 for d in data
                     if d.get("catalyst_gate_match") and d.get("quake_gate_match"))
    print(f"\nBoth dialects gate-match: {both_match}/{len(data)}")


def analyze_e4():
    """E4: Unseen-dialect (FTQC) translation across models."""
    print("\n" + "=" * 70)
    print("E4: Unseen Dialect Translation (FTQC)")
    print("=" * 70)

    e4_dir = RESULTS_BASE / "e4"
    if not e4_dir.exists():
        print(f"  WARNING: {e4_dir} not found")
        return

    for jsonl in sorted(e4_dir.glob("ftqc_*.jsonl")):
        model = jsonl.stem.replace("ftqc_", "")
        data = load_jsonl(jsonl)
        if not data:
            continue

        # Per-circuit success rates (success = translation_path == "ai_agent" with QIR)
        per_circuit = {}
        times = []
        for d in data:
            circuit = d.get("circuit", "?")
            ok = bool(d.get("qir")) and d.get("success", False)
            per_circuit.setdefault(circuit, []).append(ok)
            if ok and d.get("translation_time_s") is not None:
                times.append(d["translation_time_s"])

        total_ok = sum(sum(v) for v in per_circuit.values())
        total_n = sum(len(v) for v in per_circuit.values())
        avg_t = (sum(times) / len(times)) if times else 0.0

        print(f"\n--- {model} ---")
        for circuit, runs in sorted(per_circuit.items()):
            print(f"  {circuit:<25} {sum(runs)}/{len(runs)}")
        print(f"  TOTAL: {total_ok}/{total_n}, avg {avg_t:.1f}s/translation")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    target = sys.argv[1].lower()
    analyzers = {
        "e1": analyze_e1,
        "e2": analyze_e2,
        "e3": analyze_e3,
        "e4": analyze_e4,
    }

    if target == "all":
        for fn in analyzers.values():
            fn()
    elif target in analyzers:
        analyzers[target]()
    else:
        print(f"Unknown experiment: {target}")
        print(f"Available: {', '.join(analyzers.keys())}, all")


if __name__ == "__main__":
    main()
