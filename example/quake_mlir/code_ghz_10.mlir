module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_1TXD86X9Q4 = "__nvqpp__mlirgen____nvqppBuilderKernel_1TXD86X9Q4_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_1TXD86X9Q4() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<10>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<10>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<10>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<10>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<10>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<10>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<10>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<10>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<10>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<10>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<10>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut = quake.mz %20 : (!quake.ref) -> !quake.measure
    %21 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_10 = arith.constant 1 : i64
    %22 = quake.extract_ref %0[%c1_i64_10] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_11 = quake.mz %22 : (!quake.ref) -> !quake.measure
    %23 = quake.discriminate %measOut_11 : (!quake.measure) -> i1
    %c2_i64_12 = arith.constant 2 : i64
    %24 = quake.extract_ref %0[%c2_i64_12] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_13 = quake.mz %24 : (!quake.ref) -> !quake.measure
    %25 = quake.discriminate %measOut_13 : (!quake.measure) -> i1
    %c3_i64_14 = arith.constant 3 : i64
    %26 = quake.extract_ref %0[%c3_i64_14] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_15 = quake.mz %26 : (!quake.ref) -> !quake.measure
    %27 = quake.discriminate %measOut_15 : (!quake.measure) -> i1
    %c4_i64_16 = arith.constant 4 : i64
    %28 = quake.extract_ref %0[%c4_i64_16] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_17 = quake.mz %28 : (!quake.ref) -> !quake.measure
    %29 = quake.discriminate %measOut_17 : (!quake.measure) -> i1
    %c5_i64_18 = arith.constant 5 : i64
    %30 = quake.extract_ref %0[%c5_i64_18] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_19 = quake.mz %30 : (!quake.ref) -> !quake.measure
    %31 = quake.discriminate %measOut_19 : (!quake.measure) -> i1
    %c6_i64_20 = arith.constant 6 : i64
    %32 = quake.extract_ref %0[%c6_i64_20] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_21 = quake.mz %32 : (!quake.ref) -> !quake.measure
    %33 = quake.discriminate %measOut_21 : (!quake.measure) -> i1
    %c7_i64_22 = arith.constant 7 : i64
    %34 = quake.extract_ref %0[%c7_i64_22] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_23 = quake.mz %34 : (!quake.ref) -> !quake.measure
    %35 = quake.discriminate %measOut_23 : (!quake.measure) -> i1
    %c8_i64_24 = arith.constant 8 : i64
    %36 = quake.extract_ref %0[%c8_i64_24] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_25 = quake.mz %36 : (!quake.ref) -> !quake.measure
    %37 = quake.discriminate %measOut_25 : (!quake.measure) -> i1
    %c9_i64_26 = arith.constant 9 : i64
    %38 = quake.extract_ref %0[%c9_i64_26] : (!quake.veq<10>, i64) -> !quake.ref
    %measOut_27 = quake.mz %38 : (!quake.ref) -> !quake.measure
    %39 = quake.discriminate %measOut_27 : (!quake.measure) -> i1
    return
  }
}
