#!/usr/bin/env python3
"""Analyze experiment results and generate tables/plots for the paper.

Usage:
  python experiments/analyze_results.py e1      # E1 correctness table
  python experiments/analyze_results.py e2      # E2 scalability plots
  python experiments/analyze_results.py e3      # E3 path comparison
  python experiments/analyze_results.py e4      # E4 mutation ROC
  python experiments/analyze_results.py e5      # E5 LLM profiling
  python experiments/analyze_results.py e6      # E6 cross-dialect
  python experiments/analyze_results.py all     # Everything
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

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

    # Try standard JSONL first (one JSON per line)
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

    # Fall back to multi-line JSON: use decoder to find object boundaries
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        # Skip whitespace
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

    # Count overall pass rates
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

            # Infer qubit count from filename
            import re
            m = re.search(r'ghz_(\d+)', name)
            qubits = int(m.group(1)) if m else "?"

            print(f"{name:<30} {str(qubits):>6} {time_ms:>10.1f} "
                  f"{tvd:>8.4f} {gates:>6}")


def analyze_e3():
    """E3: Agentic comparison — summarize by path and model."""
    print("\n" + "=" * 70)
    print("E3: Agentic vs. Deterministic vs. Hybrid")
    print("=" * 70)

    # Deterministic baseline
    det_data = load_jsonl(RESULTS_BASE / "e3" / "deterministic.jsonl")
    if det_data:
        tvds = [d.get("verification", {}).get("similarity", 0)
                for d in det_data if d.get("verification")]
        avg_tvd = sum(tvds) / len(tvds) if tvds else 0
        times = [d.get("translation_time_s", 0) for d in det_data]
        avg_time = sum(times) / len(times) if times else 0
        print(f"\nDeterministic: avg TVD={avg_tvd:.4f}, avg time={avg_time*1000:.1f}ms, "
              f"n={len(det_data)}")

    # Agentic + hybrid per model
    for prefix in ["agentic", "hybrid"]:
        for model_file in sorted(RESULTS_BASE.glob(f"e3/{prefix}_*.jsonl")):
            data = load_jsonl(model_file)
            if not data:
                continue
            model = model_file.stem.replace(f"{prefix}_", "")
            tvds = [d.get("verification", {}).get("similarity", 0)
                    for d in data if d.get("verification")]
            avg_tvd = sum(tvds) / len(tvds) if tvds else 0
            times = [d.get("translation_time_s", 0) for d in data]
            avg_time = sum(times) / len(times) if times else 0
            iters = [d.get("iterations", 1) for d in data]
            avg_iter = sum(iters) / len(iters) if iters else 0
            errors = sum(1 for d in data if "error" in d)
            print(f"{prefix.title():>8} ({model}): avg TVD={avg_tvd:.4f}, "
                  f"avg time={avg_time:.2f}s, avg iters={avg_iter:.1f}, "
                  f"errors={errors}, n={len(data)}")


def analyze_e4():
    """E4: Mutation testing — detection rates and ROC data."""
    print("\n" + "=" * 70)
    print("E4: Mutation Verification")
    print("=" * 70)

    for mode in ["shots", "probs"]:
        path = RESULTS_BASE / "e4" / f"mutations_{mode}.jsonl"
        data = load_jsonl(path)
        if not data:
            continue

        print(f"\n--- {mode} mode ---")

        # Baseline (correct translations)
        baselines = [d for d in data if d.get("mutation") == "none"]
        mutations = [d for d in data if d.get("mutation") != "none"]

        if baselines:
            avg_baseline = sum(d.get("similarity", 0) for d in baselines) / len(baselines)
            print(f"Baseline TVD (correct): {avg_baseline:.4f} (n={len(baselines)})")

        # Per mutation type
        by_type = defaultdict(list)
        for d in mutations:
            by_type[d["mutation"]].append(d)

        print(f"\n{'Mutation Type':<20} {'Tested':>6} {'Detected':>8} {'Rate':>6} {'Avg TVD':>8}")
        print("-" * 55)

        total_tested, total_detected = 0, 0
        for mut_type, items in sorted(by_type.items()):
            tested = len(items)
            detected = sum(1 for d in items if d.get("detected"))
            rate = 100 * detected / tested if tested else 0
            avg_tvd = sum(d.get("similarity", 0) for d in items
                          if d.get("similarity", -1) >= 0) / max(1, tested)
            print(f"{mut_type:<20} {tested:>6} {detected:>8} {rate:>5.1f}% {avg_tvd:>8.4f}")
            total_tested += tested
            total_detected += detected

        if total_tested > 0:
            print(f"\nOverall detection rate: {total_detected}/{total_tested} "
                  f"({100*total_detected/total_tested:.1f}%)")


def analyze_e5():
    """E5: LLM profiling — model comparison table."""
    print("\n" + "=" * 70)
    print("E5: LLM Model Performance Profiling")
    print("=" * 70)

    print(f"\n{'Model':<20} {'Success':>8} {'Avg TVD':>8} {'Avg Time':>10} "
          f"{'Avg Iters':>10} {'Gate Match':>10}")
    print("-" * 70)

    for model_file in sorted(RESULTS_BASE.glob("e5/profile_*.jsonl")):
        data = load_jsonl(model_file)
        if not data:
            continue
        model = model_file.stem.replace("profile_", "")
        total = len(data)
        errors = sum(1 for d in data if "error" in d)
        successes = total - errors

        valid = [d for d in data if "error" not in d]
        tvds = [d.get("verification", {}).get("similarity", 0)
                for d in valid if d.get("verification")]
        times = [d.get("translation_time_s", 0) for d in valid]
        iters = [d.get("iterations", 1) for d in valid]
        gate_matches = sum(1 for d in valid
                          if d.get("gate_comparison", {}).get("matches"))

        avg_tvd = sum(tvds) / len(tvds) if tvds else 0
        avg_time = sum(times) / len(times) if times else 0
        avg_iter = sum(iters) / len(iters) if iters else 0
        match_rate = 100 * gate_matches / len(valid) if valid else 0

        print(f"{model:<20} {successes:>5}/{total:<3} {avg_tvd:>7.4f} "
              f"{avg_time:>9.2f}s {avg_iter:>9.1f} {match_rate:>9.1f}%")


def analyze_e6():
    """E6: Cross-dialect portability."""
    print("\n" + "=" * 70)
    print("E6: Cross-Dialect Portability")
    print("=" * 70)

    path = RESULTS_BASE / "e6" / "cross_dialect.jsonl"
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
        "e5": analyze_e5,
        "e6": analyze_e6,
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
