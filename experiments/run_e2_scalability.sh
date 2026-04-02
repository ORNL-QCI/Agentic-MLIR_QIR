#!/usr/bin/env bash
# E2 — Scalability: Circuit Size vs. Translation Quality
# GHZ scaling ladder (5 to 100 qubits), both dialects.
# Expected time: ~10–20 minutes (deterministic) + hours if agentic enabled
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e2"
mkdir -p "$RESULTS_DIR"

GHZ_SIZES=(5 10 15 20 25 30 100)
SHOTS=1000

# Optional: set AGENTIC_MODEL to run agentic path too
# e.g., AGENTIC_MODEL=llama3.1-8b bash experiments/run_e2_scalability.sh
AGENTIC_MODEL="${AGENTIC_MODEL:-}"

echo "=== E2: Scalability (GHZ Scaling Ladder) ==="
echo "Sizes: ${GHZ_SIZES[*]}"
echo "Results → $RESULTS_DIR"
[ -n "$AGENTIC_MODEL" ] && echo "Agentic model: $AGENTIC_MODEL"
echo ""

# Circuits >= 50 qubits can't be simulated (state vector OOM)
MAX_SIM_QUBITS=30

# ── Deterministic path ───────────────────────────────────────────────────────
echo "--- Deterministic (shots) ---"
> "$RESULTS_DIR/deterministic_shots.jsonl"
for n in "${GHZ_SIZES[@]}"; do
  for dialect_dir in example/catalyst_mlir example/quake_mlir; do
    f="$dialect_dir/code_ghz_${n}.mlir"
    [ -f "$f" ] || continue
    dialect=$(basename "$dialect_dir" | sed 's/_mlir//')
    echo "  GHZ-${n} ($dialect) ..."
    if [ "$n" -gt "$MAX_SIM_QUBITS" ]; then
      python translate.py "$f" --json --no-verify \
        >> "$RESULTS_DIR/deterministic_shots.jsonl" 2>/dev/null
    else
      python translate.py "$f" --json --shots "$SHOTS" \
        >> "$RESULTS_DIR/deterministic_shots.jsonl" 2>/dev/null
    fi
  done
done

echo ""
echo "--- Deterministic (probs) ---"
> "$RESULTS_DIR/deterministic_probs.jsonl"
for n in "${GHZ_SIZES[@]}"; do
  for dialect_dir in example/catalyst_mlir example/quake_mlir; do
    f="$dialect_dir/code_ghz_${n}.mlir"
    [ -f "$f" ] || continue
    dialect=$(basename "$dialect_dir" | sed 's/_mlir//')
    echo "  GHZ-${n} ($dialect) ..."
    if [ "$n" -gt "$MAX_SIM_QUBITS" ]; then
      python translate.py "$f" --json --no-verify \
        >> "$RESULTS_DIR/deterministic_probs.jsonl" 2>/dev/null
    else
      python translate.py "$f" --json --mode probs \
        >> "$RESULTS_DIR/deterministic_probs.jsonl" 2>/dev/null
    fi
  done
done

# Also add Bell (2q) and GHZ-3 from examples/mlir
echo ""
echo "--- Small circuits (Bell, GHZ-3) ---"
for f in examples/mlir/bell_state.mlir examples/mlir/ghz_state.mlir; do
  [ -f "$f" ] || continue
  echo "  $(basename "$f") ..."
  python translate.py "$f" --json --shots "$SHOTS" \
    >> "$RESULTS_DIR/deterministic_shots.jsonl" 2>/dev/null
  python translate.py "$f" --json --mode probs \
    >> "$RESULTS_DIR/deterministic_probs.jsonl" 2>/dev/null
done

# ── Agentic path (if model specified) ────────────────────────────────────────
if [ -n "$AGENTIC_MODEL" ]; then
  echo ""
  echo "--- Agentic ($AGENTIC_MODEL, shots) ---"
  > "$RESULTS_DIR/agentic_${AGENTIC_MODEL}.jsonl"
  for n in "${GHZ_SIZES[@]}"; do
    f="example/catalyst_mlir/code_ghz_${n}.mlir"
    [ -f "$f" ] || continue
    echo "  GHZ-${n} (catalyst, $AGENTIC_MODEL) ..."
    python translate.py "$f" --json --model "$AGENTIC_MODEL" \
      --force-agentic --shots "$SHOTS" \
      >> "$RESULTS_DIR/agentic_${AGENTIC_MODEL}.jsonl" 2>/dev/null
  done
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=== E2 Summary ==="
for file in "$RESULTS_DIR"/*.jsonl; do
  echo "  $(basename "$file"): $(wc -l < "$file") entries"
done
echo ""
echo "E2 complete. Run 'python experiments/analyze_results.py e2' for plots."
