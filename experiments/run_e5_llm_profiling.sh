#!/usr/bin/env bash
# E5 — LLM Model Performance & Time Profiling (LLM-only path)
# Replaces the old RAG ablation study. Tests multiple models on the
# force-agentic path to measure translation quality, time, and iterations.
# Expected time: ~4–8 hours depending on available models
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e5"
mkdir -p "$RESULTS_DIR"

SHOTS=1000
REPEATS=3

# All models to profile — comment out unavailable ones
MODELS=(
  llama3.1-8b
  codellama-13b
  llama3.1-70b-q4
  codellama-34b-q4
  gpt-oss-20b          # HuggingFace free tier (requires HF_TOKEN)
)

# Representative subset — mix of easy and hard circuits
CIRCUITS=(
  # Easy (should succeed with any model)
  example/catalyst_mlir/code_bell.mlir
  example/catalyst_mlir/code_ghz_5.mlir
  # Medium
  example/catalyst_mlir/code_ghz_10.mlir
  example/catalyst_mlir/code_random_circuit_658.mlir
  example/catalyst_mlir/code_random_circuit_3990.mlir
  # Hard (conditionals, diverse gates)
  example/catalyst_mlir/code_classic_teleportation.mlir
  example/catalyst_mlir/code_random_circuit_1847.mlir
  example/catalyst_mlir/steane_ft1qb.mlir
)

echo "=== E5: LLM Model Performance Profiling ==="
echo "Models: ${MODELS[*]}"
echo "Circuits: ${#CIRCUITS[@]}"
echo "Repeats: $REPEATS"
echo "Results → $RESULTS_DIR"
echo ""

for model in "${MODELS[@]}"; do
  echo "--- Model: $model ---"
  OUTFILE="$RESULTS_DIR/profile_${model}.jsonl"
  > "$OUTFILE"

  for f in "${CIRCUITS[@]}"; do
    [ -f "$f" ] || { echo "  SKIP: $f not found"; continue; }
    name="$(basename "$f" .mlir)"
    for run in $(seq 1 "$REPEATS"); do
      echo "  $name (run $run/$REPEATS) ..."
      START_TIME=$(date +%s%N)

      python translate.py "$f" --json --model "$model" \
        --force-agentic --shots "$SHOTS" 2>/dev/null | \
        python -c "
import json, sys, time
data = json.load(sys.stdin)
data['model'] = '$model'
data['circuit'] = '$name'
data['run'] = $run
data['file'] = '$f'
print(json.dumps(data))
" >> "$OUTFILE" || \
        echo "{\"model\":\"$model\",\"circuit\":\"$name\",\"run\":$run,\"file\":\"$f\",\"error\":\"failed\"}" \
          >> "$OUTFILE"
    done
  done

  entries=$(wc -l < "$OUTFILE")
  echo "  → $entries entries written"
  echo ""
done

# ── Summary ──────────────────────────────────────────────────────────────────
echo "=== E5 Summary ==="
for file in "$RESULTS_DIR"/profile_*.jsonl; do
  [ -f "$file" ] || continue
  model=$(basename "$file" .jsonl | sed 's/profile_//')
  total=$(wc -l < "$file")
  errors=$(grep -c '"error"' "$file" 2>/dev/null || echo 0)
  successes=$((total - errors))

  # Extract average time if available
  avg_time=$(python -c "
import json
times = []
for line in open('$file'):
    d = json.loads(line)
    t = d.get('translation_time_s')
    if t: times.append(t)
if times:
    print(f'{sum(times)/len(times):.2f}s avg')
else:
    print('no timing data')
" 2>/dev/null || echo "N/A")

  echo "  $model: $successes/$total succeeded, $avg_time"
done
echo ""
echo "E5 complete. Run 'python experiments/analyze_results.py e5' for comparison."
