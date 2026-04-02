module @run_ghz10 {
  func.func public @jit_run_ghz10() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:10 = catalyst.launch_kernel @module_ghz_10_qubits::@ghz_10_qubits() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz_10_qubits {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz_10_qubits() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 10) : !quantum.reg
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
      %mres, %out_qubit = quantum.measure %out_qubits_8#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_9, %out_qubit_10 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_11 = tensor.from_elements %mres_9 : tensor<i1>
      %mres_12, %out_qubit_13 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_14 = tensor.from_elements %mres_12 : tensor<i1>
      %mres_15, %out_qubit_16 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_17 = tensor.from_elements %mres_15 : tensor<i1>
      %mres_18, %out_qubit_19 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_20 = tensor.from_elements %mres_18 : tensor<i1>
      %mres_21, %out_qubit_22 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_23 = tensor.from_elements %mres_21 : tensor<i1>
      %mres_24, %out_qubit_25 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_26 = tensor.from_elements %mres_24 : tensor<i1>
      %mres_27, %out_qubit_28 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_29 = tensor.from_elements %mres_27 : tensor<i1>
      %mres_30, %out_qubit_31 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_32 = tensor.from_elements %mres_30 : tensor<i1>
      %mres_33, %out_qubit_34 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_35 = tensor.from_elements %mres_33 : tensor<i1>
      %11 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %12 = quantum.insert %11[ 1], %out_qubit_10 : !quantum.reg, !quantum.bit
      %13 = quantum.insert %12[ 2], %out_qubit_13 : !quantum.reg, !quantum.bit
      %14 = quantum.insert %13[ 3], %out_qubit_16 : !quantum.reg, !quantum.bit
      %15 = quantum.insert %14[ 4], %out_qubit_19 : !quantum.reg, !quantum.bit
      %16 = quantum.insert %15[ 5], %out_qubit_22 : !quantum.reg, !quantum.bit
      %17 = quantum.insert %16[ 6], %out_qubit_25 : !quantum.reg, !quantum.bit
      %18 = quantum.insert %17[ 7], %out_qubit_28 : !quantum.reg, !quantum.bit
      %19 = quantum.insert %18[ 8], %out_qubit_31 : !quantum.reg, !quantum.bit
      %20 = quantum.insert %19[ 9], %out_qubit_34 : !quantum.reg, !quantum.bit
      quantum.dealloc %20 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_11, %from_elements_14, %from_elements_17, %from_elements_20, %from_elements_23, %from_elements_26, %from_elements_29, %from_elements_32, %from_elements_35 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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