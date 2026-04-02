module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_ZTJTF5RF8F = "__nvqpp__mlirgen____nvqppBuilderKernel_ZTJTF5RF8F_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_ZTJTF5RF8F() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<65>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<65>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<65>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<65>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<65>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<65>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<65>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<65>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<65>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<65>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<65>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<65>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<65>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<65>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<65>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<65>, i64) -> !quake.ref
    %c15_i64 = arith.constant 15 : i64
    %31 = quake.extract_ref %0[%c15_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%30] %31 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_15 = arith.constant 0 : i64
    %32 = quake.extract_ref %0[%c0_i64_15] : (!quake.veq<65>, i64) -> !quake.ref
    %c16_i64 = arith.constant 16 : i64
    %33 = quake.extract_ref %0[%c16_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%32] %33 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_16 = arith.constant 0 : i64
    %34 = quake.extract_ref %0[%c0_i64_16] : (!quake.veq<65>, i64) -> !quake.ref
    %c17_i64 = arith.constant 17 : i64
    %35 = quake.extract_ref %0[%c17_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%34] %35 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_17 = arith.constant 0 : i64
    %36 = quake.extract_ref %0[%c0_i64_17] : (!quake.veq<65>, i64) -> !quake.ref
    %c18_i64 = arith.constant 18 : i64
    %37 = quake.extract_ref %0[%c18_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%36] %37 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_18 = arith.constant 0 : i64
    %38 = quake.extract_ref %0[%c0_i64_18] : (!quake.veq<65>, i64) -> !quake.ref
    %c19_i64 = arith.constant 19 : i64
    %39 = quake.extract_ref %0[%c19_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%38] %39 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_19 = arith.constant 0 : i64
    %40 = quake.extract_ref %0[%c0_i64_19] : (!quake.veq<65>, i64) -> !quake.ref
    %c20_i64 = arith.constant 20 : i64
    %41 = quake.extract_ref %0[%c20_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%40] %41 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_20 = arith.constant 0 : i64
    %42 = quake.extract_ref %0[%c0_i64_20] : (!quake.veq<65>, i64) -> !quake.ref
    %c21_i64 = arith.constant 21 : i64
    %43 = quake.extract_ref %0[%c21_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%42] %43 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_21 = arith.constant 0 : i64
    %44 = quake.extract_ref %0[%c0_i64_21] : (!quake.veq<65>, i64) -> !quake.ref
    %c22_i64 = arith.constant 22 : i64
    %45 = quake.extract_ref %0[%c22_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%44] %45 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_22 = arith.constant 0 : i64
    %46 = quake.extract_ref %0[%c0_i64_22] : (!quake.veq<65>, i64) -> !quake.ref
    %c23_i64 = arith.constant 23 : i64
    %47 = quake.extract_ref %0[%c23_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%46] %47 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_23 = arith.constant 0 : i64
    %48 = quake.extract_ref %0[%c0_i64_23] : (!quake.veq<65>, i64) -> !quake.ref
    %c24_i64 = arith.constant 24 : i64
    %49 = quake.extract_ref %0[%c24_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%48] %49 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_24 = arith.constant 0 : i64
    %50 = quake.extract_ref %0[%c0_i64_24] : (!quake.veq<65>, i64) -> !quake.ref
    %c25_i64 = arith.constant 25 : i64
    %51 = quake.extract_ref %0[%c25_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%50] %51 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_25 = arith.constant 0 : i64
    %52 = quake.extract_ref %0[%c0_i64_25] : (!quake.veq<65>, i64) -> !quake.ref
    %c26_i64 = arith.constant 26 : i64
    %53 = quake.extract_ref %0[%c26_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%52] %53 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_26 = arith.constant 0 : i64
    %54 = quake.extract_ref %0[%c0_i64_26] : (!quake.veq<65>, i64) -> !quake.ref
    %c27_i64 = arith.constant 27 : i64
    %55 = quake.extract_ref %0[%c27_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%54] %55 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_27 = arith.constant 0 : i64
    %56 = quake.extract_ref %0[%c0_i64_27] : (!quake.veq<65>, i64) -> !quake.ref
    %c28_i64 = arith.constant 28 : i64
    %57 = quake.extract_ref %0[%c28_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%56] %57 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_28 = arith.constant 0 : i64
    %58 = quake.extract_ref %0[%c0_i64_28] : (!quake.veq<65>, i64) -> !quake.ref
    %c29_i64 = arith.constant 29 : i64
    %59 = quake.extract_ref %0[%c29_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%58] %59 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_29 = arith.constant 0 : i64
    %60 = quake.extract_ref %0[%c0_i64_29] : (!quake.veq<65>, i64) -> !quake.ref
    %c30_i64 = arith.constant 30 : i64
    %61 = quake.extract_ref %0[%c30_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%60] %61 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_30 = arith.constant 0 : i64
    %62 = quake.extract_ref %0[%c0_i64_30] : (!quake.veq<65>, i64) -> !quake.ref
    %c31_i64 = arith.constant 31 : i64
    %63 = quake.extract_ref %0[%c31_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%62] %63 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_31 = arith.constant 0 : i64
    %64 = quake.extract_ref %0[%c0_i64_31] : (!quake.veq<65>, i64) -> !quake.ref
    %c32_i64 = arith.constant 32 : i64
    %65 = quake.extract_ref %0[%c32_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%64] %65 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_32 = arith.constant 0 : i64
    %66 = quake.extract_ref %0[%c0_i64_32] : (!quake.veq<65>, i64) -> !quake.ref
    %c33_i64 = arith.constant 33 : i64
    %67 = quake.extract_ref %0[%c33_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%66] %67 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_33 = arith.constant 0 : i64
    %68 = quake.extract_ref %0[%c0_i64_33] : (!quake.veq<65>, i64) -> !quake.ref
    %c34_i64 = arith.constant 34 : i64
    %69 = quake.extract_ref %0[%c34_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%68] %69 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_34 = arith.constant 0 : i64
    %70 = quake.extract_ref %0[%c0_i64_34] : (!quake.veq<65>, i64) -> !quake.ref
    %c35_i64 = arith.constant 35 : i64
    %71 = quake.extract_ref %0[%c35_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%70] %71 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_35 = arith.constant 0 : i64
    %72 = quake.extract_ref %0[%c0_i64_35] : (!quake.veq<65>, i64) -> !quake.ref
    %c36_i64 = arith.constant 36 : i64
    %73 = quake.extract_ref %0[%c36_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%72] %73 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_36 = arith.constant 0 : i64
    %74 = quake.extract_ref %0[%c0_i64_36] : (!quake.veq<65>, i64) -> !quake.ref
    %c37_i64 = arith.constant 37 : i64
    %75 = quake.extract_ref %0[%c37_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%74] %75 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_37 = arith.constant 0 : i64
    %76 = quake.extract_ref %0[%c0_i64_37] : (!quake.veq<65>, i64) -> !quake.ref
    %c38_i64 = arith.constant 38 : i64
    %77 = quake.extract_ref %0[%c38_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%76] %77 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_38 = arith.constant 0 : i64
    %78 = quake.extract_ref %0[%c0_i64_38] : (!quake.veq<65>, i64) -> !quake.ref
    %c39_i64 = arith.constant 39 : i64
    %79 = quake.extract_ref %0[%c39_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%78] %79 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_39 = arith.constant 0 : i64
    %80 = quake.extract_ref %0[%c0_i64_39] : (!quake.veq<65>, i64) -> !quake.ref
    %c40_i64 = arith.constant 40 : i64
    %81 = quake.extract_ref %0[%c40_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%80] %81 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_40 = arith.constant 0 : i64
    %82 = quake.extract_ref %0[%c0_i64_40] : (!quake.veq<65>, i64) -> !quake.ref
    %c41_i64 = arith.constant 41 : i64
    %83 = quake.extract_ref %0[%c41_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%82] %83 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_41 = arith.constant 0 : i64
    %84 = quake.extract_ref %0[%c0_i64_41] : (!quake.veq<65>, i64) -> !quake.ref
    %c42_i64 = arith.constant 42 : i64
    %85 = quake.extract_ref %0[%c42_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%84] %85 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_42 = arith.constant 0 : i64
    %86 = quake.extract_ref %0[%c0_i64_42] : (!quake.veq<65>, i64) -> !quake.ref
    %c43_i64 = arith.constant 43 : i64
    %87 = quake.extract_ref %0[%c43_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%86] %87 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_43 = arith.constant 0 : i64
    %88 = quake.extract_ref %0[%c0_i64_43] : (!quake.veq<65>, i64) -> !quake.ref
    %c44_i64 = arith.constant 44 : i64
    %89 = quake.extract_ref %0[%c44_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%88] %89 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_44 = arith.constant 0 : i64
    %90 = quake.extract_ref %0[%c0_i64_44] : (!quake.veq<65>, i64) -> !quake.ref
    %c45_i64 = arith.constant 45 : i64
    %91 = quake.extract_ref %0[%c45_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%90] %91 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_45 = arith.constant 0 : i64
    %92 = quake.extract_ref %0[%c0_i64_45] : (!quake.veq<65>, i64) -> !quake.ref
    %c46_i64 = arith.constant 46 : i64
    %93 = quake.extract_ref %0[%c46_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%92] %93 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_46 = arith.constant 0 : i64
    %94 = quake.extract_ref %0[%c0_i64_46] : (!quake.veq<65>, i64) -> !quake.ref
    %c47_i64 = arith.constant 47 : i64
    %95 = quake.extract_ref %0[%c47_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%94] %95 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_47 = arith.constant 0 : i64
    %96 = quake.extract_ref %0[%c0_i64_47] : (!quake.veq<65>, i64) -> !quake.ref
    %c48_i64 = arith.constant 48 : i64
    %97 = quake.extract_ref %0[%c48_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%96] %97 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_48 = arith.constant 0 : i64
    %98 = quake.extract_ref %0[%c0_i64_48] : (!quake.veq<65>, i64) -> !quake.ref
    %c49_i64 = arith.constant 49 : i64
    %99 = quake.extract_ref %0[%c49_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%98] %99 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_49 = arith.constant 0 : i64
    %100 = quake.extract_ref %0[%c0_i64_49] : (!quake.veq<65>, i64) -> !quake.ref
    %c50_i64 = arith.constant 50 : i64
    %101 = quake.extract_ref %0[%c50_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%100] %101 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_50 = arith.constant 0 : i64
    %102 = quake.extract_ref %0[%c0_i64_50] : (!quake.veq<65>, i64) -> !quake.ref
    %c51_i64 = arith.constant 51 : i64
    %103 = quake.extract_ref %0[%c51_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%102] %103 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_51 = arith.constant 0 : i64
    %104 = quake.extract_ref %0[%c0_i64_51] : (!quake.veq<65>, i64) -> !quake.ref
    %c52_i64 = arith.constant 52 : i64
    %105 = quake.extract_ref %0[%c52_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%104] %105 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_52 = arith.constant 0 : i64
    %106 = quake.extract_ref %0[%c0_i64_52] : (!quake.veq<65>, i64) -> !quake.ref
    %c53_i64 = arith.constant 53 : i64
    %107 = quake.extract_ref %0[%c53_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%106] %107 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_53 = arith.constant 0 : i64
    %108 = quake.extract_ref %0[%c0_i64_53] : (!quake.veq<65>, i64) -> !quake.ref
    %c54_i64 = arith.constant 54 : i64
    %109 = quake.extract_ref %0[%c54_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%108] %109 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_54 = arith.constant 0 : i64
    %110 = quake.extract_ref %0[%c0_i64_54] : (!quake.veq<65>, i64) -> !quake.ref
    %c55_i64 = arith.constant 55 : i64
    %111 = quake.extract_ref %0[%c55_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%110] %111 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_55 = arith.constant 0 : i64
    %112 = quake.extract_ref %0[%c0_i64_55] : (!quake.veq<65>, i64) -> !quake.ref
    %c56_i64 = arith.constant 56 : i64
    %113 = quake.extract_ref %0[%c56_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%112] %113 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_56 = arith.constant 0 : i64
    %114 = quake.extract_ref %0[%c0_i64_56] : (!quake.veq<65>, i64) -> !quake.ref
    %c57_i64 = arith.constant 57 : i64
    %115 = quake.extract_ref %0[%c57_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%114] %115 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_57 = arith.constant 0 : i64
    %116 = quake.extract_ref %0[%c0_i64_57] : (!quake.veq<65>, i64) -> !quake.ref
    %c58_i64 = arith.constant 58 : i64
    %117 = quake.extract_ref %0[%c58_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%116] %117 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_58 = arith.constant 0 : i64
    %118 = quake.extract_ref %0[%c0_i64_58] : (!quake.veq<65>, i64) -> !quake.ref
    %c59_i64 = arith.constant 59 : i64
    %119 = quake.extract_ref %0[%c59_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%118] %119 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_59 = arith.constant 0 : i64
    %120 = quake.extract_ref %0[%c0_i64_59] : (!quake.veq<65>, i64) -> !quake.ref
    %c60_i64 = arith.constant 60 : i64
    %121 = quake.extract_ref %0[%c60_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%120] %121 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_60 = arith.constant 0 : i64
    %122 = quake.extract_ref %0[%c0_i64_60] : (!quake.veq<65>, i64) -> !quake.ref
    %c61_i64 = arith.constant 61 : i64
    %123 = quake.extract_ref %0[%c61_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%122] %123 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_61 = arith.constant 0 : i64
    %124 = quake.extract_ref %0[%c0_i64_61] : (!quake.veq<65>, i64) -> !quake.ref
    %c62_i64 = arith.constant 62 : i64
    %125 = quake.extract_ref %0[%c62_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%124] %125 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_62 = arith.constant 0 : i64
    %126 = quake.extract_ref %0[%c0_i64_62] : (!quake.veq<65>, i64) -> !quake.ref
    %c63_i64 = arith.constant 63 : i64
    %127 = quake.extract_ref %0[%c63_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%126] %127 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_63 = arith.constant 0 : i64
    %128 = quake.extract_ref %0[%c0_i64_63] : (!quake.veq<65>, i64) -> !quake.ref
    %c64_i64 = arith.constant 64 : i64
    %129 = quake.extract_ref %0[%c64_i64] : (!quake.veq<65>, i64) -> !quake.ref
    quake.x [%128] %129 : (!quake.ref, !quake.ref) -> ()
    %measOut = quake.mz %0 : (!quake.veq<65>) -> !cc.stdvec<!quake.measure>
    %130 = quake.discriminate %measOut : (!cc.stdvec<!quake.measure>) -> !cc.stdvec<i1>
    return
  }
}
