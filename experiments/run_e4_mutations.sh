#!/usr/bin/env bash
# E4 — Verification Pipeline Reliability via Mutation Testing
# Runs all 5 mutation types on 7 circuits, both shots and probs modes.
# Expected time: ~30–60 minutes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e4"
mkdir -p "$RESULTS_DIR"

echo "=== E4: Mutation Verification ==="
echo "Results → $RESULTS_DIR"
echo ""

# ── Shots mode ───────────────────────────────────────────────────────────────
echo "--- Batch (shots mode, 1000 shots) ---"
python experiments/inject_mutations.py --batch --mode shots --shots 1000 \
  -o "$RESULTS_DIR/mutations_shots.jsonl"

echo ""

# ── Probs mode ───────────────────────────────────────────────────────────────
echo "--- Batch (probs mode) ---"
python experiments/inject_mutations.py --batch --mode probs \
  -o "$RESULTS_DIR/mutations_probs.jsonl"

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=== E4 Summary ==="
for file in "$RESULTS_DIR"/*.jsonl; do
  total=$(grep -c '"mutation"' "$file" 2>/dev/null || echo 0)
  mutations=$(grep -v '"none"' "$file" | grep -c '"mutation"' 2>/dev/null || echo 0)
  detected=$(grep -v '"none"' "$file" | grep -c '"detected": true' 2>/dev/null || echo 0)
  echo "  $(basename "$file"): $mutations mutations tested, $detected detected"
done
echo ""
echo "E4 complete. Run 'python experiments/analyze_results.py e4' for ROC curves."
