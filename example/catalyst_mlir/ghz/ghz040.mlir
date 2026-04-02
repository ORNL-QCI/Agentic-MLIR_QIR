module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:40 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19, %0#20, %0#21, %0#22, %0#23, %0#24, %0#25, %0#26, %0#27, %0#28, %0#29, %0#30, %0#31, %0#32, %0#33, %0#34, %0#35, %0#36, %0#37, %0#38, %0#39 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/.venv/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 40) : !quantum.reg
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
      %36 = quantum.extract %0[ 35] : !quantum.reg -> !quantum.bit
      %out_qubits_34:2 = quantum.custom "CNOT"() %out_qubits_33#0, %36 : !quantum.bit, !quantum.bit
      %37 = quantum.extract %0[ 36] : !quantum.reg -> !quantum.bit
      %out_qubits_35:2 = quantum.custom "CNOT"() %out_qubits_34#0, %37 : !quantum.bit, !quantum.bit
      %38 = quantum.extract %0[ 37] : !quantum.reg -> !quantum.bit
      %out_qubits_36:2 = quantum.custom "CNOT"() %out_qubits_35#0, %38 : !quantum.bit, !quantum.bit
      %39 = quantum.extract %0[ 38] : !quantum.reg -> !quantum.bit
      %out_qubits_37:2 = quantum.custom "CNOT"() %out_qubits_36#0, %39 : !quantum.bit, !quantum.bit
      %40 = quantum.extract %0[ 39] : !quantum.reg -> !quantum.bit
      %out_qubits_38:2 = quantum.custom "CNOT"() %out_qubits_37#0, %40 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_38#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_39, %out_qubit_40 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_41 = tensor.from_elements %mres_39 : tensor<i1>
      %mres_42, %out_qubit_43 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_44 = tensor.from_elements %mres_42 : tensor<i1>
      %mres_45, %out_qubit_46 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_47 = tensor.from_elements %mres_45 : tensor<i1>
      %mres_48, %out_qubit_49 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_50 = tensor.from_elements %mres_48 : tensor<i1>
      %mres_51, %out_qubit_52 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_53 = tensor.from_elements %mres_51 : tensor<i1>
      %mres_54, %out_qubit_55 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_56 = tensor.from_elements %mres_54 : tensor<i1>
      %mres_57, %out_qubit_58 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_59 = tensor.from_elements %mres_57 : tensor<i1>
      %mres_60, %out_qubit_61 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_62 = tensor.from_elements %mres_60 : tensor<i1>
      %mres_63, %out_qubit_64 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_65 = tensor.from_elements %mres_63 : tensor<i1>
      %mres_66, %out_qubit_67 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_68 = tensor.from_elements %mres_66 : tensor<i1>
      %mres_69, %out_qubit_70 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_71 = tensor.from_elements %mres_69 : tensor<i1>
      %mres_72, %out_qubit_73 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_74 = tensor.from_elements %mres_72 : tensor<i1>
      %mres_75, %out_qubit_76 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_77 = tensor.from_elements %mres_75 : tensor<i1>
      %mres_78, %out_qubit_79 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_80 = tensor.from_elements %mres_78 : tensor<i1>
      %mres_81, %out_qubit_82 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_83 = tensor.from_elements %mres_81 : tensor<i1>
      %mres_84, %out_qubit_85 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_86 = tensor.from_elements %mres_84 : tensor<i1>
      %mres_87, %out_qubit_88 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_89 = tensor.from_elements %mres_87 : tensor<i1>
      %mres_90, %out_qubit_91 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_92 = tensor.from_elements %mres_90 : tensor<i1>
      %mres_93, %out_qubit_94 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_95 = tensor.from_elements %mres_93 : tensor<i1>
      %mres_96, %out_qubit_97 = quantum.measure %out_qubits_19#1 : i1, !quantum.bit
      %from_elements_98 = tensor.from_elements %mres_96 : tensor<i1>
      %mres_99, %out_qubit_100 = quantum.measure %out_qubits_20#1 : i1, !quantum.bit
      %from_elements_101 = tensor.from_elements %mres_99 : tensor<i1>
      %mres_102, %out_qubit_103 = quantum.measure %out_qubits_21#1 : i1, !quantum.bit
      %from_elements_104 = tensor.from_elements %mres_102 : tensor<i1>
      %mres_105, %out_qubit_106 = quantum.measure %out_qubits_22#1 : i1, !quantum.bit
      %from_elements_107 = tensor.from_elements %mres_105 : tensor<i1>
      %mres_108, %out_qubit_109 = quantum.measure %out_qubits_23#1 : i1, !quantum.bit
      %from_elements_110 = tensor.from_elements %mres_108 : tensor<i1>
      %mres_111, %out_qubit_112 = quantum.measure %out_qubits_24#1 : i1, !quantum.bit
      %from_elements_113 = tensor.from_elements %mres_111 : tensor<i1>
      %mres_114, %out_qubit_115 = quantum.measure %out_qubits_25#1 : i1, !quantum.bit
      %from_elements_116 = tensor.from_elements %mres_114 : tensor<i1>
      %mres_117, %out_qubit_118 = quantum.measure %out_qubits_26#1 : i1, !quantum.bit
      %from_elements_119 = tensor.from_elements %mres_117 : tensor<i1>
      %mres_120, %out_qubit_121 = quantum.measure %out_qubits_27#1 : i1, !quantum.bit
      %from_elements_122 = tensor.from_elements %mres_120 : tensor<i1>
      %mres_123, %out_qubit_124 = quantum.measure %out_qubits_28#1 : i1, !quantum.bit
      %from_elements_125 = tensor.from_elements %mres_123 : tensor<i1>
      %mres_126, %out_qubit_127 = quantum.measure %out_qubits_29#1 : i1, !quantum.bit
      %from_elements_128 = tensor.from_elements %mres_126 : tensor<i1>
      %mres_129, %out_qubit_130 = quantum.measure %out_qubits_30#1 : i1, !quantum.bit
      %from_elements_131 = tensor.from_elements %mres_129 : tensor<i1>
      %mres_132, %out_qubit_133 = quantum.measure %out_qubits_31#1 : i1, !quantum.bit
      %from_elements_134 = tensor.from_elements %mres_132 : tensor<i1>
      %mres_135, %out_qubit_136 = quantum.measure %out_qubits_32#1 : i1, !quantum.bit
      %from_elements_137 = tensor.from_elements %mres_135 : tensor<i1>
      %mres_138, %out_qubit_139 = quantum.measure %out_qubits_33#1 : i1, !quantum.bit
      %from_elements_140 = tensor.from_elements %mres_138 : tensor<i1>
      %mres_141, %out_qubit_142 = quantum.measure %out_qubits_34#1 : i1, !quantum.bit
      %from_elements_143 = tensor.from_elements %mres_141 : tensor<i1>
      %mres_144, %out_qubit_145 = quantum.measure %out_qubits_35#1 : i1, !quantum.bit
      %from_elements_146 = tensor.from_elements %mres_144 : tensor<i1>
      %mres_147, %out_qubit_148 = quantum.measure %out_qubits_36#1 : i1, !quantum.bit
      %from_elements_149 = tensor.from_elements %mres_147 : tensor<i1>
      %mres_150, %out_qubit_151 = quantum.measure %out_qubits_37#1 : i1, !quantum.bit
      %from_elements_152 = tensor.from_elements %mres_150 : tensor<i1>
      %mres_153, %out_qubit_154 = quantum.measure %out_qubits_38#1 : i1, !quantum.bit
      %from_elements_155 = tensor.from_elements %mres_153 : tensor<i1>
      %41 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %42 = quantum.insert %41[ 1], %out_qubit_40 : !quantum.reg, !quantum.bit
      %43 = quantum.insert %42[ 2], %out_qubit_43 : !quantum.reg, !quantum.bit
      %44 = quantum.insert %43[ 3], %out_qubit_46 : !quantum.reg, !quantum.bit
      %45 = quantum.insert %44[ 4], %out_qubit_49 : !quantum.reg, !quantum.bit
      %46 = quantum.insert %45[ 5], %out_qubit_52 : !quantum.reg, !quantum.bit
      %47 = quantum.insert %46[ 6], %out_qubit_55 : !quantum.reg, !quantum.bit
      %48 = quantum.insert %47[ 7], %out_qubit_58 : !quantum.reg, !quantum.bit
      %49 = quantum.insert %48[ 8], %out_qubit_61 : !quantum.reg, !quantum.bit
      %50 = quantum.insert %49[ 9], %out_qubit_64 : !quantum.reg, !quantum.bit
      %51 = quantum.insert %50[ 10], %out_qubit_67 : !quantum.reg, !quantum.bit
      %52 = quantum.insert %51[ 11], %out_qubit_70 : !quantum.reg, !quantum.bit
      %53 = quantum.insert %52[ 12], %out_qubit_73 : !quantum.reg, !quantum.bit
      %54 = quantum.insert %53[ 13], %out_qubit_76 : !quantum.reg, !quantum.bit
      %55 = quantum.insert %54[ 14], %out_qubit_79 : !quantum.reg, !quantum.bit
      %56 = quantum.insert %55[ 15], %out_qubit_82 : !quantum.reg, !quantum.bit
      %57 = quantum.insert %56[ 16], %out_qubit_85 : !quantum.reg, !quantum.bit
      %58 = quantum.insert %57[ 17], %out_qubit_88 : !quantum.reg, !quantum.bit
      %59 = quantum.insert %58[ 18], %out_qubit_91 : !quantum.reg, !quantum.bit
      %60 = quantum.insert %59[ 19], %out_qubit_94 : !quantum.reg, !quantum.bit
      %61 = quantum.insert %60[ 20], %out_qubit_97 : !quantum.reg, !quantum.bit
      %62 = quantum.insert %61[ 21], %out_qubit_100 : !quantum.reg, !quantum.bit
      %63 = quantum.insert %62[ 22], %out_qubit_103 : !quantum.reg, !quantum.bit
      %64 = quantum.insert %63[ 23], %out_qubit_106 : !quantum.reg, !quantum.bit
      %65 = quantum.insert %64[ 24], %out_qubit_109 : !quantum.reg, !quantum.bit
      %66 = quantum.insert %65[ 25], %out_qubit_112 : !quantum.reg, !quantum.bit
      %67 = quantum.insert %66[ 26], %out_qubit_115 : !quantum.reg, !quantum.bit
      %68 = quantum.insert %67[ 27], %out_qubit_118 : !quantum.reg, !quantum.bit
      %69 = quantum.insert %68[ 28], %out_qubit_121 : !quantum.reg, !quantum.bit
      %70 = quantum.insert %69[ 29], %out_qubit_124 : !quantum.reg, !quantum.bit
      %71 = quantum.insert %70[ 30], %out_qubit_127 : !quantum.reg, !quantum.bit
      %72 = quantum.insert %71[ 31], %out_qubit_130 : !quantum.reg, !quantum.bit
      %73 = quantum.insert %72[ 32], %out_qubit_133 : !quantum.reg, !quantum.bit
      %74 = quantum.insert %73[ 33], %out_qubit_136 : !quantum.reg, !quantum.bit
      %75 = quantum.insert %74[ 34], %out_qubit_139 : !quantum.reg, !quantum.bit
      %76 = quantum.insert %75[ 35], %out_qubit_142 : !quantum.reg, !quantum.bit
      %77 = quantum.insert %76[ 36], %out_qubit_145 : !quantum.reg, !quantum.bit
      %78 = quantum.insert %77[ 37], %out_qubit_148 : !quantum.reg, !quantum.bit
      %79 = quantum.insert %78[ 38], %out_qubit_151 : !quantum.reg, !quantum.bit
      %80 = quantum.insert %79[ 39], %out_qubit_154 : !quantum.reg, !quantum.bit
      quantum.dealloc %80 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_41, %from_elements_44, %from_elements_47, %from_elements_50, %from_elements_53, %from_elements_56, %from_elements_59, %from_elements_62, %from_elements_65, %from_elements_68, %from_elements_71, %from_elements_74, %from_elements_77, %from_elements_80, %from_elements_83, %from_elements_86, %from_elements_89, %from_elements_92, %from_elements_95, %from_elements_98, %from_elements_101, %from_elements_104, %from_elements_107, %from_elements_110, %from_elements_113, %from_elements_116, %from_elements_119, %from_elements_122, %from_elements_125, %from_elements_128, %from_elements_131, %from_elements_134, %from_elements_137, %from_elements_140, %from_elements_143, %from_elements_146, %from_elements_149, %from_elements_152, %from_elements_155 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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