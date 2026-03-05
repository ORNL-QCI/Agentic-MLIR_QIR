---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #e0e0e0
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px 50px;
  }
  h1 { color: #00d4ff; font-size: 2em; }
  h2 { color: #7b68ee; font-size: 1.5em; }
  h3 { color: #50fa7b; font-size: 1.15em; }
  code {
    background-color: #2d2d4e;
    color: #50fa7b;
    padding: 1px 5px;
    border-radius: 3px;
  }
  pre {
    background-color: #16213e !important;
    border-left: 4px solid #00d4ff;
    font-size: 0.72em;
  }
  a { color: #00d4ff; }
  table { color: #e0e0e0; width: 100%; }
  th { background-color: #2d2d4e; color: #00d4ff; }
  td { background-color: #1a1a2e; }
  blockquote {
    border-left: 4px solid #7b68ee;
    color: #b0b0d0;
    padding-left: 12px;
  }
  strong { color: #ff79c6; }
  em { color: #f1fa8c; }
  .lead h1 { font-size: 2.4em; }
  ul li { margin-bottom: 6px; }
  .box {
    background: #16213e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
  }
---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# MLIR → QIR Quantum Circuit Translator

### An AI-powered tool that converts quantum programs between compiler formats

<br>

**2 Dialects** · **4-Level Verification** · **Real Quantum Simulation** · **Web UI** · **CLI** · **Free Cloud LLM**

---

## What does this tool do?

A quantum program written in one framework (e.g. PennyLane or CUDA Quantum) cannot directly run on hardware or simulators that expect a different format.

**This tool translates automatically:**

```
PennyLane Catalyst MLIR  ──┐
                            ├──► QIR (.ll)  ──► Any QIR-compatible simulator/hardware
CUDA Quantum Quake MLIR  ──┘
```

> Think of it like a **universal adapter** — the quantum program stays the same, only the format changes.

---

## Background: What is a Quantum Circuit?

A quantum circuit is a *program for a quantum computer*, made of:

| Component | What it is | Classical analogy |
|-----------|------------|-------------------|
| **Qubit** | Quantum bit — can be 0, 1, or both at once | Bit (0 or 1) |
| **Gate** | Operation that transforms a qubit | Logic gate (AND, OR…) |
| **Measurement** | Read the qubit — collapses to 0 or 1 | Read a register |

**Example — Bell State** (2 qubits in a perfectly correlated pair):

```
q0: ──H──●──M
         │
q1: ─────X──M
```

- `H` = Hadamard (puts q0 into superposition)
- `●──X` = CNOT (entangles q0 and q1)
- Result: always measure `00` or `11`, never `01` or `10`

---

## Background: What is MLIR?

**MLIR** = *Multi-Level Intermediate Representation*

It is the internal language that quantum compilers use to describe circuits **before** they are lowered to hardware instructions. Think of it as the compiler's "source code" that humans can read.

**Example — Bell State in Catalyst MLIR:**
```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0]
%out = quantum.custom "Hadamard"() %1 : !quantum.bit
%2 = quantum.extract %0[ 1]
%out_0:2 = quantum.custom "CNOT"() %out, %2 : !quantum.bit, !quantum.bit
```

**Example — Same circuit in Quake MLIR (CUDA Quantum):**
```mlir
%0 = quake.alloca !quake.veq<2>
%1 = quake.extract_ref %0[0] : (!quake.veq<2>, i64) -> !quake.ref
quake.h %1 : (!quake.ref) -> ()
quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
```

Both describe the **same Bell state** but use different syntax.

---

## Background: What is QIR?

**QIR** = *Quantum Intermediate Representation* — a standard by the QIR Alliance (Microsoft, NVIDIA, AWS…)

It is LLVM IR (the same format used by C/C++ compilers) with quantum extensions. Hardware and simulators that support QIR can run circuits from **any** framework.

**Example — Bell State in QIR:**
```llvm
define void @main() #0 {
  call void @__quantum__rt__initialize(i8* null)
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null,
       %Qubit* inttoptr (i64 1 to %Qubit*))
  call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
  call void @__quantum__qis__mz__body(%Qubit* inttoptr (i64 1 to %Qubit*),
       %Result* inttoptr (i64 1 to %Result*))
  ret void
}
```

> QIR looks like assembly code — precise, low-level, universal.

---

## The Problem: A Format Zoo

Quantum frameworks each use their own compiler format:

| Framework | Language | IR Format |
|-----------|----------|-----------|
| **PennyLane Catalyst** | Python | Catalyst MLIR (`quantum.*`) |
| **CUDA Quantum** | Python/C++ | Quake MLIR (`quake.*`) |
| **Qiskit** | Python | OpenQASM 3 |
| **Hardware/Simulators** | — | **QIR** (LLVM-based) |

**The pain:** A circuit written in PennyLane cannot easily run on a CUDA Quantum simulator, and vice versa. You need to *translate*.

Doing this by hand is tedious and error-prone — the formats have very different structures with complex rules (SSA variables, conditional branches, parameter encoding…).

---

## The Solution: This Tool

```
┌─────────────────────────────────────────────────────────┐
│              MLIR → QIR Translator                      │
│                                                         │
│  Input              Pipeline              Output        │
│                                                         │
│  Catalyst MLIR ──► Detect dialect                       │
│                 ──► Parse (SSA-aware)   ──► QIR (.ll)   │
│  Quake MLIR    ──► Generate QIR                         │
│                 ──► Verify (4 levels)                   │
│                                                         │
│  Web UI: paste MLIR → click Translate → get QIR         │
└─────────────────────────────────────────────────────────┘
```

**Key properties:**
- **Automatic** — no manual work required
- **Accurate** — verified by running both the original and translated circuit on real simulators
- **Extensible** — easy to add new input formats

---

## The Full Pipeline (Step by Step)

```
OpenQASM3  ──► cudaq kernel ──► Quake MLIR ──┐
                                               │
Catalyst MLIR ─────────────────────────────────┤
                                               │
                         ┌─────────────────────▼──────────────────┐
                         │  Step 1: Dialect Detection              │
                         │  Step 2: SSA-Aware Parser               │
                         │            ↓ MLIRCircuit                │
                         │  Step 3: QIR Generator                  │
                         │            ↓ QIR code (.ll)             │
                         │  Step 4: AI Agents (RAG + LLM)         │
                         │  Step 5: Verification (gate + TVD)     │
                         └─────────────────────────────────────────┘
                                               │
                                          QIR Output
```

---

## Step 1: Dialect Detection

The tool *automatically* recognises which format the input is:

| What it looks for | Dialect detected |
|-------------------|-----------------|
| `quantum.custom`, `quantum.alloc`, `!quantum.bit` | **Catalyst** (PennyLane) |
| `quake.alloca`, `quake.h`, `!quake.veq` | **Quake** (CUDA Quantum) |

```python
class DialectDetector:
    def detect(self, mlir_code: str):
        for dialect in self.dialects:
            if dialect.can_parse(mlir_code):
                return dialect
```

> No configuration needed — just paste your MLIR and the tool figures it out.

---

## Step 2: Why Parsing is Hard — SSA Variables

MLIR uses **SSA form** (Static Single Assignment). Every value is assigned exactly once and given a name like `%out`, `%1`, `%cst`. The challenge: qubit indices are *buried* inside chains of variable references.

**Example — GHZ-5 (wrong vs correct):**

```
Naive (WRONG):  extract digit from variable name
  %out_qubits_1  →  qubit 1   ❌ produces CNOT(0,1), CNOT(1,2), CNOT(1,3)

SSA-aware (CORRECT): trace the variable back through the chain
  %out_qubits_1#0  ←  CNOT output#0  ←  CNOT input#0
  ←  %out_qubits_0#0  ←  CNOT input#0  ←  extract[0]  =  qubit 0 ✓
```

**The parser maintains 3 tracking dictionaries:**

```python
ssa_qubit:     { "%out" → 0 }     # SSA var → physical qubit index
ssa_constants: { "%cst" → 2.59 }  # SSA var → rotation angle
ssa_meas:      { "%m0"  → 0 }     # SSA var → measurement result index
```

---

## Step 2: Quake Dialect Parsing (CUDA Quantum)

Quake MLIR uses a different pattern — qubit refs are extracted via index, gates use type annotations:

```mlir
%0 = quake.alloca !quake.veq<5>          ← allocate 5 qubits
%c0 = arith.constant 0 : i64            ← integer constant (qubit index)
%1 = quake.extract_ref %0[%c0]          ← qubit 0 reference
quake.h %1 : (!quake.ref) -> ()         ← Hadamard on qubit 0
quake.x [%1] %3 : (!quake.ref, ...) → () ← CNOT: [ctrl] tgt
quake.rx (%cst) %1 : (f64, !quake.ref) → () ← parametric gate
quake.mz %1 : (!quake.ref) -> !quake.measure ← measurement
```

**Key difference from Catalyst:** controlled gates are written as `gate [ctrl] tgt` (control in brackets).

The parser resolves all qubit references through the SSA chain and produces the same `MLIRCircuit` intermediate representation — so the QIR generator works unchanged.

---

## Step 3: QIR Code Generation

Once parsed, the `MLIRCircuit` is converted to QIR using a template system.

```
MLIRCircuit.ordered_ops:
  [("gate", H(q0)), ("gate", CNOT(q0,q1)), ("measurement", q0), ("measurement", q1)]
          │
          ▼
QIR entry function:
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr(i64 1 ...))
  call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
  call void @__quantum__qis__mz__body(%Qubit* inttoptr(i64 1 ...), %Result* ...)
```

**Why `ordered_ops`?** Gates and measurements must appear in the exact same order as the source MLIR. A circuit like `H → measure → if-measure-then-Z` would be wrong if measurements were grouped separately.

**17 gates supported:** H, X, Y, Z, S, T, S†, T†, RX, RY, RZ, CNOT, CZ, SWAP, CY, Toffoli, CSWAP

---

## Step 3: Conditional QIR (Teleportation)

Some circuits apply gates *based on measurement outcomes* (e.g. quantum teleportation applies Z or X corrections depending on what was measured). This becomes an `if/else` block in QIR:

```llvm
; Read measurement result
%cond0 = call i1 @__quantum__qis__read_result__body(%Result* inttoptr(i64 1 ...))
br i1 %cond0, label %then0, label %else0

then0:
  call void @__quantum__qis__z__body(%Qubit* inttoptr(i64 2 ...))  ; Z correction
  br label %continue0

else0:
  br label %continue0     ; nothing to do

continue0:
  ; ... next conditional ...
```

The parser traces measurement results through up to **5 IR operations** to link the `scf.if` block to the right measurement index.

---

## Intelligent Translation Routing

The pipeline routes each circuit based on whether the dialect is recognised:

```
MLIR Input
    │
    ▼
Dialect Detection
    │
    ├─── Known (Catalyst/Quake) ──► Deterministic Parser ──► QIR Generator ──┐
    │                                                                          │
    └─── Unknown ──► WebFetchTool (fetch dialect spec) ──► TranslationAgent ──┤
                          + RAGTool (local docs)                               │
                                                                               ▼
                                                                    Verification Pipeline
                                                                               │
                                                              ┌────────────────┴───────────────┐
                                                           PASS ✓                           FAIL ✗
                                                              │                               │
                                                          QIR Output            Structured feedback
                                                                                (gate diff + TVD)
                                                                                      │
                                                                           Repair Agent (LLM)
                                                                              ↑ up to 3 iters
```

**Translation paths recorded:**

| Path | When |
|------|------|
| `deterministic` | Known dialect, passes on first try |
| `ai_agent` | Unknown dialect — agent translates |
| `deterministic+repair` | Known dialect fails verify; agent repairs |

---

## Agentic Pipeline: `translate_with_verification()`

```python
# Phase 0 — dialect routing
try:
    dialect = MLIRParser().get_detected_dialect(mlir)
    is_known = True
except UnsupportedDialectError:
    dialect = infer_hint(mlir)   # scan for namespace prefix
    is_known = False

# Phase 1 — initial QIR
if is_known:
    qir = QIRGenerator().generate(MLIRParser().parse(mlir))
else:
    agent.attach_web_tools()    # WebFetchTool + SerperDevTool
    qir = agent.translate_with_feedback(mlir, dialect, iteration=1)

# Phase 2 — verify + repair loop
for i in range(1, max_iterations + 1):
    vr = run_verification_pipeline(mlir, qir, shots=1000)
    if vr["gate_comparison"]["matches"] and vr["similarity_passes"]:
        return SUCCESS          # ✓ PASS

    feedback = build_feedback_string(vr)   # structured repair instructions
    qir = agent.translate_with_feedback(
              mlir, dialect, feedback=feedback, previous_qir=qir, iteration=i+1)
```

**Structured feedback sent to the repair agent:**
```
GATE COUNT MISMATCH:
  Gate 'rx': MLIR has 2, QIR has 1 (diff -1)  ← Missing in QIR: rx
SIMULATION MISMATCH: TVD similarity is 72.3% (need >= 95%)
  Check gate order, parameters, and qubit indexing.
```

---

## Multi-Provider LLM Support

The tool supports **three LLM backends** — choose based on available hardware:

| Model key | Provider | VRAM | Cost | Setup |
|-----------|----------|------|------|-------|
| `llama3.1-8b` | Ollama (local) | ~8 GB | Free | `ollama pull llama3.1:8b-instruct` |
| `llama3.1-70b-q4` | Ollama (local) | ~40 GB | Free | `ollama pull llama3.1:70b-instruct-q4_K_M` |
| `codellama-13b` | Ollama (local) | ~13 GB | Free | `ollama pull codellama:13b` |
| **`gpt-oss-20b`** | **HuggingFace API** ☁️ | **None** | **Free tier** | `export HF_TOKEN=hf_...` |

### New: `gpt-oss-20b` via HuggingFace (no GPU needed)

```bash
# Get a free token at https://huggingface.co/settings/tokens
export HF_TOKEN=hf_...

# Use it in CLI
python translate.py circuit.mlir --model gpt-oss-20b

# Or select it in the Web UI sidebar
# Sidebar shows: ✅ HF_TOKEN found  or  ⚠ Set HF_TOKEN env var
```

- **Open-weight** model (Apache 2.0) by OpenAI
- Served via litellm: `huggingface/openai/gpt-oss-20b`
- CrewAI 1.10.0 upgraded from 0.28.8 (previously broken due to `langchain-core` conflict)

---

## New: CLI (`translate.py`)

A developer-facing command-line interface — no browser needed:

### Basic usage

```bash
# Translate a file (metadata → stderr, QIR → stdout — safe to pipe)
python translate.py examples/mlir/bell_state.mlir

# Read from stdin
cat circuit.mlir | python translate.py -

# Save QIR to file (metadata → stdout)
python translate.py circuit.mlir -o circuit.ll

# Skip simulation (gate counts only — much faster)
python translate.py circuit.mlir --no-verify
```

### Agentic pipeline

```bash
python translate.py circuit.mlir --model llama3.1-8b           # Ollama
python translate.py circuit.mlir --model gpt-oss-20b            # HuggingFace (free)
python translate.py circuit.mlir --model llama3.1-8b --max-iterations 5
```

### JSON output (scripting / CI)

```bash
python translate.py circuit.mlir --json | jq '.gate_comparison.matches'
python translate.py circuit.mlir --json | jq '.verification.similarity'
python translate.py circuit.mlir --json | jq -r '.qir' > circuit.ll
```

### Metadata shown (on stderr / stdout)

```
── Translation Metadata ──────────────────────────────
  Dialect          : catalyst
  Translation path : deterministic
  Translation time : 12.3 ms
  Iterations       : 1

── Gate Counts ───────────────────────────────────────
  Gate            MLIR   QIR  Status
  ──────────────────────────────────
  cnot               1     1  ✓ match
  h                  1     1  ✓ match
  Total              2     2  ✓ match

── Simulation Verification ───────────────────────────
  QIR backend      : real execution
  MLIR backend     : Catalyst (qjit) (real execution)
  Gate match       : PASS
  TVD similarity   : 98.6%  PASS

✓ SUCCESS — translation verified
```

| Exit code | Meaning |
|-----------|---------|
| `0` | Translation verified |
| `1` | Verification failed / error |
| `2` | Unknown dialect — use `--model` |
| `130` | Ctrl-C |

---

## Step 5: 4-Level Verification

After translation, the tool automatically checks the output is correct:

| Level | Method | What it checks |
|-------|--------|----------------|
| **1 — Gate Count** | Count gates by type | Same number of H, CNOT, RX, etc. |
| **2 — QIR Execution** | `qirrunner` (QIR Alliance simulator) | Run QIR, get measurement statistics |
| **3 — MLIR Execution** | PennyLane Catalyst (`@qjit`) | Run original MLIR, get statistics |
| **4 — TVD Similarity** | Total Variation Distance | Results must agree ≥ 95% |

**Pass condition:** Gate counts match **AND** TVD ≥ 95%

> Real Bell state result: QIR gives `{00: 514, 11: 486}`, Catalyst gives `{00: 504, 11: 496}` → **TVD = 98.6% ✅ PASS**

---

## The Web UI

Open in any browser — no installation needed for users:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Sidebar                  │ MLIR Input           │ QIR Output           │
│                          │                      │                      │
│ Model: 💻 llama3.1-8b    │  module {            │ define void @main()  │
│  [Ollama — ~8GB VRAM]    │    quantum.alloc...  │   call void @h__body │
│ Model: ☁️ gpt-oss-20b    │    quantum.custom... │   call void @cnot... │
│  [HuggingFace — free]    │    ...               │                      │
│                          │                      │                      │
│ [Catalyst] Bell State    │  [🚀 Translate]      │ Time: 2.3ms          │
│ [Quake] GHZ-5            │  [🗑 Clear]          │ Iterations: 1        │
│ Max Iterations: 3        │                      │ Path: Deterministic  │
│                          ├──────────────────────┴──────────────────────┤
│                          │ ✅ PASS — Gate counts match, TVD 98.6%      │
│                          │   QIR backend: real   MLIR: Catalyst (real)│
│                          │   [Bar charts: QIR blue vs Catalyst orange] │
│                          │   Gate table: h=1✓  cnot=1✓                │
└────────────────────────────────────────────────────────────────────────┘
```

**New in this version:**
- **Three metric columns**: Translation Time · Iterations · **Translation Path**
- **Model selector** shows provider type (`💻 Local` / `☁️ API`) + free tier badge
- **Provider info card**: Ollama shows VRAM; HuggingFace shows `✅ HF_TOKEN found`
- Verification pre-computed during agentic run; on-demand for fast deterministic path

---

## New: OpenQASM3 → Quake → QIR Pipeline

We added a full pipeline starting from **OpenQASM 3** (the most common quantum circuit text format):

```
OpenQASM 3 source
      │
      ▼  (CUDA Quantum's cudaq.make_kernel + kernel.module)
Quake MLIR  ──► QuakeDialect parser ──► MLIRCircuit ──► QIR
      │
      ▼  (cudaq.translate)
cudaq QIR (vendor-specific)
```

**8 example circuits** are pre-converted and available in the UI:

| Circuit | Qubits | Gates |
|---------|--------|-------|
| Bell State | 2 | H, CNOT |
| GHZ-5 | 5 | H, 4× CNOT |
| Classic Teleportation | 3 | H, 2× CNOT, X, Z, measurements |
| Random circuits (5×) | 2–4 | Mixed gate sets |

---

## New: Session Logging

When the app is shared over the network, every translation is **automatically logged**:

```json
{
  "timestamp": "2026-02-26T11:14:04.919",
  "session_id": "a3f7c12b",
  "dialect": "quake",
  "translation_time_s": 0.003,
  "circuit_info": { "num_qubits": 2, "num_gates": 2 },
  "mlir_input": "module attributes { quake.alloca ...",
  "qir_output": "; ModuleID = 'translated-circuit' ..."
}
```

- File: **`logs/translations.jsonl`** — one JSON line per translation
- Each user gets a random `session_id` (per browser tab)
- **Thread-safe:** concurrent users write without conflicts
- Inspect with: `python -c "import json; [print(json.loads(l)['session_id'], json.loads(l)['dialect']) for l in open('logs/translations.jsonl')]"`

---

## Sharing with Multiple Users

Streamlit handles multiple concurrent users **out of the box:**

```bash
# Start the app accessible on your network
streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

- Share: `http://<your-IP>:8501`
- Each browser tab = **independent session** with its own input/output state
- Users never see each other's work
- All translations are logged to `logs/translations.jsonl` for review

---

## Example: Bell State — Full Walkthrough

**Input (Catalyst MLIR):**
```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0]          → ssa_qubit["%1"] = 0
%out = quantum.custom "Hadamard"() %1 → ssa_qubit["%out"] = 0
%2 = quantum.extract %0[ 1]          → ssa_qubit["%2"] = 1
%out_0:2 = quantum.custom "CNOT"() %out, %2
                                      → ssa_qubit["%out_0#0"] = 0 (ctrl)
                                      → ssa_qubit["%out_0#1"] = 1 (tgt)
```

**Output (QIR):**
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
call void @__quantum__qis__cnot__body(%Qubit* null,
     %Qubit* inttoptr (i64 1 to %Qubit*))
call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
```

**Verification:** QIR `{00:514, 11:486}` vs Catalyst `{00:504, 11:496}` → TVD 98.6% ✅

---

## Example: GHZ-5 — Quake Dialect

**Input (Quake MLIR — CUDA Quantum format):**
```mlir
quake.h  %1 : (!quake.ref) -> ()           ← H on qubit 0
quake.x [%2] %3 : (!quake.ref, ...) -> ()  ← CNOT(0,1)
quake.x [%4] %5 : (!quake.ref, ...) -> ()  ← CNOT(0,2)
quake.x [%6] %7 : (!quake.ref, ...) -> ()  ← CNOT(0,3)
quake.x [%8] %9 : (!quake.ref, ...) -> ()  ← CNOT(0,4)
```

**Output (QIR):**
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr(i64 1 ...))
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr(i64 2 ...))
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr(i64 3 ...))
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr(i64 4 ...))
```

**Gate count:** MLIR `{h:1, cnot:4}` = QIR `{h:1, cnot:4}` ✅ | **TVD: 99% ✅**

---

## Example: Quantum Teleportation (Conditional)

The teleportation circuit *corrects* errors based on measurement outcomes:

```
q0 ──H──●──────────M(bit0)
q1 ──────X──●──H──M(bit1)
q2 ──────────X────[Z if bit0]──[X if bit1]
```

**What makes it hard:**
- Gates depend on *classical results* of mid-circuit measurements
- The `scf.if` condition in MLIR is linked to the measurement through **5 intermediate IR operations**:

```
quantum.measure → tensor.from_elements → stablehlo.convert
               → stablehlo.compare → tensor.extract → scf.if
```

The parser traces all 5 steps to correctly link `scf.if` to measurement index 0 or 1, then generates conditional QIR blocks with `br i1 %cond, label %then, label %else`.

---

## Verification Results (All Tested Circuits)

### Catalyst dialect circuits

| Circuit | MLIR Exec | QIR Exec | TVD | Status |
|---------|-----------|----------|-----|--------|
| Bell State | `{00:504, 11:496}` | `{00:514, 11:486}` | **98.6%** | ✅ PASS |
| GHZ-3 | `{000:510, 111:490}` | `{000:496, 111:504}` | **98.0%** | ✅ PASS |
| Teleportation | `{000:...}` | `{000:...}` | **96.4%** | ✅ PASS |

### Quake dialect circuits (CUDA Quantum)

| Circuit | cudaq Exec | QIR Exec | TVD | Status |
|---------|------------|----------|-----|--------|
| Bell State | `{00:~500, 11:~500}` | `{00:~500, 11:~500}` | **≥96%** | ✅ PASS |
| GHZ-5 | `{00000:~500, 11111:~500}` | `{00000:~500, 11111:~500}` | **99%** | ✅ PASS |
| Random circuits | Uniform dist. | Uniform dist. | **≥96%** | ✅ PASS |

*All at 1000 shots. TVD threshold: 95%.*

---

## Gate Count Verification (Dual Dialect)

The gate counter now handles both dialects:

**Catalyst MLIR** — looks for `quantum.custom "GateName"()`:
```
quantum.custom "Hadamard"() → { h: 1 }
quantum.custom "CNOT"()     → { cnot: 1 }
```

**Quake MLIR** — looks for `quake.<gate>` patterns:
```
quake.h  %1      → { h: 1 }
quake.x [%2] %3  → { cnot: 1 }   ← controlled X = CNOT
quake.x  %3      → { x: 1 }      ← plain X (no control)
quake.rx (%cst)  → { rx: 1 }
```

Bell State result: **MLIR: `{h:1, cnot:1}` = QIR: `{h:1, cnot:1}`** → ✅ MATCH

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.12 | All components |
| **CLI** | `translate.py` | File/stdin/JSON/pipe developer interface |
| **Web UI** | Streamlit + Plotly | Interactive interface |
| **Dialect 1** | PennyLane Catalyst 0.14 | Catalyst MLIR parsing + `@qjit` execution |
| **Dialect 2** | CUDA Quantum 0.13 | Quake MLIR parsing + `cudaq.sample()` exec |
| **QIR Execution** | `qirrunner 0.9.1` | Real sparse QIR simulator — no LLVM needed |
| **Agent Framework** | **CrewAI 1.10.0** | Multi-agent orchestration (upgraded from 0.28.8) |
| **LLM — local** | Ollama | Llama 3.1 8B/70B, CodeLlama 13B/34B |
| **LLM — cloud** | HuggingFace Inference API | `gpt-oss-20b` (free tier, no GPU) |
| **Web tools** | `WebFetchTool` / `ScrapeWebsiteTool` | Unknown-dialect spec research |
| **Verification** | `pipeline.py` | Shared `run_verification_pipeline()` |
| **RAG / Vector DB** | ChromaDB + SentenceTransformers | Context-aware retrieval |
| **Source IRs** | MLIR (Catalyst + Quake dialects) | Input formats |
| **Target IR** | QIR 1.0 (LLVM IR) | Output format |
| **Logging** | JSONL file | Session audit trail |

---

## Project Structure

```
agentic_mlir_qir_updated/
├── translate.py             ← CLI entry point (python translate.py ...)
├── src/
│   ├── dialects/            ← BaseDialect, CatalystDialect, QuakeDialect
│   ├── parsers/             ← MLIRParser (auto-delegates to dialect)
│   ├── generators/          ← QIRGenerator (template-based)
│   ├── verification/
│   │   ├── pipeline.py      ← run_verification_pipeline() — shared entry point
│   │   ├── qir_runner.py    ← qirrunner 0.9.1 — real QIR execution
│   │   ├── catalyst_runner.py ← pennylane-catalyst — real MLIR execution
│   │   └── quake_runner.py  ← cudaq subprocess — Quake execution
│   ├── agents/              ← CrewAI 1.x TranslationAgent + VerificationAgent
│   │   └── crew_manager.py  ← translate_with_verification() orchestration
│   ├── tools/
│   │   ├── rag_tool.py      ← ChromaDB knowledge retrieval
│   │   ├── gate_counter_tool.py
│   │   └── web_fetch_tool.py ← WebFetchTool + get_web_tools()
│   ├── config/
│   │   └── llm_config.py    ← Ollama + HuggingFace + OpenAI model configs
│   ├── rag/                 ← ChromaDB, embeddings, knowledge chunking
│   └── ui/                  ← Streamlit app (3-metric row, multi-provider)
├── examples/
│   ├── mlir/                ← Catalyst MLIR examples
│   └── quake_mlir/          ← Quake MLIR examples
├── example_quake/           ← OpenQASM3 → Quake conversion script
├── logs/                    ← translations.jsonl (auto-created)
├── knowledge_base/          ← QIR specs, MLIR docs
└── docs/                    ← This presentation
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2a. Local LLM — start Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b-instruct          # ~4.7 GB
# ollama pull llama3.1:70b-instruct-q4_K_M  # ~40 GB, best quality
```

### 2b. Cloud LLM — HuggingFace (no GPU needed, free)
```bash
# Get token at https://huggingface.co/settings/tokens
export HF_TOKEN=hf_...                    # one-time setup
```

### 3. Initialize knowledge base (for RAG)
```bash
python scripts/fetch_knowledge.py && python scripts/initialize_db.py
```

### 4. Use the CLI (quickest path for developers)
```bash
python translate.py examples/mlir/bell_state.mlir            # deterministic
python translate.py circuit.mlir --model llama3.1-8b         # agentic (Ollama)
python translate.py circuit.mlir --model gpt-oss-20b         # agentic (HF free)
python translate.py circuit.mlir --json                       # JSON output
python translate.py --list-models                             # show all keys
```

### 5. Launch the web UI
```bash
# Local only:
streamlit run src/ui/app.py

# Share on network:
streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### 6. Generate Quake MLIR from OpenQASM3
```bash
python example_quake/openqasm_to_quake_mlir.py
```

---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# Summary

<br>

| What | Details |
|------|---------|
| **Input** | Catalyst MLIR · Quake MLIR · OpenQASM3 |
| **Output** | Standard QIR (.ll) — any QIR-compatible simulator |
| **Translation paths** | Deterministic / AI Agent / Det. + AI Repair |
| **Verification** | Gate count match + ≥95% TVD (real simulators) |
| **Web UI** | Streamlit · Translation Path metric · session logging |
| **CLI** | `translate.py` — file/stdin/`--json`/`--model`/`-o` |
| **LLM backends** | Ollama (local GPU) **or** HuggingFace API (free, no GPU) |
| **Free cloud model** | `gpt-oss-20b` — 20B, Apache 2.0, HF Inference API |
| **AI agents** | CrewAI 1.10 · RAG (ChromaDB) · WebFetchTool |

<br>

Built with Python · CrewAI 1.10 · ChromaDB · Ollama · HuggingFace · Streamlit
`qirrunner` · `pennylane-catalyst` · `cudaq` · `translate.py`
