#!/usr/bin/env bash
# E3 — Agentic vs. Deterministic vs. Hybrid Translation Paths
# 14-circuit representative subset, 2 models, 3 repeats.
# Expected time: ~6–10 hours (LLM inference heavy)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e3"
mkdir -p "$RESULTS_DIR"

SHOTS=1000
REPEATS=3
MODELS=(llama3.1-8b codellama-13b)

# Representative subset — covers all circuit categories
CIRCUITS=(
  # Standard
  example/catalyst_mlir/code_bell.mlir
  # GHZ scaling (3 sizes)
  example/catalyst_mlir/code_ghz_5.mlir
  example/catalyst_mlir/code_ghz_10.mlir
  example/catalyst_mlir/code_ghz_20.mlir
  # Conditional
  example/catalyst_mlir/code_classic_teleportation.mlir
  # MBQC
  example/quake_mlir/code_mbqc_teleport.mlir
  example/quake_mlir/code_mbqc_rotation_rz.mlir
  example/quake_mlir/code_mbqc_rotation_rx.mlir
  example/quake_mlir/code_mbqc_cnot.mlir
  # Random (diverse gate sets)
  example/catalyst_mlir/code_random_circuit_658.mlir
  example/catalyst_mlir/code_random_circuit_1847.mlir
  example/catalyst_mlir/code_random_circuit_3990.mlir
  example/catalyst_mlir/code_random_circuit_6994.mlir
  # QEC
  example/catalyst_mlir/steane_ft1qb.mlir
)

echo "=== E3: Agentic vs. Deterministic vs. Hybrid ==="
echo "Circuits: ${#CIRCUITS[@]}"
echo "Models: ${MODELS[*]}"
echo "Repeats: $REPEATS"
echo "Results → $RESULTS_DIR"
echo ""

# ── Path A: Deterministic (baseline) ─────────────────────────────────────────
echo "--- Path A: Deterministic ---"
> "$RESULTS_DIR/deterministic.jsonl"
for f in "${CIRCUITS[@]}"; do
  [ -f "$f" ] || { echo "  SKIP (not found): $f"; continue; }
  name="$(basename "$f" .mlir)"
  echo "  $name ..."
  python translate.py "$f" --json --shots "$SHOTS" \
    >> "$RESULTS_DIR/deterministic.jsonl" 2>/dev/null || \
    echo "{\"file\":\"$f\",\"error\":\"failed\"}" >> "$RESULTS_DIR/deterministic.jsonl"
done

# ── Path B: Force-agentic (LLM only) ────────────────────────────────────────
for model in "${MODELS[@]}"; do
  echo ""
  echo "--- Path B: Force-agentic ($model) ---"
  > "$RESULTS_DIR/agentic_${model}.jsonl"
  for f in "${CIRCUITS[@]}"; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .mlir)"
    for run in $(seq 1 "$REPEATS"); do
      echo "  $name ($model, run $run/$REPEATS) ..."
      python translate.py "$f" --json --model "$model" \
        --force-agentic --shots "$SHOTS" \
        >> "$RESULTS_DIR/agentic_${model}.jsonl" 2>/dev/null || \
        echo "{\"file\":\"$f\",\"model\":\"$model\",\"run\":$run,\"error\":\"failed\"}" \
          >> "$RESULTS_DIR/agentic_${model}.jsonl"
    done
  done
done

# ── Path C: Hybrid (deterministic + repair) ──────────────────────────────────
for model in "${MODELS[@]}"; do
  echo ""
  echo "--- Path C: Hybrid ($model) ---"
  > "$RESULTS_DIR/hybrid_${model}.jsonl"
  for f in "${CIRCUITS[@]}"; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .mlir)"
    for run in $(seq 1 "$REPEATS"); do
      echo "  $name ($model, run $run/$REPEATS) ..."
      # Hybrid = use --model without --force-agentic
      # Deterministic runs first; if verify fails, agent repairs
      python translate.py "$f" --json --model "$model" \
        --shots "$SHOTS" \
        >> "$RESULTS_DIR/hybrid_${model}.jsonl" 2>/dev/null || \
        echo "{\"file\":\"$f\",\"model\":\"$model\",\"run\":$run,\"error\":\"failed\"}" \
          >> "$RESULTS_DIR/hybrid_${model}.jsonl"
    done
  done
done

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=== E3 Summary ==="
for file in "$RESULTS_DIR"/*.jsonl; do
  echo "  $(basename "$file"): $(wc -l < "$file") entries"
done
echo ""
echo "E3 complete. Run 'python experiments/analyze_results.py e3' for plots."
