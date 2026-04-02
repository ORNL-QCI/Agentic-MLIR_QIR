module @run_ghz15 {
  func.func public @jit_run_ghz15() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:15 = catalyst.launch_kernel @module_ghz_15_qubits::@ghz_15_qubits() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz_15_qubits {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz_15_qubits() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 15) : !quantum.reg
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
      %mres, %out_qubit = quantum.measure %out_qubits_13#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_14, %out_qubit_15 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_16 = tensor.from_elements %mres_14 : tensor<i1>
      %mres_17, %out_qubit_18 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_19 = tensor.from_elements %mres_17 : tensor<i1>
      %mres_20, %out_qubit_21 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_22 = tensor.from_elements %mres_20 : tensor<i1>
      %mres_23, %out_qubit_24 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_25 = tensor.from_elements %mres_23 : tensor<i1>
      %mres_26, %out_qubit_27 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_28 = tensor.from_elements %mres_26 : tensor<i1>
      %mres_29, %out_qubit_30 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_31 = tensor.from_elements %mres_29 : tensor<i1>
      %mres_32, %out_qubit_33 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_34 = tensor.from_elements %mres_32 : tensor<i1>
      %mres_35, %out_qubit_36 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_37 = tensor.from_elements %mres_35 : tensor<i1>
      %mres_38, %out_qubit_39 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_40 = tensor.from_elements %mres_38 : tensor<i1>
      %mres_41, %out_qubit_42 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_43 = tensor.from_elements %mres_41 : tensor<i1>
      %mres_44, %out_qubit_45 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_46 = tensor.from_elements %mres_44 : tensor<i1>
      %mres_47, %out_qubit_48 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_49 = tensor.from_elements %mres_47 : tensor<i1>
      %mres_50, %out_qubit_51 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_52 = tensor.from_elements %mres_50 : tensor<i1>
      %mres_53, %out_qubit_54 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_55 = tensor.from_elements %mres_53 : tensor<i1>
      %16 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %17 = quantum.insert %16[ 1], %out_qubit_15 : !quantum.reg, !quantum.bit
      %18 = quantum.insert %17[ 2], %out_qubit_18 : !quantum.reg, !quantum.bit
      %19 = quantum.insert %18[ 3], %out_qubit_21 : !quantum.reg, !quantum.bit
      %20 = quantum.insert %19[ 4], %out_qubit_24 : !quantum.reg, !quantum.bit
      %21 = quantum.insert %20[ 5], %out_qubit_27 : !quantum.reg, !quantum.bit
      %22 = quantum.insert %21[ 6], %out_qubit_30 : !quantum.reg, !quantum.bit
      %23 = quantum.insert %22[ 7], %out_qubit_33 : !quantum.reg, !quantum.bit
      %24 = quantum.insert %23[ 8], %out_qubit_36 : !quantum.reg, !quantum.bit
      %25 = quantum.insert %24[ 9], %out_qubit_39 : !quantum.reg, !quantum.bit
      %26 = quantum.insert %25[ 10], %out_qubit_42 : !quantum.reg, !quantum.bit
      %27 = quantum.insert %26[ 11], %out_qubit_45 : !quantum.reg, !quantum.bit
      %28 = quantum.insert %27[ 12], %out_qubit_48 : !quantum.reg, !quantum.bit
      %29 = quantum.insert %28[ 13], %out_qubit_51 : !quantum.reg, !quantum.bit
      %30 = quantum.insert %29[ 14], %out_qubit_54 : !quantum.reg, !quantum.bit
      quantum.dealloc %30 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_16, %from_elements_19, %from_elements_22, %from_elements_25, %from_elements_28, %from_elements_31, %from_elements_34, %from_elements_37, %from_elements_40, %from_elements_43, %from_elements_46, %from_elements_49, %from_elements_52, %from_elements_55 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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
