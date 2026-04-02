module @run {
  func.func public @jit_run() -> tensor<f64> attributes {llvm.emit_c_interface} {
    %0 = catalyst.launch_kernel @module_code_rotation_rx::@code_rotation_rx() : () -> tensor<f64>
    return %0 : tensor<f64>
  }
  module @module_code_rotation_rx {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @code_rotation_rx() -> tensor<f64> attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %cst = arith.constant -1.5707963267948966 : f64
      %cst_0 = arith.constant 0.78539816339744828 : f64
      %c = stablehlo.constant dense<1> : tensor<i64>
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 3) : !quantum.reg
      %1 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
      %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_1 = quantum.custom "Hadamard"() %2 : !quantum.bit
      %3 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits_2:2 = quantum.custom "CZ"() %3, %out_qubits_1 : !quantum.bit, !quantum.bit
      %out_qubits_3:2 = quantum.custom "CZ"() %out_qubits_2#1, %out_qubits : !quantum.bit, !quantum.bit
      %out_qubits_4 = quantum.custom "RZ"(%cst_0) %out_qubits_3#0 : !quantum.bit
      %out_qubits_5 = quantum.custom "Hadamard"() %out_qubits_4 : !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_5 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %4 = stablehlo.convert %from_elements : (tensor<i1>) -> tensor<i64>
      %5 = stablehlo.compare  EQ, %4, %c,  SIGNED : (tensor<i64>, tensor<i64>) -> tensor<i1>
      %out_qubits_6 = quantum.custom "Hadamard"() %out_qubits_2#0 : !quantum.bit
      %mres_7, %out_qubit_8 = quantum.measure %out_qubits_6 : i1, !quantum.bit
      %from_elements_9 = tensor.from_elements %mres_7 : tensor<i1>
      %6 = stablehlo.convert %from_elements_9 : (tensor<i1>) -> tensor<i64>
      %7 = stablehlo.compare  EQ, %6, %c,  SIGNED : (tensor<i64>, tensor<i64>) -> tensor<i1>
      %out_qubits_10 = quantum.custom "RX"(%cst) %out_qubits_3#1 : !quantum.bit
      %8 = quantum.insert %0[ 1], %out_qubit : !quantum.reg, !quantum.bit
      %9 = quantum.insert %8[ 2], %out_qubits_10 : !quantum.reg, !quantum.bit
      %10 = quantum.insert %9[ 0], %out_qubit_8 : !quantum.reg, !quantum.bit
      %extracted = tensor.extract %7[] : tensor<i1>
      %11 = scf.if %extracted -> (!quantum.reg) {
        %16 = quantum.extract %10[ 2] : !quantum.reg -> !quantum.bit
        %out_qubits_13 = quantum.custom "PauliX"() %16 : !quantum.bit
        %17 = quantum.insert %10[ 2], %out_qubits_13 : !quantum.reg, !quantum.bit
        scf.yield %17 : !quantum.reg
      } else {
        scf.yield %10 : !quantum.reg
      }
      %extracted_11 = tensor.extract %5[] : tensor<i1>
      %12 = scf.if %extracted_11 -> (!quantum.reg) {
        %16 = quantum.extract %11[ 2] : !quantum.reg -> !quantum.bit
        %out_qubits_13 = quantum.custom "PauliZ"() %16 : !quantum.bit
        %17 = quantum.insert %11[ 2], %out_qubits_13 : !quantum.reg, !quantum.bit
        scf.yield %17 : !quantum.reg
      } else {
        scf.yield %11 : !quantum.reg
      }
      %13 = quantum.extract %12[ 2] : !quantum.reg -> !quantum.bit
      %14 = quantum.namedobs %13[ PauliZ] : !quantum.obs
      %15 = quantum.expval %14 : f64
      %from_elements_12 = tensor.from_elements %15 : tensor<f64>
      quantum.dealloc %12 : !quantum.reg
      quantum.device_release
      return %from_elements_12 : tensor<f64>
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