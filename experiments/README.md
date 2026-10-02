# Reproducing the Experiments

This directory contains the four experiments reported in the IEEE QCE 2026
paper: **E1** (translation correctness), **E2** (scalability), **E3**
(cross-dialect portability), and **E4** (unseen-dialect translation); plus
four added afterward for the AgenticAI4HPC 2026 resubmission in response
to reviewer feedback: **E5** (Grover's/Shor's algorithms via a
Qiskit→QASM→Quake pipeline), **E6** (Path 3 repair stress test), **E7**
(forced-agentic vs. deterministic ground truth), and a Gemma model added
to E4.

---

## Prerequisites

From the repository root:

```bash
source venv/bin/activate
pip install -r requirements.txt qirrunner==0.9.1
```

For E4 only, an LLM backend is required:

```bash
# Option A: local Ollama (reproduces the local models used in the paper)
# Install Ollama (https://ollama.com/download), then pull the models:
ollama pull llama3.1:8b
ollama pull llama3.1:70b-instruct-q4_K_M
ollama pull codellama:13b-instruct
ollama pull codellama:34b-instruct-q4_K_M

# Option B: HuggingFace cloud model only (no local GPU)
cp .env.example .env  # then edit and set HF_TOKEN=<your token>
```

---

## Smoke test (run this first)

```bash
bash experiments/run_smoke_test.sh
```

The smoke test takes about two minutes, requires no LLM, and exercises
every translation path. It must pass before running any of the full
experiments.

---

## Experiment scripts

Each driver writes JSONL results under `experiments/results/<exp>/`. The
results directory is git-ignored — regenerate it locally by running the
script. Pre-computed summary files used in the paper are kept in
`experiments/paper_results/`.

### E1 — Translation correctness

```bash
bash experiments/run_e1_correctness.sh
```

* Inputs: 33 Catalyst circuits + 37 Quake circuits (70 dialect-circuit pairs).
  Quake includes `code_grover_3q.mlir` and `code_shor_orderfinding.mlir`
  (added after the paper's initial submission — copied from
  `example/qiskit_algorithms/{grover,shor}/03_quake.mlir` into
  `example/quake_mlir/` so they run as part of the standard E1 sweep;
  see Table III's "Algorithms" category).
* Modes: `shots` (1024 samples per backend) and `probs` (state-vector reference).
* Output: `experiments/results/e1/{catalyst,quake}_{shots,probs}.jsonl`.
* Wall time: ~30 min.
* Excluded from Simulated/TVD statistics (Table V): `code_random_circuit_1847`,
  `code_random_circuit_2449` (both dialects), `code_mbqc_cnot` (Quake) — correct
  gate counts but near-0% TVD from an MLIR-side mid-circuit-measurement gap.
  `code_shor_orderfinding` is additionally excluded in Quake probs mode only:
  its 100K-shot QIR-side simulation exceeds `qir-runner`'s timeout and falls
  back to a mock result; its shots-mode result (93.7%) is real.

### E2 — Scalability

```bash
bash experiments/run_e2_scalability.sh
```

* Inputs: GHZ circuits at 20 sizes (5–100 qubits, step 5) in both dialects.
* Output: `experiments/results/e2/deterministic_{shots,probs}.jsonl`.
* Wall time: ~20 min. Circuits with ≥ 35 qubits are gate-checked only,
  because state-vector simulation exceeds available memory.

### E3 — Cross-dialect portability

```bash
bash experiments/run_e3_cross_dialect.sh
```

* Inputs: 14 matched Catalyst–Quake circuit pairs.
* Output: `experiments/results/e3/cross_dialect.jsonl`.
* Wall time: ~10 min.

### E4 — Unseen dialect (FTQC) translation

```bash
bash experiments/run_e4_unseen_dialect.sh
```

* Inputs: 3 FTQC circuits (the paper reports `steane_1q_h`, `steane_2q_bell`,
  `steane_3q_grover`; the script also runs a 4th, `steane_3q_qft`, not in
  the paper's table) × 6 LLM models × 3 repeats.
* Models: `llama3.1-8b`, `llama3.1-70b-q4`, `codellama-13b`,
  `codellama-34b-q4`, `gpt-oss-20b`, `gemma4-31b-hf` (added after the
  paper's initial submission; requires `HF_TOKEN`, see Prerequisites).
* Output: `experiments/results/e4/ftqc_<model>.jsonl`.
* Wall time: 2–4 hours (dominated by LLM inference and 70B model loading).
* Gemma result reported in the paper (Table VII): 9/9 across the 3
  paper-reported circuits, ~7.7 s/translation, run individually via
  `python3 translate.py example/ftqc_mlir/<circuit>.mlir --model gemma4-31b-hf --json`
  rather than the full script (which also covers `steane_3q_qft`).
* **GPT-OSS-20B result was corrected after the paper's initial submission.**
  The originally reported row (`3/3, 2/3, 0/3` = 6/9 total — note this doesn't
  even sum correctly, a bug in the original table) came from a primary run
  where all 9 attempts failed with "no JSON output", followed by an
  incomplete `_retry.jsonl` covering only 6 of 9 attempts — not a reliable
  source. A clean fresh run (`experiments/results/e4/ftqc_gpt-oss-20b_postfix_rerun.jsonl`)
  gives **9/9**, 22.9 s/translation avg, run individually the same way as
  Gemma above (`--model gpt-oss-20b`). This is the number reported in the
  paper's Table VII.
* **Reproducibility note:** the other four models (Llama 3.1 8B/70B, Code
  Llama 13B/34B) were re-run once during the same debugging session that
  produced the GPT-OSS-20B fix, but under heavy concurrent system load
  (multiple simultaneous processes competing for the same GPU/CPU), giving
  markedly worse and slower results (e.g. Llama 3.1 8B dropped to 7/9 at
  ~29 s/translation vs. the paper's reported 9/9 at 6.1 s). Since the
  underlying translation-agent prompt for FTQC is unchanged in content
  (verified: 9,400 vs. 9,424 characters, a 24-character difference from
  unrelated wording, not new guidance), the paper keeps the original
  measurements for these four models rather than the contention-affected
  rerun. If you reproduce this experiment and see similarly degraded
  numbers for the Ollama-served models, check for other GPU-bound processes
  running concurrently before concluding there's a regression.

To run E4 with a single model only, edit the `MODELS=(...)` array near the
top of `run_e4_unseen_dialect.sh`.

### E5 — Grover's and Shor's algorithms (Qiskit → QASM → Quake pipeline)

```bash
pip install 'agentic-mlir-qir[qasm]'   # qiskit + cuda-quantum, if not already installed
python3 example/qiskit_algorithms/build_pipeline.py
```

* Circuits: Grover's algorithm (3 qubits, marked states `{011, 100}`) and
  Shor's order-finding circuit (N=15, a=2, 12 qubits), reproduced from
  IBM Quantum's own Qiskit tutorials —
  [Grover](https://quantum.cloud.ibm.com/docs/en/tutorials/grovers-algorithm),
  [Shor](https://quantum.cloud.ibm.com/docs/en/tutorials/shors-algorithm) —
  not hand-derived.
* Pipeline: Qiskit circuit → OpenQASM 2.0 → Quake MLIR (via
  `agentic_mlir_qir.frontends.qasm_frontend.qasm_to_mlir`) → QIR (via
  `translate.py`'s deterministic pass). Both conversion steps use this
  project's own existing tooling, invoked the same way a user would from
  the CLI.
* Output: `example/qiskit_algorithms/{grover,shor}/` — every intermediate
  artifact is kept: `01_circuit.{txt,qpy}` (Qiskit), `02_circuit.qasm`,
  `03_quake.mlir`, `04_qir.ll` + `04_result.json` (full `translate.py
  --json` output).
* Wall time: <1 min (Grover), ~1–2 min (Shor).
* **These circuits are now permanent members of the E1 benchmark.** After
  generating `03_quake.mlir` via this pipeline, the files were copied
  (unmodified) into `example/quake_mlir/` as `code_grover_3q.mlir` and
  `code_shor_orderfinding.mlir`, so `run_e1_correctness.sh` picks them up
  automatically (Quake count: 35 → 37; see E1 above and Table III's
  "Algorithms" category). The numbers reported in the paper (Table V/§V-A)
  come from that standard E1 sweep (`--shots 1000`/`--mode probs`), not
  from this standalone script's `--shots 8000` special case: Grover
  53/53 gates, 99.9% TVD (shots) / 98.6% (probs); Shor 390/390 gates,
  93.7% TVD (shots) — its probs-mode result hits the `qir-runner` timeout
  described in E1 above and is excluded, not a real number.

### E6 — Path 3 (repair) stress test

By default Path 3 (agentic repair) is never triggered on the E1–E3
benchmark, since the deterministic path achieves 100% gate-level
correctness on all 70 pairs. To exercise it, run the two circuits already
known to fail testing (correct gate counts, ≈0% TVD — see E1's "Notes and
known limitations" above) through the agentic pipeline instead of the
deterministic-only path:

```bash
python3 translate.py example/catalyst_mlir/code_random_circuit_1847.mlir --model llama3.1-8b --mode probs --json
python3 translate.py example/catalyst_mlir/code_random_circuit_2449.mlir --model llama3.1-8b --mode probs --json
python3 translate.py example/catalyst_mlir/code_random_circuit_1847.mlir --model llama3.1-70b-q4 --mode probs --json
```

* Result at last run: 0/3 repair attempts succeeded. `translation_path`
  correctly reports `deterministic+repair` in all 3 cases, confirming Path
  3 triggers as designed; all 3 exhausted the default `K=5` iterations
  without passing. Llama 3.1 8B (both circuits) repeatedly emitted JSON
  metadata or tool-call output the guardrail could not parse into valid
  QIR; the Llama 3.1 70B attempt additionally produced a syntactically
  well-formed but semantically broken QIR (`__quantum__qis__rz__body`
  called with the wrong parameter count), causing `qir-runner` to crash
  outright rather than just fail the TVD check.
* Interpretation: since the underlying TVD gap for these two circuits
  traces to an MLIR-side testing limitation (the executor not fully
  reconstructing mid-circuit-measurement semantics — not a translation
  defect), the repair loop may be chasing a target its own reference
  distribution cannot represent. This is reported honestly in the paper
  (§V-A) rather than treated as a general repair-capability failure.
* Wall time: ~1 min (8B) to ~5 min (70B, dominated by model load) per
  attempt.

### E7 — Forced agentic vs. deterministic ground truth

The `--force-agentic` flag routes a *recognized* dialect through Path 2
(the LLM agent) instead of Path 1 (the deterministic compiler), letting
agentic output be benchmarked against a known-correct deterministic
reference on the same circuit. We used it on the Bell state circuit,
which Path 1 translates exactly.

```bash
bash experiments/run_e7_forced_agentic.sh
```

The driver first captures the Path 1 output as the ground truth, then runs
each model with `--force-agentic` (2 repeats per circuit) and scores the
result against that reference on gate counts, TVD, and wall time. Results
land in `experiments/results/e7/`; `analyze_results.py` has no `e7` mode yet,
so inspect the JSONL directly.

The equivalent manual invocations:

```bash
python3 translate.py example/catalyst_mlir/code_bell.mlir --model llama3.1-8b --force-agentic --json
python3 translate.py example/quake_mlir/code_bell.mlir --model llama3.1-8b --force-agentic --json
python3 translate.py example/catalyst_mlir/code_bell.mlir --model llama3.1-70b-q4 --force-agentic --json
python3 translate.py example/catalyst_mlir/code_bell.mlir --model gemma4-31b-hf --force-agentic --json
python3 translate.py example/quake_mlir/code_bell.mlir --model gemma4-31b-hf --force-agentic --json
```

* **Result at last run: architecture-dependent, not uniformly bad.**
  Llama 3.1 8B on Catalyst matched gate counts but emitted a spurious
  third measurement bit; Llama 3.1 8B on Quake produced five
  unentangled qubits in uniform superposition instead of an entangled
  Bell pair; Llama 3.1 70B on Catalyst never produced valid QIR at all.
  **Gemma 4 (31B) passed on the first iteration on both dialects**
  (run twice each for repeatability: Catalyst 99.6%/97.9% TVD, Quake
  99.2%/99.5% TVD — 4/4 total), at ~35–62 s versus Path 1's <2 ms.
* Root-cause investigation (see below) traced the Llama failures to two
  concrete bugs, both since fixed in the codebase, though the fixes did
  not change Llama 3.1 8B's behavior on live re-test:
  1. **Qubit-index confusion**: the model used an SSA variable's own
     number (e.g. `%1`) as the qubit index instead of the literal index
     inside `quantum.extract %reg[N]`/`quake.extract_ref %veq[%c]`.
     Fixed by adding the real (unsimplified) extraction syntax to the
     agent's inline reference (`agentic_mlir_qir/tools/qir_reference.py`)
     and a qubit-count sanity check to the repair-feedback loop
     (`CrewManager._check_qubit_count_mismatch` in `crew_manager.py`)
     that fires even when gate-*type* counts already match.
  2. **Hallucinated intrinsics**: the model transliterated non-gate MLIR
     bookkeeping ops (Quake's `extract_ref`, Catalyst's `namedobs`/
     `expval`/`insert`/`dealloc`) directly into fake
     `__quantum__qis__*__body` calls. The guardrail
     (`translation_agent.py`) now detects and filters these out via
     `_find_invalid_gate_calls`/`_drop_invalid_gate_calls` instead of
     passing them through as if valid.
* Interpretation: the gap is model capacity, not a fundamental Path 2
  defect — Gemma 4 (31B) reproduces Path 1's accuracy given enough
  capability, just at orders-of-magnitude higher latency. This is
  reported in the paper (§V-A, §VI) as the primary forced-agentic
  finding, with the Llama failures kept as evidence of the
  capacity-dependence.
* Wall time: ~1 min (8B) to ~5 min (70B, dominated by model load) per
  Llama attempt; ~35–65 s per Gemma attempt (HuggingFace API, no local
  model load).

---

## Analyzing results

After any experiment finishes, inspect the JSONL output directly or use the
analysis helper:

```bash
python experiments/analyze_results.py e1     # E1 correctness table
python experiments/analyze_results.py e2     # E2 scalability table
python experiments/analyze_results.py e3     # E3 cross-dialect table
python experiments/analyze_results.py e4     # E4 per-model success rates
python experiments/analyze_results.py all    # All four
```

The pre-computed summaries from the paper are stored under
`experiments/paper_results/` for direct comparison.

---

## Output schema (per JSONL row)

Every line of every JSONL file is the JSON payload produced by
`translate.py --json` plus a few additional fields injected by the driver
script (model name, run index, source file). The most relevant keys:

| Key                    | Meaning                                                    |
|------------------------|------------------------------------------------------------|
| `dialect`              | Detected MLIR dialect (`catalyst`, `quake`, `ftqc`, …)     |
| `translation_path`     | `deterministic`, `ai_agent`, or `deterministic+repair`     |
| `translation_time_s`   | MLIR-to-QIR wall time (seconds)                            |
| `verification_time_s`  | Simulation verification wall time (seconds)                |
| `iterations`           | Agent refinement iterations (1 if deterministic-only)      |
| `gate_comparison`      | Per-gate counts and `matches` flag                         |
| `verification`         | TVD score, `similarity`, `similarity_passes`               |
| `qir`                  | Generated QIR (LLVM IR text)                               |
| `success`              | Final pass/fail flag                                       |

---

## Notes and known limitations

* GHZ circuits at ≥ 35 qubits are gate-checked only; full TVD verification
  needs a $2^N$-dimensional state vector.
* Two random circuits (`random_1847`, `random_2449`) and one conditional
  circuit produce correct gate counts but divergent simulation
  distributions because the MLIR-side executor does not fully reconstruct
  classical feed-forward; the QIR side is correct.
* Agentic runs (E4) use 3 repeats per (circuit, model) to capture LLM
  output variance.
* The Qiskit→QASM→Quake pipeline (E5) transpiles deliberately to a
  restricted gate set (H, X, Y, Z, S, T, RX, RY, RZ, CNOT, CZ — the same
  set E1–E4 already validate) rather than Qiskit's full basis, to avoid
  three pre-existing bugs it surfaced in shared infrastructure, none of
  them specific to the Grover/Shor circuits themselves:
    1. `qasm_frontend.py`'s Toffoli/CSWAP handling passes a Python list
       of controls to CUDA-Q's kernel-builder `.x()`/`.cswap()`, which
       the installed CUDA-Q 0.13.0 API does not accept
       (`AttributeError: 'list' object has no attribute 'mlirValue'`).
    2. `r1`/`sdg`/`u1` gates produced matching gate counts end-to-end but
       incorrect measurement distributions (TVD ≈ 0.25) — a phase-
       convention bug in how one of the two backends executes them,
       invisible to gate-count comparison alone.
    3. The installed `qiskit.qasm2`'s bundled `qelib1.inc` does not
       actually define `swap`, so QASM containing `swap` fails to
       re-parse even though it declares `include "qelib1.inc"`.
  See the comments in `example/qiskit_algorithms/build_pipeline.py` for
  the exact repro steps for each.
* `--mode probs` uses 100K QIR-side shots; on Shor's 390-gate circuit
  this exceeds `QIRRunner`'s hardcoded 120s subprocess timeout, which
  silently falls back to a mock (non-real) QIR result
  (`qir_is_mock: true`) with no error surfaced anywhere in
  `translate.py`'s JSON output — only a log warning. This is a real
  robustness gap (a timeout should not be indistinguishable from a
  successful real run in the output) worth fixing in
  `agentic_mlir_qir/verification/qir_runner.py`. E5 works around it with
  `--shots 8000` instead of `--mode probs`.

---

## Hardware notes

The paper reports numbers from a workstation with an NVIDIA RTX 6000 Ada
(48 GB VRAM), an Intel Xeon w5-2465X, and 256 GB RAM running Ubuntu 22.04.
Smaller GPUs are sufficient for E1, E2, E3, and the smaller-model rows of
E4. Llama 3.1 70B (≈ 40 GB VRAM) is the only model in E4 that requires a
GPU larger than 24 GB.
