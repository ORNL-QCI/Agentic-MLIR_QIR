; ModuleID = 'steane_2q_bell'
source_filename = "steane_2q_bell"

define void @steane_2q_bell() #0 {
entry:
  call void @__quantum__rt__initialize(ptr null)
  ; --- Steane [[7,1,3]] encoding: encode |0_L> for logical qubit 0 (physical 0-6) ---
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
  ; --- end Steane encoding for logical qubit 0 ---
  ; --- Steane [[7,1,3]] encoding: encode |0_L> for logical qubit 1 (physical 7-13) ---
  call void @__quantum__qis__h__body(ptr inttoptr (i64 7 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 8 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 10 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 7 to ptr), ptr inttoptr (i64 9 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 7 to ptr), ptr inttoptr (i64 11 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 7 to ptr), ptr inttoptr (i64 13 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 8 to ptr), ptr inttoptr (i64 9 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 8 to ptr), ptr inttoptr (i64 12 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 8 to ptr), ptr inttoptr (i64 13 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 10 to ptr), ptr inttoptr (i64 11 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 10 to ptr), ptr inttoptr (i64 12 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 10 to ptr), ptr inttoptr (i64 13 to ptr))
  ; --- end Steane encoding for logical qubit 1 ---
  ; logical_h on qubit 0 (transversal H on physical 0-6)
  call void @__quantum__qis__h__body(ptr null)
  call void @__quantum__qis__h__body(ptr inttoptr (i64 1 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 3 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__h__body(ptr inttoptr (i64 6 to ptr))
  ; logical_cnot(qubit 0 -> qubit 1) (transversal CNOT: physical i -> i+7)
  call void @__quantum__qis__cnot__body(ptr null, ptr inttoptr (i64 7 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 8 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 2 to ptr), ptr inttoptr (i64 9 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 10 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 4 to ptr), ptr inttoptr (i64 11 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 5 to ptr), ptr inttoptr (i64 12 to ptr))
  call void @__quantum__qis__cnot__body(ptr inttoptr (i64 6 to ptr), ptr inttoptr (i64 13 to ptr))
  ; logical_measure qubit 0 → 7 physical mz (0-6)
  call void @__quantum__qis__mz__body(ptr null, ptr null)
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 1 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 2 to ptr), ptr inttoptr (i64 2 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 3 to ptr), ptr inttoptr (i64 3 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 4 to ptr), ptr inttoptr (i64 4 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 5 to ptr), ptr inttoptr (i64 5 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 6 to ptr), ptr inttoptr (i64 6 to ptr))
  ; logical_measure qubit 1 → 7 physical mz (7-13)
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 7 to ptr), ptr inttoptr (i64 7 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 8 to ptr), ptr inttoptr (i64 8 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 9 to ptr), ptr inttoptr (i64 9 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 10 to ptr), ptr inttoptr (i64 10 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 11 to ptr), ptr inttoptr (i64 11 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 12 to ptr), ptr inttoptr (i64 12 to ptr))
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 13 to ptr), ptr inttoptr (i64 13 to ptr))
  call void @__quantum__rt__array_record_output(i64 14, ptr null)
  call void @__quantum__rt__result_record_output(ptr null, ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 1 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 2 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 3 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 4 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 5 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 6 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 7 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 8 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 9 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 10 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 11 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 12 to ptr), ptr null)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 13 to ptr), ptr null)
  ret void
}

declare void @__quantum__qis__cnot__body(ptr, ptr)
declare void @__quantum__qis__h__body(ptr)
declare void @__quantum__qis__mz__body(ptr, ptr writeonly) #1
declare void @__quantum__rt__array_record_output(i64, ptr)
declare void @__quantum__rt__initialize(ptr)
declare void @__quantum__rt__result_record_output(ptr, ptr)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="base" "required_num_qubits"="14" "required_num_results"="14" }
attributes #1 = { "irreversible" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
