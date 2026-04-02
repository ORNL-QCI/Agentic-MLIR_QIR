module @run_ghz {
  func.func public @jit_run_ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {llvm.emit_c_interface} {
    %0:45 = catalyst.launch_kernel @module_ghz::@ghz() : () -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>)
    return %0#0, %0#1, %0#2, %0#3, %0#4, %0#5, %0#6, %0#7, %0#8, %0#9, %0#10, %0#11, %0#12, %0#13, %0#14, %0#15, %0#16, %0#17, %0#18, %0#19, %0#20, %0#21, %0#22, %0#23, %0#24, %0#25, %0#26, %0#27, %0#28, %0#29, %0#30, %0#31, %0#32, %0#33, %0#34, %0#35, %0#36, %0#37, %0#38, %0#39, %0#40, %0#41, %0#42, %0#43, %0#44 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
  }
  module @module_ghz {
    module attributes {transform.with_named_sequence} {
      transform.named_sequence @__transform_main(%arg0: !transform.op<"builtin.module">) {
        transform.yield 
      }
    }
    func.func public @ghz() -> (tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>) attributes {diff_method = "parameter-shift", llvm.linkage = #llvm.linkage<internal>, qnode} {
      %c0_i64 = arith.constant 0 : i64
      quantum.device shots(%c0_i64) ["/home/kew/.venv/lib/python3.10/site-packages/pennylane_lightning/liblightning_qubit_catalyst.so", "LightningSimulator", "{'mcmc': False, 'num_burnin': 0, 'kernel_name': None}"]
      %0 = quantum.alloc( 45) : !quantum.reg
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
      %41 = quantum.extract %0[ 40] : !quantum.reg -> !quantum.bit
      %out_qubits_39:2 = quantum.custom "CNOT"() %out_qubits_38#0, %41 : !quantum.bit, !quantum.bit
      %42 = quantum.extract %0[ 41] : !quantum.reg -> !quantum.bit
      %out_qubits_40:2 = quantum.custom "CNOT"() %out_qubits_39#0, %42 : !quantum.bit, !quantum.bit
      %43 = quantum.extract %0[ 42] : !quantum.reg -> !quantum.bit
      %out_qubits_41:2 = quantum.custom "CNOT"() %out_qubits_40#0, %43 : !quantum.bit, !quantum.bit
      %44 = quantum.extract %0[ 43] : !quantum.reg -> !quantum.bit
      %out_qubits_42:2 = quantum.custom "CNOT"() %out_qubits_41#0, %44 : !quantum.bit, !quantum.bit
      %45 = quantum.extract %0[ 44] : !quantum.reg -> !quantum.bit
      %out_qubits_43:2 = quantum.custom "CNOT"() %out_qubits_42#0, %45 : !quantum.bit, !quantum.bit
      %mres, %out_qubit = quantum.measure %out_qubits_43#0 : i1, !quantum.bit
      %from_elements = tensor.from_elements %mres : tensor<i1>
      %mres_44, %out_qubit_45 = quantum.measure %out_qubits_0#1 : i1, !quantum.bit
      %from_elements_46 = tensor.from_elements %mres_44 : tensor<i1>
      %mres_47, %out_qubit_48 = quantum.measure %out_qubits_1#1 : i1, !quantum.bit
      %from_elements_49 = tensor.from_elements %mres_47 : tensor<i1>
      %mres_50, %out_qubit_51 = quantum.measure %out_qubits_2#1 : i1, !quantum.bit
      %from_elements_52 = tensor.from_elements %mres_50 : tensor<i1>
      %mres_53, %out_qubit_54 = quantum.measure %out_qubits_3#1 : i1, !quantum.bit
      %from_elements_55 = tensor.from_elements %mres_53 : tensor<i1>
      %mres_56, %out_qubit_57 = quantum.measure %out_qubits_4#1 : i1, !quantum.bit
      %from_elements_58 = tensor.from_elements %mres_56 : tensor<i1>
      %mres_59, %out_qubit_60 = quantum.measure %out_qubits_5#1 : i1, !quantum.bit
      %from_elements_61 = tensor.from_elements %mres_59 : tensor<i1>
      %mres_62, %out_qubit_63 = quantum.measure %out_qubits_6#1 : i1, !quantum.bit
      %from_elements_64 = tensor.from_elements %mres_62 : tensor<i1>
      %mres_65, %out_qubit_66 = quantum.measure %out_qubits_7#1 : i1, !quantum.bit
      %from_elements_67 = tensor.from_elements %mres_65 : tensor<i1>
      %mres_68, %out_qubit_69 = quantum.measure %out_qubits_8#1 : i1, !quantum.bit
      %from_elements_70 = tensor.from_elements %mres_68 : tensor<i1>
      %mres_71, %out_qubit_72 = quantum.measure %out_qubits_9#1 : i1, !quantum.bit
      %from_elements_73 = tensor.from_elements %mres_71 : tensor<i1>
      %mres_74, %out_qubit_75 = quantum.measure %out_qubits_10#1 : i1, !quantum.bit
      %from_elements_76 = tensor.from_elements %mres_74 : tensor<i1>
      %mres_77, %out_qubit_78 = quantum.measure %out_qubits_11#1 : i1, !quantum.bit
      %from_elements_79 = tensor.from_elements %mres_77 : tensor<i1>
      %mres_80, %out_qubit_81 = quantum.measure %out_qubits_12#1 : i1, !quantum.bit
      %from_elements_82 = tensor.from_elements %mres_80 : tensor<i1>
      %mres_83, %out_qubit_84 = quantum.measure %out_qubits_13#1 : i1, !quantum.bit
      %from_elements_85 = tensor.from_elements %mres_83 : tensor<i1>
      %mres_86, %out_qubit_87 = quantum.measure %out_qubits_14#1 : i1, !quantum.bit
      %from_elements_88 = tensor.from_elements %mres_86 : tensor<i1>
      %mres_89, %out_qubit_90 = quantum.measure %out_qubits_15#1 : i1, !quantum.bit
      %from_elements_91 = tensor.from_elements %mres_89 : tensor<i1>
      %mres_92, %out_qubit_93 = quantum.measure %out_qubits_16#1 : i1, !quantum.bit
      %from_elements_94 = tensor.from_elements %mres_92 : tensor<i1>
      %mres_95, %out_qubit_96 = quantum.measure %out_qubits_17#1 : i1, !quantum.bit
      %from_elements_97 = tensor.from_elements %mres_95 : tensor<i1>
      %mres_98, %out_qubit_99 = quantum.measure %out_qubits_18#1 : i1, !quantum.bit
      %from_elements_100 = tensor.from_elements %mres_98 : tensor<i1>
      %mres_101, %out_qubit_102 = quantum.measure %out_qubits_19#1 : i1, !quantum.bit
      %from_elements_103 = tensor.from_elements %mres_101 : tensor<i1>
      %mres_104, %out_qubit_105 = quantum.measure %out_qubits_20#1 : i1, !quantum.bit
      %from_elements_106 = tensor.from_elements %mres_104 : tensor<i1>
      %mres_107, %out_qubit_108 = quantum.measure %out_qubits_21#1 : i1, !quantum.bit
      %from_elements_109 = tensor.from_elements %mres_107 : tensor<i1>
      %mres_110, %out_qubit_111 = quantum.measure %out_qubits_22#1 : i1, !quantum.bit
      %from_elements_112 = tensor.from_elements %mres_110 : tensor<i1>
      %mres_113, %out_qubit_114 = quantum.measure %out_qubits_23#1 : i1, !quantum.bit
      %from_elements_115 = tensor.from_elements %mres_113 : tensor<i1>
      %mres_116, %out_qubit_117 = quantum.measure %out_qubits_24#1 : i1, !quantum.bit
      %from_elements_118 = tensor.from_elements %mres_116 : tensor<i1>
      %mres_119, %out_qubit_120 = quantum.measure %out_qubits_25#1 : i1, !quantum.bit
      %from_elements_121 = tensor.from_elements %mres_119 : tensor<i1>
      %mres_122, %out_qubit_123 = quantum.measure %out_qubits_26#1 : i1, !quantum.bit
      %from_elements_124 = tensor.from_elements %mres_122 : tensor<i1>
      %mres_125, %out_qubit_126 = quantum.measure %out_qubits_27#1 : i1, !quantum.bit
      %from_elements_127 = tensor.from_elements %mres_125 : tensor<i1>
      %mres_128, %out_qubit_129 = quantum.measure %out_qubits_28#1 : i1, !quantum.bit
      %from_elements_130 = tensor.from_elements %mres_128 : tensor<i1>
      %mres_131, %out_qubit_132 = quantum.measure %out_qubits_29#1 : i1, !quantum.bit
      %from_elements_133 = tensor.from_elements %mres_131 : tensor<i1>
      %mres_134, %out_qubit_135 = quantum.measure %out_qubits_30#1 : i1, !quantum.bit
      %from_elements_136 = tensor.from_elements %mres_134 : tensor<i1>
      %mres_137, %out_qubit_138 = quantum.measure %out_qubits_31#1 : i1, !quantum.bit
      %from_elements_139 = tensor.from_elements %mres_137 : tensor<i1>
      %mres_140, %out_qubit_141 = quantum.measure %out_qubits_32#1 : i1, !quantum.bit
      %from_elements_142 = tensor.from_elements %mres_140 : tensor<i1>
      %mres_143, %out_qubit_144 = quantum.measure %out_qubits_33#1 : i1, !quantum.bit
      %from_elements_145 = tensor.from_elements %mres_143 : tensor<i1>
      %mres_146, %out_qubit_147 = quantum.measure %out_qubits_34#1 : i1, !quantum.bit
      %from_elements_148 = tensor.from_elements %mres_146 : tensor<i1>
      %mres_149, %out_qubit_150 = quantum.measure %out_qubits_35#1 : i1, !quantum.bit
      %from_elements_151 = tensor.from_elements %mres_149 : tensor<i1>
      %mres_152, %out_qubit_153 = quantum.measure %out_qubits_36#1 : i1, !quantum.bit
      %from_elements_154 = tensor.from_elements %mres_152 : tensor<i1>
      %mres_155, %out_qubit_156 = quantum.measure %out_qubits_37#1 : i1, !quantum.bit
      %from_elements_157 = tensor.from_elements %mres_155 : tensor<i1>
      %mres_158, %out_qubit_159 = quantum.measure %out_qubits_38#1 : i1, !quantum.bit
      %from_elements_160 = tensor.from_elements %mres_158 : tensor<i1>
      %mres_161, %out_qubit_162 = quantum.measure %out_qubits_39#1 : i1, !quantum.bit
      %from_elements_163 = tensor.from_elements %mres_161 : tensor<i1>
      %mres_164, %out_qubit_165 = quantum.measure %out_qubits_40#1 : i1, !quantum.bit
      %from_elements_166 = tensor.from_elements %mres_164 : tensor<i1>
      %mres_167, %out_qubit_168 = quantum.measure %out_qubits_41#1 : i1, !quantum.bit
      %from_elements_169 = tensor.from_elements %mres_167 : tensor<i1>
      %mres_170, %out_qubit_171 = quantum.measure %out_qubits_42#1 : i1, !quantum.bit
      %from_elements_172 = tensor.from_elements %mres_170 : tensor<i1>
      %mres_173, %out_qubit_174 = quantum.measure %out_qubits_43#1 : i1, !quantum.bit
      %from_elements_175 = tensor.from_elements %mres_173 : tensor<i1>
      %46 = quantum.insert %0[ 0], %out_qubit : !quantum.reg, !quantum.bit
      %47 = quantum.insert %46[ 1], %out_qubit_45 : !quantum.reg, !quantum.bit
      %48 = quantum.insert %47[ 2], %out_qubit_48 : !quantum.reg, !quantum.bit
      %49 = quantum.insert %48[ 3], %out_qubit_51 : !quantum.reg, !quantum.bit
      %50 = quantum.insert %49[ 4], %out_qubit_54 : !quantum.reg, !quantum.bit
      %51 = quantum.insert %50[ 5], %out_qubit_57 : !quantum.reg, !quantum.bit
      %52 = quantum.insert %51[ 6], %out_qubit_60 : !quantum.reg, !quantum.bit
      %53 = quantum.insert %52[ 7], %out_qubit_63 : !quantum.reg, !quantum.bit
      %54 = quantum.insert %53[ 8], %out_qubit_66 : !quantum.reg, !quantum.bit
      %55 = quantum.insert %54[ 9], %out_qubit_69 : !quantum.reg, !quantum.bit
      %56 = quantum.insert %55[ 10], %out_qubit_72 : !quantum.reg, !quantum.bit
      %57 = quantum.insert %56[ 11], %out_qubit_75 : !quantum.reg, !quantum.bit
      %58 = quantum.insert %57[ 12], %out_qubit_78 : !quantum.reg, !quantum.bit
      %59 = quantum.insert %58[ 13], %out_qubit_81 : !quantum.reg, !quantum.bit
      %60 = quantum.insert %59[ 14], %out_qubit_84 : !quantum.reg, !quantum.bit
      %61 = quantum.insert %60[ 15], %out_qubit_87 : !quantum.reg, !quantum.bit
      %62 = quantum.insert %61[ 16], %out_qubit_90 : !quantum.reg, !quantum.bit
      %63 = quantum.insert %62[ 17], %out_qubit_93 : !quantum.reg, !quantum.bit
      %64 = quantum.insert %63[ 18], %out_qubit_96 : !quantum.reg, !quantum.bit
      %65 = quantum.insert %64[ 19], %out_qubit_99 : !quantum.reg, !quantum.bit
      %66 = quantum.insert %65[ 20], %out_qubit_102 : !quantum.reg, !quantum.bit
      %67 = quantum.insert %66[ 21], %out_qubit_105 : !quantum.reg, !quantum.bit
      %68 = quantum.insert %67[ 22], %out_qubit_108 : !quantum.reg, !quantum.bit
      %69 = quantum.insert %68[ 23], %out_qubit_111 : !quantum.reg, !quantum.bit
      %70 = quantum.insert %69[ 24], %out_qubit_114 : !quantum.reg, !quantum.bit
      %71 = quantum.insert %70[ 25], %out_qubit_117 : !quantum.reg, !quantum.bit
      %72 = quantum.insert %71[ 26], %out_qubit_120 : !quantum.reg, !quantum.bit
      %73 = quantum.insert %72[ 27], %out_qubit_123 : !quantum.reg, !quantum.bit
      %74 = quantum.insert %73[ 28], %out_qubit_126 : !quantum.reg, !quantum.bit
      %75 = quantum.insert %74[ 29], %out_qubit_129 : !quantum.reg, !quantum.bit
      %76 = quantum.insert %75[ 30], %out_qubit_132 : !quantum.reg, !quantum.bit
      %77 = quantum.insert %76[ 31], %out_qubit_135 : !quantum.reg, !quantum.bit
      %78 = quantum.insert %77[ 32], %out_qubit_138 : !quantum.reg, !quantum.bit
      %79 = quantum.insert %78[ 33], %out_qubit_141 : !quantum.reg, !quantum.bit
      %80 = quantum.insert %79[ 34], %out_qubit_144 : !quantum.reg, !quantum.bit
      %81 = quantum.insert %80[ 35], %out_qubit_147 : !quantum.reg, !quantum.bit
      %82 = quantum.insert %81[ 36], %out_qubit_150 : !quantum.reg, !quantum.bit
      %83 = quantum.insert %82[ 37], %out_qubit_153 : !quantum.reg, !quantum.bit
      %84 = quantum.insert %83[ 38], %out_qubit_156 : !quantum.reg, !quantum.bit
      %85 = quantum.insert %84[ 39], %out_qubit_159 : !quantum.reg, !quantum.bit
      %86 = quantum.insert %85[ 40], %out_qubit_162 : !quantum.reg, !quantum.bit
      %87 = quantum.insert %86[ 41], %out_qubit_165 : !quantum.reg, !quantum.bit
      %88 = quantum.insert %87[ 42], %out_qubit_168 : !quantum.reg, !quantum.bit
      %89 = quantum.insert %88[ 43], %out_qubit_171 : !quantum.reg, !quantum.bit
      %90 = quantum.insert %89[ 44], %out_qubit_174 : !quantum.reg, !quantum.bit
      quantum.dealloc %90 : !quantum.reg
      quantum.device_release
      return %from_elements, %from_elements_46, %from_elements_49, %from_elements_52, %from_elements_55, %from_elements_58, %from_elements_61, %from_elements_64, %from_elements_67, %from_elements_70, %from_elements_73, %from_elements_76, %from_elements_79, %from_elements_82, %from_elements_85, %from_elements_88, %from_elements_91, %from_elements_94, %from_elements_97, %from_elements_100, %from_elements_103, %from_elements_106, %from_elements_109, %from_elements_112, %from_elements_115, %from_elements_118, %from_elements_121, %from_elements_124, %from_elements_127, %from_elements_130, %from_elements_133, %from_elements_136, %from_elements_139, %from_elements_142, %from_elements_145, %from_elements_148, %from_elements_151, %from_elements_154, %from_elements_157, %from_elements_160, %from_elements_163, %from_elements_166, %from_elements_169, %from_elements_172, %from_elements_175 : tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>, tensor<i1>
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