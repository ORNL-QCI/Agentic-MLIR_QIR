module @circuit {
  func.func public @jit_circuit() -> tensor<128xf64> attributes {llvm.emit_c_interface} {
    %0 = catalyst.launch_kernel @module_circuit::@circuit() : () -> tensor<128xf64>
    return %0 : tensor<128xf64>
  }
  module @module_circuit {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @circuit() -> tensor<128xf64> attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/mlir/.vcatalyst/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 7) : !quantum.reg
      %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
      %2 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
      %3 = quantum.extract %0[ 4] : !quantum.reg -> !quantum.bit
      %out_qubits_1:2 = quantum.custom "CNOT"() %out_qubits_0#0, %3 : !quantum.bit, !quantum.bit
      %4 = quantum.extract %0[ 6] : !quantum.reg -> !quantum.bit
      %out_qubits_2:2 = quantum.custom "CNOT"() %out_qubits_1#0, %4 : !quantum.bit, !quantum.bit
      %out_qubits_3 = quantum.custom "Hadamard"() %out_qubits_2#0 : !quantum.bit
      %5 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_4 = quantum.custom "Hadamard"() %5 : !quantum.bit
      %out_qubits_5:2 = quantum.custom "CNOT"() %out_qubits_4, %out_qubits_0#1 : !quantum.bit, !quantum.bit
      %6 = quantum.extract %0[ 5] : !quantum.reg -> !quantum.bit
      %out_qubits_6:2 = quantum.custom "CNOT"() %out_qubits_5#0, %6 : !quantum.bit, !quantum.bit
      %out_qubits_7:2 = quantum.custom "CNOT"() %out_qubits_6#0, %out_qubits_2#1 : !quantum.bit, !quantum.bit
      %out_qubits_8 = quantum.custom "Hadamard"() %out_qubits_7#0 : !quantum.bit
      %out_qubits_9 = quantum.custom "Hadamard"() %out_qubits_5#1 : !quantum.bit
      %7 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_10 = quantum.custom "Hadamard"() %7 : !quantum.bit
      %out_qubits_11:2 = quantum.custom "CNOT"() %out_qubits_10, %out_qubits_1#1 : !quantum.bit, !quantum.bit
      %out_qubits_12:2 = quantum.custom "CNOT"() %out_qubits_11#0, %out_qubits_6#1 : !quantum.bit, !quantum.bit
      %out_qubits_13:2 = quantum.custom "CNOT"() %out_qubits_12#0, %out_qubits_7#1 : !quantum.bit, !quantum.bit
      %out_qubits_14 = quantum.custom "Hadamard"() %out_qubits_13#0 : !quantum.bit
      %out_qubits_15 = quantum.custom "Hadamard"() %out_qubits_11#1 : !quantum.bit
      %out_qubits_16 = quantum.custom "Hadamard"() %out_qubits_12#1 : !quantum.bit
      %out_qubits_17 = quantum.custom "Hadamard"() %out_qubits_13#1 : !quantum.bit
      %8 = quantum.compbasis qubits %out_qubits_3, %out_qubits_8, %out_qubits_9, %out_qubits_14, %out_qubits_15, %out_qubits_16, %out_qubits_17 : !quantum.obs
      %9 = quantum.probs %8 : tensor<128xf64>
      %10 = quantum.insert %0[ 0], %out_qubits_3 : !quantum.reg, !quantum.bit
      %11 = quantum.insert %10[ 1], %out_qubits_8 : !quantum.reg, !quantum.bit
      %12 = quantum.insert %11[ 3], %out_qubits_14 : !quantum.reg, !quantum.bit
      %13 = quantum.insert %12[ 2], %out_qubits_9 : !quantum.reg, !quantum.bit
      %14 = quantum.insert %13[ 4], %out_qubits_15 : !quantum.reg, !quantum.bit
      %15 = quantum.insert %14[ 6], %out_qubits_17 : !quantum.reg, !quantum.bit
      %16 = quantum.insert %15[ 5], %out_qubits_16 : !quantum.reg, !quantum.bit
      quantum.dealloc %16 : !quantum.reg
      quantum.device_release
      return %9 : tensor<128xf64>
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