module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:4 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/mlir/.vcatalyst/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 4) : !quantum.reg
      %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
      %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
      %3 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits_1:2 = quantum.custom "CNOT"() %out_qubits_0#0, %3 : !quantum.bit, !quantum.bit
      %4 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_2:2 = quantum.custom "CNOT"() %out_qubits_1#0, %4 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_2#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_3, %out_qubit_4 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_5 = tensor.from_elements %mres_3 : tensor<i1>
      %mres_6, %out_qubit_7 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_8 = tensor.from_elements %mres_6 : tensor<i1>
      %mres_9, %out_qubit_10 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_11 = tensor.from_elements %mres_9 : tensor<i1>
      %5 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %6 = quantum.insert %5[ 1], %out_qubit_4 : !quantum.reg, !quantum.bit
      %7 = quantum.insert %6[ 2], %out_qubit_7 : !quantum.reg, !quantum.bit
      %8 = quantum.insert %7[ 3], %out_qubit_10 : !quantum.reg, !quantum.bit
      quantum.dealloc %8 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_5, %from_elements_8, %from_elements_11 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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