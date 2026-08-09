# Agentic MLIR-to-QIR Translator

An open-source system for translating quantum circuits from Multi-Level
Intermediate Representation (MLIR) dialects — Catalyst, Quake, and unseen
dialects such as FTQC — into the Quantum Intermediate Representation (QIR).

The system selects one of three translation paths based on dialect recognition
and verification outcome:

1. **Deterministic** — a hand-written parser and QIR generator handle dialects
   with known grammars (Catalyst, Quake).
2. **Agentic** — an LLM agent generates QIR for unseen dialects under a
   structured prompt.
3. **Repair** — when verification fails on the deterministic path, the LLM
   agent corrects the output through a feedback loop.

A dual-backend verification pipeline executes the source MLIR and the generated
QIR on independent simulators and compares the resulting bitstring
distributions via total variation distance (TVD).

This repository accompanies the paper "Agentic MLIR-to-QIR Translation with
Dual-Backend Testing: A Hybrid Deterministic and LLM Approach".

---

## Repository layout

```
.
├── translate.py          # CLI entry point (MLIR/QASM file → QIR)
├── agentic_mlir_qir/     # Source package (parsers, generators, agents, verification)
├── example/              # Benchmark circuits
│   ├── catalyst_mlir/    #   Catalyst-dialect MLIR
│   ├── quake_mlir/       #   Quake-dialect MLIR
│   ├── ftqc_mlir/        #   FTQC-dialect MLIR (unseen dialect)
│   ├── qasm/             #   OpenQASM 2.0 / 3.0
│   ├── qiskit_algorithms/#   Qiskit-generated Shor and Grover pipelines
│   └── qir/              #   Reference QIR ground truth
├── experiments/          # Experiment scripts (E1–E4) and analysis
├── scripts/              # setup.sh bootstrap, ground-truth generator
├── tests/                # Test suite
└── requirements.txt
```

---

## Installation

```bash
bash scripts/setup.sh
source venv/bin/activate
```

The script creates a virtual environment, installs dependencies, installs
CUDA-Q where supported, and writes a `.env` file. To do it manually:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install qirrunner==0.9.1     # QIR execution backend
pip install cudaq==0.13.0        # optional, Linux only — enables OpenQASM input
```

Platform support:

| Capability                          | Requires             | Linux | macOS / Windows |
| ----------------------------------- | -------------------- | :---: | :-------------: |
| Deterministic MLIR → QIR            | `requirements.txt`   |  ✅   |       ✅        |
| OpenQASM → QIR + Quake verification | `cudaq`              |  ✅   |       ❌        |
| Agentic path (unseen dialects)      | `HF_TOKEN` or Ollama |  ✅   |       ✅        |

---

## Usage

```bash
# Deterministic translation (Catalyst dialect)
python translate.py example/catalyst_mlir/code_bell.mlir

# Unseen FTQC dialect — routes to the agentic path automatically
python translate.py example/ftqc_mlir/steane_2q_bell.mlir

# OpenQASM 2.0 / 3.0 input (auto-detected)
python translate.py example/qasm/bell_state_v2.qasm

# Read from stdin
cat example/qasm/ghz_state_v2.qasm | python translate.py -

# Write QIR to a file; metadata then goes to stdout
python translate.py example/catalyst_mlir/code_bell.mlir -o bell.ll

# JSON output for CI and scripting
python translate.py example/catalyst_mlir/code_bell.mlir --json

# Skip simulation verification (faster)
python translate.py example/catalyst_mlir/code_bell.mlir --no-verify
```

Example output:

```text
── Translation Metadata ────────────────────────────
  Dialect          : quake
  Translation path : deterministic

── Simulation Verification ─────────────────────────
  Gate match       : PASS
  TVD similarity   : 96.2%  PASS
  QIR distribution : 00:525  11:475
  MLIR distribution: 00:487  11:513

✓ SUCCESS — translation verified
```

From Python:

```python
import agentic_mlir_qir as amq

mlir = open("example/catalyst_mlir/code_bell.mlir").read()
res = amq.translate(mlir, verify=True)
print(res.dialect, res.translation_path, res.success)
print(res.qir)

qasm = open("example/qasm/bell_state_v2.qasm").read()
res = amq.translate_qasm(qasm, verify=True, shots=2000)
print(res.source_format, res.verification.similarity)
```

### OpenQASM support

OpenQASM 2.0 and 3.0 circuits are parsed by Qiskit and lowered to Quake-dialect
MLIR by CUDA-Q, then flow through the same deterministic pipeline. Supported
gates: `h x y z s t sdg tdg rx ry rz p/u1 u3 cx cy cz ch swap crx cry crz cp
ccx cswap`. Anything else raises a clear error.

### Streamlit demo

```bash
streamlit run agentic_mlir_qir/ui/app.py
```

---

## LLM configuration

The agentic path needs either a HuggingFace token or a local Ollama instance.
Both are optional — the deterministic path requires no LLM.

```bash
cp .env.example .env
# Set HF_TOKEN=hf_... from https://huggingface.co/settings/tokens
```

Registered cloud models:

| Model key        | HF model                           | Notes                                             |
| ---------------- | ---------------------------------- | ------------------------------------------------- |
| `gemma4-31b-hf`  | `google/gemma-4-31B-it`            | Default. Open-weight, ungated                     |
| `gpt-oss-20b`    | `openai/gpt-oss-20b`               | Open-weight, free tier                            |
| `llama3.1-8b-hf` | `meta-llama/Llama-3.1-8B-Instruct` | Gated — requires access approval from Meta        |

Local models via Ollama (`llama3.1-8b`, `codellama-13b`, and others) need a
local GPU. Run `python translate.py --list-models` for the full list.

When the agentic path runs without an explicit `--model`, the first model with
credentials available is used, in the order `gemma4-31b-hf` → `gpt-oss-20b` →
`llama3.1-8b`. Known dialects still take the deterministic path and never
contact an LLM; pass `--force-agentic` to override that.

---

## Software versions

| Package            | Version |
| ------------------ | ------- |
| Python             | 3.12    |
| PennyLane          | 0.44.0  |
| PennyLane-Catalyst | 0.14.0  |
| CUDA-Q             | 0.13    |
| qir-runner         | 0.9.1   |
| CrewAI             | 1.10.0  |
| Ollama             | 0.6     |

Pinned versions are recorded in `requirements.txt`. `qir-runner` and CrewAI are
under active development; later releases may require minor adaptation.

---

## Citation

```bibtex
@inproceedings{afrose2026agentic,
  author    = {Sharmin Afrose and Vicente Leyton-Ortega and Narasinga Rao Miniskar and Elaine Wong and Travis S. Humble},
  title     = {Agentic MLIR-to-QIR Translation with Dual-Backend Testing: A Hybrid Deterministic and LLM Approach},
  year      = {2026}
}
```

---

## License

Apache License, Version 2.0. See `pyproject.toml` for the package-level
license declaration.

---

## Acknowledgments

This work was supported by the U.S. Department of Energy, Office of Science
under Contract No. DE-AC05-00OR22725, with funding from the Office of
Advanced Scientific Computing Research's Accelerated Research in Quantum
Computing Program's Modular and Error-Aware Software Stack for Heterogeneous
Quantum Computing Ecosystems (MACH-Q) project.

The authors thank the broader quantum-compiler community for the open-source
tools this work builds on, including PennyLane Catalyst, NVIDIA CUDA-Q, the
QIR Alliance and `qir-runner`, and the CrewAI multi-agent framework.

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
([https://www.energy.gov/doe-public-access-plan](https://www.energy.gov/doe-public-access-plan)).

### Authors

Sharmin Afrose, Vicente Leyton-Ortega, Narasinga Rao Miniskar, Elaine Wong,
and Travis S. Humble — Oak Ridge National Laboratory, Oak Ridge, TN, USA
(<{afroses, leytonortheva, miniskarnr, wongey, humblets}@ornl.gov>).
