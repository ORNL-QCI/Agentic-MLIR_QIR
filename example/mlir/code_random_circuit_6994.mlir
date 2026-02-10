module @run {
  func.func public @jit_run() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:4 = catalyst.launch_kernel @module_quantum_circuit::@quantum_circuit() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_quantum_circuit {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @quantum_circuit() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %cst = arith.constant 1.720000e+00 : f64
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 4) : !quantum.reg
      %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "PauliY"() %1 : !quantum.bit
      %out_qubits_0 = quantum.custom "RX"(%cst) %out_qubits : !quantum.bit
      %2 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits_1:2 = quantum.custom "CNOT"() %2, %out_qubits_0 : !quantum.bit, !quantum.bit
      %out_qubits_2 = quantum.custom "PauliZ"() %out_qubits_1#1 : !quantum.bit
      %out_qubits_3:2 = quantum.custom "SWAP"() %out_qubits_2, %out_qubits_1#0 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_3#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %3 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_4 = quantum.custom "Hadamard"() %3 : !quantum.bit
      %out_qubits_5 = quantum.custom "PauliY"() %out_qubits_4 : !quantum.bit
      %out_qubits_6 = quantum.custom "S"() %out_qubits_5 : !quantum.bit
      %mres_7, %out_qubit_8 = quantum.measure %out_qubits_6 : i1, !quantum.bit
      %from_elements_9 = tensor.from_elements %mres_7 : tensor<i1>
      %mres_10, %out_qubit_11 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_12 = tensor.from_elements %mres_10 : tensor<i1>
      %4 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_13 = quantum.custom "T"() %4 : !quantum.bit
      %out_qubits_14 = quantum.custom "S"() %out_qubits_13 : !quantum.bit
      %mres_15, %out_qubit_16 = quantum.measure %out_qubits_14 : i1, !quantum.bit
      %from_elements_17 = tensor.from_elements %mres_15 : tensor<i1>
      %5 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %6 = quantum.insert %5[ 3], %out_qubit_16 : !quantum.reg, !quantum.bit
      %7 = quantum.insert %6[ 2], %out_qubit_11 : !quantum.reg, !quantum.bit
      %8 = quantum.insert %7[ 1], %out_qubit_8 : !quantum.reg, !quantum.bit
      quantum.dealloc %8 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_9, %from_elements_12, %from_elements_17 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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