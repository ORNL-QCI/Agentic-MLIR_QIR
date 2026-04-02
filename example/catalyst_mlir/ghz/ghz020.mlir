module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:20 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/.venv/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 20) : !quantum.reg
      %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
      %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
      %3 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits_1:2 = quantum.custom "CNOT"() %out_qubits_0#0, %3 : !quantum.bit, !quantum.bit
      %4 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_2:2 = quantum.custom "CNOT"() %out_qubits_1#0, %4 : !quantum.bit, !quantum.bit
      %5 = quantum.extract %0[ 4] : !quantum.reg -> !quantum.bit
      %out_qubits_3:2 = quantum.custom "CNOT"() %out_qubits_2#0, %5 : !quantum.bit, !quantum.bit
      %6 = quantum.extract %0[ 5] : !quantum.reg -> !quantum.bit
      %out_qubits_4:2 = quantum.custom "CNOT"() %out_qubits_3#0, %6 : !quantum.bit, !quantum.bit
      %7 = quantum.extract %0[ 6] : !quantum.reg -> !quantum.bit
      %out_qubits_5:2 = quantum.custom "CNOT"() %out_qubits_4#0, %7 : !quantum.bit, !quantum.bit
      %8 = quantum.extract %0[ 7] : !quantum.reg -> !quantum.bit
      %out_qubits_6:2 = quantum.custom "CNOT"() %out_qubits_5#0, %8 : !quantum.bit, !quantum.bit
      %9 = quantum.extract %0[ 8] : !quantum.reg -> !quantum.bit
      %out_qubits_7:2 = quantum.custom "CNOT"() %out_qubits_6#0, %9 : !quantum.bit, !quantum.bit
      %10 = quantum.extract %0[ 9] : !quantum.reg -> !quantum.bit
      %out_qubits_8:2 = quantum.custom "CNOT"() %out_qubits_7#0, %10 : !quantum.bit, !quantum.bit
      %11 = quantum.extract %0[ 10] : !quantum.reg -> !quantum.bit
      %out_qubits_9:2 = quantum.custom "CNOT"() %out_qubits_8#0, %11 : !quantum.bit, !quantum.bit
      %12 = quantum.extract %0[ 11] : !quantum.reg -> !quantum.bit
      %out_qubits_10:2 = quantum.custom "CNOT"() %out_qubits_9#0, %12 : !quantum.bit, !quantum.bit
      %13 = quantum.extract %0[ 12] : !quantum.reg -> !quantum.bit
      %out_qubits_11:2 = quantum.custom "CNOT"() %out_qubits_10#0, %13 : !quantum.bit, !quantum.bit
      %14 = quantum.extract %0[ 13] : !quantum.reg -> !quantum.bit
      %out_qubits_12:2 = quantum.custom "CNOT"() %out_qubits_11#0, %14 : !quantum.bit, !quantum.bit
      %15 = quantum.extract %0[ 14] : !quantum.reg -> !quantum.bit
      %out_qubits_13:2 = quantum.custom "CNOT"() %out_qubits_12#0, %15 : !quantum.bit, !quantum.bit
      %16 = quantum.extract %0[ 15] : !quantum.reg -> !quantum.bit
      %out_qubits_14:2 = quantum.custom "CNOT"() %out_qubits_13#0, %16 : !quantum.bit, !quantum.bit
      %17 = quantum.extract %0[ 16] : !quantum.reg -> !quantum.bit
      %out_qubits_15:2 = quantum.custom "CNOT"() %out_qubits_14#0, %17 : !quantum.bit, !quantum.bit
      %18 = quantum.extract %0[ 17] : !quantum.reg -> !quantum.bit
      %out_qubits_16:2 = quantum.custom "CNOT"() %out_qubits_15#0, %18 : !quantum.bit, !quantum.bit
      %19 = quantum.extract %0[ 18] : !quantum.reg -> !quantum.bit
      %out_qubits_17:2 = quantum.custom "CNOT"() %out_qubits_16#0, %19 : !quantum.bit, !quantum.bit
      %20 = quantum.extract %0[ 19] : !quantum.reg -> !quantum.bit
      %out_qubits_18:2 = quantum.custom "CNOT"() %out_qubits_17#0, %20 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_18#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_19, %out_qubit_20 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_21 = tensor.from_elements %mres_19 : tensor<i1>
      %mres_22, %out_qubit_23 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_24 = tensor.from_elements %mres_22 : tensor<i1>
      %mres_25, %out_qubit_26 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_27 = tensor.from_elements %mres_25 : tensor<i1>
      %mres_28, %out_qubit_29 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_30 = tensor.from_elements %mres_28 : tensor<i1>
      %mres_31, %out_qubit_32 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_33 = tensor.from_elements %mres_31 : tensor<i1>
      %mres_34, %out_qubit_35 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_36 = tensor.from_elements %mres_34 : tensor<i1>
      %mres_37, %out_qubit_38 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_39 = tensor.from_elements %mres_37 : tensor<i1>
      %mres_40, %out_qubit_41 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_42 = tensor.from_elements %mres_40 : tensor<i1>
      %mres_43, %out_qubit_44 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_45 = tensor.from_elements %mres_43 : tensor<i1>
      %mres_46, %out_qubit_47 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_48 = tensor.from_elements %mres_46 : tensor<i1>
      %mres_49, %out_qubit_50 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_51 = tensor.from_elements %mres_49 : tensor<i1>
      %mres_52, %out_qubit_53 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_54 = tensor.from_elements %mres_52 : tensor<i1>
      %mres_55, %out_qubit_56 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_57 = tensor.from_elements %mres_55 : tensor<i1>
      %mres_58, %out_qubit_59 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_60 = tensor.from_elements %mres_58 : tensor<i1>
      %mres_61, %out_qubit_62 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_63 = tensor.from_elements %mres_61 : tensor<i1>
      %mres_64, %out_qubit_65 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_66 = tensor.from_elements %mres_64 : tensor<i1>
      %mres_67, %out_qubit_68 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_69 = tensor.from_elements %mres_67 : tensor<i1>
      %mres_70, %out_qubit_71 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_72 = tensor.from_elements %mres_70 : tensor<i1>
      %mres_73, %out_qubit_74 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_75 = tensor.from_elements %mres_73 : tensor<i1>
      %21 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %22 = quantum.insert %21[ 1], %out_qubit_20 : !quantum.reg, !quantum.bit
      %23 = quantum.insert %22[ 2], %out_qubit_23 : !quantum.reg, !quantum.bit
      %24 = quantum.insert %23[ 3], %out_qubit_26 : !quantum.reg, !quantum.bit
      %25 = quantum.insert %24[ 4], %out_qubit_29 : !quantum.reg, !quantum.bit
      %26 = quantum.insert %25[ 5], %out_qubit_32 : !quantum.reg, !quantum.bit
      %27 = quantum.insert %26[ 6], %out_qubit_35 : !quantum.reg, !quantum.bit
      %28 = quantum.insert %27[ 7], %out_qubit_38 : !quantum.reg, !quantum.bit
      %29 = quantum.insert %28[ 8], %out_qubit_41 : !quantum.reg, !quantum.bit
      %30 = quantum.insert %29[ 9], %out_qubit_44 : !quantum.reg, !quantum.bit
      %31 = quantum.insert %30[ 10], %out_qubit_47 : !quantum.reg, !quantum.bit
      %32 = quantum.insert %31[ 11], %out_qubit_50 : !quantum.reg, !quantum.bit
      %33 = quantum.insert %32[ 12], %out_qubit_53 : !quantum.reg, !quantum.bit
      %34 = quantum.insert %33[ 13], %out_qubit_56 : !quantum.reg, !quantum.bit
      %35 = quantum.insert %34[ 14], %out_qubit_59 : !quantum.reg, !quantum.bit
      %36 = quantum.insert %35[ 15], %out_qubit_62 : !quantum.reg, !quantum.bit
      %37 = quantum.insert %36[ 16], %out_qubit_65 : !quantum.reg, !quantum.bit
      %38 = quantum.insert %37[ 17], %out_qubit_68 : !quantum.reg, !quantum.bit
      %39 = quantum.insert %38[ 18], %out_qubit_71 : !quantum.reg, !quantum.bit
      %40 = quantum.insert %39[ 19], %out_qubit_74 : !quantum.reg, !quantum.bit
      quantum.dealloc %40 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_21, %from_elements_24, %from_elements_27, %from_elements_30, %from_elements_33, %from_elements_36, %from_elements_39, %from_elements_42, %from_elements_45, %from_elements_48, %from_elements_51, %from_elements_54, %from_elements_57, %from_elements_60, %from_elements_63, %from_elements_66, %from_elements_69, %from_elements_72, %from_elements_75 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
    }
  }
  func.func @setup() {
    quantum.init
    return
  }
  func.func @teardown() {
    quantum.finalize
    return
  }
}