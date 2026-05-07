"""Inline QIR reference context for translation agents.

Instead of asking the LLM to call a RAG tool (which small models fail at),
we inject the gate mappings and translation patterns directly into the prompt.
This follows the "context engineering" approach: pre-compute relevant context,
inject it, and let the agent focus on reasoning rather than retrieval.
"""

# ── Gate Mapping Table ────────────────────────────────────────────────────────
GATE_MAPPINGS = """\
## MLIR → QIR Gate Mappings

### Single-Qubit Gates
| MLIR Gate (Catalyst)  | QIR Function                    | Signature             |
|-----------------------|---------------------------------|-----------------------|
| Hadamard              | __quantum__qis__h__body         | (%Qubit*)             |
| PauliX                | __quantum__qis__x__body         | (%Qubit*)             |
| PauliY                | __quantum__qis__y__body         | (%Qubit*)             |
| PauliZ                | __quantum__qis__z__body         | (%Qubit*)             |
| S                     | __quantum__qis__s__body         | (%Qubit*)             |
| T                     | __quantum__qis__t__body         | (%Qubit*)             |

### Parameterised Gates
| MLIR Gate | QIR Function                    | Signature               |
|-----------|---------------------------------|-------------------------|
| RX        | __quantum__qis__rx__body        | (double, %Qubit*)       |
| RY        | __quantum__qis__ry__body        | (double, %Qubit*)       |
| RZ        | __quantum__qis__rz__body        | (double, %Qubit*)       |

### Two-Qubit Gates
| MLIR Gate | QIR Function                    | Signature                 |
|-----------|---------------------------------|---------------------------|
| CNOT      | __quantum__qis__cnot__body      | (%Qubit*, %Qubit*)        |
| CZ        | __quantum__qis__cz__body        | (%Qubit*, %Qubit*)        |
| SWAP      | __quantum__qis__swap__body      | (%Qubit*, %Qubit*)        |

### Measurement
| MLIR Op          | QIR Function                    | Signature                     |
|------------------|---------------------------------|-------------------------------|
| quantum.measure  | __quantum__qis__mz__body        | (%Qubit*, %Result* writeonly) |

### Qubit Pointer Syntax
- Qubit 0: `null`
- Qubit N: `inttoptr (i64 N to %Qubit*)`
- Result 0: `null`
- Result N: `inttoptr (i64 N to %Result*)`
"""

# ── Complete QIR Template (Bell State) ────────────────────────────────────────
QIR_TEMPLATE = """\
## Complete QIR Example (2-qubit Bell State: H on q0, CNOT q0→q1)

```llvm
; ModuleID = 'bell-state'
source_filename = "bell-state"

%Qubit = type opaque
%Result = type opaque

define void @main() #0 {
entry:
  call void @__quantum__rt__initialize(i8* null)
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
  call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
  call void @__quantum__qis__mz__body(%Qubit* inttoptr (i64 1 to %Qubit*), %Result* inttoptr (i64 1 to %Result*))
  call void @__quantum__rt__array_record_output(i64 2, i8* null)
  call void @__quantum__rt__result_record_output(%Result* null, i8* null)
  call void @__quantum__rt__result_record_output(%Result* inttoptr (i64 1 to %Result*), i8* null)
  ret void
}

declare void @__quantum__rt__initialize(i8*)
declare void @__quantum__qis__h__body(%Qubit*)
declare void @__quantum__qis__cnot__body(%Qubit*, %Qubit*)
declare void @__quantum__qis__mz__body(%Qubit*, %Result* writeonly) #1
declare void @__quantum__rt__array_record_output(i64, i8*)
declare void @__quantum__rt__result_record_output(%Result*, i8*)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="2" "required_num_results"="2" }
attributes #1 = { "irreversible" }

!llvm.module.flags = !{!0, !1, !2, !3}
!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
```

Example of a CZ gate (for comparison with CNOT above — these are distinct gates):
```llvm
call void @__quantum__qis__cz__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
```
"""

# ── Translation Patterns ─────────────────────────────────────────────────────
TRANSLATION_PATTERNS = """\
## Key Translation Patterns

### Qubit Allocation
MLIR `quantum.alloc(N)` + `quantum.extract %reg[i]` → QIR uses static qubit pointers (no allocation call needed).

### Gate Sequencing
MLIR SSA: `%out = quantum.custom "Hadamard"() %q0` → QIR: `call void @__quantum__qis__h__body(%Qubit* null)`
The SSA chain in MLIR tracks qubit state; in QIR, just emit the gate calls in order.

### Measurements
MLIR: `%mres, %out = quantum.measure %q` → QIR: `call void @__quantum__qis__mz__body(%Qubit* <ptr>, %Result* <ptr>)`
Each qubit gets its own Result slot (0, 1, 2, ...).

### Output Recording (REQUIRED at end of @main)
```llvm
call void @__quantum__rt__array_record_output(i64 <num_qubits>, i8* null)
call void @__quantum__rt__result_record_output(%Result* null, i8* null)           ; result 0
call void @__quantum__rt__result_record_output(%Result* inttoptr (i64 1 to %Result*), i8* null) ; result 1
; ... one per qubit
```

### Conditional Operations (mid-circuit measurement)
MLIR: `scf.if %cond` → QIR: `br i1 %cond, label %then, label %else` with basic blocks.

### Gate Keyword Inference for Unknown Dialects

When translating MLIR from an unrecognized dialect, identify the QIR gate by scanning the MLIR operation name for a recognized gate keyword. The keyword may appear as a bare token, a prefix, a suffix, or surrounded by underscores or dots.

Recognized keywords (longest match wins when multiple could apply):

| Keyword         | QIR Function                     |
|-----------------|----------------------------------|
| `cnot`, `cx`    | `__quantum__qis__cnot__body`     |
| `cz`            | `__quantum__qis__cz__body`       |
| `swap`          | `__quantum__qis__swap__body`     |
| `rx`            | `__quantum__qis__rx__body`       |
| `ry`            | `__quantum__qis__ry__body`       |
| `rz`            | `__quantum__qis__rz__body`       |
| `h`             | `__quantum__qis__h__body`        |
| `x`             | `__quantum__qis__x__body`        |
| `y`             | `__quantum__qis__y__body`        |
| `z`             | `__quantum__qis__z__body`        |
| `s`             | `__quantum__qis__s__body`        |
| `t`             | `__quantum__qis__t__body`        |
| `mz`, `measure` | `__quantum__qis__mz__body`       |

Matching rules (generic across any dialect):
1. An op name may have a dialect prefix (`<dialect>.`), a role prefix (e.g. `logical_`, `phys_`, `ctrl_`), or a role suffix (e.g. `_gate`, `_op`). Strip these and match the remaining gate keyword.
2. Prefer the **longest** keyword match. If `cnot` matches, do not also match `x` or `not`.
3. `cz` and `cnot` are DIFFERENT gates. Do not substitute one for the other.
4. The qubit count equals the number of qubits allocated or initialized in the source MLIR. Do not invent extra qubits.
5. Emit exactly one `mz` measurement per measured qubit. Do not duplicate.
6. Any `init_zero` or similar "prepare |0>" op is implicit in QIR — emit no gate call for it.

### SSA-Form MLIR: Multi-Result Gate Operations

Many MLIR dialects use value-semantic SSA form where each gate operation produces **new SSA values** representing the post-gate qubit state. A single gate operation on N qubits returns N output SSA values — these are NOT new qubits, they are the updated handles for the SAME qubits.

Example pattern (generic):
```
%out1, %out2 = <dialect>.<op>_cz %in1, %in2 : (...) -> (...)
```
This is ONE CZ gate on two qubits. It emits ONE QIR call:
```
call void @__quantum__qis__cz__body(<ptr for qubit of in1>, <ptr for qubit of in2>)
```
Do NOT emit two gate calls. Do NOT allocate new qubits for `%out1`, `%out2` — they refer to the same physical qubits as `%in1`, `%in2` after the gate is applied.

Rules for SSA-form translation:
1. Track each SSA value to a physical qubit index. When a gate produces new SSA names, they inherit the qubit indices of their inputs in the same order.
2. Count qubits from `init_zero`, `alloc`, or the first appearance of each logical qubit variable — NOT from the output SSA names of subsequent gates.
3. Two output SSA names from one two-qubit gate = one gate call in QIR, not two.
4. For the measurement step, use the LAST SSA handle of each qubit (the one just before `measure`/`mz`) to identify which qubit to measure. Emit one `mz` per qubit, not per SSA name.

### Literal Operation-Preserving Translation (CRITICAL)

Your job is to translate MLIR to QIR **literally**, operation by operation. Do NOT try to optimize or simplify the circuit. Even if you notice that certain gate sequences could be simplified mathematically, you must NOT apply those simplifications.

Strict rules:

1. **One MLIR gate op = one QIR gate call.** If the MLIR has 6 `h` ops, the QIR must have exactly 6 `h` calls. Not 2, not 8 — exactly 6.
2. **Do NOT drop or cancel gates.** Even if two consecutive H gates mathematically cancel, emit BOTH in the QIR.
3. **Do NOT introduce gates that are not in the MLIR.** If the MLIR has no `cnot` operations, the QIR must have zero `cnot` calls. Do NOT invent gates to "make the circuit work."
4. **Do NOT apply circuit identities or equivalences.** For example:
   - H-Z-H is NOT equivalent to CNOT in this translation. If the MLIR says H, Z, H, emit three separate QIR calls: `h`, `z`, `h`.
   - H-X-H is NOT equivalent to Z. Emit H, X, H.
   - H-CNOT-H is NOT equivalent to CZ. Emit H, CNOT, H.
5. **Preserve gate order.** Emit QIR gate calls in the same order the ops appear in the MLIR.
6. **Gate count must match exactly.** Before finalizing, count each gate type in the MLIR and confirm the QIR has the same count per type.

If you simplify or substitute, the verification pipeline WILL detect the mismatch and reject your output. Translate faithfully.
"""


def get_qir_reference_context() -> str:
    """Return the full QIR reference to inject into the translation prompt."""
    return f"{GATE_MAPPINGS}\n{QIR_TEMPLATE}\n{TRANSLATION_PATTERNS}"
