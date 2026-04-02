# Experiment Design for IEEE QCE 2026 — QSYS Track
# Agentic LLM-Aided Translation of Quantum Intermediate Representations with Automated Verification

**Target:** IEEE QCE 2026 — Quantum System Software (QSYS) Track
**Format:** Full paper (8–10 pages + 2 reference pages)
**Abstract deadline:** April 6, 2026 (AoE)
**Full paper deadline:** April 13, 2026 (AoE)
**Notification:** July 6, 2026
**Created:** 2026-04-01
**Revised:** 2026-04-01 (updated with full circuit inventory + probs mode)

---

## QSYS Track Alignment

Our system hits 4 of the track's top topics:

| QSYS Topic | Our System |
|---|---|
| Quantum-specific **intermediate representations** | MLIR-to-QIR translation |
| **Generative AI** in quantum software creation | LLM-aided agentic translation |
| **Testing, validation, verification** methodologies | Dual-backend TVD verification pipeline |
| **Compilers, transpilers**, and profilers | Multi-dialect parser + QIR generator |

---

## Complete Circuit Inventory

### Catalyst Dialect — `example/catalyst_mlir/` (20 files)

| ID | Circuit | File | Qubits | Gate Types | Category |
|---|---|---|---|---|---|
| C1 | Bell state | `code_bell.mlir` | 2 | H, CNOT | Standard |
| C2 | GHZ-5 | `code_ghz_5.mlir` | 5 | H, CNOT×4 | GHZ scaling |
| C3 | GHZ-10 | `code_ghz_10.mlir` | 10 | H, CNOT×9 | GHZ scaling |
| C4 | GHZ-15 | `code_ghz_15.mlir` | 15 | H, CNOT×14 | GHZ scaling |
| C5 | GHZ-20 | `code_ghz_20.mlir` | 20 | H, CNOT×19 | GHZ scaling |
| C6 | GHZ-25 | `code_ghz_25.mlir` | 25 | H, CNOT×24 | GHZ scaling |
| C7 | GHZ-30 | `code_ghz_30.mlir` | 30 | H, CNOT×29 | GHZ scaling |
| C8 | GHZ-100 | `code_ghz_100.mlir` | 100 | H, CNOT×99 | GHZ scaling |
| C9 | Classic teleportation | `code_classic_teleportation.mlir` | 3 | H, CNOT, X, Z, scf.if | Conditional |
| C10 | MBQC teleport | `code_teleport.mlir` | 2 | H, CZ, scf.if | MBQC |
| C11 | MBQC rotation RZ | `code_rz.mlir` | 2 | H, CZ, RZ(π/4), scf.if | MBQC parametric |
| C12 | MBQC rotation RX | `code_rx.mlir` | 3 | H, CZ, RZ, RX, scf.if | MBQC parametric |
| C13 | MBQC CNOT | `code_cnot.mlir` | 4 | H, CZ, scf.if | MBQC multi-correction |
| C14 | Steane code (FTQC) | `steane_ft1qb.mlir` | 7 | H, CNOT×10, Probs | QEC |
| C15 | Autodiff gradient | `autodiff_gradient.mlir` | 1 | RX(θ), ExpVal(PauliZ) | Variational/Gradient |
| C16–C20 | Random circuits | `code_random_circuit_{658,1847,2449,3990,6994}.mlir` | 2–7 | Mixed (T, S, RX, RY, RZ, CZ, SWAP) | Robustness |

Also in `examples/mlir/`: `bell_state.mlir` (2q), `ghz_state.mlir` (3q), `parametric_rotation.mlir` (1q RX/RY/RZ).

### Quake Dialect — `example/quake_mlir/` (18 files)

| ID | Circuit | File | Qubits | Gate Types | Category |
|---|---|---|---|---|---|
| Q1 | Bell state | `code_bell.mlir` | 2 | H, X(CNOT) | Standard |
| Q2 | GHZ-5 | `code_ghz_5.mlir` | 5 | H, X(CNOT)×4 | GHZ scaling |
| Q3 | GHZ-10 | `code_ghz_10.mlir` | 10 | H, X(CNOT)×9 | GHZ scaling |
| Q4 | GHZ-15 | `code_ghz_15.mlir` | 15 | H, X(CNOT)×14 | GHZ scaling |
| Q5 | GHZ-20 | `code_ghz_20.mlir` | 20 | H, X(CNOT)×19 | GHZ scaling |
| Q6 | GHZ-25 | `code_ghz_25.mlir` | 25 | H, X(CNOT)×24 | GHZ scaling |
| Q7 | GHZ-30 | `code_ghz_30.mlir` | 30 | H, X(CNOT)×29 | GHZ scaling |
| Q8 | GHZ-100 | `code_ghz_100.mlir` | 100 | H, X(CNOT)×99 | GHZ scaling |
| Q9 | Classic teleportation | `code_classic_teleportation.mlir` | 3 | H, CNOT, Z, cc.if | Conditional |
| Q10 | MBQC teleport | `code_mbqc_teleport.mlir` | 2 | H, CZ, cc.if | MBQC |
| Q11 | MBQC rotation RZ | `code_mbqc_rotation_rz.mlir` | 2 | H, CZ, RZ, cc.if | MBQC parametric |
| Q12 | MBQC rotation RX | `code_mbqc_rotation_rx.mlir` | 3 | H, CZ, RZ, RX, cc.if | MBQC parametric |
| Q13 | MBQC CNOT | `code_mbqc_cnot.mlir` | 4 | H, CZ, cc.if | MBQC multi-correction |
| Q14–Q18 | Random circuits | `code_random_circuit_{658,1847,2449,3990,6994}.mlir` | 2–7 | Mixed | Robustness |

### QIR Ground Truth (via qiskit-qir)

| File | Qubits | Source |
|---|---|---|
| `examples/qir/bell_state_generated.ll` | 2 | Qiskit QuantumCircuit |
| `examples/qir/code_ghz_30.ll` | 30 | Qiskit QuantumCircuit |
| `examples/qir/code_ghz_100.ll` | 100 | Qiskit QuantumCircuit |

### Circuit Categories Summary

| Category | Count | Qubit Range | Dialects | Key Feature |
|---|---|---|---|---|
| **GHZ scaling** | 7 sizes × 2 dialects = 14 | 5–100 | Both | Scalability ladder |
| **Standard** (Bell, GHZ-3) | 3 × 2 = 6 | 2–3 | Both | Baseline correctness |
| **Conditional** (teleportation) | 1 × 2 = 2 | 3 | Both | Mid-circuit measurement |
| **MBQC** | 4 × 2 = 8 | 2–4 | Both | Measurement-based QC |
| **Parametric** | 1 (Catalyst) + 1 (RX/RY/RZ) | 1 | Catalyst | Rotation gates |
| **QEC** (Steane code) | 1 | 7 | Catalyst | Error correction |
| **Variational** (autodiff) | 1 | 1 | Catalyst | Gradient/ExpVal |
| **Random** | 5 × 2 = 10 | 2–7 | Both | Gate diversity |
| **Total unique circuits** | **~23** | 1–100 | | |
| **Total files** | **~46** | | | |

### Verification Modes

| Mode | MLIR side | QIR side | Shot noise | Use case |
|---|---|---|---|---|
| `shots` (default) | `qml.sample()` 1K shots | `qirrunner` 1K shots | Both sides | Realistic execution |
| `probs` (new) | `qml.probs()` exact | `qirrunner` 100K shots | QIR only (~0.04%) | Proving semantic correctness |

---

## E1 — Translation Correctness Across Dialects (Table 1)

> **RQ:** Can the system produce semantically correct QIR from both Catalyst and Quake MLIR?

| Dimension | Detail |
|---|---|
| Circuits | **All 23 unique circuits**, both dialects where available (46 total files) |
| Path | Deterministic only |
| Verification | Both `shots` (1000) and `probs` (exact) modes |
| Metrics | Gate match (binary), TVD similarity (%), structural QIR validity |
| Ground truth | GHZ-30 and GHZ-100: compare against `qiskit-qir` reference `.ll` files |
| Key output | **Table 1**: circuit × dialect × mode → {gate_match, TVD}. **Heatmap** of TVD results. |

**Circuit breakdown for E1:**

| Group | Circuits | Expected Difficulty |
|---|---|---|
| Standard | Bell, GHZ-3, GHZ-5 | Easy — baseline |
| GHZ scaling | GHZ-{10,15,20,25,30,100} | Easy for deterministic — tests scalability |
| MBQC | teleport, rotation_rz, rotation_rx, cnot | Medium — conditionals |
| Random | 5 circuits | Medium — diverse gate sets |
| QEC | Steane code | Hard — complex structure |
| Variational | autodiff gradient | Hard — ExpVal/gradient ops |

**Key insight:** Probs mode should give ~100% TVD for all correct translations, while shots mode gives 96–99%. Reporting both proves shot noise is the only source of TVD < 100%.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## E2 — Scalability: Circuit Size vs. Translation Quality

> **RQ:** How does translation quality and time scale with circuit complexity?

| Dimension | Detail |
|---|---|
| Circuits | GHZ-{2,3,5,10,15,20,25,30,100} — 9-point scaling ladder × 2 dialects |
| Paths | Deterministic, Agentic (best model) |
| Verification | `probs` mode (for clean scaling curves without shot noise) |
| Metrics | Translation time (ms), TVD, QIR token count, gate count accuracy |
| Key plots | (a) **Line chart**: qubit count (x) vs translation time (y, log scale), one line per path × dialect. (b) **Scatter**: qubit count vs TVD. |
| Hypothesis | Deterministic: O(n) time, TVD ≈ 100% at all sizes. Agentic: degrades past ~20-30 qubits (context window). |

**New:** Using `probs` mode eliminates shot noise from the scaling curve, so any TVD drop is purely from translation error — much cleaner signal.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## E3 — Agentic vs. Deterministic vs. Hybrid Translation Paths

> **RQ:** When does LLM-aided translation add value over deterministic parsing?

| Dimension | Detail |
|---|---|
| Circuits | Representative subset (14 circuits): Bell, GHZ-{5,10,20}, teleportation, MBQC-{teleport, rz, rx, cnot}, random-{658,1847,3990,6994}, Steane code |
| Dialects | Both Catalyst and Quake where available |
| Paths | (a) Deterministic, (b) Force-agentic, (c) Hybrid (deterministic + repair) |
| Models | `llama3.1-8b` (general), `codellama-13b` (code-specialized) |
| Repeats | 3 per (circuit, path, model) — captures LLM variance |
| Metrics | TVD, gate match rate, wall-clock time, iterations to converge |
| Key plots | (a) **Grouped bar chart**: path × model → avg TVD. (b) **Box plot**: TVD distribution per path. (c) **Stacked bar**: time breakdown (parse + verify + repair). |

**New in circuit selection:** MBQC circuits test conditional handling (harder for LLMs). Steane code tests QEC patterns.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## E4 — Verification Pipeline Reliability via Mutation Testing

> **RQ:** Does dual-backend simulation with TVD reliably detect translation errors?

| Dimension | Detail |
|---|---|
| Method | (a) Run correct translations → record TVD. (b) Inject deliberate errors into correct QIR → record TVD. |
| Mutation types | 5 categories: |
| | 1. **Gate substitution**: H → X |
| | 2. **Qubit swap**: CNOT(0,1) → CNOT(1,0) |
| | 3. **Gate deletion**: remove one CNOT from GHZ |
| | 4. **Parameter perturbation**: RX(π/4) → RX(π/2) |
| | 5. **Gate insertion**: add spurious Z gate |
| Circuits | Bell, GHZ-{3,5,10}, parametric, MBQC-rz, random-{658, 3990} (8 circuits) |
| Verification | Both `shots` and `probs` modes |
| Metrics | TVD for correct vs mutated, detection rate per mutation type, false positive/negative rates |
| Key plots | (a) **ROC curve**: TVD threshold (x) vs detection rate (y). (b) **Bar chart**: detection rate per mutation type. (c) **Comparison**: TVD vs KL divergence detection. |
| Script | `experiments/inject_mutations.py` — takes correct `.ll`, applies mutation, returns modified `.ll` |

**New:** Using `probs` mode on mutations makes the signal cleaner — a mutated circuit should give TVD significantly below 100%, while a correct circuit gives exactly 100%. Clear separation.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## E5 — LLM Model Performance & Time Profiling (LLM-Only Path)

> **RQ:** How do different LLM models compare in translation quality, speed, and iteration count on the force-agentic (LLM-only) path?

| Dimension | Detail |
|---|---|
| Circuits | 8-circuit subset: Bell, GHZ-{5,10}, random-{658,3990}, teleportation, random-1847, Steane code |
| Models | `llama3.1-8b`, `codellama-13b`, `gpt-oss-20b` (+ optionally `llama3.1-70b-q4`, `codellama-34b-q4` if GPU available) |
| Path | Force-agentic only (`--force-agentic --model KEY`) |
| Repeats | 3 per (circuit, model) |
| Metrics | TVD similarity, gate match rate, wall-clock translation time, iterations to converge, success rate |
| Key plots | (a) **Radar chart**: model → {TVD, speed, iterations, success rate}. (b) **Pareto frontier**: quality (TVD) vs cost (time). (c) **Bar chart**: per-model success rate by circuit difficulty. |
| Key insight | Is code-specialized (CodeLlama) better than general (Llama3.1) for IR translation? How does free cloud (gpt-oss-20b) compare to local models? |
| Script | `experiments/run_e5_llm_profiling.sh` |

**Rationale:** Replaced RAG ablation study — the system now uses context engineering (structured prompts) rather than RAG retrieval. This experiment provides practical model selection guidance for quantum tool developers.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## E6 — Cross-Dialect Portability: Same Circuit, Different Origins

> **RQ:** Does the system produce semantically equivalent QIR regardless of input dialect?

| Dimension | Detail |
|---|---|
| Circuits | All circuits available in BOTH Catalyst and Quake (15+ matched pairs): Bell, GHZ-{5,10,15,20,25,30,100}, teleportation, MBQC-{teleport,rz,rx,cnot}, random×5 |
| Method | Translate same logical circuit from Catalyst MLIR and Quake MLIR → compare the two QIR outputs |
| Verification | `probs` mode (eliminates shot noise from comparison) |
| Metrics | Gate-level structural diff of two QIRs, TVD between QIR_catalyst and QIR_quake executions |
| Key plot | **Scatter**: TVD(QIR from Catalyst) vs TVD(QIR from Quake) per circuit. Points on diagonal = both equally correct. |

**New:** MBQC circuits add conditional-handling portability testing. With `probs` mode, any deviation from 100% TVD is a real semantic difference, not shot noise.

<!-- REVIEW COMMENT:
Your comments here...
-->

---

## Experiments Deferred to Future Work

| Idea | Decision | Reason |
|---|---|---|
| Unseen dialect handling | **Defer** | Hard to evaluate rigorously in 12 days; good future work |
| 5+ model comparison | **Now E5** | Full LLM profiling replaces RAG ablation |
| RAG ablation study | **Dropped** | System uses context engineering, not RAG |
| Mock vs real backend comparison | **Report in E1** | Row in Table 1 |
| TVD vs KL divergence | **Folded into E4** | Extra column in ROC analysis |
| Autodiff/gradient circuit translation | **Stretch goal** | Requires ExpVal/gradient ops in QIR generator — may not parse |

---

## Execution Timeline (12-Day Sprint)

| Days | Experiment | Priority | Estimated Time | Notes |
|---|---|---|---|---|
| 1–2 | **E1** — Correctness baseline | CRITICAL | ~1 hr | Deterministic only, both modes |
| 2–3 | **E2** — Scalability (GHZ ladder) | HIGH | ~2 hr | Deterministic fast; agentic for 1 model |
| 3–4 | **E6** — Cross-dialect portability | HIGH | ~1 hr | Unique differentiator, probs mode |
| 4–6 | **E4** — Mutation verification | HIGH | ~4 hr | Write injection script, run experiments |
| 6–9 | **E3** — Agentic comparison | MEDIUM | ~8 hr | Slowest (LLM runs × 3 repeats) |
| 9–10 | **E5** — LLM profiling | MEDIUM | ~4–8 hr | Multi-model comparison |
| 10–12 | **Writing** | CRITICAL | — | Paper draft, figures, polish |

---

## Recommended Paper Structure (10 pages)

| Section | Pages | Content |
|---|---|---|
| 1. Introduction | 1.0 | Quantum compilation gap, MLIR ecosystem fragmentation, 4 contributions |
| 2. Background | 1.0 | MLIR, QIR, Catalyst, Quake, MBQC, LLM-aided code generation |
| 3. System Architecture | 1.5 | Pipeline diagram, 3-path routing, extensible registry, probs mode |
| 4. Verification Pipeline | 1.0 | Gate counting, dual-backend simulation, TVD (shots + exact), mutation testing |
| 5. Evaluation | 3.5 | E1–E6 results with figures and tables |
| 6. Discussion | 1.0 | When to use which path, limitations, threats to validity |
| 7. Related Work | 0.5 | QIR spec, Catalyst, cudaq, LLM4Code, Qiskit transpiler |
| 8. Conclusion | 0.5 | Summary, future work (unseen dialects, hardware backends) |
| References | 2.0 | (extra pages allowed) |

---

## Data Collection

All experiments use `translate.py --json`:

```bash
RESULTS_DIR="experiments/results"
mkdir -p "$RESULTS_DIR"

# Canonical circuit directories
CATALYST_DIR="example/catalyst_mlir"
QUAKE_DIR="example/quake_mlir"
CATALYST_EXTRA="examples/mlir"

# E1: Correctness (deterministic, both dialects)
for f in "$CATALYST_DIR"/*.mlir "$CATALYST_EXTRA"/*.mlir; do
  python translate.py "$f" --json --shots 1000 >> "$RESULTS_DIR/e1_catalyst_shots.jsonl"
done
for f in "$QUAKE_DIR"/*.mlir; do
  python translate.py "$f" --json --shots 1000 >> "$RESULTS_DIR/e1_quake_shots.jsonl"
done

# E2: Scalability (GHZ ladder)
for n in 5 10 15 20 25 30 100; do
  python translate.py "$CATALYST_DIR/code_ghz_${n}.mlir" --json --shots 1000 \
    >> "$RESULTS_DIR/e2_scaling.jsonl"
  python translate.py "$QUAKE_DIR/code_ghz_${n}.mlir" --json --shots 1000 \
    >> "$RESULTS_DIR/e2_scaling.jsonl"
done

# E3: Agentic comparison (representative subset)
REPR_CIRCUITS=(
  "$CATALYST_DIR/code_bell.mlir"
  "$CATALYST_DIR/code_ghz_5.mlir"
  "$CATALYST_DIR/code_ghz_10.mlir"
  "$CATALYST_DIR/code_ghz_20.mlir"
  "$CATALYST_DIR/code_classic_teleportation.mlir"
  "$CATALYST_DIR/code_teleport.mlir"
  "$CATALYST_DIR/code_rz.mlir"
  "$CATALYST_DIR/code_rx.mlir"
  "$CATALYST_DIR/code_cnot.mlir"
  "$CATALYST_DIR/code_random_circuit_658.mlir"
  "$CATALYST_DIR/code_random_circuit_1847.mlir"
  "$CATALYST_DIR/code_random_circuit_3990.mlir"
  "$CATALYST_DIR/code_random_circuit_6994.mlir"
  "$CATALYST_DIR/steane_ft1qb.mlir"
)
MODELS=(llama3.1-8b codellama-13b)
for circuit in "${REPR_CIRCUITS[@]}"; do
  for model in "${MODELS[@]}"; do
    for run in $(seq 1 3); do
      python translate.py "$circuit" --json --model "$model" \
        --force-agentic --shots 1000 >> "$RESULTS_DIR/e3_agentic_${model}.jsonl"
    done
  done
done
```

Results directory: `experiments/results/`

---

## Scripts Needed

| Script | Purpose | Status |
|---|---|---|
| `experiments/run_smoke_test.sh` | Quick sanity check (~2 min) | DONE |
| `experiments/run_e1_correctness.sh` | E1 deterministic baseline (both modes) | DONE |
| `experiments/run_e2_scalability.sh` | E2 GHZ scaling ladder | DONE |
| `experiments/run_e3_agentic.sh` | E3 path comparison (3 paths × 2 models × 3 repeats) | DONE |
| `experiments/inject_mutations.py` | E4 error injection into QIR `.ll` files (5 mutation types) | DONE |
| `experiments/run_e4_mutations.sh` | E4 mutation verification (shots + probs) | DONE |
| `experiments/run_e5_llm_profiling.sh` | E5 LLM model performance profiling | DONE |
| `experiments/run_e6_cross_dialect.sh` | E6 cross-dialect portability (14 matched pairs) | DONE |
| `experiments/analyze_results.py` | Generate tables and summaries from JSONL | DONE |

### How to Run

```bash
# 1. Smoke test first (2 min)
bash experiments/run_smoke_test.sh

# 2. Deterministic experiments (fast, no LLM needed)
bash experiments/run_e1_correctness.sh      # ~15-30 min
bash experiments/run_e2_scalability.sh      # ~10-20 min
bash experiments/run_e6_cross_dialect.sh    # ~10-20 min

# 3. Mutation testing (no LLM needed)
bash experiments/run_e4_mutations.sh        # ~30-60 min

# 4. LLM experiments (requires Ollama or HF_TOKEN)
bash experiments/run_e3_agentic.sh          # ~6-10 hr
bash experiments/run_e5_llm_profiling.sh    # ~4-8 hr

# 5. Analyze all results
python experiments/analyze_results.py all
```
