#!/usr/bin/env bash
# Smoke test — quick sanity check that all experiment paths work.
# Run this FIRST before any full experiment.
# Expected time: ~2 minutes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

RESULTS_DIR="experiments/results/smoke"
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

PASS=0
FAIL=0

smoke() {
  local label="$1"; shift
  echo -n "  $label ... "
  if "$@" >> "$RESULTS_DIR/smoke.log" 2>&1; then
    echo "OK"
    PASS=$((PASS + 1))
  else
    echo "FAILED (see $RESULTS_DIR/smoke.log)"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Smoke Test ==="
echo ""

# 1. Deterministic — Catalyst Bell (shots mode)
smoke "Catalyst Bell (shots)" \
  python translate.py examples/mlir/bell_state.mlir --json --shots 100

# 2. Deterministic — Catalyst Bell (probs mode)
smoke "Catalyst Bell (probs)" \
  python translate.py examples/mlir/bell_state.mlir --json --mode probs

# 3. Deterministic — Quake Bell
smoke "Quake Bell (shots)" \
  python translate.py example/quake_mlir/code_bell.mlir --json --shots 100

# 4. Large circuit — GHZ-30 Catalyst
smoke "Catalyst GHZ-30" \
  python translate.py example/catalyst_mlir/ghz/ghz030.mlir --json --shots 100

# 5. Large circuit — GHZ-100 Quake (no-verify: 100-qubit simulation is OOM)
smoke "Quake GHZ-100 (no-verify)" \
  python translate.py example/quake_mlir/ghz/ghz100.mlir --json --no-verify

# 6. Conditional — teleportation
smoke "Catalyst teleportation" \
  python translate.py example/catalyst_mlir/code_classic_teleportation.mlir --json --shots 100

# 7. Random circuit
smoke "Random circuit 658" \
  python translate.py example/catalyst_mlir/code_random_circuit_658.mlir --json --shots 100

# 8. No-verify mode
smoke "No-verify mode" \
  python translate.py examples/mlir/bell_state.mlir --json --no-verify

# 9. JSON output structure check
smoke "JSON structure" \
  python -c "
import subprocess, json, sys
r = subprocess.run(
    ['python', 'translate.py', 'examples/mlir/bell_state.mlir', '--json', '--shots', '100'],
    capture_output=True, text=True
)
d = json.loads(r.stdout)
assert 'qir' in d, 'missing qir key'
assert 'dialect' in d, 'missing dialect key'
assert 'translation_path' in d, 'missing translation_path key'
assert 'verification' in d or 'gate_comparison' in d, 'missing verification keys'
print('JSON structure OK')
"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
if [ "$FAIL" -gt 0 ]; then
  echo "Check $RESULTS_DIR/smoke.log for details"
  exit 1
fi
echo "All smoke tests passed. Safe to run full experiments."
