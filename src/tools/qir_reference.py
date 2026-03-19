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
"""


def get_qir_reference_context() -> str:
    """Return the full QIR reference to inject into the translation prompt."""
    return f"{GATE_MAPPINGS}\n{QIR_TEMPLATE}\n{TRANSLATION_PATTERNS}"
