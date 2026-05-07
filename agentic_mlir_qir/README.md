# Source layout

This document describes the code organization of the agentic MLIR-to-QIR
translator. The layout maps directly onto the four-component system
described in Section III of the paper: *parsing*, *translation*,
*verification*, and *guardrail / output recovery*.

```
src/
├── parsers/        # MLIR → MLIRCircuit (deterministic parser)
├── dialects/       # Dialect-specific gate metadata + dialect detection
├── generators/     # MLIRCircuit → QIR (deterministic generator + guardrail assembler)
├── agents/         # CrewAI orchestration: translation + verification agents
├── tools/          # Inline QIR reference, web fetch, simulator discovery
├── verification/   # Dual-backend verification pipeline + simulator registry
├── ui/             # Streamlit demo (optional)
├── utils/          # Run logger
├── config/         # Hydra-style settings, LLM model config
└── rag/            # Optional RAG knowledge base (only used by HITL UI button)
```

---

## Module reference

### `parsers/`

* **`mlir_parser.py`** — single-pass, SSA-aware MLIR parser. Detects the
  dialect, traverses the program, and produces an `MLIRCircuit` data
  structure containing an ordered operation list, qubit allocation
  metadata, parameter constants, and conditional block boundaries.

### `dialects/`

* **`base_dialect.py`** — abstract dialect descriptor; raises
  `UnsupportedDialectError` for unrecognised dialects.
* **`catalyst_dialect.py`** — Catalyst gate names and signatures.
* **`quake_dialect.py`** — Quake gate names, including controlled-gate
  shorthand (`quake.x [ctrl] target` etc.).
* **`dialect_detector.py`** — pattern-based dialect classifier driven by
  marker tokens (`quantum.custom`, `quake.alloca`, `!ftqc.logical_qubit`,
  …).

### `generators/`

* **`qir_generator.py`** — emits complete LLVM IR from a parsed
  `MLIRCircuit`. Used by the deterministic translation path.
* **`qir_assembler.py`** — guardrail-side assembler: takes a list of
  parsed gate operations (extracted from possibly-broken LLM output) and
  produces a syntactically valid QIR module by re-instantiating the same
  templates as `qir_generator.py`.
* **`templates.py`** — string templates for QIR header, declarations,
  attributes, and metadata.

### `agents/`

* **`crew_manager.py`** — top-level orchestrator. Runs the deterministic
  path first when the dialect is known, then enters an iterative
  verification + repair loop on failure, up to `max_iterations`.
* **`translation_agent.py`** — CrewAI agent that produces QIR from MLIR.
  Wraps the LLM with the inline QIR reference and applies
  `_apply_output_guardrail()` to every response.
* **`verification_agent.py`** — CrewAI agent that issues structured
  feedback when verification fails (used by the repair path).

### `tools/`

* **`qir_reference.py`** — the inline gate-mapping table, complete QIR
  template, and translation patterns that are injected into the agent
  prompt (the *context engineering* component of the paper).
* **`web_fetch_tool.py`** — optional web fetcher for unseen-dialect
  documentation.
* **`simulator_discovery_tool.py`** — optional helper that searches for
  simulators matching an unrecognised dialect.
* **`gate_counter_tool.py`**, **`qir_search_tool.py`**, **`rag_tool.py`**
  — supplementary tools available to the agent (the RAG tool is unused by
  default; context engineering replaces it).

### `verification/`

* **`pipeline.py`** — `run_verification_pipeline(mlir, qir, shots)` is the
  single entry point used by `translate.py` and the Streamlit UI. It
  orchestrates the four stages: gate-count comparison, QIR execution,
  MLIR execution, and TVD distribution comparison.
* **`gate_counter.py`** — counts gates in MLIR and QIR (per dialect),
  including a generic keyword extractor for unseen dialects.
* **`metrics.py`** — TVD computation and the 95 % similarity threshold.
* **`simulator_registry.py`** — registry pattern that lets each dialect
  pick its own MLIR-side simulator backend.
* **`qir_runner.py` / `_qir_subprocess_runner.py`** — runs generated QIR
  through the `qir-runner` Python package in an isolated subprocess
  (avoids LLVM library conflicts with PennyLane Catalyst).
* **`catalyst_runner.py`** — MLIR-side simulator for the Catalyst dialect
  (PennyLane + `@catalyst.qjit`).
* **`quake_runner.py` / `_quake_subprocess_runner.py`** — MLIR-side
  simulator for the Quake dialect (CUDA-Q `cudaq.sample()`).

### `ui/`

* **`app.py`** — Streamlit web demo: paste MLIR, view the generated QIR
  and verification results side by side. Optional; not required for
  experiments.

### `config/`

* **`settings.py`** — runtime configuration (paths, defaults, log levels).
* **`llm_config.py`** — model registry. Maps short model keys
  (`llama3.1-8b`, `gpt-oss-20b`, …) to provider info (Ollama vs.
  HuggingFace), VRAM estimates, and LiteLLM model strings.

### `utils/`

* **`run_logger.py`** — appends per-translation records to
  `logs/translations.jsonl` and writes a per-circuit Markdown report to
  `example_run_info/`.

### `rag/` (optional)

The RAG knowledge base is used only by the Streamlit UI's
"Fetch documentation & retry" button (a human-in-the-loop helper). The
paper experiments do **not** depend on RAG — context engineering replaces
it for the agentic path. The RAG modules are kept for users who want to
extend the system.

---

## Data flow at runtime

```
                        ┌────────────────────┐
   MLIR source  ───────►│  dialect_detector  │
                        └──────────┬─────────┘
                                   │
                  ┌────────────────┴────────────────┐
                  ▼                                 ▼
         known dialect                       unseen dialect
                  │                                 │
                  ▼                                 ▼
         parsers + generators                    agents (CrewAI)
         (deterministic QIR)                  + tools.qir_reference
                  │                                 │
                  └────────────────┬────────────────┘
                                   ▼
                       verification.pipeline
                       (gate count + QIR run + MLIR run + TVD)
                                   │
                  ┌────────────────┴────────────────┐
                  ▼                                 ▼
                pass                              fail
                  │                                 │
                  ▼                                 ▼
            return QIR                  agents.crew_manager → repair
```

The repair branch feeds the verification report back into the translation
agent for up to `max_iterations` rounds (default 5), and the system
returns the highest-scoring attempt seen across iterations.

---

## Extending the system

* **Add a new dialect.** Drop a `<dialect>_dialect.py` into `dialects/`,
  register dialect tokens in `dialect_detector.py`, and (if you want a
  deterministic parser) extend `parsers/mlir_parser.py`. The system will
  automatically fall back to the agentic path until the deterministic
  parser is in place.
* **Add a new MLIR-side simulator.** Implement a runner in `verification/`
  and register it in `simulator_registry.py`. The verification pipeline
  will pick it up by dialect.
* **Add a new LLM backend.** Extend `LLMConfig.MODELS` in
  `config/llm_config.py`. Any LiteLLM-supported provider works.
