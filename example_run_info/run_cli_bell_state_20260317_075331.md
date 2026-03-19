# CLI Translation Run — `bell_state`

- **Date**: 2026-03-17 07:53:31
- **Source**: `examples/mlir/bell_state.mlir`
- **Model**: `deterministic (no LLM)`
- **Dialect**: `catalyst`
- **Translation Path**: `deterministic`
- **Iterations**: 1
- **Translation Time**: 11.01 s
- **Simulation Shots**: 1000
- **Overall Result**: ✅ SUCCESS

---

## Gate Comparison

| Gate | MLIR | QIR | Status |
|------|------|-----|--------|
| `cnot` | 1 | 1 | ✅ match |
| `h` | 1 | 1 | ✅ match |
| **Total** | **2** | **2** | **✅ match** |

---

## Verification Results

| Metric | Value |
|--------|-------|
| QIR backend | real execution |
| MLIR backend | Catalyst (qjit) (real execution) |
| Gate match | ✅ PASS |
| TVD similarity | 98.3% — ✅ PASS |

### Distribution Comparison

| Outcome | QIR Count | MLIR Count |
|---------|-----------|------------|
| `00` | 486 | 503 |
| `11` | 514 | 497 |

---

## MLIR Input

```mlir
// Bell State Circuit - Creates entangled pair |00⟩ + |11⟩
// Catalyst dialect (PennyLane)

func.func @bell_state() {
  %0 = quantum.alloc( 2) : !quantum.reg
  %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
  %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
  %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
  %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
  %3 = quantum.measure %out_qubits_0#0 : !quantum.meas
  %4 = quantum.measure %out_qubits_0#1 : !quantum.meas
  func.return
}
```

---

## QIR Output

```llvm
; ModuleID = 'translated-circuit'
source_filename = "translated-circuit"

%Qubit = type opaque
%Result = type opaque

define void @main() #0 {
entry:
  call void @__quantum__rt__initialize(i8* null)
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
  ret void
}


declare void @__quantum__rt__initialize(i8*)

declare void @__quantum__qis__h__body(%Qubit*)
declare void @__quantum__qis__cnot__body(%Qubit*, %Qubit*)

declare void @__quantum__qis__mz__body(%Qubit*, %Result* writeonly) #1



declare void @__quantum__rt__array_record_output(i64, i8*)

declare void @__quantum__rt__result_record_output(%Result*, i8*)


attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="2" "required_num_results"="0" }
attributes #1 = { "irreversible" }


!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
```
