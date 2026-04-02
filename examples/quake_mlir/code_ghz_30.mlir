module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_Z8UEQ41492 = "__nvqpp__mlirgen____nvqppBuilderKernel_Z8UEQ41492_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_Z8UEQ41492() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<30>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<30>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<30>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<30>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<30>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<30>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<30>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<30>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<30>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<30>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<30>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<30>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<30>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<30>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<30>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<30>, i64) -> !quake.ref
    %c15_i64 = arith.constant 15 : i64
    %31 = quake.extract_ref %0[%c15_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%30] %31 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_15 = arith.constant 0 : i64
    %32 = quake.extract_ref %0[%c0_i64_15] : (!quake.veq<30>, i64) -> !quake.ref
    %c16_i64 = arith.constant 16 : i64
    %33 = quake.extract_ref %0[%c16_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%32] %33 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_16 = arith.constant 0 : i64
    %34 = quake.extract_ref %0[%c0_i64_16] : (!quake.veq<30>, i64) -> !quake.ref
    %c17_i64 = arith.constant 17 : i64
    %35 = quake.extract_ref %0[%c17_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%34] %35 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_17 = arith.constant 0 : i64
    %36 = quake.extract_ref %0[%c0_i64_17] : (!quake.veq<30>, i64) -> !quake.ref
    %c18_i64 = arith.constant 18 : i64
    %37 = quake.extract_ref %0[%c18_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%36] %37 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_18 = arith.constant 0 : i64
    %38 = quake.extract_ref %0[%c0_i64_18] : (!quake.veq<30>, i64) -> !quake.ref
    %c19_i64 = arith.constant 19 : i64
    %39 = quake.extract_ref %0[%c19_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%38] %39 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_19 = arith.constant 0 : i64
    %40 = quake.extract_ref %0[%c0_i64_19] : (!quake.veq<30>, i64) -> !quake.ref
    %c20_i64 = arith.constant 20 : i64
    %41 = quake.extract_ref %0[%c20_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%40] %41 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_20 = arith.constant 0 : i64
    %42 = quake.extract_ref %0[%c0_i64_20] : (!quake.veq<30>, i64) -> !quake.ref
    %c21_i64 = arith.constant 21 : i64
    %43 = quake.extract_ref %0[%c21_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%42] %43 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_21 = arith.constant 0 : i64
    %44 = quake.extract_ref %0[%c0_i64_21] : (!quake.veq<30>, i64) -> !quake.ref
    %c22_i64 = arith.constant 22 : i64
    %45 = quake.extract_ref %0[%c22_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%44] %45 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_22 = arith.constant 0 : i64
    %46 = quake.extract_ref %0[%c0_i64_22] : (!quake.veq<30>, i64) -> !quake.ref
    %c23_i64 = arith.constant 23 : i64
    %47 = quake.extract_ref %0[%c23_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%46] %47 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_23 = arith.constant 0 : i64
    %48 = quake.extract_ref %0[%c0_i64_23] : (!quake.veq<30>, i64) -> !quake.ref
    %c24_i64 = arith.constant 24 : i64
    %49 = quake.extract_ref %0[%c24_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%48] %49 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_24 = arith.constant 0 : i64
    %50 = quake.extract_ref %0[%c0_i64_24] : (!quake.veq<30>, i64) -> !quake.ref
    %c25_i64 = arith.constant 25 : i64
    %51 = quake.extract_ref %0[%c25_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%50] %51 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_25 = arith.constant 0 : i64
    %52 = quake.extract_ref %0[%c0_i64_25] : (!quake.veq<30>, i64) -> !quake.ref
    %c26_i64 = arith.constant 26 : i64
    %53 = quake.extract_ref %0[%c26_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%52] %53 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_26 = arith.constant 0 : i64
    %54 = quake.extract_ref %0[%c0_i64_26] : (!quake.veq<30>, i64) -> !quake.ref
    %c27_i64 = arith.constant 27 : i64
    %55 = quake.extract_ref %0[%c27_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%54] %55 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_27 = arith.constant 0 : i64
    %56 = quake.extract_ref %0[%c0_i64_27] : (!quake.veq<30>, i64) -> !quake.ref
    %c28_i64 = arith.constant 28 : i64
    %57 = quake.extract_ref %0[%c28_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%56] %57 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_28 = arith.constant 0 : i64
    %58 = quake.extract_ref %0[%c0_i64_28] : (!quake.veq<30>, i64) -> !quake.ref
    %c29_i64 = arith.constant 29 : i64
    %59 = quake.extract_ref %0[%c29_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%58] %59 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_29 = arith.constant 0 : i64
    %60 = quake.extract_ref %0[%c0_i64_29] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut = quake.mz %60 : (!quake.ref) -> !quake.measure
    %61 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_30 = arith.constant 1 : i64
    %62 = quake.extract_ref %0[%c1_i64_30] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_31 = quake.mz %62 : (!quake.ref) -> !quake.measure
    %63 = quake.discriminate %measOut_31 : (!quake.measure) -> i1
    %c2_i64_32 = arith.constant 2 : i64
    %64 = quake.extract_ref %0[%c2_i64_32] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_33 = quake.mz %64 : (!quake.ref) -> !quake.measure
    %65 = quake.discriminate %measOut_33 : (!quake.measure) -> i1
    %c3_i64_34 = arith.constant 3 : i64
    %66 = quake.extract_ref %0[%c3_i64_34] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_35 = quake.mz %66 : (!quake.ref) -> !quake.measure
    %67 = quake.discriminate %measOut_35 : (!quake.measure) -> i1
    %c4_i64_36 = arith.constant 4 : i64
    %68 = quake.extract_ref %0[%c4_i64_36] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_37 = quake.mz %68 : (!quake.ref) -> !quake.measure
    %69 = quake.discriminate %measOut_37 : (!quake.measure) -> i1
    %c5_i64_38 = arith.constant 5 : i64
    %70 = quake.extract_ref %0[%c5_i64_38] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_39 = quake.mz %70 : (!quake.ref) -> !quake.measure
    %71 = quake.discriminate %measOut_39 : (!quake.measure) -> i1
    %c6_i64_40 = arith.constant 6 : i64
    %72 = quake.extract_ref %0[%c6_i64_40] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_41 = quake.mz %72 : (!quake.ref) -> !quake.measure
    %73 = quake.discriminate %measOut_41 : (!quake.measure) -> i1
    %c7_i64_42 = arith.constant 7 : i64
    %74 = quake.extract_ref %0[%c7_i64_42] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_43 = quake.mz %74 : (!quake.ref) -> !quake.measure
    %75 = quake.discriminate %measOut_43 : (!quake.measure) -> i1
    %c8_i64_44 = arith.constant 8 : i64
    %76 = quake.extract_ref %0[%c8_i64_44] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_45 = quake.mz %76 : (!quake.ref) -> !quake.measure
    %77 = quake.discriminate %measOut_45 : (!quake.measure) -> i1
    %c9_i64_46 = arith.constant 9 : i64
    %78 = quake.extract_ref %0[%c9_i64_46] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_47 = quake.mz %78 : (!quake.ref) -> !quake.measure
    %79 = quake.discriminate %measOut_47 : (!quake.measure) -> i1
    %c10_i64_48 = arith.constant 10 : i64
    %80 = quake.extract_ref %0[%c10_i64_48] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_49 = quake.mz %80 : (!quake.ref) -> !quake.measure
    %81 = quake.discriminate %measOut_49 : (!quake.measure) -> i1
    %c11_i64_50 = arith.constant 11 : i64
    %82 = quake.extract_ref %0[%c11_i64_50] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_51 = quake.mz %82 : (!quake.ref) -> !quake.measure
    %83 = quake.discriminate %measOut_51 : (!quake.measure) -> i1
    %c12_i64_52 = arith.constant 12 : i64
    %84 = quake.extract_ref %0[%c12_i64_52] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_53 = quake.mz %84 : (!quake.ref) -> !quake.measure
    %85 = quake.discriminate %measOut_53 : (!quake.measure) -> i1
    %c13_i64_54 = arith.constant 13 : i64
    %86 = quake.extract_ref %0[%c13_i64_54] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_55 = quake.mz %86 : (!quake.ref) -> !quake.measure
    %87 = quake.discriminate %measOut_55 : (!quake.measure) -> i1
    %c14_i64_56 = arith.constant 14 : i64
    %88 = quake.extract_ref %0[%c14_i64_56] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_57 = quake.mz %88 : (!quake.ref) -> !quake.measure
    %89 = quake.discriminate %measOut_57 : (!quake.measure) -> i1
    %c15_i64_58 = arith.constant 15 : i64
    %90 = quake.extract_ref %0[%c15_i64_58] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_59 = quake.mz %90 : (!quake.ref) -> !quake.measure
    %91 = quake.discriminate %measOut_59 : (!quake.measure) -> i1
    %c16_i64_60 = arith.constant 16 : i64
    %92 = quake.extract_ref %0[%c16_i64_60] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_61 = quake.mz %92 : (!quake.ref) -> !quake.measure
    %93 = quake.discriminate %measOut_61 : (!quake.measure) -> i1
    %c17_i64_62 = arith.constant 17 : i64
    %94 = quake.extract_ref %0[%c17_i64_62] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_63 = quake.mz %94 : (!quake.ref) -> !quake.measure
    %95 = quake.discriminate %measOut_63 : (!quake.measure) -> i1
    %c18_i64_64 = arith.constant 18 : i64
    %96 = quake.extract_ref %0[%c18_i64_64] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_65 = quake.mz %96 : (!quake.ref) -> !quake.measure
    %97 = quake.discriminate %measOut_65 : (!quake.measure) -> i1
    %c19_i64_66 = arith.constant 19 : i64
    %98 = quake.extract_ref %0[%c19_i64_66] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_67 = quake.mz %98 : (!quake.ref) -> !quake.measure
    %99 = quake.discriminate %measOut_67 : (!quake.measure) -> i1
    %c20_i64_68 = arith.constant 20 : i64
    %100 = quake.extract_ref %0[%c20_i64_68] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_69 = quake.mz %100 : (!quake.ref) -> !quake.measure
    %101 = quake.discriminate %measOut_69 : (!quake.measure) -> i1
    %c21_i64_70 = arith.constant 21 : i64
    %102 = quake.extract_ref %0[%c21_i64_70] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_71 = quake.mz %102 : (!quake.ref) -> !quake.measure
    %103 = quake.discriminate %measOut_71 : (!quake.measure) -> i1
    %c22_i64_72 = arith.constant 22 : i64
    %104 = quake.extract_ref %0[%c22_i64_72] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_73 = quake.mz %104 : (!quake.ref) -> !quake.measure
    %105 = quake.discriminate %measOut_73 : (!quake.measure) -> i1
    %c23_i64_74 = arith.constant 23 : i64
    %106 = quake.extract_ref %0[%c23_i64_74] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_75 = quake.mz %106 : (!quake.ref) -> !quake.measure
    %107 = quake.discriminate %measOut_75 : (!quake.measure) -> i1
    %c24_i64_76 = arith.constant 24 : i64
    %108 = quake.extract_ref %0[%c24_i64_76] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_77 = quake.mz %108 : (!quake.ref) -> !quake.measure
    %109 = quake.discriminate %measOut_77 : (!quake.measure) -> i1
    %c25_i64_78 = arith.constant 25 : i64
    %110 = quake.extract_ref %0[%c25_i64_78] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_79 = quake.mz %110 : (!quake.ref) -> !quake.measure
    %111 = quake.discriminate %measOut_79 : (!quake.measure) -> i1
    %c26_i64_80 = arith.constant 26 : i64
    %112 = quake.extract_ref %0[%c26_i64_80] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_81 = quake.mz %112 : (!quake.ref) -> !quake.measure
    %113 = quake.discriminate %measOut_81 : (!quake.measure) -> i1
    %c27_i64_82 = arith.constant 27 : i64
    %114 = quake.extract_ref %0[%c27_i64_82] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_83 = quake.mz %114 : (!quake.ref) -> !quake.measure
    %115 = quake.discriminate %measOut_83 : (!quake.measure) -> i1
    %c28_i64_84 = arith.constant 28 : i64
    %116 = quake.extract_ref %0[%c28_i64_84] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_85 = quake.mz %116 : (!quake.ref) -> !quake.measure
    %117 = quake.discriminate %measOut_85 : (!quake.measure) -> i1
    %c29_i64_86 = arith.constant 29 : i64
    %118 = quake.extract_ref %0[%c29_i64_86] : (!quake.veq<30>, i64) -> !quake.ref
    %measOut_87 = quake.mz %118 : (!quake.ref) -> !quake.measure
    %119 = quake.discriminate %measOut_87 : (!quake.measure) -> i1
    return
  }
}
