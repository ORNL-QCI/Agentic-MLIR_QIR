module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21 = "__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<5>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<5>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<5>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<5>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<5>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut = quake.mz %10 : (!quake.ref) -> !quake.measure
    %11 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_5 = arith.constant 1 : i64
    %12 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_6 = quake.mz %12 : (!quake.ref) -> !quake.measure
    %13 = quake.discriminate %measOut_6 : (!quake.measure) -> i1
    %c2_i64_7 = arith.constant 2 : i64
    %14 = quake.extract_ref %0[%c2_i64_7] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_8 = quake.mz %14 : (!quake.ref) -> !quake.measure
    %15 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    %c3_i64_9 = arith.constant 3 : i64
    %16 = quake.extract_ref %0[%c3_i64_9] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_10 = quake.mz %16 : (!quake.ref) -> !quake.measure
    %17 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    %c4_i64_11 = arith.constant 4 : i64
    %18 = quake.extract_ref %0[%c4_i64_11] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_12 = quake.mz %18 : (!quake.ref) -> !quake.measure
    %19 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
    return
  }
}
