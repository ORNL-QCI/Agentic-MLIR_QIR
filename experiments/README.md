# Reproducing Experiments

This directory contains all scripts needed to reproduce the results from the IEEE QCE 2026 paper.

## Quick Start

```bash
# 1. Smoke test (2 min, no LLM needed)
bash experiments/run_smoke_test.sh

# 2. All deterministic experiments (~1 hour, no LLM)
bash experiments/run_e1_correctness.sh
bash experiments/run_e2_scalability.sh
bash experiments/run_e6_cross_dialect.sh
bash experiments/run_e4_mutations.sh

# 3. LLM experiments (requires Ollama, ~10-18 hours)
bash experiments/run_e3_agentic.sh
bash experiments/run_e5_llm_profiling.sh

# 4. Analyze all results
python experiments/analyze_results.py all
```

## Scripts

| Script | Experiment | LLM? | Time |
|--------|-----------|------|------|
| `run_smoke_test.sh` | Sanity check | No | 2 min |
| `run_e1_correctness.sh` | E1: Translation correctness | No | 30 min |
| `run_e2_scalability.sh` | E2: GHZ scaling (2-100 qubits) | No | 20 min |
| `run_e3_agentic.sh` | E3: Path comparison (det/agentic/hybrid) | Yes | 8 hr |
| `run_e4_mutations.sh` | E4: Mutation-based verification testing | No | 30 min |
| `run_e5_llm_profiling.sh` | E5: 5-model LLM comparison | Yes | 8 hr |
| `run_e6_cross_dialect.sh` | E6: Cross-dialect portability | No | 20 min |
| `inject_mutations.py` | E4 support: QIR error injection | No | - |
| `analyze_results.py` | Generate tables from JSONL results | No | - |

## Prerequisites for LLM Experiments

```bash
# Local models (Ollama)
ollama pull llama3.1:8b-instruct
ollama pull codellama:13b-instruct
ollama pull llama3.1:70b-instruct-q4_K_M    # optional, 40GB VRAM
ollama pull codellama:34b-instruct-q4_K_M   # optional, 20GB VRAM

# Cloud model (HuggingFace free tier)
export HF_TOKEN=hf_...
```

## Output

Results are written to `experiments/results/<experiment>/` as JSONL files.

```bash
# View results for a specific experiment
python experiments/analyze_results.py e1

# View all results
python experiments/analyze_results.py all
```

## Notes

- GHZ-100 circuits skip simulation verification (100-qubit state vector exceeds memory)
- Two circuits with partial measurements (random_1847, random_2449) show TVD=0% due to measurement-wire mismatch between backends; gate counts are correct
- Agentic experiments use 3 repeats per (circuit, model) to capture LLM output variance

## Experiment Plan

See [QCE2026_EXPERIMENT_PLAN.md](QCE2026_EXPERIMENT_PLAN.md) for the full experiment design.
