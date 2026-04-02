module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_D2SE8M2Z0R = "__nvqpp__mlirgen____nvqppBuilderKernel_D2SE8M2Z0R_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_D2SE8M2Z0R() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<15>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<15>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<15>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<15>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<15>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<15>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<15>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<15>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<15>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<15>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<15>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<15>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<15>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<15>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<15>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<15>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut = quake.mz %30 : (!quake.ref) -> !quake.measure
    %31 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_15 = arith.constant 1 : i64
    %32 = quake.extract_ref %0[%c1_i64_15] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_16 = quake.mz %32 : (!quake.ref) -> !quake.measure
    %33 = quake.discriminate %measOut_16 : (!quake.measure) -> i1
    %c2_i64_17 = arith.constant 2 : i64
    %34 = quake.extract_ref %0[%c2_i64_17] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_18 = quake.mz %34 : (!quake.ref) -> !quake.measure
    %35 = quake.discriminate %measOut_18 : (!quake.measure) -> i1
    %c3_i64_19 = arith.constant 3 : i64
    %36 = quake.extract_ref %0[%c3_i64_19] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_20 = quake.mz %36 : (!quake.ref) -> !quake.measure
    %37 = quake.discriminate %measOut_20 : (!quake.measure) -> i1
    %c4_i64_21 = arith.constant 4 : i64
    %38 = quake.extract_ref %0[%c4_i64_21] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_22 = quake.mz %38 : (!quake.ref) -> !quake.measure
    %39 = quake.discriminate %measOut_22 : (!quake.measure) -> i1
    %c5_i64_23 = arith.constant 5 : i64
    %40 = quake.extract_ref %0[%c5_i64_23] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_24 = quake.mz %40 : (!quake.ref) -> !quake.measure
    %41 = quake.discriminate %measOut_24 : (!quake.measure) -> i1
    %c6_i64_25 = arith.constant 6 : i64
    %42 = quake.extract_ref %0[%c6_i64_25] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_26 = quake.mz %42 : (!quake.ref) -> !quake.measure
    %43 = quake.discriminate %measOut_26 : (!quake.measure) -> i1
    %c7_i64_27 = arith.constant 7 : i64
    %44 = quake.extract_ref %0[%c7_i64_27] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_28 = quake.mz %44 : (!quake.ref) -> !quake.measure
    %45 = quake.discriminate %measOut_28 : (!quake.measure) -> i1
    %c8_i64_29 = arith.constant 8 : i64
    %46 = quake.extract_ref %0[%c8_i64_29] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_30 = quake.mz %46 : (!quake.ref) -> !quake.measure
    %47 = quake.discriminate %measOut_30 : (!quake.measure) -> i1
    %c9_i64_31 = arith.constant 9 : i64
    %48 = quake.extract_ref %0[%c9_i64_31] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_32 = quake.mz %48 : (!quake.ref) -> !quake.measure
    %49 = quake.discriminate %measOut_32 : (!quake.measure) -> i1
    %c10_i64_33 = arith.constant 10 : i64
    %50 = quake.extract_ref %0[%c10_i64_33] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_34 = quake.mz %50 : (!quake.ref) -> !quake.measure
    %51 = quake.discriminate %measOut_34 : (!quake.measure) -> i1
    %c11_i64_35 = arith.constant 11 : i64
    %52 = quake.extract_ref %0[%c11_i64_35] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_36 = quake.mz %52 : (!quake.ref) -> !quake.measure
    %53 = quake.discriminate %measOut_36 : (!quake.measure) -> i1
    %c12_i64_37 = arith.constant 12 : i64
    %54 = quake.extract_ref %0[%c12_i64_37] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_38 = quake.mz %54 : (!quake.ref) -> !quake.measure
    %55 = quake.discriminate %measOut_38 : (!quake.measure) -> i1
    %c13_i64_39 = arith.constant 13 : i64
    %56 = quake.extract_ref %0[%c13_i64_39] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_40 = quake.mz %56 : (!quake.ref) -> !quake.measure
    %57 = quake.discriminate %measOut_40 : (!quake.measure) -> i1
    %c14_i64_41 = arith.constant 14 : i64
    %58 = quake.extract_ref %0[%c14_i64_41] : (!quake.veq<15>, i64) -> !quake.ref
    %measOut_42 = quake.mz %58 : (!quake.ref) -> !quake.measure
    %59 = quake.discriminate %measOut_42 : (!quake.measure) -> i1
    return
  }
}
