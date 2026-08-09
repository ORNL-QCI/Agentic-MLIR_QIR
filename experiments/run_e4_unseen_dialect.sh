#!/usr/bin/env bash
# E4 — Unseen Dialect Translation: FTQC (Steane Code)
# Tests the agentic pipeline on the FTQC dialect, which is NOT registered
# in the deterministic parser. The system must infer the dialect as "ftqc"
# and use LLM-aided translation to produce valid QIR.
# Expected time: ~2–4 hours (LLM inference)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e4"
mkdir -p "$RESULTS_DIR"

SHOTS=1000
REPEATS=3
MODELS=(llama3.1-8b llama3.1-70b-q4 codellama-13b codellama-34b-q4 gpt-oss-20b gemma4-31b-hf)

# FTQC circuits (unseen dialect — deterministic path will fail with exit 2)
FTQC_DIR="example/ftqc_mlir"
CIRCUITS=(
  "$FTQC_DIR/steane_1q_h.mlir"
  "$FTQC_DIR/steane_2q_bell.mlir"
  "$FTQC_DIR/steane_3q_grover.mlir"
  "$FTQC_DIR/steane_3q_qft.mlir"
)

# Reference QIR files for structural comparison
declare -A REFERENCE_QIR=(
  [steane_1q_h]="example/qir/steane_1q_h.ll"
  [steane_2q_bell]="example/qir/steane_2q_bell.ll"
  [steane_3q_grover]="example/qir/steane_3q_grover.ll"
  [steane_3q_qft]="example/qir/steane_3q_qft.ll"
)

echo "=== E4: Unseen Dialect Translation (FTQC) ==="
echo "Circuits: ${#CIRCUITS[@]}"
echo "Models: ${MODELS[*]}"
echo "Repeats: $REPEATS"
echo "Results → $RESULTS_DIR"
echo ""

# ── Step 0: Confirm deterministic path fails (expected) ─────────────────────
echo "--- Step 0: Verify deterministic path rejects FTQC ---"
for f in "${CIRCUITS[@]}"; do
  name="$(basename "$f" .mlir)"
  set +e
  python translate.py "$f" --json --no-verify > /dev/null 2>&1
  exit_code=$?
  set -e
  if [ "$exit_code" -eq 2 ]; then
    echo "  ✓ $name → exit 2 (unsupported dialect, as expected)"
  else
    echo "  ✗ $name → exit $exit_code (unexpected! should be 2)"
  fi
done
echo ""

# ── Step 1: Agentic translation ────────────────────────────────────────────
for model in "${MODELS[@]}"; do
  echo "--- Model: $model ---"
  OUTFILE="$RESULTS_DIR/ftqc_${model}.jsonl"
  > "$OUTFILE"

  for f in "${CIRCUITS[@]}"; do
    [ -f "$f" ] || { echo "  SKIP: $f not found"; continue; }
    name="$(basename "$f" .mlir)"
    ref_qir="${REFERENCE_QIR[$name]:-}"

    for run in $(seq 1 "$REPEATS"); do
      echo "  $name ($model, run $run/$REPEATS) ..."

      # Run agentic translation; write exactly one JSON line to $OUTFILE.
      # Disable pipefail for this pipe: translate.py returns non-zero on
      # verification failure, which is NOT a script error here.
      set +o pipefail
      LINE=$(python translate.py "$f" --json --model "$model" \
        --shots "$SHOTS" 2>/dev/null | \
        python -c "
import json, sys

try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    data = {'error': 'translate.py produced no JSON output'}
data['model'] = '$model'
data['circuit'] = '$name'
data['run'] = $run
data['file'] = '$f'
data['reference_qir'] = '$ref_qir'

# Structural comparison against reference if available
if '$ref_qir' and data.get('qir'):
    ref_text = open('$ref_qir').read() if '$ref_qir' else ''
    qir_text = data['qir']
    import re
    def count_qir_ops(text):
        h = len(re.findall(r'call void @__quantum__qis__h__body', text))
        cnot = len(re.findall(r'call void @__quantum__qis__cnot__body', text))
        cz = len(re.findall(r'call void @__quantum__qis__cz__body', text))
        z = len(re.findall(r'call void @__quantum__qis__z__body', text))
        mz = len(re.findall(r'call void @__quantum__qis__mz__body', text))
        num_qubits_match = re.search(r'required_num_qubits[\"\'\\s=]+(\d+)', text)
        num_qubits = int(num_qubits_match.group(1)) if num_qubits_match else -1
        return {'h': h, 'cnot': cnot, 'cz': cz, 'z': z, 'mz': mz, 'num_qubits': num_qubits}
    ref_ops = count_qir_ops(ref_text)
    gen_ops = count_qir_ops(qir_text)
    data['reference_ops'] = ref_ops
    data['generated_ops'] = gen_ops
    data['ops_match'] = (ref_ops == gen_ops)
    data['qubits_match'] = (ref_ops['num_qubits'] == gen_ops['num_qubits'])

print(json.dumps(data))
")
      set -o pipefail
      if [ -n "$LINE" ]; then
        echo "$LINE" >> "$OUTFILE"
      else
        echo "{\"model\":\"$model\",\"circuit\":\"$name\",\"run\":$run,\"file\":\"$f\",\"error\":\"empty output\"}" \
          >> "$OUTFILE"
      fi
    done
  done

  entries=$(wc -l < "$OUTFILE")
  echo "  → $entries entries written"
  echo ""
done

# ── Summary ──────────────────────────────────────────────────────────────────
echo "=== E4 Summary ==="
for file in "$RESULTS_DIR"/ftqc_*.jsonl; do
  [ -f "$file" ] || continue
  model=$(basename "$file" .jsonl | sed 's/ftqc_//')
  total=$(wc -l < "$file")
  errors=$(grep -c '"error"' "$file" 2>/dev/null || echo 0)
  successes=$((total - errors))

  # Count structural matches
  ops_matches=$(python -c "
import json
count = 0
for line in open('$file'):
    d = json.loads(line)
    if d.get('ops_match'): count += 1
print(count)
" 2>/dev/null || echo "?")

  echo "  $model: $successes/$total translated, $ops_matches ops-matched with reference"
done
echo ""
echo "E4 complete. Run 'python experiments/analyze_results.py e4' for analysis."
