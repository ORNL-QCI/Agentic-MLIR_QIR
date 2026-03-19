# Research Paper Experiment Plan
# Agentic LLM-Aided Translation of Quantum Intermediate Representations with Automated Verification

**Created:** 2026-03-18
**Codebase:** agentic_mlir_qir_updated

---

## E1 — Deterministic vs. Agentic Translation Accuracy

**RQ:** Does the agentic path match or exceed the deterministic parser on known dialects?

| Dimension | Detail |
|-----------|--------|
| Circuits | All Catalyst (4) + Quake (10) examples (14 total) |
| Paths | `deterministic`, `ai_agent` (via `--force-agentic --model KEY`) |
| Models | `llama3.1-8b`, `codellama-13b`, `gpt-oss-20b` |
| Metrics | Gate match (binary), TVD similarity (%), iterations to converge, wall-clock time |
| Shots | 1000 (default) |
| Runs | 5 repeats per (circuit, path, model) to capture LLM variance |
| CLI | `python translate.py INPUT --json --model M --force-agentic --shots 1000` vs `python translate.py INPUT --json` |
| Output | Table: circuit x path x model -> {gate_match, TVD, iterations, time_s}. Box-plot of TVD across repeats. |

---

## E2 — Multi-Dialect Coverage & Unknown Dialect Handling

**RQ:** How does the system handle dialects beyond Catalyst and Quake?

| Dimension | Detail |
|-----------|--------|
| Dialects | Catalyst (known), Quake (known), 2-3 synthetic "unknown" dialects (hand-craft MLIR with invented namespace, e.g. `myq.h`, `myq.cx`) |
| Paths | Deterministic (expected: exit code 2 for unknown), agentic with web tools |
| Models | `llama3.1-8b`, `codellama-13b` |
| Metrics | Success/fail, exit code, whether agent found relevant docs, TVD if translation produced |
| Key insight | Demonstrates graceful degradation + agent's web-research capability for novel dialects |

---

## E3 — Agentic Repair Convergence

**RQ:** How many iterations does the repair loop need, and does feedback monotonically improve quality?

| Dimension | Detail |
|-----------|--------|
| Circuits | Bell, GHZ, parametric rotation, teleportation (conditional) |
| Method | `--force-agentic --max-iterations 10 --model M --json` |
| Data | Extract `iteration_history` from JSON: per-iteration gate_match, TVD, QIR diff |
| Plot | Line chart: iteration number (x) vs TVD similarity (y), one line per circuit. Annotate gate_match flip points. |
| Models | `llama3.1-8b`, `codellama-13b` |
| Hypothesis | Most circuits converge in <=3 iterations; conditional circuits need more |

---

## E4 — LLM Model Comparison

**RQ:** How do model size and architecture affect translation quality and cost?

| Dimension | Detail |
|-----------|--------|
| Models | `llama3.1-8b`, `llama3.1-70b-q4`, `codellama-13b`, `codellama-34b-q4`, `gpt-oss-20b` |
| Circuits | All 14 examples |
| Metrics | TVD similarity, gate match rate, avg iterations, avg time, VRAM usage (for local) |
| Repeats | 3 per (circuit, model) |
| Plot | Radar chart per model (TVD, speed, iteration count). Pareto frontier: quality vs cost/time. |
| Key insight | Is code-specialized (CodeLlama) better than general (Llama3.1) for IR translation? |

---

## E5 — Circuit Complexity Scaling

**RQ:** How does translation quality degrade with circuit size?

| Dimension | Detail |
|-----------|--------|
| Circuits | Programmatically generate MLIR for: N-qubit GHZ (N=2,3,5,8,10,15,20), random circuits (depth 5,10,20,50) |
| Script | Generator that emits valid Catalyst MLIR with H + CNOT chains (see `experiments/generate_circuits.py`) |
| Paths | Deterministic + agentic (best model from E4) |
| Metrics | Translation time, TVD similarity, token count of QIR output, iterations |
| Plot | Scatter: qubit count (x) vs TVD (y), colored by path. Line: qubit count vs time. |
| Hypothesis | Deterministic scales linearly; agentic degrades after ~10 qubits due to token limits |

---

## E6 — Verification Pipeline Reliability

**RQ:** How often do real backends succeed vs. fall back to mock?

| Dimension | Detail |
|-----------|--------|
| Method | Run all 14 circuits; log `qir_is_mock` and `catalyst_is_mock` from verification result |
| Environments | (a) Full install (qirrunner + catalyst), (b) qirrunner only, (c) catalyst only, (d) neither |
| Metrics | Fraction real vs mock per backend, TVD agreement between real-real vs mock-mock |
| Key insight | Validates that mock distributions are faithful enough for development without hardware |

---

## E7 — RAG Knowledge Base Impact

**RQ:** Does the knowledge base improve agentic translation quality?

| Dimension | Detail |
|-----------|--------|
| Method | Compare agentic runs with KB populated vs. empty ChromaDB |
| Setup | (a) `python scripts/initialize_db.py` then translate, (b) wipe ChromaDB, translate same circuits |
| Circuits | All 14 examples + 2 unknown-dialect synthetics |
| Metrics | TVD similarity delta, iteration count delta, qualitative QIR diff |
| Plot | Paired bar chart: with-KB vs without-KB TVD per circuit |

---

## E8 — Hybrid Path (Deterministic + Repair) Efficiency

**RQ:** Is the hybrid path faster and better than pure agentic?

| Dimension | Detail |
|-----------|--------|
| Circuits | Introduce deliberate errors in deterministic output (e.g., wrong gate mapping) to trigger repair |
| Paths | Pure agentic (`--force-agentic`) vs hybrid (default, let repair kick in) |
| Metrics | Total time, iterations needed, final TVD |
| Plot | Stacked bar: parse time + verify time + repair time for hybrid vs full agentic time |
| Key insight | Hybrid path gives deterministic speed with LLM safety net |

---

## E9 — TVD vs. KL Divergence as Verification Metric

**RQ:** Is TVD the right metric, or does KL divergence catch different failure modes?

| Dimension | Detail |
|-----------|--------|
| Method | For every run in E1-E4, compute both TVD similarity and KL divergence |
| Plot | Scatter: TVD (x) vs KL (y), colored by pass/fail. Identify cases where metrics disagree. |
| Analysis | ROC curve: which metric better separates correct from incorrect translations at various thresholds |

---

## Data Collection

All experiments use `translate.py --json` piped to a collection script:

```bash
#!/usr/bin/env bash
# experiments/run_experiments.sh
# Usage: bash experiments/run_experiments.sh E1   (or E2, E3, etc.)

RESULTS_DIR="experiments/results"
mkdir -p "$RESULTS_DIR"

CATALYST_CIRCUITS=(examples/mlir/*.mlir)
QUAKE_CIRCUITS=(examples/quake_mlir/*.mlir)
ALL_CIRCUITS=("${CATALYST_CIRCUITS[@]}" "${QUAKE_CIRCUITS[@]}")
MODELS=(llama3.1-8b codellama-13b gpt-oss-20b)

case "$1" in
  E1)
    for circuit in "${ALL_CIRCUITS[@]}"; do
      # Deterministic
      python translate.py "$circuit" --json --shots 1000 >> "$RESULTS_DIR/e1_deterministic.jsonl"
      # Agentic per model
      for model in "${MODELS[@]}"; do
        for run in $(seq 1 5); do
          python translate.py "$circuit" --json --model "$model" \
            --force-agentic --shots 1000 >> "$RESULTS_DIR/e1_agentic_${model}.jsonl"
        done
      done
    done
    ;;
  E3)
    for circuit in examples/mlir/bell_state.mlir examples/mlir/ghz_state.mlir \
                   examples/mlir/parametric_rotation.mlir; do
      for model in "${MODELS[@]}"; do
        python translate.py "$circuit" --json --model "$model" \
          --force-agentic --max-iterations 10 --shots 1000 >> "$RESULTS_DIR/e3_convergence.jsonl"
      done
    done
    ;;
  E4)
    ALL_MODELS=(llama3.1-8b llama3.1-70b-q4 codellama-13b codellama-34b-q4 gpt-oss-20b)
    for circuit in "${ALL_CIRCUITS[@]}"; do
      for model in "${ALL_MODELS[@]}"; do
        for run in $(seq 1 3); do
          python translate.py "$circuit" --json --model "$model" \
            --force-agentic --shots 1000 >> "$RESULTS_DIR/e4_model_comparison.jsonl"
        done
      done
    done
    ;;
  *)
    echo "Usage: $0 {E1|E3|E4|...}"
    ;;
esac
```

All results also land in `logs/translations.jsonl` + `example_run_info/` for cross-referencing.

---

## Suggested Paper Structure

1. **Introduction** — Quantum compilation gap, need for flexible IR translation
2. **Background** — MLIR, QIR, Catalyst, CUDA Quantum, LLM-aided code generation
3. **System Architecture** — Parser -> Generator -> Agent -> Verifier pipeline (Figure 1)
4. **Verification Pipeline** — Gate counting + dual-backend simulation + TVD (Section 4)
5. **Experiments E1-E9** — Results and analysis (Section 5)
6. **Discussion** — When to use deterministic vs agentic, model selection guidance
7. **Related Work** — QIR spec, Catalyst, CUDA Quantum, LLM4Code
8. **Conclusion**

---

## Circuit Inventory

### Catalyst Dialect (`examples/mlir/`)
| Circuit | File | Qubits | Gates |
|---------|------|--------|-------|
| Bell State | `bell_state.mlir` | 2 | H, CNOT |
| GHZ State | `ghz_state.mlir` | 3 | H, CNOTx2 |
| Parametric Rotation | `parametric_rotation.mlir` | 1 | RX, RY, RZ |
| Quake Bell (cross-dialect) | `quake_bell_state.mlir` | 2 | H, CNOT |

### Catalyst Extended (`example/catalyst_mlir/`)
| Circuit | File | Qubits | Gates |
|---------|------|--------|-------|
| GHZ-5 | `code_ghz_5.mlir` | 5 | H, CNOTx4 |

### Quake Dialect (`examples/quake_mlir/`)
| Circuit | File | Qubits | Notes |
|---------|------|--------|-------|
| Bell | `code_bell.mlir` | 2 | Standard Bell |
| GHZ-5 | `code_ghz_5.mlir` | 5 | 5-qubit GHZ |
| Teleportation | `code_classic_teleportation.mlir` | 3 | Mid-circuit measurement + cc.if |
| Random circuits | `code_random_circuit_*.mlir` | varies | Robustness testing |
