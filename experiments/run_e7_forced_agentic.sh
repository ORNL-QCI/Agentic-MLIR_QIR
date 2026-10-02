#!/usr/bin/env bash
# E7 — Forced Agentic vs. Deterministic Ground Truth
# Routes a *recognized* dialect (Catalyst, Quake) through Path 2 (the LLM
# agent) via --force-agentic instead of Path 1 (the deterministic compiler).
# Because Path 1 translates these circuits exactly, its output serves as a
# known-correct reference for scoring the agentic output on the same circuit.
# Expected time: ~1 min (8B) to ~5 min (70B) per attempt; ~35-65 s per Gemma
# attempt. Full sweep is roughly 30-60 minutes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/e7"
mkdir -p "$RESULTS_DIR"

SHOTS=1000
REPEATS=2
MODELS=(llama3.1-8b llama3.1-70b-q4 gemma4-31b-hf)

# Known dialects — Path 1 handles these exactly, so they have a ground truth.
CIRCUITS=(
  "example/catalyst_mlir/code_bell.mlir"
  "example/quake_mlir/code_bell.mlir"
)

echo "=== E7: Forced Agentic vs. Deterministic Ground Truth ==="
echo "Circuits: ${#CIRCUITS[@]}"
echo "Models: ${MODELS[*]}"
echo "Repeats: $REPEATS"
echo "Results → $RESULTS_DIR"
echo ""

# ── Step 0: Establish the deterministic reference ───────────────────────────
# Path 1 output is the ground truth every agentic attempt is scored against.
echo "--- Step 0: Deterministic reference (Path 1) ---"
for f in "${CIRCUITS[@]}"; do
  [ -f "$f" ] || { echo "  SKIP: $f not found"; continue; }
  name="$(basename "$f" .mlir)"
  dialect="$(basename "$(dirname "$f")" | sed 's/_mlir//')"
  REF_FILE="$RESULTS_DIR/reference_${dialect}_${name}.json"

  set +o pipefail
  python translate.py "$f" --json --no-verify 2>/dev/null > "$REF_FILE"
  set -o pipefail

  if [ -s "$REF_FILE" ]; then
    echo "  ✓ $dialect/$name → reference captured"
  else
    echo "  ✗ $dialect/$name → deterministic path produced no output"
  fi
done
echo ""

# ── Step 1: Forced agentic translation ──────────────────────────────────────
for model in "${MODELS[@]}"; do
  echo "--- Model: $model ---"
  OUTFILE="$RESULTS_DIR/forced_agentic_${model}.jsonl"
  > "$OUTFILE"

  for f in "${CIRCUITS[@]}"; do
    [ -f "$f" ] || { echo "  SKIP: $f not found"; continue; }
    name="$(basename "$f" .mlir)"
    dialect="$(basename "$(dirname "$f")" | sed 's/_mlir//')"
    REF_FILE="$RESULTS_DIR/reference_${dialect}_${name}.json"

    for run in $(seq 1 "$REPEATS"); do
      echo "  $dialect/$name ($model, run $run/$REPEATS) ..."

      # translate.py returns non-zero when verification fails, which is a
      # legitimate E7 outcome rather than a script error — disable pipefail.
      set +o pipefail
      LINE=$(python translate.py "$f" --json --model "$model" --force-agentic \
        --shots "$SHOTS" 2>/dev/null | \
        python -c "
import json, sys

try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    data = {'error': 'translate.py produced no JSON output'}

data['model']    = '$model'
data['circuit']  = '$name'
data['dialect']  = '$dialect'
data['run']      = $run
data['file']     = '$f'
data['forced_agentic'] = True

# Score against the Path 1 reference for the same circuit.
try:
    ref = json.load(open('$REF_FILE'))
except (OSError, json.JSONDecodeError, ValueError):
    ref = {}

ref_gates = (ref.get('gate_comparison') or {}).get('qir_gates') or {}
gen_gates = (data.get('gate_comparison') or {}).get('qir_gates') or {}
data['reference_gates'] = ref_gates
data['generated_gates'] = gen_gates
data['gates_match']     = bool(ref_gates) and ref_gates == gen_gates

ref_qir = ref.get('qir') or ''
gen_qir = data.get('qir') or ''
data['reference_qir_chars'] = len(ref_qir)
data['generated_qir_chars'] = len(gen_qir)
data['produced_qir']        = bool(gen_qir.strip())

verification = data.get('verification') or {}
data['tvd_similarity'] = verification.get('similarity')

print(json.dumps(data))
")
      set -o pipefail
      if [ -n "$LINE" ]; then
        echo "$LINE" >> "$OUTFILE"
      else
        echo "{\"model\":\"$model\",\"circuit\":\"$name\",\"dialect\":\"$dialect\",\"run\":$run,\"file\":\"$f\",\"error\":\"empty output\"}" \
          >> "$OUTFILE"
      fi
    done
  done

  entries=$(wc -l < "$OUTFILE")
  echo "  → $entries entries written"
  echo ""
done

# ── Summary ─────────────────────────────────────────────────────────────────
echo "=== E7 Summary ==="
echo "(agentic output scored against the Path 1 deterministic reference)"
echo ""
for file in "$RESULTS_DIR"/forced_agentic_*.jsonl; do
  [ -f "$file" ] || continue
  model=$(basename "$file" .jsonl | sed 's/forced_agentic_//')

  python -c "
import json

rows = []
for line in open('$file'):
    line = line.strip()
    if line:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass

total     = len(rows)
produced  = sum(1 for r in rows if r.get('produced_qir'))
matched   = sum(1 for r in rows if r.get('gates_match'))
verified  = sum(1 for r in rows if r.get('success'))
tvds      = [r['tvd_similarity'] for r in rows if r.get('tvd_similarity') is not None]
mean_tvd  = f'{sum(tvds)/len(tvds):.1%}' if tvds else 'n/a'
times     = [r['translation_time_s'] for r in rows if r.get('translation_time_s') is not None]
mean_time = f'{sum(times)/len(times):.1f}s' if times else 'n/a'

print(f'  {\"$model\":<18} {produced}/{total} produced QIR, '
      f'{matched}/{total} gate-matched, {verified}/{total} verified, '
      f'mean TVD {mean_tvd}, mean {mean_time}')
" 2>/dev/null || echo "  $model: (could not parse $file)"
done
echo ""
echo "E7 complete. Inspect $RESULTS_DIR/*.jsonl directly —"
echo "analyze_results.py does not yet have an 'e7' mode."
