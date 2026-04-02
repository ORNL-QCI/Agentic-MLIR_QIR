module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:35 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19, %0#20, %0#21, %0#22, %0#23, %0#24, %0#25, %0#26, %0#27, %0#28, %0#29, %0#30, %0#31, %0#32, %0#33, %0#34 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/.venv/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 35) : !quantum.reg
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
      %31 = quantum.extract %0[ 30] : !quantum.reg -> !quantum.bit
      %out_qubits_29:2 = quantum.custom "CNOT"() %out_qubits_28#0, %31 : !quantum.bit, !quantum.bit
      %32 = quantum.extract %0[ 31] : !quantum.reg -> !quantum.bit
      %out_qubits_30:2 = quantum.custom "CNOT"() %out_qubits_29#0, %32 : !quantum.bit, !quantum.bit
      %33 = quantum.extract %0[ 32] : !quantum.reg -> !quantum.bit
      %out_qubits_31:2 = quantum.custom "CNOT"() %out_qubits_30#0, %33 : !quantum.bit, !quantum.bit
      %34 = quantum.extract %0[ 33] : !quantum.reg -> !quantum.bit
      %out_qubits_32:2 = quantum.custom "CNOT"() %out_qubits_31#0, %34 : !quantum.bit, !quantum.bit
      %35 = quantum.extract %0[ 34] : !quantum.reg -> !quantum.bit
      %out_qubits_33:2 = quantum.custom "CNOT"() %out_qubits_32#0, %35 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_33#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_34, %out_qubit_35 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_36 = tensor.from_elements %mres_34 : tensor<i1>
      %mres_37, %out_qubit_38 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_39 = tensor.from_elements %mres_37 : tensor<i1>
      %mres_40, %out_qubit_41 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_42 = tensor.from_elements %mres_40 : tensor<i1>
      %mres_43, %out_qubit_44 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_45 = tensor.from_elements %mres_43 : tensor<i1>
      %mres_46, %out_qubit_47 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_48 = tensor.from_elements %mres_46 : tensor<i1>
      %mres_49, %out_qubit_50 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_51 = tensor.from_elements %mres_49 : tensor<i1>
      %mres_52, %out_qubit_53 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_54 = tensor.from_elements %mres_52 : tensor<i1>
      %mres_55, %out_qubit_56 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_57 = tensor.from_elements %mres_55 : tensor<i1>
      %mres_58, %out_qubit_59 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_60 = tensor.from_elements %mres_58 : tensor<i1>
      %mres_61, %out_qubit_62 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_63 = tensor.from_elements %mres_61 : tensor<i1>
      %mres_64, %out_qubit_65 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_66 = tensor.from_elements %mres_64 : tensor<i1>
      %mres_67, %out_qubit_68 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_69 = tensor.from_elements %mres_67 : tensor<i1>
      %mres_70, %out_qubit_71 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_72 = tensor.from_elements %mres_70 : tensor<i1>
      %mres_73, %out_qubit_74 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_75 = tensor.from_elements %mres_73 : tensor<i1>
      %mres_76, %out_qubit_77 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_78 = tensor.from_elements %mres_76 : tensor<i1>
      %mres_79, %out_qubit_80 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_81 = tensor.from_elements %mres_79 : tensor<i1>
      %mres_82, %out_qubit_83 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_84 = tensor.from_elements %mres_82 : tensor<i1>
      %mres_85, %out_qubit_86 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_87 = tensor.from_elements %mres_85 : tensor<i1>
      %mres_88, %out_qubit_89 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_90 = tensor.from_elements %mres_88 : tensor<i1>
      %mres_91, %out_qubit_92 = quantum.measure %out_qubits_19#1 : i1, !quantum.bit
      %from_elements_93 = tensor.from_elements %mres_91 : tensor<i1>
      %mres_94, %out_qubit_95 = quantum.measure %out_qubits_20#1 : i1, !quantum.bit
      %from_elements_96 = tensor.from_elements %mres_94 : tensor<i1>
      %mres_97, %out_qubit_98 = quantum.measure %out_qubits_21#1 : i1, !quantum.bit
      %from_elements_99 = tensor.from_elements %mres_97 : tensor<i1>
      %mres_100, %out_qubit_101 = quantum.measure %out_qubits_22#1 : i1, !quantum.bit
      %from_elements_102 = tensor.from_elements %mres_100 : tensor<i1>
      %mres_103, %out_qubit_104 = quantum.measure %out_qubits_23#1 : i1, !quantum.bit
      %from_elements_105 = tensor.from_elements %mres_103 : tensor<i1>
      %mres_106, %out_qubit_107 = quantum.measure %out_qubits_24#1 : i1, !quantum.bit
      %from_elements_108 = tensor.from_elements %mres_106 : tensor<i1>
      %mres_109, %out_qubit_110 = quantum.measure %out_qubits_25#1 : i1, !quantum.bit
      %from_elements_111 = tensor.from_elements %mres_109 : tensor<i1>
      %mres_112, %out_qubit_113 = quantum.measure %out_qubits_26#1 : i1, !quantum.bit
      %from_elements_114 = tensor.from_elements %mres_112 : tensor<i1>
      %mres_115, %out_qubit_116 = quantum.measure %out_qubits_27#1 : i1, !quantum.bit
      %from_elements_117 = tensor.from_elements %mres_115 : tensor<i1>
      %mres_118, %out_qubit_119 = quantum.measure %out_qubits_28#1 : i1, !quantum.bit
      %from_elements_120 = tensor.from_elements %mres_118 : tensor<i1>
      %mres_121, %out_qubit_122 = quantum.measure %out_qubits_29#1 : i1, !quantum.bit
      %from_elements_123 = tensor.from_elements %mres_121 : tensor<i1>
      %mres_124, %out_qubit_125 = quantum.measure %out_qubits_30#1 : i1, !quantum.bit
      %from_elements_126 = tensor.from_elements %mres_124 : tensor<i1>
      %mres_127, %out_qubit_128 = quantum.measure %out_qubits_31#1 : i1, !quantum.bit
      %from_elements_129 = tensor.from_elements %mres_127 : tensor<i1>
      %mres_130, %out_qubit_131 = quantum.measure %out_qubits_32#1 : i1, !quantum.bit
      %from_elements_132 = tensor.from_elements %mres_130 : tensor<i1>
      %mres_133, %out_qubit_134 = quantum.measure %out_qubits_33#1 : i1, !quantum.bit
      %from_elements_135 = tensor.from_elements %mres_133 : tensor<i1>
      %36 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %37 = quantum.insert %36[ 1], %out_qubit_35 : !quantum.reg, !quantum.bit
      %38 = quantum.insert %37[ 2], %out_qubit_38 : !quantum.reg, !quantum.bit
      %39 = quantum.insert %38[ 3], %out_qubit_41 : !quantum.reg, !quantum.bit
      %40 = quantum.insert %39[ 4], %out_qubit_44 : !quantum.reg, !quantum.bit
      %41 = quantum.insert %40[ 5], %out_qubit_47 : !quantum.reg, !quantum.bit
      %42 = quantum.insert %41[ 6], %out_qubit_50 : !quantum.reg, !quantum.bit
      %43 = quantum.insert %42[ 7], %out_qubit_53 : !quantum.reg, !quantum.bit
      %44 = quantum.insert %43[ 8], %out_qubit_56 : !quantum.reg, !quantum.bit
      %45 = quantum.insert %44[ 9], %out_qubit_59 : !quantum.reg, !quantum.bit
      %46 = quantum.insert %45[ 10], %out_qubit_62 : !quantum.reg, !quantum.bit
      %47 = quantum.insert %46[ 11], %out_qubit_65 : !quantum.reg, !quantum.bit
      %48 = quantum.insert %47[ 12], %out_qubit_68 : !quantum.reg, !quantum.bit
      %49 = quantum.insert %48[ 13], %out_qubit_71 : !quantum.reg, !quantum.bit
      %50 = quantum.insert %49[ 14], %out_qubit_74 : !quantum.reg, !quantum.bit
      %51 = quantum.insert %50[ 15], %out_qubit_77 : !quantum.reg, !quantum.bit
      %52 = quantum.insert %51[ 16], %out_qubit_80 : !quantum.reg, !quantum.bit
      %53 = quantum.insert %52[ 17], %out_qubit_83 : !quantum.reg, !quantum.bit
      %54 = quantum.insert %53[ 18], %out_qubit_86 : !quantum.reg, !quantum.bit
      %55 = quantum.insert %54[ 19], %out_qubit_89 : !quantum.reg, !quantum.bit
      %56 = quantum.insert %55[ 20], %out_qubit_92 : !quantum.reg, !quantum.bit
      %57 = quantum.insert %56[ 21], %out_qubit_95 : !quantum.reg, !quantum.bit
      %58 = quantum.insert %57[ 22], %out_qubit_98 : !quantum.reg, !quantum.bit
      %59 = quantum.insert %58[ 23], %out_qubit_101 : !quantum.reg, !quantum.bit
      %60 = quantum.insert %59[ 24], %out_qubit_104 : !quantum.reg, !quantum.bit
      %61 = quantum.insert %60[ 25], %out_qubit_107 : !quantum.reg, !quantum.bit
      %62 = quantum.insert %61[ 26], %out_qubit_110 : !quantum.reg, !quantum.bit
      %63 = quantum.insert %62[ 27], %out_qubit_113 : !quantum.reg, !quantum.bit
      %64 = quantum.insert %63[ 28], %out_qubit_116 : !quantum.reg, !quantum.bit
      %65 = quantum.insert %64[ 29], %out_qubit_119 : !quantum.reg, !quantum.bit
      %66 = quantum.insert %65[ 30], %out_qubit_122 : !quantum.reg, !quantum.bit
      %67 = quantum.insert %66[ 31], %out_qubit_125 : !quantum.reg, !quantum.bit
      %68 = quantum.insert %67[ 32], %out_qubit_128 : !quantum.reg, !quantum.bit
      %69 = quantum.insert %68[ 33], %out_qubit_131 : !quantum.reg, !quantum.bit
      %70 = quantum.insert %69[ 34], %out_qubit_134 : !quantum.reg, !quantum.bit
      quantum.dealloc %70 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_36, %from_elements_39, %from_elements_42, %from_elements_45, %from_elements_48, %from_elements_51, %from_elements_54, %from_elements_57, %from_elements_60, %from_elements_63, %from_elements_66, %from_elements_69, %from_elements_72, %from_elements_75, %from_elements_78, %from_elements_81, %from_elements_84, %from_elements_87, %from_elements_90, %from_elements_93, %from_elements_96, %from_elements_99, %from_elements_102, %from_elements_105, %from_elements_108, %from_elements_111, %from_elements_114, %from_elements_117, %from_elements_120, %from_elements_123, %from_elements_126, %from_elements_129, %from_elements_132, %from_elements_135 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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