module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_2MVHALGQMO = "__nvqpp__mlirgen____nvqppBuilderKernel_2MVHALGQMO_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_2MVHALGQMO() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<20>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<20>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<20>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<20>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<20>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<20>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<20>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<20>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<20>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<20>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<20>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<20>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<20>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<20>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<20>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<20>, i64) -> !quake.ref
    %c15_i64 = arith.constant 15 : i64
    %31 = quake.extract_ref %0[%c15_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%30] %31 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_15 = arith.constant 0 : i64
    %32 = quake.extract_ref %0[%c0_i64_15] : (!quake.veq<20>, i64) -> !quake.ref
    %c16_i64 = arith.constant 16 : i64
    %33 = quake.extract_ref %0[%c16_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%32] %33 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_16 = arith.constant 0 : i64
    %34 = quake.extract_ref %0[%c0_i64_16] : (!quake.veq<20>, i64) -> !quake.ref
    %c17_i64 = arith.constant 17 : i64
    %35 = quake.extract_ref %0[%c17_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%34] %35 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_17 = arith.constant 0 : i64
    %36 = quake.extract_ref %0[%c0_i64_17] : (!quake.veq<20>, i64) -> !quake.ref
    %c18_i64 = arith.constant 18 : i64
    %37 = quake.extract_ref %0[%c18_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%36] %37 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_18 = arith.constant 0 : i64
    %38 = quake.extract_ref %0[%c0_i64_18] : (!quake.veq<20>, i64) -> !quake.ref
    %c19_i64 = arith.constant 19 : i64
    %39 = quake.extract_ref %0[%c19_i64] : (!quake.veq<20>, i64) -> !quake.ref
    quake.x [%38] %39 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_19 = arith.constant 0 : i64
    %40 = quake.extract_ref %0[%c0_i64_19] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut = quake.mz %40 : (!quake.ref) -> !quake.measure
    %41 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_20 = arith.constant 1 : i64
    %42 = quake.extract_ref %0[%c1_i64_20] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_21 = quake.mz %42 : (!quake.ref) -> !quake.measure
    %43 = quake.discriminate %measOut_21 : (!quake.measure) -> i1
    %c2_i64_22 = arith.constant 2 : i64
    %44 = quake.extract_ref %0[%c2_i64_22] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_23 = quake.mz %44 : (!quake.ref) -> !quake.measure
    %45 = quake.discriminate %measOut_23 : (!quake.measure) -> i1
    %c3_i64_24 = arith.constant 3 : i64
    %46 = quake.extract_ref %0[%c3_i64_24] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_25 = quake.mz %46 : (!quake.ref) -> !quake.measure
    %47 = quake.discriminate %measOut_25 : (!quake.measure) -> i1
    %c4_i64_26 = arith.constant 4 : i64
    %48 = quake.extract_ref %0[%c4_i64_26] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_27 = quake.mz %48 : (!quake.ref) -> !quake.measure
    %49 = quake.discriminate %measOut_27 : (!quake.measure) -> i1
    %c5_i64_28 = arith.constant 5 : i64
    %50 = quake.extract_ref %0[%c5_i64_28] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_29 = quake.mz %50 : (!quake.ref) -> !quake.measure
    %51 = quake.discriminate %measOut_29 : (!quake.measure) -> i1
    %c6_i64_30 = arith.constant 6 : i64
    %52 = quake.extract_ref %0[%c6_i64_30] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_31 = quake.mz %52 : (!quake.ref) -> !quake.measure
    %53 = quake.discriminate %measOut_31 : (!quake.measure) -> i1
    %c7_i64_32 = arith.constant 7 : i64
    %54 = quake.extract_ref %0[%c7_i64_32] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_33 = quake.mz %54 : (!quake.ref) -> !quake.measure
    %55 = quake.discriminate %measOut_33 : (!quake.measure) -> i1
    %c8_i64_34 = arith.constant 8 : i64
    %56 = quake.extract_ref %0[%c8_i64_34] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_35 = quake.mz %56 : (!quake.ref) -> !quake.measure
    %57 = quake.discriminate %measOut_35 : (!quake.measure) -> i1
    %c9_i64_36 = arith.constant 9 : i64
    %58 = quake.extract_ref %0[%c9_i64_36] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_37 = quake.mz %58 : (!quake.ref) -> !quake.measure
    %59 = quake.discriminate %measOut_37 : (!quake.measure) -> i1
    %c10_i64_38 = arith.constant 10 : i64
    %60 = quake.extract_ref %0[%c10_i64_38] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_39 = quake.mz %60 : (!quake.ref) -> !quake.measure
    %61 = quake.discriminate %measOut_39 : (!quake.measure) -> i1
    %c11_i64_40 = arith.constant 11 : i64
    %62 = quake.extract_ref %0[%c11_i64_40] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_41 = quake.mz %62 : (!quake.ref) -> !quake.measure
    %63 = quake.discriminate %measOut_41 : (!quake.measure) -> i1
    %c12_i64_42 = arith.constant 12 : i64
    %64 = quake.extract_ref %0[%c12_i64_42] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_43 = quake.mz %64 : (!quake.ref) -> !quake.measure
    %65 = quake.discriminate %measOut_43 : (!quake.measure) -> i1
    %c13_i64_44 = arith.constant 13 : i64
    %66 = quake.extract_ref %0[%c13_i64_44] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_45 = quake.mz %66 : (!quake.ref) -> !quake.measure
    %67 = quake.discriminate %measOut_45 : (!quake.measure) -> i1
    %c14_i64_46 = arith.constant 14 : i64
    %68 = quake.extract_ref %0[%c14_i64_46] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_47 = quake.mz %68 : (!quake.ref) -> !quake.measure
    %69 = quake.discriminate %measOut_47 : (!quake.measure) -> i1
    %c15_i64_48 = arith.constant 15 : i64
    %70 = quake.extract_ref %0[%c15_i64_48] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_49 = quake.mz %70 : (!quake.ref) -> !quake.measure
    %71 = quake.discriminate %measOut_49 : (!quake.measure) -> i1
    %c16_i64_50 = arith.constant 16 : i64
    %72 = quake.extract_ref %0[%c16_i64_50] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_51 = quake.mz %72 : (!quake.ref) -> !quake.measure
    %73 = quake.discriminate %measOut_51 : (!quake.measure) -> i1
    %c17_i64_52 = arith.constant 17 : i64
    %74 = quake.extract_ref %0[%c17_i64_52] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_53 = quake.mz %74 : (!quake.ref) -> !quake.measure
    %75 = quake.discriminate %measOut_53 : (!quake.measure) -> i1
    %c18_i64_54 = arith.constant 18 : i64
    %76 = quake.extract_ref %0[%c18_i64_54] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_55 = quake.mz %76 : (!quake.ref) -> !quake.measure
    %77 = quake.discriminate %measOut_55 : (!quake.measure) -> i1
    %c19_i64_56 = arith.constant 19 : i64
    %78 = quake.extract_ref %0[%c19_i64_56] : (!quake.veq<20>, i64) -> !quake.ref
    %measOut_57 = quake.mz %78 : (!quake.ref) -> !quake.measure
    %79 = quake.discriminate %measOut_57 : (!quake.measure) -> i1
    return
  }
}
