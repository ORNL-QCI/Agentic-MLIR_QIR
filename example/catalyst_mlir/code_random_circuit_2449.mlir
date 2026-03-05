module @run {
  func.func public @jit_run() -> (tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:2 = catalyst.launch_kernel @module_quantum_circuit::@quantum_circuit() : () -> (tensor<i1>, tensor<i1>)
    return %0#0, %0#1 : tensor<i1>, tensor<i1>
  }
  module @module_quantum_circuit {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @quantum_circuit() -> (tensor<i1>, tensor<i1>) attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %cst = arith.constant 1.080000e+00 : f64
      %cst_0 = arith.constant 2.410000e+00 : f64
      %cst_1 = arith.constant 3.000000e-02 : f64
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 6) : !quantum.reg
      %1 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "RZ"(%cst_1) %1 : !quantum.bit
      %2 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_2 = quantum.custom "T"() %2 : !quantum.bit
      %3 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits_3 = quantum.custom "RX"(%cst_0) %3 : !quantum.bit
      %out_qubits_4 = quantum.custom "PauliX"() %out_qubits_3 : !quantum.bit
      %4 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits_5 = quantum.custom "RZ"(%cst) %4 : !quantum.bit
      %out_qubits_6 = quantum.custom "S"() %out_qubits_5 : !quantum.bit
      %5 = quantum.extract %0[ 4] : !quantum.reg -> !quantum.bit
      %out_qubits_7:2 = quantum.custom "CNOT"() %5, %out_qubits_6 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %6 = quantum.extract %0[ 5] : !quantum.reg -> !quantum.bit
      %out_qubits_8 = quantum.custom "PauliX"() %6 : !quantum.bit
      %out_qubits_9 = quantum.custom "PauliY"() %out_qubits_8 : !quantum.bit
      %mres_10, %out_qubit_11 = quantum.measure %out_qubits_9 : i1, !quantum.bit
      %from_elements_12 = tensor.from_elements %mres_10 : tensor<i1>
      %7 = quantum.insert %0[ 5], %out_qubit_11 : !quantum.reg, !quantum.bit
      %8 = quantum.insert %7[ 1], %out_qubits : !quantum.reg, !quantum.bit
      %9 = quantum.insert %8[ 2], %out_qubit : !quantum.reg, !quantum.bit
      %10 = quantum.insert %9[ 3], %out_qubits_2 : !quantum.reg, !quantum.bit
      %11 = quantum.insert %10[ 0], %out_qubits_4 : !quantum.reg, !quantum.bit
      %12 = quantum.insert %11[ 4], %out_qubits_7#0 : !quantum.reg, !quantum.bit
      quantum.dealloc %12 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_12 : tensor<i1>, tensor<i1>
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
