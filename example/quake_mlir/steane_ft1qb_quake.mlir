module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_YNAJ63O8PN = "__nvqpp__mlirgen____nvqppBuilderKernel_YNAJ63O8PN_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_YNAJ63O8PN() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<7>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %2 = quake.extract_ref %0[%c1_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %2 : (!quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %3 = quake.extract_ref %0[%c3_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %3 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<7>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<7>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %7 = quake.extract_ref %0[%c4_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<7>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %9 = quake.extract_ref %0[%c6_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_3 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_3] : (!quake.veq<7>, i64) -> !quake.ref
    %c2_i64_4 = arith.constant 2 : i64
    %11 = quake.extract_ref %0[%c2_i64_4] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_5 = arith.constant 1 : i64
    %12 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<7>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %13 = quake.extract_ref %0[%c5_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %14 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<7>, i64) -> !quake.ref
    %c6_i64_7 = arith.constant 6 : i64
    %15 = quake.extract_ref %0[%c6_i64_7] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c3_i64_8 = arith.constant 3 : i64
    %16 = quake.extract_ref %0[%c3_i64_8] : (!quake.veq<7>, i64) -> !quake.ref
    %c4_i64_9 = arith.constant 4 : i64
    %17 = quake.extract_ref %0[%c4_i64_9] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c3_i64_10 = arith.constant 3 : i64
    %18 = quake.extract_ref %0[%c3_i64_10] : (!quake.veq<7>, i64) -> !quake.ref
    %c5_i64_11 = arith.constant 5 : i64
    %19 = quake.extract_ref %0[%c5_i64_11] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c3_i64_12 = arith.constant 3 : i64
    %20 = quake.extract_ref %0[%c3_i64_12] : (!quake.veq<7>, i64) -> !quake.ref
    %c6_i64_13 = arith.constant 6 : i64
    %21 = quake.extract_ref %0[%c6_i64_13] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %22 : (!quake.ref) -> ()
    %c1_i64_15 = arith.constant 1 : i64
    %23 = quake.extract_ref %0[%c1_i64_15] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %23 : (!quake.ref) -> ()
    %c2_i64_16 = arith.constant 2 : i64
    %24 = quake.extract_ref %0[%c2_i64_16] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %24 : (!quake.ref) -> ()
    %c3_i64_17 = arith.constant 3 : i64
    %25 = quake.extract_ref %0[%c3_i64_17] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %25 : (!quake.ref) -> ()
    %c4_i64_18 = arith.constant 4 : i64
    %26 = quake.extract_ref %0[%c4_i64_18] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %26 : (!quake.ref) -> ()
    %c5_i64_19 = arith.constant 5 : i64
    %27 = quake.extract_ref %0[%c5_i64_19] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %27 : (!quake.ref) -> ()
    %c6_i64_20 = arith.constant 6 : i64
    %28 = quake.extract_ref %0[%c6_i64_20] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %28 : (!quake.ref) -> ()
    %c0_i64_21 = arith.constant 0 : i64
    %29 = quake.extract_ref %0[%c0_i64_21] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut = quake.mz %29 : (!quake.ref) -> !quake.measure
    %30 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_22 = arith.constant 1 : i64
    %31 = quake.extract_ref %0[%c1_i64_22] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_23 = quake.mz %31 : (!quake.ref) -> !quake.measure
    %32 = quake.discriminate %measOut_23 : (!quake.measure) -> i1
    %c2_i64_24 = arith.constant 2 : i64
    %33 = quake.extract_ref %0[%c2_i64_24] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_25 = quake.mz %33 : (!quake.ref) -> !quake.measure
    %34 = quake.discriminate %measOut_25 : (!quake.measure) -> i1
    %c3_i64_26 = arith.constant 3 : i64
    %35 = quake.extract_ref %0[%c3_i64_26] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_27 = quake.mz %35 : (!quake.ref) -> !quake.measure
    %36 = quake.discriminate %measOut_27 : (!quake.measure) -> i1
    %c4_i64_28 = arith.constant 4 : i64
    %37 = quake.extract_ref %0[%c4_i64_28] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_29 = quake.mz %37 : (!quake.ref) -> !quake.measure
    %38 = quake.discriminate %measOut_29 : (!quake.measure) -> i1
    %c5_i64_30 = arith.constant 5 : i64
    %39 = quake.extract_ref %0[%c5_i64_30] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_31 = quake.mz %39 : (!quake.ref) -> !quake.measure
    %40 = quake.discriminate %measOut_31 : (!quake.measure) -> i1
    %c6_i64_32 = arith.constant 6 : i64
    %41 = quake.extract_ref %0[%c6_i64_32] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_33 = quake.mz %41 : (!quake.ref) -> !quake.measure
    %42 = quake.discriminate %measOut_33 : (!quake.measure) -> i1
    return
  }
}
