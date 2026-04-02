module @run_ghz25 {
  func.func public @jit_run_ghz25() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:25 = catalyst.launch_kernel @module_ghz_25_qubits::@ghz_25_qubits() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19, %0#20, %0#21, %0#22, %0#23, %0#24 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz_25_qubits {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz_25_qubits() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "adjoint", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/usr/local/lib/python3.12/dist-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 25) : !quantum.reg
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
      %21 = quantum.extract %0[ 20] : !quantum.reg -> !quantum.bit
      %out_qubits_19:2 = quantum.custom "CNOT"() %out_qubits_18#0, %21 : !quantum.bit, !quantum.bit
      %22 = quantum.extract %0[ 21] : !quantum.reg -> !quantum.bit
      %out_qubits_20:2 = quantum.custom "CNOT"() %out_qubits_19#0, %22 : !quantum.bit, !quantum.bit
      %23 = quantum.extract %0[ 22] : !quantum.reg -> !quantum.bit
      %out_qubits_21:2 = quantum.custom "CNOT"() %out_qubits_20#0, %23 : !quantum.bit, !quantum.bit
      %24 = quantum.extract %0[ 23] : !quantum.reg -> !quantum.bit
      %out_qubits_22:2 = quantum.custom "CNOT"() %out_qubits_21#0, %24 : !quantum.bit, !quantum.bit
      %25 = quantum.extract %0[ 24] : !quantum.reg -> !quantum.bit
      %out_qubits_23:2 = quantum.custom "CNOT"() %out_qubits_22#0, %25 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_23#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_24, %out_qubit_25 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_26 = tensor.from_elements %mres_24 : tensor<i1>
      %mres_27, %out_qubit_28 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_29 = tensor.from_elements %mres_27 : tensor<i1>
      %mres_30, %out_qubit_31 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_32 = tensor.from_elements %mres_30 : tensor<i1>
      %mres_33, %out_qubit_34 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_35 = tensor.from_elements %mres_33 : tensor<i1>
      %mres_36, %out_qubit_37 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_38 = tensor.from_elements %mres_36 : tensor<i1>
      %mres_39, %out_qubit_40 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_41 = tensor.from_elements %mres_39 : tensor<i1>
      %mres_42, %out_qubit_43 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_44 = tensor.from_elements %mres_42 : tensor<i1>
      %mres_45, %out_qubit_46 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_47 = tensor.from_elements %mres_45 : tensor<i1>
      %mres_48, %out_qubit_49 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_50 = tensor.from_elements %mres_48 : tensor<i1>
      %mres_51, %out_qubit_52 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_53 = tensor.from_elements %mres_51 : tensor<i1>
      %mres_54, %out_qubit_55 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_56 = tensor.from_elements %mres_54 : tensor<i1>
      %mres_57, %out_qubit_58 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_59 = tensor.from_elements %mres_57 : tensor<i1>
      %mres_60, %out_qubit_61 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_62 = tensor.from_elements %mres_60 : tensor<i1>
      %mres_63, %out_qubit_64 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_65 = tensor.from_elements %mres_63 : tensor<i1>
      %mres_66, %out_qubit_67 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_68 = tensor.from_elements %mres_66 : tensor<i1>
      %mres_69, %out_qubit_70 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_71 = tensor.from_elements %mres_69 : tensor<i1>
      %mres_72, %out_qubit_73 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_74 = tensor.from_elements %mres_72 : tensor<i1>
      %mres_75, %out_qubit_76 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_77 = tensor.from_elements %mres_75 : tensor<i1>
      %mres_78, %out_qubit_79 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_80 = tensor.from_elements %mres_78 : tensor<i1>
      %mres_81, %out_qubit_82 = quantum.measure %out_qubits_19#1 : i1, !quantum.bit
      %from_elements_83 = tensor.from_elements %mres_81 : tensor<i1>
      %mres_84, %out_qubit_85 = quantum.measure %out_qubits_20#1 : i1, !quantum.bit
      %from_elements_86 = tensor.from_elements %mres_84 : tensor<i1>
      %mres_87, %out_qubit_88 = quantum.measure %out_qubits_21#1 : i1, !quantum.bit
      %from_elements_89 = tensor.from_elements %mres_87 : tensor<i1>
      %mres_90, %out_qubit_91 = quantum.measure %out_qubits_22#1 : i1, !quantum.bit
      %from_elements_92 = tensor.from_elements %mres_90 : tensor<i1>
      %mres_93, %out_qubit_94 = quantum.measure %out_qubits_23#1 : i1, !quantum.bit
      %from_elements_95 = tensor.from_elements %mres_93 : tensor<i1>
      %26 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %27 = quantum.insert %26[ 1], %out_qubit_25 : !quantum.reg, !quantum.bit
      %28 = quantum.insert %27[ 2], %out_qubit_28 : !quantum.reg, !quantum.bit
      %29 = quantum.insert %28[ 3], %out_qubit_31 : !quantum.reg, !quantum.bit
      %30 = quantum.insert %29[ 4], %out_qubit_34 : !quantum.reg, !quantum.bit
      %31 = quantum.insert %30[ 5], %out_qubit_37 : !quantum.reg, !quantum.bit
      %32 = quantum.insert %31[ 6], %out_qubit_40 : !quantum.reg, !quantum.bit
      %33 = quantum.insert %32[ 7], %out_qubit_43 : !quantum.reg, !quantum.bit
      %34 = quantum.insert %33[ 8], %out_qubit_46 : !quantum.reg, !quantum.bit
      %35 = quantum.insert %34[ 9], %out_qubit_49 : !quantum.reg, !quantum.bit
      %36 = quantum.insert %35[ 10], %out_qubit_52 : !quantum.reg, !quantum.bit
      %37 = quantum.insert %36[ 11], %out_qubit_55 : !quantum.reg, !quantum.bit
      %38 = quantum.insert %37[ 12], %out_qubit_58 : !quantum.reg, !quantum.bit
      %39 = quantum.insert %38[ 13], %out_qubit_61 : !quantum.reg, !quantum.bit
      %40 = quantum.insert %39[ 14], %out_qubit_64 : !quantum.reg, !quantum.bit
      %41 = quantum.insert %40[ 15], %out_qubit_67 : !quantum.reg, !quantum.bit
      %42 = quantum.insert %41[ 16], %out_qubit_70 : !quantum.reg, !quantum.bit
      %43 = quantum.insert %42[ 17], %out_qubit_73 : !quantum.reg, !quantum.bit
      %44 = quantum.insert %43[ 18], %out_qubit_76 : !quantum.reg, !quantum.bit
      %45 = quantum.insert %44[ 19], %out_qubit_79 : !quantum.reg, !quantum.bit
      %46 = quantum.insert %45[ 20], %out_qubit_82 : !quantum.reg, !quantum.bit
      %47 = quantum.insert %46[ 21], %out_qubit_85 : !quantum.reg, !quantum.bit
      %48 = quantum.insert %47[ 22], %out_qubit_88 : !quantum.reg, !quantum.bit
      %49 = quantum.insert %48[ 23], %out_qubit_91 : !quantum.reg, !quantum.bit
      %50 = quantum.insert %49[ 24], %out_qubit_94 : !quantum.reg, !quantum.bit
      quantum.dealloc %50 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_26, %from_elements_29, %from_elements_32, %from_elements_35, %from_elements_38, %from_elements_41, %from_elements_44, %from_elements_47, %from_elements_50, %from_elements_53, %from_elements_56, %from_elements_59, %from_elements_62, %from_elements_65, %from_elements_68, %from_elements_71, %from_elements_74, %from_elements_77, %from_elements_80, %from_elements_83, %from_elements_86, %from_elements_89, %from_elements_92, %from_elements_95 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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