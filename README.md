# MLIR-to-QIR Quantum Circuit Translator

A hybrid system that translates quantum circuits from MLIR dialects (Catalyst, Quake) to QIR using deterministic parsing, LLM-based agentic translation, and dual-backend verification.

**Paper:** _Agentic MLIR-to-QIR Translation with Dual-Backend Verification_ (IEEE QCE 2026)

## What It Does

```
Catalyst MLIR  ──┐
                  ├──> Deterministic Parser / LLM Agent ──> QIR (.ll)
Quake MLIR     ──┘                                            │
                                                              ▼
                                              Dual-Backend Verification
                                              (QIR Runner vs MLIR Backend)
                                                              │
                                                         TVD >= 95%?
                                                          ├── Yes: PASS
                                                          └── No: Repair loop
```

Three translation paths:
- **Deterministic** (fast, 100% accuracy on known dialects)
- **Agentic** (LLM-based, for unseen dialects)
- **Hybrid** (deterministic + LLM repair on verification failure)

## Quick Start

### Prerequisites

- Python 3.12+
- NVIDIA GPU with 8GB+ VRAM (for local LLMs; optional if using HuggingFace API)
- [Ollama](https://ollama.com/) (for local LLM serving; optional)

### Install

```bash
git clone <repo-url> && cd agentic_mlir_qir_updated

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Translate a circuit (CLI)

```bash
# Deterministic (no LLM needed)
python translate.py examples/mlir/bell_state.mlir

# With verification (shots mode)
python translate.py examples/mlir/bell_state.mlir --shots 1000

# With verification (exact probability mode, zero shot noise)
python translate.py examples/mlir/bell_state.mlir --mode probs

# Save QIR to file
python translate.py examples/mlir/bell_state.mlir -o output.ll

# JSON output (for scripting)
python translate.py examples/mlir/bell_state.mlir --json

# Gate comparison only (no simulation, faster)
python translate.py examples/mlir/bell_state.mlir --gate-only

# Skip all verification (fastest, translation only)
python translate.py examples/mlir/bell_state.mlir --no-verify
```

### Agentic translation (requires LLM)

```bash
# Option A: Local Ollama
ollama pull llama3.1:8b-instruct
python translate.py circuit.mlir --model llama3.1-8b

# Option B: HuggingFace free tier (no GPU needed)
export HF_TOKEN=hf_...   # get token at https://huggingface.co/settings/tokens
python translate.py circuit.mlir --model gpt-oss-20b

# Force LLM path even for known dialects
python translate.py circuit.mlir --model llama3.1-8b --force-agentic

# List all available models
python translate.py --list-models
```

### Launch the Web UI

```bash
streamlit run src/ui/app.py

# Share on network
streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

## CLI Reference

```
python translate.py [OPTIONS] FILE

Positional:
  FILE                   MLIR file path, or '-' for stdin

Options:
  -o FILE                Write QIR to file (metadata to stdout)
  --model KEY            Enable agentic pipeline with this model
  --force-agentic        Skip deterministic parser (requires --model)
  --max-iterations N     Max repair iterations (default: 5)
  --shots N              Simulation shots (default: 1000)
  --mode {shots,probs}   Verification mode (default: shots)
  --gate-only            Gate comparison only (no simulation)
  --no-verify            Skip all verification
  --json                 JSON output for scripting/CI
  --quiet / -q           QIR only, no metadata
  --list-models          Show available model keys

Exit codes:
  0    Translation verified
  1    Verification failed or error
  2    Unseen dialect (use --model)
  130  Ctrl-C
```

## Verification Modes

| Mode | MLIR Side | QIR Side | Shot Noise | Use Case |
|------|-----------|----------|------------|----------|
| `shots` (default) | `qml.sample()` 1K shots | `qirrunner` 1K shots | Both sides | Realistic execution |
| `probs` | `qml.probs()` exact | `qirrunner` 100K shots | QIR only (~0.04%) | Proving semantic correctness |

## Project Structure

```
agentic_mlir_qir_updated/
├── translate.py                  # CLI entry point
├── src/
│   ├── config/                   # Settings, LLM model configs
│   ├── dialects/                 # BaseDialect, CatalystDialect, QuakeDialect
│   ├── parsers/                  # SSA-aware MLIR parser
│   ├── generators/               # Template-based QIR generator
│   ├── verification/
│   │   ├── pipeline.py           # 4-stage verification (gate + QIR exec + MLIR exec + TVD)
│   │   ├── simulator_registry.py # Extensible backend registry with can_handle()
│   │   ├── qir_runner.py         # QIR execution via qirrunner (subprocess isolation)
│   │   ├── catalyst_runner.py    # Catalyst MLIR execution via PennyLane qjit
│   │   ├── quake_runner.py       # Quake MLIR execution via cudaq
│   │   ├── gate_counter.py       # Gate counting + comparison
│   │   └── metrics.py            # TVD, KL divergence, exact probability comparison
│   ├── agents/
│   │   ├── crew_manager.py       # CrewAI orchestration + 3-path routing
│   │   ├── translation_agent.py  # LLM translation with context engineering
│   │   └── verification_agent.py # Verification feedback
│   ├── tools/
│   │   ├── web_fetch_tool.py     # Web search for unseen dialects
│   │   ├── rag_tool.py           # ChromaDB knowledge retrieval
│   │   ├── gate_counter_tool.py  # Gate counting for agents
│   │   └── simulator_discovery_tool.py  # Find/cache simulators for unseen dialects
│   └── ui/
│       └── app.py                # Streamlit web interface
├── examples/
│   ├── mlir/                     # Catalyst MLIR examples
│   ├── quake_mlir/               # Quake MLIR examples (via cudaq)
│   └── qir/                      # QIR ground truth (via qiskit-qir)
├── example/
│   ├── catalyst_mlir/            # Catalyst examples (GHZ 5-100, MBQC, QEC, random)
│   ├── quake_mlir/               # Quake examples (GHZ 5-100, MBQC, random)
│   ├── ftqc_mlir/                # FTQC (unseen dialect) examples (Steane code)
│   └── qir/                      # Reference QIR files (hand-written + qiskit-qir)
├── example_quake/
│   └── openqasm_to_quake_mlir.py # OpenQASM 3 -> Quake MLIR converter
├── QIR/
│   └── qir_generation.py         # Qiskit -> QIR ground truth generator
├── experiments/                  # Reproducible experiment scripts (see below)
├── knowledge_base/               # Auto-populated docs (QIR specs, MLIR docs)
└── scripts/                      # Setup scripts (Ollama, knowledge base)
```

## Reproducing Experiments

The `experiments/` directory contains scripts to reproduce all results from the paper.

### Smoke test (2 minutes, no LLM needed)

```bash
bash experiments/run_smoke_test.sh
```

### Deterministic experiments (no LLM needed, ~1 hour total)

```bash
bash experiments/run_e1_correctness.sh    # E1: Translation correctness
bash experiments/run_e2_scalability.sh    # E2: GHZ scaling (2-100 qubits)
bash experiments/run_e6_cross_dialect.sh  # E6: Cross-dialect portability
bash experiments/run_e4_mutations.sh      # E4: Mutation-based verification testing
```

### LLM experiments (requires Ollama or HF_TOKEN, ~10-18 hours)

```bash
# Start Ollama and pull models first
ollama pull llama3.1:8b-instruct
ollama pull codellama:13b-instruct

bash experiments/run_e3_agentic.sh        # E3: Deterministic vs Agentic vs Hybrid
bash experiments/run_e5_llm_profiling.sh  # E5: 5-model performance comparison
bash experiments/run_e7_unseen_dialect.sh # E7: Unseen dialect (FTQC)
```

For E5 with all 5 models (including cloud):
```bash
export HF_TOKEN=hf_...  # for gpt-oss-20b
# Also ensure llama3.1:70b and codellama:34b are pulled for full profiling
bash experiments/run_e5_llm_profiling.sh
```

### Analyze results

```bash
python experiments/analyze_results.py all   # All experiments
python experiments/analyze_results.py e1    # Single experiment
```

Results are written to `experiments/results/` as JSONL files.

### Experiment Summary

| Experiment | What It Tests | LLM Needed | Time |
|------------|--------------|------------|------|
| E1 | Translation correctness (72 circuit-dialect pairs) | No | ~30 min |
| E2 | Scalability (GHZ 5-100 qubits, 20 sizes) | No | ~20 min |
| E3 | Deterministic vs Agentic vs Hybrid paths | Yes | ~8 hr |
| E4 | Verification reliability (5 mutation types) | No | ~30 min |
| E5 | LLM model profiling (5 models) | Yes | ~8 hr |
| E6 | Cross-dialect portability (14 matched pairs) | No | ~20 min |
| E7 | Unseen dialect translation (FTQC) | Yes | ~30 min |

## Benchmark Circuits

39 unique circuits across 9 categories:

| Category | Circuits | Qubits | Dialects |
|----------|----------|--------|----------|
| Standard (Bell, GHZ-3) | 2 | 2-3 | Both |
| GHZ scaling | 20 (GHZ-5 to GHZ-100, every 5) | 5-100 | Both |
| MBQC | 4 (teleport, RZ, RX, CNOT) | 2-4 | Both |
| Conditional | 1 (teleportation) | 3 | Both |
| Random | 5 | 2-7 | Both |
| QEC | 1 (Steane code) | 7 | Catalyst |
| Parametric | 1 (RX/RY/RZ) | 1 | Catalyst |
| Variational | 1 (autodiff gradient) | 1 | Catalyst |
| FTQC (unseen) | 4 (Steane 1Q-3Q) | 1-3 logical | FTQC only |

Generate additional Quake MLIR circuits from OpenQASM:
```bash
python example_quake/openqasm_to_quake_mlir.py
```

Generate QIR ground truth from Qiskit:
```bash
python QIR/qir_generation.py > examples/qir/output.ll
```

## Supported LLM Models

| Model | Provider | Params | VRAM | Setup |
|-------|----------|--------|------|-------|
| llama3.1-8b | Ollama (local) | 8B | ~6 GB | `ollama pull llama3.1:8b-instruct` |
| codellama-13b | Ollama (local) | 13B | ~8 GB | `ollama pull codellama:13b-instruct` |
| codellama-34b-q4 | Ollama (local) | 34B | ~20 GB | `ollama pull codellama:34b-instruct-q4_K_M` |
| llama3.1-70b-q4 | Ollama (local) | 70B | ~40 GB | `ollama pull llama3.1:70b-instruct-q4_K_M` |
| gpt-oss-20b | HuggingFace API | 20B | Cloud | `export HF_TOKEN=hf_...` |

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pennylane | 0.44.0 | Quantum ML framework |
| pennylane-catalyst | 0.14.0 | Catalyst MLIR JIT execution |
| cudaq | 0.13 | CUDA Quantum / Quake dialect |
| qirrunner | 0.9.1 | QIR execution (qir-alliance) |
| crewai | 1.10.0 | Multi-agent orchestration |
| streamlit | 1.54+ | Web UI |
| pyqir | 0.12.3 | QIR parsing |

## Environment Setup

```bash
cp .env.example .env
# Edit .env with your tokens:
#   HF_TOKEN=hf_...          (for gpt-oss-20b cloud model)
#   SERPER_API_KEY=...        (optional, for web search tool)
```

## Optional: Knowledge Base (for RAG mode)

The system defaults to context engineering (no RAG needed). To enable RAG:

```bash
python scripts/fetch_knowledge.py    # Download QIR specs, MLIR docs
python scripts/initialize_db.py      # Index into ChromaDB
```

## License

MIT
