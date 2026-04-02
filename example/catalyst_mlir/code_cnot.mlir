module @run {
  func.func public @jit_run() -> tensor<f64> attributes {llvm.emit_c_interface} {
    %0 = catalyst.launch_kernel @module_code_rotation_cnot::@code_rotation_cnot() : () -> tensor<f64>
    return %0 : tensor<f64>
  }
  module @module_code_rotation_cnot {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @code_rotation_cnot() -> tensor<f64> attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c = stablehlo.constant dense<1> : tensor<i64>
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 4) : !quantum.reg
      %1 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
      %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
      %2 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
      %out_qubits_0:2 = quantum.custom "CZ"() %2, %out_qubits : !quantum.bit, !quantum.bit
      %3 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
      %out_qubits_1:2 = quantum.custom "CZ"() %3, %out_qubits_0#1 : !quantum.bit, !quantum.bit
      %out_qubits_2 = quantum.custom "Hadamard"() %out_qubits_1#0 : !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_2 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %4 = stablehlo.convert %from_elements : (tensor<i1>) -> tensor<i64>
      %5 = stablehlo.compare  EQ, %4, %c,  SIGNED : (tensor<i64>, tensor<i64>) -> tensor<i1>
      %6 = quantum.extract %0[ 3] : !quantum.reg -> !quantum.bit
      %out_qubits_3 = quantum.custom "Hadamard"() %6 : !quantum.bit
      %out_qubits_4:2 = quantum.custom "CZ"() %out_qubits_1#1, %out_qubits_3 : !quantum.bit, !quantum.bit
      %out_qubits_5 = quantum.custom "Hadamard"() %out_qubits_4#0 : !quantum.bit
      %mres_6, %out_qubit_7 = quantum.measure %out_qubits_5 : i1, !quantum.bit
      %from_elements_8 = tensor.from_elements %mres_6 : tensor<i1>
      %7 = stablehlo.convert %from_elements_8 : (tensor<i1>) -> tensor<i64>
      %8 = stablehlo.compare  EQ, %7, %c,  SIGNED : (tensor<i64>, tensor<i64>) -> tensor<i1>
      %9 = stablehlo.convert %from_elements : (tensor<i1>) -> tensor<i64>
      %10 = stablehlo.compare  EQ, %9, %c,  SIGNED : (tensor<i64>, tensor<i64>) -> tensor<i1>
      %11 = quantum.insert %0[ 2], %out_qubit_7 : !quantum.reg, !quantum.bit
      %12 = quantum.insert %11[ 3], %out_qubits_4#1 : !quantum.reg, !quantum.bit
      %13 = quantum.insert %12[ 0], %out_qubits_0#0 : !quantum.reg, !quantum.bit
      %14 = quantum.insert %13[ 1], %out_qubit : !quantum.reg, !quantum.bit
      %extracted = tensor.extract %10[] : tensor<i1>
      %15 = scf.if %extracted -> (!quantum.reg) {
        %21 = quantum.extract %14[ 0] : !quantum.reg -> !quantum.bit
        %out_qubits_12 = quantum.custom "PauliZ"() %21 : !quantum.bit
        %22 = quantum.insert %14[ 0], %out_qubits_12 : !quantum.reg, !quantum.bit
        scf.yield %22 : !quantum.reg
      } else {
        scf.yield %14 : !quantum.reg
      }
      %extracted_9 = tensor.extract %8[] : tensor<i1>
      %16 = scf.if %extracted_9 -> (!quantum.reg) {
        %21 = quantum.extract %15[ 3] : !quantum.reg -> !quantum.bit
        %out_qubits_12 = quantum.custom "PauliX"() %21 : !quantum.bit
        %22 = quantum.insert %15[ 3], %out_qubits_12 : !quantum.reg, !quantum.bit
        scf.yield %22 : !quantum.reg
      } else {
        scf.yield %15 : !quantum.reg
      }
      %extracted_10 = tensor.extract %5[] : tensor<i1>
      %17 = scf.if %extracted_10 -> (!quantum.reg) {
        %21 = quantum.extract %16[ 3] : !quantum.reg -> !quantum.bit
        %out_qubits_12 = quantum.custom "PauliZ"() %21 : !quantum.bit
        %22 = quantum.insert %16[ 3], %out_qubits_12 : !quantum.reg, !quantum.bit
        scf.yield %22 : !quantum.reg
      } else {
        scf.yield %16 : !quantum.reg
      }
      %18 = quantum.extract %17[ 3] : !quantum.reg -> !quantum.bit
      %19 = quantum.namedobs %18[ PauliZ] : !quantum.obs
      %20 = quantum.expval %19 : f64
      %from_elements_11 = tensor.from_elements %20 : tensor<f64>
      quantum.dealloc %17 : !quantum.reg
      quantum.device_release
      return %from_elements_11 : tensor<f64>
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