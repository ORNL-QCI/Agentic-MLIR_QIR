# Agentic MLIR-to-QIR Translator

An open-source system for translating quantum circuits between Multi-Level
Intermediate Representation (MLIR) dialects (Catalyst, Quake, and unseen
dialects such as FTQC) and the Quantum Intermediate Representation (QIR).
The system selects between three translation paths based on dialect
recognition and verification outcomes:

1. **Deterministic path** — a hand-written parser plus QIR generator handles
   dialects with known grammars (Catalyst and Quake).
2. **Agentic path** — a large language model (LLM) agent generates QIR for
   unseen dialects under a structured prompt, with inline context engineering
   in place of retrieval-augmented generation.
3. **Repair path** — when verification fails on the deterministic path, the
   LLM agent corrects the output through a feedback loop.

A dual-backend verification pipeline executes the source MLIR and the
generated QIR on independent simulators and compares the resulting bitstring
distributions via total variation distance (TVD).

This repository accompanies the paper "Agentic MLIR-to-QIR Translation with
Verification: A Hybrid Deterministic and LLM Approach" (IEEE QCE 2026).

---

## Repository layout

```
.
├── translate.py                # Main CLI entry point (MLIR file → QIR)
├── agentic_mlir_qir/           # Source package (parsers, generators, agents, verification)
│   └── README.md               # Code architecture
├── experiments/                # Experiment scripts (E1, E2, E3, E4) and analysis
│   └── README.md               # How to run each experiment
├── example/                    # Benchmark circuit suite (38 circuits)
│   ├── catalyst_mlir/          # Catalyst-dialect MLIR inputs
│   ├── quake_mlir/             # Quake-dialect MLIR inputs
│   ├── ftqc_mlir/              # FTQC-dialect MLIR inputs (unseen dialect)
│   ├── qasm/                   # OpenQASM 2.0/3.0 inputs (via Qiskit + CUDA-Q)
│   └── qir/                    # Reference QIR ground truth
├── scripts/                    # Helper utilities (Qiskit-QIR ground-truth generator, Ollama setup)
├── requirements.txt
├── .env.example                # Template for API keys (HF_TOKEN, etc.)
└── README.md
```

---

## Quick start

### 1. Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install QIR runtime

The verification pipeline executes generated QIR through `qir-runner`:

```bash
pip install qirrunner==0.9.1
```

### 3. (Optional) Install LLM backends

The agentic path requires either a local Ollama instance or a HuggingFace
token. Both are optional — the deterministic path works without any LLM.

**Local LLMs via Ollama:**

```bash
# Install Ollama: https://ollama.com/download
bash scripts/setup_llm.sh        # Pulls Llama 3.1 8B, Code Llama 13B, etc.
```

**HuggingFace cloud LLMs:**

```bash
cp .env.example .env
# Edit .env and set HF_TOKEN=<your free HuggingFace token>
```

### 4. Run a translation

```bash
# Deterministic translation (Catalyst dialect, Bell state)
python translate.py example/catalyst_mlir/code_bell.mlir

# Agentic translation on the unseen FTQC dialect (requires Ollama + Llama 3.1)
python translate.py example/ftqc_mlir/steane_2q_bell.mlir --model llama3.1-8b

# JSON output (for CI / scripting)
python translate.py example/catalyst_mlir/code_bell.mlir --json

# Skip simulation verification (faster)
python translate.py example/catalyst_mlir/code_bell.mlir --no-verify

# List all available LLM model keys
python translate.py --list-models
```

### 4b. Translate OpenQASM input (optional)

OpenQASM 2.0 and 3.0 circuits are supported via a two-step path that reuses
existing tools: **Qiskit** parses the QASM and **CUDA-Q** emits Quake-dialect
MLIR, which then flows through the same deterministic MLIR → QIR pipeline.

The QASM frontend needs three packages. `qiskit` and `qiskit-qasm3-import`
are already in `requirements.txt` (installed in step 1); CUDA-Q is installed
the same way as the Quake verification backend:

```bash
# Qiskit + the OpenQASM 3 loader come from requirements.txt (step 1).
# Add CUDA-Q (see https://nvidia.github.io/cuda-quantum for your platform):
pip install cuda-quantum==0.13

# Translate an OpenQASM 2.0 circuit (with dual-backend verification)
python translate.py example/qasm/bell_state_v2.qasm

# Translate an OpenQASM 3.0 circuit
python translate.py example/qasm/bell_state_v3.qasm

# Read QASM from stdin (input starting with OPENQASM is auto-detected)
cat example/qasm/ghz_state_v2.qasm | python translate.py -

# Skip simulation verification (faster)
python translate.py example/qasm/bell_state_v2.qasm --no-verify

# Write the QIR to a file (translation metadata goes to stdout)
python translate.py example/qasm/bell_state_v2.qasm -o bell.ll

# JSON output for CI / scripting (includes "source_format": "openqasm2")
python translate.py example/qasm/bell_state_v2.qasm --json
```

Expected output for the Bell state (`bell_state_v2.qasm`):

```text
  Source format    : openqasm2 (converted to Quake MLIR via Qiskit + CUDA-Q)

── Translation Metadata ────────────────────────────
  Dialect          : quake
  Translation path : deterministic

── Gate Counts ─────────────────────────────────────
  Total              2     2  ✓ match

── Simulation Verification ─────────────────────────
  MLIR backend     : quake (QuakeRunner) (real execution)
  Gate match       : PASS
  TVD similarity   : 96.2%  PASS          # varies slightly with shot noise
  QIR distribution : 00:525  11:475
  MLIR distribution: 00:487  11:513

✓ SUCCESS — translation verified
```

From Python:

```python
import agentic_mlir_qir as amq

qasm = open("example/qasm/bell_state_v2.qasm").read()
res = amq.translate_qasm(qasm, verify=True, shots=2000)

print(res.source_format, res.dialect, res.success)   # openqasm2 quake True
print(res.verification.similarity)                    # ~0.96–1.0 (shot-noise dependent)
print(res.qir)                                         # the generated QIR (LLVM IR)
```

Supported gates: `h x y z s t sdg tdg rx ry rz p/u1 u3 cx cy cz ch swap
crx cry crz cp ccx cswap` (others raise a clear error).

### 5. Run the Streamlit demo (optional)

```bash
streamlit run agentic_mlir_qir/ui/app.py
```

---

## Reproducing paper experiments

The four experiments reported in the paper (E1, E2, E3, E4) each have a
shell driver under `experiments/`:

| Experiment | Script                                  | Wall time     |
|------------|-----------------------------------------|---------------|
| E1 — Translation Correctness            | `experiments/run_e1_correctness.sh`     | ~30 min       |
| E2 — Scalability                        | `experiments/run_e2_scalability.sh`     | ~20 min       |
| E3 — Cross-Dialect Portability          | `experiments/run_e3_cross_dialect.sh`   | ~10 min       |
| E4 — Unseen-Dialect Translation (FTQC)  | `experiments/run_e4_unseen_dialect.sh`  | 2–4 h (LLM)   |

A smoke test that exercises every translation path in roughly two minutes is
available at `experiments/run_smoke_test.sh`. See
[experiments/README.md](experiments/README.md) for full details, expected
outputs, and analysis commands.

---

## Hardware used in the paper

* NVIDIA RTX 6000 Ada GPU (48 GB VRAM)
* Intel Xeon w5-2465X CPU
* 256 GB RAM
* Ubuntu 22.04, Python 3.12

The deterministic path runs comfortably on a CPU-only laptop; the agentic
path needs a GPU large enough for the chosen Ollama model (≈ 6 GB for
Llama 3.1 8B, ≈ 40 GB for Llama 3.1 70B).

---

## Software versions

| Package              | Version  |
|----------------------|----------|
| PennyLane            | 0.44.0   |
| PennyLane-Catalyst   | 0.14.0   |
| CUDA-Q               | 0.13     |
| qir-runner           | 0.9.1    |
| CrewAI               | 1.10.0   |
| Ollama               | 0.6      |
| Python               | 3.12     |

The pinned versions used in the paper are recorded in `requirements.txt`.
`qir-runner` and CrewAI are under active development; later releases may
require minor adaptation.

---

## Citation

If you use this codebase, please cite:

```bibtex
@inproceedings{afrose2026agentic,
  author    = {Sharmin Afrose and Vicente Leyton-Ortega and Narasinga Rao Miniskar and Elaine Wong and Travis S. Humble},
  title     = {Agentic MLIR-to-QIR Translation with Verification: A Hybrid Deterministic and LLM Approach},
  booktitle = {Submitted to 2026 IEEE International Conference on Quantum Computing and Engineering (QCE)},
  year      = {2026}
}
```

---

## License

This codebase is released under the Apache License, Version 2.0. See
`pyproject.toml` for the package-level license declaration.

---

## Acknowledgments

This work was supported by the U.S. Department of Energy, Office of Science
under Contract No. DE-AC05-00OR22725, with funding from the Office of
Advanced Scientific Computing Research's Accelerated Research in Quantum
Computing Program's Modular and Error-Aware Software Stack for Heterogeneous
Quantum Computing Ecosystems (MACH-Q) project.

The authors thank the broader quantum-compiler community for the open-source
tools this work builds on, including PennyLane Catalyst, NVIDIA CUDA-Q,
the QIR Alliance and `qir-runner`, and the CrewAI multi-agent framework.

### DOE Public Access Plan

This manuscript has been authored by UT-Battelle, LLC, under Contract No.
DE-AC05-00OR22725 with the U.S. Department of Energy. The United States
Government retains and the publisher, by accepting the article for
publication, acknowledges that the United States Government retains a
non-exclusive, paid-up, irrevocable, worldwide license to publish or reproduce
the published form of this manuscript, or allow others to do so, for United
States Government purposes. The Department of Energy will provide public
access to these results of federally sponsored research in accordance with the
DOE Public Access Plan
(<https://www.energy.gov/doe-public-access-plan>).

### Authors and affiliation

Sharmin Afrose, Vicente Leyton-Ortega, Narasinga Rao Miniskar, Elaine Wong,
and Travis S. Humble &mdash; Oak Ridge National Laboratory, Oak Ridge, TN, USA
(<{afroses, leytonortheva, miniskarnr, wongey, humblets}@ornl.gov>).
