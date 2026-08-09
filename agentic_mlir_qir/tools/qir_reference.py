"""Inline QIR reference context for translation agents.

Instead of asking the LLM to call a RAG tool (which small models fail at),
we inject the gate mappings and translation patterns directly into the prompt.
This follows the "context engineering" approach: pre-compute relevant context,
inject it, and let the agent focus on reasoning rather than retrieval.

The reference is dialect-conditional: Catalyst- and Quake-specific guidance
(register-extraction syntax, non-gate scaffolding ops) is only injected when
translating that dialect. Bloating every prompt with dialect-specific detail
irrelevant to the circuit being translated (e.g. Catalyst notes injected while
translating an unrelated FTQC circuit) measurably degrades smaller models —
see the FTQC regression this was introduced to fix.
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

# ── Core Translation Patterns (dialect-agnostic, always injected) ─────────────
CORE_PATTERNS = """\
## Key Translation Patterns

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
7. `extract`, `extract_ref`, `alloc`, `alloca` are register bookkeeping, not gates — emit no QIR call for them.

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

# ── Catalyst-specific patterns (only injected for dialect == "catalyst") ──────
CATALYST_PATTERNS = """\
### Catalyst Qubit Register Extraction (CRITICAL — most common indexing error)

Catalyst allocates a qubit **register** and then extracts individual qubit
handles from it. The extraction op is NOT a gate — never emit a QIR call for
it. The physical qubit index is the LITERAL INTEGER inside the brackets
`[...]`, never the SSA variable's own number.

```
%0 = quantum.alloc(2) : !quantum.reg
%1 = quantum.extract %0[0] : !quantum.reg -> !quantum.bit   ; %1 IS qubit 0 (index in brackets, NOT "1")
%out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit ; H on qubit 0 (same physical qubit as %1)
%2 = quantum.extract %0[1] : !quantum.reg -> !quantum.bit   ; %2 IS qubit 1
%out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
  ; CNOT(control=qubit 0, target=qubit 1) — control is %out_qubits (still qubit 0), target is %2 (qubit 1)
```
Correct QIR: `h 0` then `cnot 0 1`. WRONG (common mistake): `h 1` — do NOT use the
SSA variable's numeric suffix (`%1`, `%2`) as the qubit index. Only the number
inside `quantum.extract %reg[N]` is the qubit index. A qubit keeps its index
through every gate that consumes and re-produces its SSA handle (e.g.
`%out_qubits` after H is still qubit 0).

### Catalyst Non-Gate Ops (CRITICAL — ignore these completely)

Real Catalyst MLIR (as opposed to a simplified textbook example) is usually
wrapped in JIT/gradient/expectation-value scaffolding that has NO gate content
and NO QIR equivalent. A circuit written to return expectation values (common
when Catalyst is used with `@qjit`) contains many ops beyond the actual gates:

```
quantum.device shots(%c0_i64) [...]         ; simulator config — NOT a gate
%0 = quantum.alloc(2) : !quantum.reg        ; register allocation — NOT a gate
%1 = quantum.extract %0[0] : ...            ; qubit reference — NOT a gate
%out = quantum.custom "Hadamard"() %1 : ... ; <-- THIS is the only real gate op
%3 = quantum.namedobs %out[PauliZ] : ...    ; observable definition — NOT a gate
%4 = quantum.expval %3 : f64                ; expectation value readout — NOT a gate
%from_elements = tensor.from_elements %4 : ...  ; tensor packaging — NOT a gate
%7 = quantum.insert %0[0], %out : ...       ; write qubit back to register — NOT a gate
quantum.dealloc %8 : !quantum.reg           ; register deallocation — NOT a gate
quantum.device_release                      ; simulator teardown — NOT a gate
```

Out of every op in a real Catalyst kernel, ONLY `quantum.custom "<GateName>"()`
(the actual gate) and `quantum.measure` (the actual measurement) translate to
QIR calls. Every other op listed above — `device`, `alloc`, `extract`,
`namedobs`, `expval`, `insert`, `dealloc`, `device_release`, and any
`tensor.*`/`arith.*` op — is bookkeeping around the circuit and must be
SKIPPED ENTIRELY. Do NOT invent QIR calls like `__quantum__qis__namedobs__body`
or `__quantum__qis__expval__body` — these have no QIR equivalent. If you see
`quantum.namedobs`/`quantum.expval` at the end of a circuit, that circuit is
being measured for an expectation value rather than sampled directly — still
translate it as: apply the real gates in order, then `mz` every qubit that was
used, exactly as if it had been measured with `quantum.measure`.
"""

# ── Quake-specific patterns (only injected for dialect == "quake") ────────────
QUAKE_PATTERNS = """\
### Quake Qubit Register Extraction (CRITICAL — most common indexing error)

Quake allocates a qubit **register** and extracts individual qubit handles from
it via `quake.extract_ref %veq[%c]`, where the index is a separate constant SSA
value. The extraction op is NOT a gate — never emit a QIR call for it.

```
%0 = quake.alloca !quake.veq<2>
%c0_i64 = arith.constant 0 : i64
%1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref  ; %1 IS qubit 0 (constant value 0, NOT SSA name "%1")
quake.h %1 : (!quake.ref) -> ()                                          ; H on qubit 0
%c1_i64 = arith.constant 1 : i64
%3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref  ; %3 IS qubit 1 (constant value 1)
quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()  ; controlled-X (=CNOT): control=%2's qubit, target=%3's qubit
```
Correct QIR: `h 0` then `cnot 0 1`. To find the index, trace the SSA value passed
into `extract_ref`'s brackets back to its `arith.constant N` definition — use N,
not any SSA variable number.

`quake.x [%ctrl] %target` (an `x`/`y`/`z` op with a bracketed control-qubit list
before the target) is a CONTROLLED gate, not a bare one-qubit gate: one control
→ `cnot` (for x) / controlled-Z-style `cz` (for z); do not drop the control and
emit a plain single-qubit `x`.
"""


def get_qir_reference_context(dialect: str = None) -> str:
    """Return the QIR reference to inject into the translation prompt.

    Dialect-specific sections (Catalyst/Quake register-extraction syntax and
    non-gate scaffolding ops) are only included when translating that dialect,
    so an unrelated circuit (e.g. FTQC) doesn't get its prompt diluted with
    guidance about ops it will never see.
    """
    parts = [GATE_MAPPINGS, QIR_TEMPLATE, CORE_PATTERNS]
    dialect_lc = (dialect or "").lower()
    if dialect_lc == "catalyst":
        parts.append(CATALYST_PATTERNS)
    elif dialect_lc == "quake":
        parts.append(QUAKE_PATTERNS)
    return "\n".join(parts)
