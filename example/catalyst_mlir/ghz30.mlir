module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:30 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19, %0#20, %0#21, %0#22, %0#23, %0#24, %0#25, %0#26, %0#27, %0#28, %0#29 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/mlir/.vcatalyst/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 30) : !quantum.reg
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
      %26 = quantum.extract %0[ 25] : !quantum.reg -> !quantum.bit
      %out_qubits_24:2 = quantum.custom "CNOT"() %out_qubits_23#0, %26 : !quantum.bit, !quantum.bit
      %27 = quantum.extract %0[ 26] : !quantum.reg -> !quantum.bit
      %out_qubits_25:2 = quantum.custom "CNOT"() %out_qubits_24#0, %27 : !quantum.bit, !quantum.bit
      %28 = quantum.extract %0[ 27] : !quantum.reg -> !quantum.bit
      %out_qubits_26:2 = quantum.custom "CNOT"() %out_qubits_25#0, %28 : !quantum.bit, !quantum.bit
      %29 = quantum.extract %0[ 28] : !quantum.reg -> !quantum.bit
      %out_qubits_27:2 = quantum.custom "CNOT"() %out_qubits_26#0, %29 : !quantum.bit, !quantum.bit
      %30 = quantum.extract %0[ 29] : !quantum.reg -> !quantum.bit
      %out_qubits_28:2 = quantum.custom "CNOT"() %out_qubits_27#0, %30 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_28#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_29, %out_qubit_30 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_31 = tensor.from_elements %mres_29 : tensor<i1>
      %mres_32, %out_qubit_33 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_34 = tensor.from_elements %mres_32 : tensor<i1>
      %mres_35, %out_qubit_36 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_37 = tensor.from_elements %mres_35 : tensor<i1>
      %mres_38, %out_qubit_39 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_40 = tensor.from_elements %mres_38 : tensor<i1>
      %mres_41, %out_qubit_42 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_43 = tensor.from_elements %mres_41 : tensor<i1>
      %mres_44, %out_qubit_45 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_46 = tensor.from_elements %mres_44 : tensor<i1>
      %mres_47, %out_qubit_48 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_49 = tensor.from_elements %mres_47 : tensor<i1>
      %mres_50, %out_qubit_51 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_52 = tensor.from_elements %mres_50 : tensor<i1>
      %mres_53, %out_qubit_54 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_55 = tensor.from_elements %mres_53 : tensor<i1>
      %mres_56, %out_qubit_57 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_58 = tensor.from_elements %mres_56 : tensor<i1>
      %mres_59, %out_qubit_60 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_61 = tensor.from_elements %mres_59 : tensor<i1>
      %mres_62, %out_qubit_63 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_64 = tensor.from_elements %mres_62 : tensor<i1>
      %mres_65, %out_qubit_66 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_67 = tensor.from_elements %mres_65 : tensor<i1>
      %mres_68, %out_qubit_69 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_70 = tensor.from_elements %mres_68 : tensor<i1>
      %mres_71, %out_qubit_72 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_73 = tensor.from_elements %mres_71 : tensor<i1>
      %mres_74, %out_qubit_75 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_76 = tensor.from_elements %mres_74 : tensor<i1>
      %mres_77, %out_qubit_78 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_79 = tensor.from_elements %mres_77 : tensor<i1>
      %mres_80, %out_qubit_81 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_82 = tensor.from_elements %mres_80 : tensor<i1>
      %mres_83, %out_qubit_84 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_85 = tensor.from_elements %mres_83 : tensor<i1>
      %mres_86, %out_qubit_87 = quantum.measure %out_qubits_19#1 : i1, !quantum.bit
      %from_elements_88 = tensor.from_elements %mres_86 : tensor<i1>
      %mres_89, %out_qubit_90 = quantum.measure %out_qubits_20#1 : i1, !quantum.bit
      %from_elements_91 = tensor.from_elements %mres_89 : tensor<i1>
      %mres_92, %out_qubit_93 = quantum.measure %out_qubits_21#1 : i1, !quantum.bit
      %from_elements_94 = tensor.from_elements %mres_92 : tensor<i1>
      %mres_95, %out_qubit_96 = quantum.measure %out_qubits_22#1 : i1, !quantum.bit
      %from_elements_97 = tensor.from_elements %mres_95 : tensor<i1>
      %mres_98, %out_qubit_99 = quantum.measure %out_qubits_23#1 : i1, !quantum.bit
      %from_elements_100 = tensor.from_elements %mres_98 : tensor<i1>
      %mres_101, %out_qubit_102 = quantum.measure %out_qubits_24#1 : i1, !quantum.bit
      %from_elements_103 = tensor.from_elements %mres_101 : tensor<i1>
      %mres_104, %out_qubit_105 = quantum.measure %out_qubits_25#1 : i1, !quantum.bit
      %from_elements_106 = tensor.from_elements %mres_104 : tensor<i1>
      %mres_107, %out_qubit_108 = quantum.measure %out_qubits_26#1 : i1, !quantum.bit
      %from_elements_109 = tensor.from_elements %mres_107 : tensor<i1>
      %mres_110, %out_qubit_111 = quantum.measure %out_qubits_27#1 : i1, !quantum.bit
      %from_elements_112 = tensor.from_elements %mres_110 : tensor<i1>
      %mres_113, %out_qubit_114 = quantum.measure %out_qubits_28#1 : i1, !quantum.bit
      %from_elements_115 = tensor.from_elements %mres_113 : tensor<i1>
      %31 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %32 = quantum.insert %31[ 1], %out_qubit_30 : !quantum.reg, !quantum.bit
      %33 = quantum.insert %32[ 2], %out_qubit_33 : !quantum.reg, !quantum.bit
      %34 = quantum.insert %33[ 3], %out_qubit_36 : !quantum.reg, !quantum.bit
      %35 = quantum.insert %34[ 4], %out_qubit_39 : !quantum.reg, !quantum.bit
      %36 = quantum.insert %35[ 5], %out_qubit_42 : !quantum.reg, !quantum.bit
      %37 = quantum.insert %36[ 6], %out_qubit_45 : !quantum.reg, !quantum.bit
      %38 = quantum.insert %37[ 7], %out_qubit_48 : !quantum.reg, !quantum.bit
      %39 = quantum.insert %38[ 8], %out_qubit_51 : !quantum.reg, !quantum.bit
      %40 = quantum.insert %39[ 9], %out_qubit_54 : !quantum.reg, !quantum.bit
      %41 = quantum.insert %40[ 10], %out_qubit_57 : !quantum.reg, !quantum.bit
      %42 = quantum.insert %41[ 11], %out_qubit_60 : !quantum.reg, !quantum.bit
      %43 = quantum.insert %42[ 12], %out_qubit_63 : !quantum.reg, !quantum.bit
      %44 = quantum.insert %43[ 13], %out_qubit_66 : !quantum.reg, !quantum.bit
      %45 = quantum.insert %44[ 14], %out_qubit_69 : !quantum.reg, !quantum.bit
      %46 = quantum.insert %45[ 15], %out_qubit_72 : !quantum.reg, !quantum.bit
      %47 = quantum.insert %46[ 16], %out_qubit_75 : !quantum.reg, !quantum.bit
      %48 = quantum.insert %47[ 17], %out_qubit_78 : !quantum.reg, !quantum.bit
      %49 = quantum.insert %48[ 18], %out_qubit_81 : !quantum.reg, !quantum.bit
      %50 = quantum.insert %49[ 19], %out_qubit_84 : !quantum.reg, !quantum.bit
      %51 = quantum.insert %50[ 20], %out_qubit_87 : !quantum.reg, !quantum.bit
      %52 = quantum.insert %51[ 21], %out_qubit_90 : !quantum.reg, !quantum.bit
      %53 = quantum.insert %52[ 22], %out_qubit_93 : !quantum.reg, !quantum.bit
      %54 = quantum.insert %53[ 23], %out_qubit_96 : !quantum.reg, !quantum.bit
      %55 = quantum.insert %54[ 24], %out_qubit_99 : !quantum.reg, !quantum.bit
      %56 = quantum.insert %55[ 25], %out_qubit_102 : !quantum.reg, !quantum.bit
      %57 = quantum.insert %56[ 26], %out_qubit_105 : !quantum.reg, !quantum.bit
      %58 = quantum.insert %57[ 27], %out_qubit_108 : !quantum.reg, !quantum.bit
      %59 = quantum.insert %58[ 28], %out_qubit_111 : !quantum.reg, !quantum.bit
      %60 = quantum.insert %59[ 29], %out_qubit_114 : !quantum.reg, !quantum.bit
      quantum.dealloc %60 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_31, %from_elements_34, %from_elements_37, %from_elements_40, %from_elements_43, %from_elements_46, %from_elements_49, %from_elements_52, %from_elements_55, %from_elements_58, %from_elements_61, %from_elements_64, %from_elements_67, %from_elements_70, %from_elements_73, %from_elements_76, %from_elements_79, %from_elements_82, %from_elements_85, %from_elements_88, %from_elements_91, %from_elements_94, %from_elements_97, %from_elements_100, %from_elements_103, %from_elements_106, %from_elements_109, %from_elements_112, %from_elements_115 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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