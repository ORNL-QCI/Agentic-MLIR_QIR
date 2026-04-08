#!/usr/bin/env bash
# E1 — Translation Correctness Across Dialects
# Deterministic path only, both shots and probs modes.
# Expected time: ~15–30 minutes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e1"
mkdir -p "$RESULTS_DIR"
SHOTS=1000

echo "=== E1: Translation Correctness ==="
echo "Results → $RESULTS_DIR"
echo ""

# ── Catalyst dialect ─────────────────────────────────────────────────────────
# Circuits with >= 50 qubits can't be simulated (state vector OOM).
# Use --no-verify for those; translation + gate counting still works.
needs_no_verify() {
  # Circuits >= 35 qubits can't be simulated (state vector OOM on 256GB RAM).
  # Translation + gate counting still works via --no-verify.
  case "$(basename "$1")" in
    ghz03[5-9]*|ghz04[0-9]*|ghz05[0-9]*|ghz06[0-9]*|ghz07[0-9]*|ghz08[0-9]*|ghz09[0-9]*|ghz100*) return 0 ;;
    *ghz_100*|*ghz_50*|*ghz_3[5-9]*|*ghz_4[0-9]*) return 0 ;;
    *) return 1 ;;
  esac
}

echo "--- Catalyst dialect (shots mode) ---"
> "$RESULTS_DIR/catalyst_shots.jsonl"
for f in example/catalyst_mlir/*.mlir example/catalyst_mlir/ghz/*.mlir examples/mlir/*.mlir; do
  name="$(basename "$f" .mlir)"
  echo "  $name ..."
  if needs_no_verify "$f"; then
    python translate.py "$f" --json --no-verify \
      >> "$RESULTS_DIR/catalyst_shots.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/catalyst_shots.jsonl"
  else
    python translate.py "$f" --json --shots "$SHOTS" \
      >> "$RESULTS_DIR/catalyst_shots.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/catalyst_shots.jsonl"
  fi
done

echo ""
echo "--- Catalyst dialect (probs mode) ---"
> "$RESULTS_DIR/catalyst_probs.jsonl"
for f in example/catalyst_mlir/*.mlir example/catalyst_mlir/ghz/*.mlir examples/mlir/*.mlir; do
  name="$(basename "$f" .mlir)"
  echo "  $name ..."
  if needs_no_verify "$f"; then
    python translate.py "$f" --json --no-verify \
      >> "$RESULTS_DIR/catalyst_probs.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/catalyst_probs.jsonl"
  else
    python translate.py "$f" --json --mode probs \
      >> "$RESULTS_DIR/catalyst_probs.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/catalyst_probs.jsonl"
  fi
done

# ── Quake dialect ────────────────────────────────────────────────────────────
echo ""
echo "--- Quake dialect (shots mode) ---"
> "$RESULTS_DIR/quake_shots.jsonl"
for f in example/quake_mlir/*.mlir example/quake_mlir/ghz/*.mlir; do
  name="$(basename "$f" .mlir)"
  echo "  $name ..."
  if needs_no_verify "$f"; then
    python translate.py "$f" --json --no-verify \
      >> "$RESULTS_DIR/quake_shots.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/quake_shots.jsonl"
  else
    python translate.py "$f" --json --shots "$SHOTS" \
      >> "$RESULTS_DIR/quake_shots.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/quake_shots.jsonl"
  fi
done

echo ""
echo "--- Quake dialect (probs mode) ---"
> "$RESULTS_DIR/quake_probs.jsonl"
for f in example/quake_mlir/*.mlir example/quake_mlir/ghz/*.mlir; do
  name="$(basename "$f" .mlir)"
  echo "  $name ..."
  if needs_no_verify "$f"; then
    python translate.py "$f" --json --no-verify \
      >> "$RESULTS_DIR/quake_probs.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/quake_probs.jsonl"
  else
    python translate.py "$f" --json --mode probs \
      >> "$RESULTS_DIR/quake_probs.jsonl" 2>/dev/null || \
      echo "{\"file\":\"$f\",\"error\":\"translation failed\"}" >> "$RESULTS_DIR/quake_probs.jsonl"
  fi
done

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=== E1 Summary ==="
for file in "$RESULTS_DIR"/*.jsonl; do
  total=$(wc -l < "$file")
  errors=$(grep -c '"error"' "$file" 2>/dev/null || echo 0)
  echo "  $(basename "$file"): $total entries, $errors errors"
done
echo ""
echo "E1 complete. Run 'python experiments/analyze_results.py e1' for tables."
