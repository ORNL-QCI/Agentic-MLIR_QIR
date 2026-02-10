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
      %cst = arith.constant 2.590000e+00 : f64
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 2) : !quantum.reg
      %1 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %2 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits:2 = quantum.custom "CNOT"() %1, %2 : !quantum.bit, !quantum.bit
      %out_qubits_0:2 = quantum.custom "SWAP"() %out_qubits#1, %out_qubits#0 : !quantum.bit, !quantum.bit
      %out_qubits_1 = quantum.custom "Hadamard"() %out_qubits_0#1 : !quantum.bit
      %out_qubits_2 = quantum.custom "S"() %out_qubits_0#0 : !quantum.bit
      %out_qubits_3 = quantum.custom "RX"(%cst) %out_qubits_2 : !quantum.bit
      %out_qubits_4 = quantum.custom "PauliY"() %out_qubits_3 : !quantum.bit
      %out_qubits_5:2 = quantum.custom "CNOT"() %out_qubits_4, %out_qubits_1 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_5#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_6, %out_qubit_7 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_8 = tensor.from_elements %mres_6 : tensor<i1>
      %3 = quantum.insert %0[ 1], %out_qubit_7 : !quantum.reg, !quantum.bit
      %4 = quantum.insert %3[ 0], %out_qubit : !quantum.reg, !quantum.bit
      quantum.dealloc %4 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_8 : tensor<i1>, tensor<i1>
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