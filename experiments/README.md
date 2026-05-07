# Reproducing the Experiments

This directory contains the four experiments reported in the IEEE QCE 2026
paper: **E1** (translation correctness), **E2** (scalability), **E3**
(cross-dialect portability), and **E4** (unseen-dialect translation).

---

## Prerequisites

From the repository root:

```bash
source venv/bin/activate
pip install -r requirements.txt qirrunner==0.9.1
```

For E4 only, an LLM backend is required:

```bash
# Option A: local Ollama (recommended; reproduces all five models in the paper)
bash scripts/setup_llm.sh

# Option B: HuggingFace cloud model only
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

* Inputs: 33 Catalyst circuits + 35 Quake circuits (68 dialect-circuit pairs).
* Modes: `shots` (1024 samples per backend) and `probs` (state-vector reference).
* Output: `experiments/results/e1/{catalyst,quake}_{shots,probs}.jsonl`.
* Wall time: ~30 min.

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

* Inputs: 3 FTQC circuits × 5 LLM models × 3 repeats = 45 trials.
* Models: `llama3.1-8b`, `llama3.1-70b-q4`, `codellama-13b`,
  `codellama-34b-q4`, `gpt-oss-20b`.
* Output: `experiments/results/e4/ftqc_<model>.jsonl`.
* Wall time: 2–4 hours (dominated by LLM inference and 70B model loading).

To run E4 with a single model only, edit the `MODELS=(...)` array near the
top of `run_e4_unseen_dialect.sh`.

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

---

## Hardware notes

The paper reports numbers from a workstation with an NVIDIA RTX 6000 Ada
(48 GB VRAM), an Intel Xeon w5-2465X, and 256 GB RAM running Ubuntu 22.04.
Smaller GPUs are sufficient for E1, E2, E3, and the smaller-model rows of
E4. Llama 3.1 70B (≈ 40 GB VRAM) is the only model in E4 that requires a
GPU larger than 24 GB.
