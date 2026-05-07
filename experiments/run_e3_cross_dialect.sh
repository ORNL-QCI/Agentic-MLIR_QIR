#!/usr/bin/env bash
# E3 — Cross-Dialect Portability: Same Circuit, Different Origins
# Translates matched Catalyst/Quake pairs and compares QIR outputs.
# Expected time: ~10–20 minutes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e3"
mkdir -p "$RESULTS_DIR"

# Matched pairs: (label, catalyst_file, quake_file)
PAIRS=(
  "bell|example/catalyst_mlir/code_bell.mlir|example/quake_mlir/code_bell.mlir"
  "ghz_5|example/catalyst_mlir/ghz/ghz005.mlir|example/quake_mlir/ghz/ghz005.mlir"
  "ghz_10|example/catalyst_mlir/ghz/ghz010.mlir|example/quake_mlir/ghz/ghz010.mlir"
  "ghz_15|example/catalyst_mlir/ghz/ghz015.mlir|example/quake_mlir/ghz/ghz015.mlir"
  "ghz_20|example/catalyst_mlir/ghz/ghz020.mlir|example/quake_mlir/ghz/ghz020.mlir"
  "ghz_25|example/catalyst_mlir/ghz/ghz025.mlir|example/quake_mlir/ghz/ghz025.mlir"
  "ghz_30|example/catalyst_mlir/ghz/ghz030.mlir|example/quake_mlir/ghz/ghz030.mlir"
  "ghz_100|example/catalyst_mlir/ghz/ghz100.mlir|example/quake_mlir/ghz/ghz100.mlir"
  "teleportation|example/catalyst_mlir/code_classic_teleportation.mlir|example/quake_mlir/code_classic_teleportation.mlir"
  "random_658|example/catalyst_mlir/code_random_circuit_658.mlir|example/quake_mlir/code_random_circuit_658.mlir"
  "random_1847|example/catalyst_mlir/code_random_circuit_1847.mlir|example/quake_mlir/code_random_circuit_1847.mlir"
  "random_2449|example/catalyst_mlir/code_random_circuit_2449.mlir|example/quake_mlir/code_random_circuit_2449.mlir"
  "random_3990|example/catalyst_mlir/code_random_circuit_3990.mlir|example/quake_mlir/code_random_circuit_3990.mlir"
  "random_6994|example/catalyst_mlir/code_random_circuit_6994.mlir|example/quake_mlir/code_random_circuit_6994.mlir"
)

echo "=== E3: Cross-Dialect Portability ==="
echo "Pairs: ${#PAIRS[@]}"
echo "Results → $RESULTS_DIR"
echo ""

> "$RESULTS_DIR/cross_dialect.jsonl"

for pair in "${PAIRS[@]}"; do
  IFS='|' read -r label catalyst_file quake_file <<< "$pair"

  [ -f "$catalyst_file" ] || { echo "  SKIP $label: $catalyst_file not found"; continue; }
  [ -f "$quake_file" ]    || { echo "  SKIP $label: $quake_file not found"; continue; }

  echo "  $label ..."

  # Translate both dialects to temp files
  catalyst_tmp="$RESULTS_DIR/.catalyst_tmp.json"
  quake_tmp="$RESULTS_DIR/.quake_tmp.json"

  # GHZ-100 can't be simulated (OOM) — use --no-verify
  VERIFY_FLAG="--mode probs"
  case "$label" in *100*|*50*) VERIFY_FLAG="--no-verify" ;; esac

  python translate.py "$catalyst_file" --json $VERIFY_FLAG \
    > "$catalyst_tmp" 2>/dev/null || echo '{"error":"failed"}' > "$catalyst_tmp"
  python translate.py "$quake_file" --json $VERIFY_FLAG \
    > "$quake_tmp" 2>/dev/null || echo '{"error":"failed"}' > "$quake_tmp"

  # Combine into one comparison record
  python -c "
import json, sys

with open('$catalyst_tmp') as f:
    catalyst = json.load(f)
with open('$quake_tmp') as f:
    quake = json.load(f)

record = {
    'circuit': '$label',
    'catalyst_file': '$catalyst_file',
    'quake_file': '$quake_file',
    'catalyst_dialect': catalyst.get('dialect', 'unknown'),
    'quake_dialect': quake.get('dialect', 'unknown'),
    'catalyst_path': catalyst.get('translation_path', ''),
    'quake_path': quake.get('translation_path', ''),
    'catalyst_time_s': catalyst.get('translation_time_s', -1),
    'quake_time_s': quake.get('translation_time_s', -1),
    'catalyst_tvd': catalyst.get('verification', {}).get('similarity', -1) if catalyst.get('verification') else -1,
    'quake_tvd': quake.get('verification', {}).get('similarity', -1) if quake.get('verification') else -1,
    'catalyst_gate_match': catalyst.get('gate_comparison', {}).get('matches', False),
    'quake_gate_match': quake.get('gate_comparison', {}).get('matches', False),
    'catalyst_error': catalyst.get('error_message'),
    'quake_error': quake.get('error_message'),
}
print(json.dumps(record))
" >> "$RESULTS_DIR/cross_dialect.jsonl"

  rm -f "$catalyst_tmp" "$quake_tmp"
done

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=== E3 Summary ==="
total=$(wc -l < "$RESULTS_DIR/cross_dialect.jsonl")
both_pass=$(python -c "
import json
count = 0
for line in open('$RESULTS_DIR/cross_dialect.jsonl'):
    d = json.loads(line)
    if d.get('catalyst_gate_match') and d.get('quake_gate_match'):
        count += 1
print(count)
" 2>/dev/null || echo "?")
echo "  $total pairs tested, $both_pass both-dialect gate matches"
echo ""
echo "E3 complete. Run 'python experiments/analyze_results.py e3' for comparison."
