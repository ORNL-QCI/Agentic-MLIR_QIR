module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS = "__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<4>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.y %1 : (!quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %2 = quake.extract_ref %0[%c3_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.t %2 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<4>, i64) -> !quake.ref
    %cst = arith.constant 1.720000e+00 : f64
    quake.rx (%cst) %3 : (f64, !quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %4 = quake.extract_ref %0[%c2_i64] : (!quake.veq<4>, i64) -> !quake.ref
    %c0_i64_1 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<4>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<4>, i64) -> !quake.ref
    quake.z %6 : (!quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %7 = quake.extract_ref %0[%c1_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<4>, i64) -> !quake.ref
    %c2_i64_4 = arith.constant 2 : i64
    %9 = quake.extract_ref %0[%c2_i64_4] : (!quake.veq<4>, i64) -> !quake.ref
    quake.swap %8, %9 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_5 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<4>, i64) -> !quake.ref
    quake.y %10 : (!quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %11 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<4>, i64) -> !quake.ref
    quake.s %11 : (!quake.ref) -> ()
    %c3_i64_7 = arith.constant 3 : i64
    %12 = quake.extract_ref %0[%c3_i64_7] : (!quake.veq<4>, i64) -> !quake.ref
    quake.s %12 : (!quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %13 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_9 = arith.constant 1 : i64
    %15 = quake.extract_ref %0[%c1_i64_9] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_10 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    %c2_i64_11 = arith.constant 2 : i64
    %17 = quake.extract_ref %0[%c2_i64_11] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_12 = quake.mz %17 : (!quake.ref) -> !quake.measure
    %18 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
    %c3_i64_13 = arith.constant 3 : i64
    %19 = quake.extract_ref %0[%c3_i64_13] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_14 = quake.mz %19 : (!quake.ref) -> !quake.measure
    %20 = quake.discriminate %measOut_14 : (!quake.measure) -> i1
    return
  }
}
