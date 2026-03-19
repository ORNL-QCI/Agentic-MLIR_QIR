; ModuleID = 'steane_1q_h'
source_filename = "steane_1q_h"

define void @steane_1q_h() #0 {
entry:
  call void @__quantum__rt__initialize(ptr null)
  ; --- Steane [[7,1,3]] encoding: encode |0_L> ---
  call void @__quantum__qis__h__body(ptr null)
  call void @__quantum__qis__h__body(ptr inttoptr (i64 1 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 3 to ptr))
  call void @__quantum__qis__cnot__body(ptr null, ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__cnot__body(ptr null, ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__cnot__body(ptr null, ptr inttoptr (i64 6 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 6 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 6 to ptr))
  ; --- end Steane encoding ---
  ; logical_h (transversal H on 7 qubits)
  call void @__quantum__qis__h__body(ptr null)
  call void @__quantum__qis__h__body(ptr inttoptr (i64 1 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 3 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 6 to ptr))
  ; logical_measure → 7 physical mz operations
  ; logical outcome = parity(r[0..N-1]) (classical XOR)
  call void @__quantum__qis__mz__body(ptr null, ptr null)
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 1 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 2 to ptr), ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 3 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 4 to ptr), ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 5 to ptr), ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 6 to ptr), ptr inttoptr (i64 6 to ptr))
  call void @__quantum__rt__array_record_output(i64 7, ptr null)
  call void @__quantum__rt__result_record_output(ptr null, ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 1 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 2 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 3 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 4 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 5 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 6 to ptr), ptr null)
  ret void
}

declare void @__quantum__qis__cnot__body(ptr, ptr)
declare void @__quantum__qis__h__body(ptr)
declare void @__quantum__qis__mz__body(ptr, ptr writeonly) #1
declare void @__quantum__rt__array_record_output(i64, ptr)
declare void @__quantum__rt__initialize(ptr)
declare void @__quantum__rt__result_record_output(ptr, ptr)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="base" "required_num_qubits"="7" "required_num_results"="7" }
attributes #1 = { "irreversible" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
