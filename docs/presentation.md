---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #e0e0e0
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #00d4ff;
  }
  h2 {
    color: #7b68ee;
  }
  h3 {
    color: #50fa7b;
  }
  code {
    background-color: #2d2d4e;
    color: #50fa7b;
  }
  pre {
    background-color: #16213e !important;
    border-left: 4px solid #00d4ff;
  }
  a {
    color: #00d4ff;
  }
  table {
    color: #e0e0e0;
  }
  th {
    background-color: #2d2d4e;
    color: #00d4ff;
  }
  td {
    background-color: #1a1a2e;
  }
  blockquote {
    border-left: 4px solid #7b68ee;
    color: #b0b0d0;
  }
  strong {
    color: #ff79c6;
  }
  em {
    color: #f1fa8c;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# LLM-Powered Multi-Agent MLIR to QIR Translator

### Bridging Quantum Compiler Representations with AI

<br>

**7-Phase Architecture** | **SSA-Aware Parsing** | **RAG-Enhanced Translation**

---

## The Problem

Quantum computing frameworks use **different intermediate representations**:

| Framework | IR | Description |
|-----------|-----|-------------|
| PennyLane Catalyst | **Catalyst MLIR** | High-level quantum dialect |
| CUDA Quantum | **Quake MLIR** | NVIDIA's quantum dialect |
| QIR Alliance | **QIR (LLVM IR)** | Universal quantum target |

<br>

> Translating between these IRs is **non-trivial**: SSA variable chains, multi-result operations, conditional branching, and parametric gates all require careful semantic analysis.

---

## Solution Overview

An **agentic, LLM-powered** translation system with 7 phases:

```
 MLIR Input ──> [Dialect Detection] ──> [SSA-Aware Parsing]
                                              |
                                              v
                   [RAG Knowledge Base] ──> [Multi-Agent Translation]
                                              |
                                              v
                   [Verification Engine] ──> [Iterative Refinement]
                                              |
                                              v
                                        QIR Output (.ll)
```

**33 modules** | **3,700+ lines** | **2 dialect adapters** | **4-level verification**

---

## System Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Streamlit Web UI                     │
├──────────────────────────────────────────────────────┤
│              CrewAI Agent Orchestration               │
│         TranslationAgent ── VerificationAgent        │
├──────────────┬──────────────┬────────────────────────┤
│ Dialect      │ Code         │ Verification           │
│ System       │ Generation   │ Engine                 │
│ ├ Detector   │ ├ Parser     │ ├ GateCounter          │
│ ├ Catalyst   │ ├ Generator  │ ├ Metrics (TVD, KL)    │
│ └ Quake      │ └ Templates  │ └ SimulatorRegistry    │
├──────────────┴──────────────┴────────────────────────┤
│         RAG: ChromaDB + SentenceTransformers         │
├──────────────────────────────────────────────────────┤
│  Ollama (LLMs)  │  HuggingFace  │  Knowledge Base   │
└──────────────────────────────────────────────────────┘
```

---

## Phase 1: Configuration & Infrastructure

### `src/config/settings.py` + `src/config/llm_config.py`

- **Pydantic-based** settings with `.env` loading
- Supports 3 LLM model tiers via Ollama:

| Model | Size | VRAM | Quality | Speed |
|-------|------|------|---------|-------|
| llama3.1:8b | 4.7 GB | 6 GB | Good | Fast |
| codellama:13b | 7.4 GB | 10 GB | Better | Medium |
| llama3.1:70b-q4 | 40 GB | 48 GB | Best | Slow |

```python
class Settings(BaseSettings):
    LLM_MODEL: str = "llama3.1:8b"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    MAX_ITERATIONS: int = 3
    GATE_COUNT_TOLERANCE: float = 0.0  # Exact match
```

---

## Phase 2: Dialect Detection & Parsing

### Plugin Architecture for MLIR Dialects

```python
class BaseDialect(ABC):
    """Abstract base — each dialect implements its own parser."""
    def can_parse(self, mlir_code: str) -> bool: ...
    def parse_circuit(self, mlir_code: str) -> MLIRCircuit: ...
    def get_gate_mapping(self) -> Dict[str, str]: ...
```

**Auto-detection** via keyword markers:

| Dialect | Markers |
|---------|---------|
| **Catalyst** | `quantum.custom`, `quantum.alloc`, `!quantum.bit` |
| **Quake** | `quake.alloca`, `quake.h`, `quake.x` |

> Extensible: add a new dialect by subclassing `BaseDialect`

---

## Phase 2: SSA-Aware Parsing (The Core Innovation)

### The Challenge

MLIR uses **Static Single Assignment** form. A CNOT gate produces 2 output wires:

```mlir
%out:2 = quantum.custom "CNOT"() %3, %4 : !quantum.bit, !quantum.bit
```

`%out#0` = control qubit, `%out#1` = target qubit — these must be **traced back** to physical qubit indices through the entire SSA chain.

### The Solution: Single-Pass SSA Tracking

```python
ssa_qubit: Dict[str, int] = {}      # %var -> physical qubit index
ssa_constants: Dict[str, float] = {} # %var -> constant value (angles)
ssa_meas_source: Dict[str, int] = {} # %var -> measurement result index
```

Every `quantum.extract`, `quantum.custom`, and `quantum.measure` updates these maps.

---

## Phase 2: SSA Variable Flow Example

### Bell State MLIR

```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0]          ──> ssa_qubit["1"] = 0
%out = quantum.custom "Hadamard"() %1 ──> ssa_qubit["out"] = 0
%2 = quantum.extract %0[ 1]          ──> ssa_qubit["2"] = 1
%out_0:2 = quantum.custom "CNOT"() %out, %2
    ──> ssa_qubit["out_0#0"] = 0  (control)
    ──> ssa_qubit["out_0#1"] = 1  (target)
%mres, %out_qubit = quantum.measure %out_0#0
    ──> resolves to physical qubit 0
```

**Result**: H(q0), CNOT(q0, q1), Measure(q0), Measure(q1)

---

## Phase 2: Parametric Gate Resolution

### Gate parameters are SSA constants, not literals

```mlir
%cst = arith.constant 2.590000e+00 : f64     ──> ssa_constants["cst"] = 2.59
%out = quantum.custom "RX"(%cst) %qubit      ──> params = [2.59]
```

The parser resolves `%cst` through the constants dictionary:

```python
def _parse_parameters(self, params_str, ssa_constants=None):
    # Resolve SSA variable references (e.g., %cst)
    if ssa_constants:
        for m in re.finditer(r'%(\w+)', params_str):
            if m.group(1) in ssa_constants:
                params.append(ssa_constants[m.group(1)])
    # Fallback: literal floats
    ...
```

**Output**: `call void @__quantum__qis__rx__body(double 2.590000e+00, %Qubit* null)`

---

## Phase 2: Conditional Branching

### Teleportation circuit uses measurement-dependent corrections

```mlir
%mres, %out_qubit = quantum.measure %qubit_1    ──> meas idx 0
%mres_2, %out_qubit_3 = quantum.measure %qubit_0 ──> meas idx 1
... (tensor.from_elements → stablehlo.compare → scf.if) ...
scf.if %condition {
    quantum.custom "PauliZ"() %target            ──> conditional gate
}
```

The parser traces measurement results through **5 IR operations** to link `scf.if` conditions back to specific measurement indices.

---

## Phase 2: Data Model

```python
@dataclass
class MLIRCircuit:
    dialect_name: str
    num_qubits: int
    gates: List[GateOperation]         # All gates (flat list)
    measurements: List[MeasurementOperation]
    qubit_allocation: QubitAllocation
    has_conditionals: bool
    conditionals: List[ConditionalBlock]
    ordered_ops: List[tuple]           # Interleaved: gate | measurement | conditional

@dataclass
class GateOperation:
    name: str           # "Hadamard", "CNOT", "RX"
    qubits: List[int]   # Physical qubit indices
    params: List[float]  # Rotation angles

@dataclass
class ConditionalBlock:
    condition_measurement_idx: int     # Which measurement controls this
    then_gates: List[GateOperation]    # Gates if measurement = 1
    else_gates: List[GateOperation]    # Gates if measurement = 0
```

---

## Phase 3: QIR Code Generation

### Template-Based Generation with Ordered Operations

```python
def _generate_entry_function(self, circuit, function_name):
    for op_type, op_data in circuit.ordered_ops:
        if op_type == "gate":
            body_lines.append(self._generate_gate_call(op_data))
        elif op_type == "measurement":
            body_lines.append(self._generate_measurement(...))
        elif op_type == "conditional":
            body_lines.extend(self._generate_conditional(op_data))
```

**Key**: Operations are emitted in **source order**, not grouped by type. This preserves the semantic meaning of interleaved gates, measurements, and conditionals.

---

## Phase 3: Gate Mapping (17 gates supported)

<div class="columns">

| Catalyst Gate | QIR Function |
|--------------|--------------|
| Hadamard | `__quantum__qis__h__body` |
| PauliX | `__quantum__qis__x__body` |
| PauliY | `__quantum__qis__y__body` |
| PauliZ | `__quantum__qis__z__body` |
| S / T | `__quantum__qis__s/t__body` |
| RX / RY / RZ | `__quantum__qis__rx/ry/rz__body` |

| Catalyst Gate | QIR Function |
|--------------|--------------|
| CNOT | `__quantum__qis__cnot__body` |
| CZ | `__quantum__qis__cz__body` |
| SWAP | `__quantum__qis__swap__body` |
| CY | `__quantum__qis__cy__body` |
| Toffoli | `__quantum__qis__ccx__body` |
| CSWAP | `__quantum__qis__cswap__body` |

</div>

---

## Phase 3: QIR Output Structure

```llvm
; ModuleID = 'circuit'          ; ─── Header
%Qubit = type opaque
%Result = type opaque

define void @main() #0 {        ; ─── Entry function
entry:
  call void @__quantum__rt__initialize(i8* null)
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null,
       %Qubit* inttoptr (i64 1 to %Qubit*))
  call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
  call void @__quantum__rt__array_record_output(i64 2, i8* null)
  ret void
}
declare void @__quantum__qis__h__body(%Qubit*)     ; ─── Declarations
declare void @__quantum__qis__cnot__body(%Qubit*, %Qubit*)

attributes #0 = { "entry_point" "required_num_qubits"="2" }
!0 = !{i32 1, !"qir_major_version", i32 1}        ; ─── Metadata
```

---

## Phase 3: Conditional QIR Generation

### Teleportation Z/X corrections

```llvm
  ; Read measurement result 1
  %cond0 = call i1 @__quantum__qis__read_result__body(
       %Result* inttoptr (i64 1 to %Result*))
  br i1 %cond0, label %then, label %else

then:
  call void @__quantum__qis__z__body(
       %Qubit* inttoptr (i64 2 to %Qubit*))       ; Z correction
  br label %continue

else:
  br label %continue

continue:
  ; Read measurement result 0
  %cond1 = call i1 @__quantum__qis__read_result__body(%Result* null)
  br i1 %cond1, label %then1, label %else1

then1:
  call void @__quantum__qis__x__body(
       %Qubit* inttoptr (i64 2 to %Qubit*))       ; X correction
  br label %continue1
```

---

## Phase 4: RAG Knowledge Base

### ChromaDB + SentenceTransformers for Context-Aware Translation

```
Knowledge Sources
├── QIR Alliance Specifications (GitHub)
├── MLIR Dialect Documentation
├── Gate Mapping Tables
├── Translation Pattern Examples
└── Research Papers (arXiv: 2101.11365, 2303.14500)
```

**Pipeline**: Fetch docs → Chunk (markdown-aware) → Embed → Store in ChromaDB

```python
class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/chromadb")
        self.embedding = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

    def query(self, query: str, n_results: int = 5):
        return self.collection.query(query_texts=[query], ...)
```

---

## Phase 5: Multi-Agent System (CrewAI)

### Two Specialized AI Agents with Iterative Refinement

```
┌────────────────────────────────────────────────────┐
│                 CrewManager                         │
│                                                    │
│  Iteration 1:                                      │
│  ┌──────────────────┐    ┌─────────────────────┐  │
│  │ TranslationAgent │───>│ VerificationAgent   │  │
│  │ + RAG Context    │    │ + Gate Counting     │  │
│  │ + LLM (Ollama)   │    │ + Metric Analysis   │  │
│  └──────────────────┘    └──────┬──────────────┘  │
│                                 │                  │
│         Pass? ──────── Yes ──> OUTPUT              │
│                  No ──> Feedback ──> Iteration 2   │
│                                                    │
│  Max iterations: 3                                 │
└────────────────────────────────────────────────────┘
```

---

## Phase 6: Verification Engine

### 4-Level Verification Pipeline

| Level | Method | What it Checks |
|-------|--------|----------------|
| **1** | Gate Counting | Exact match of gate types & counts |
| **2** | QIR Execution | Run QIR via qir-runner / Qiskit |
| **3** | MLIR Execution | Run original via Catalyst / CUDA-Q |
| **4** | Statistical | TVD & KL divergence (95% threshold) |

```python
class GateCounter:
    def compare(self, mlir_counts, qir_counts):
        return {
            "match": mlir_counts == qir_counts,
            "missing_gates": [...],   # In MLIR but not QIR
            "extra_gates": [...],     # In QIR but not MLIR
        }
```

> Simulator backends are **pluggable** via `SimulatorRegistry`

---

## Phase 7: Streamlit Web Interface

### Interactive Translation with Side-by-Side View

```
┌─────────────────────────┬─────────────────────────┐
│      MLIR Input         │      QIR Output          │
│                         │                          │
│  module @run {          │  ; ModuleID = 'circuit'  │
│    %0 = quantum.alloc(2)│  %Qubit = type opaque    │
│    %1 = quantum.extract │                          │
│    %out = quantum.custom│  define void @main() {   │
│      "Hadamard"() %1    │    call void @...h__body │
│    ...                  │    call void @...cnot    │
│                         │    ...                   │
├─────────────────────────┼─────────────────────────┤
│  [Translate to QIR]     │  [Download .ll]          │
└─────────────────────────┴─────────────────────────┘
```

- **50/50 split** layout with monospace fonts
- Load built-in examples or paste custom MLIR
- Model selection (8B / 13B / 70B)

---

## Translation Example: Bell State

<div class="columns">

### MLIR Input
```mlir
%0 = quantum.alloc( 2)
%1 = quantum.extract %0[ 0]
%out = quantum.custom
  "Hadamard"() %1
%2 = quantum.extract %0[ 1]
%out_0:2 = quantum.custom
  "CNOT"() %out, %2
%mres, %q = quantum.measure
  %out_0#0
%mres_1, %q2 = quantum.measure
  %out_0#1
```

### QIR Output
```llvm
call void
  @__quantum__qis__h__body(
    %Qubit* null)
call void
  @__quantum__qis__cnot__body(
    %Qubit* null,
    %Qubit* inttoptr
      (i64 1 to %Qubit*))
call void
  @__quantum__qis__mz__body(
    %Qubit* null,
    %Result* null)
call void
  @__quantum__qis__mz__body(
    %Qubit* inttoptr
      (i64 1 to %Qubit*),
    %Result* inttoptr
      (i64 1 to %Result*))
```

</div>

---

## Translation Example: 5-Qubit GHZ State

### MLIR: H on qubit 0, then CNOT(0, k) for k = 1..4

```llvm
; Generated QIR — all CNOTs correctly use qubit 0 as control:
call void @__quantum__qis__h__body(%Qubit* null)
call void @__quantum__qis__cnot__body(%Qubit* null,
     %Qubit* inttoptr (i64 1 to %Qubit*))
call void @__quantum__qis__cnot__body(%Qubit* null,
     %Qubit* inttoptr (i64 2 to %Qubit*))
call void @__quantum__qis__cnot__body(%Qubit* null,
     %Qubit* inttoptr (i64 3 to %Qubit*))
call void @__quantum__qis__cnot__body(%Qubit* null,
     %Qubit* inttoptr (i64 4 to %Qubit*))
```

> SSA tracking ensures qubit 0 is correctly identified as the control through all 4 CNOT operations, even as variable names change at each step.

---

## Translation Example: Parametric Circuit

### RX gate with angle parameter resolved from SSA constant

**MLIR**:
```mlir
%cst = arith.constant 2.590000e+00 : f64
%out = quantum.custom "RX"(%cst) %qubit : !quantum.bit
```

**QIR**:
```llvm
call void @__quantum__qis__rx__body(double 2.590000e+00, %Qubit* null)
```

**Declaration**:
```llvm
declare void @__quantum__qis__rx__body(double, %Qubit*)
```

> The `%cst` SSA variable is resolved to `2.59` via the `ssa_constants` tracking map, then formatted in LLVM scientific notation.

---

## Translation Example: Quantum Teleportation

### The most complex case — measurements + conditional corrections

```
Circuit: 3 qubits
  q1 ──H──●──────────── M ──────── (classical bit 1)
  q0 ─────X── CNOT ──── H ── M ── (classical bit 0)
  q2 ─────────  X  ──── [Z if bit1] ── [X if bit0] ── M
```

**Key challenge**: The `scf.if` conditional blocks depend on measurement results, requiring the parser to trace values through 5 intermediate IR operations:

```
quantum.measure → tensor.from_elements → stablehlo.convert
    → stablehlo.compare → tensor.extract → scf.if
```

---

## Project Structure

```
agentic_mlir_qir_updated/
├── src/
│   ├── config/          # Settings, LLM model configs
│   ├── dialects/        # Base + Catalyst + Quake adapters
│   ├── parsers/         # MLIR parser (delegates to dialect)
│   ├── generators/      # QIR code gen + templates
│   ├── agents/          # CrewAI translation & verification agents
│   ├── tools/           # RAG retrieval + gate counting tools
│   ├── rag/             # ChromaDB, embeddings, document chunking
│   ├── verification/    # Gate counter, metrics, simulator registry
│   └── ui/              # Streamlit web application
├── scripts/             # DB init, knowledge fetch, LLM setup
├── knowledge_base/      # QIR specs, MLIR docs, research papers
├── example/             # MLIR inputs + ground truth QIR outputs
├── data/chromadb/       # Persistent vector database
└── docs/diagrams/       # PlantUML architecture diagrams
```

**33 Python modules** across 9 packages

---

## Key Design Decisions

### Why SSA-Aware Parsing?

Naive approaches (regex on variable names) **fail** for multi-qubit gates:
```
# WRONG: extracting "1" from "out_qubits_1" as qubit index
# RIGHT: tracing %out_qubits_1 ← CNOT output#1 ← %2 ← extract[1]
```

### Why Ordered Operations?

Gates and measurements must be **interleaved**, not grouped:
```
H → CNOT → Measure → H → Measure → Conditional(Z) → Conditional(X) → Measure
```

### Why Plugin Architecture?

New quantum frameworks (Cirq, Qiskit MLIR, etc.) can be added by implementing a single `BaseDialect` subclass — no changes to the core engine.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.12 |
| **LLM Backend** | Ollama (local, GPU-accelerated) |
| **LLM Models** | Llama 3.1 (8B/70B), CodeLlama (13B) |
| **Agent Framework** | CrewAI |
| **Vector Database** | ChromaDB (persistent) |
| **Embeddings** | SentenceTransformers (all-MiniLM-L6-v2) |
| **Web UI** | Streamlit |
| **Configuration** | Pydantic + python-dotenv |
| **Target IR** | QIR 1.0 (LLVM IR-based) |
| **Source IRs** | PennyLane Catalyst MLIR, CUDA Quantum Quake |

---

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Ollama & download models
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```

### 3. Initialize knowledge base
```bash
python scripts/fetch_knowledge.py
python scripts/initialize_db.py
```

### 4. Launch the UI
```bash
streamlit run src/ui/app.py
```

---

## Testing & Validation

### Verified circuits with ground truth comparison:

| Circuit | Qubits | Gates | Conditionals | Status |
|---------|--------|-------|--------------|--------|
| Bell State | 2 | H, CNOT | No | Pass |
| GHZ-5 | 5 | H, 4x CNOT | No | Pass |
| Teleportation | 3 | 2H, 2CNOT, Z, X | Yes (2) | Pass |
| Random-658 | 2 | CNOT, SWAP, H, S, RX, Y, CNOT | No | Pass |

### Validation checks:
- Gate types and counts match ground truth
- Qubit indices correctly resolved through SSA chains
- Parameter values (rotation angles) preserved
- Conditional branching semantics correct
- Operation ordering matches source MLIR

---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# Thank You

### LLM-Powered Multi-Agent MLIR to QIR Translator

<br>

**SSA-Aware Parsing** | **Conditional Branching** | **RAG-Enhanced**
**Plugin Architecture** | **4-Level Verification** | **Iterative Refinement**

<br>

Built with Python, CrewAI, ChromaDB, Ollama, and Streamlit
