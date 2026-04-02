module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_XN0T0RKTOD = "__nvqpp__mlirgen____nvqppBuilderKernel_XN0T0RKTOD_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_XN0T0RKTOD() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<2>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref
    %c0_i64 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<2>, i64) -> !quake.ref
    %c1_i64_1 = arith.constant 1 : i64
    %4 = quake.extract_ref %0[%c1_i64_1] : (!quake.veq<2>, i64) -> !quake.ref
    quake.swap %3, %4 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    quake.s %5 : (!quake.ref) -> ()
    %c1_i64_3 = arith.constant 1 : i64
    %6 = quake.extract_ref %0[%c1_i64_3] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %6 : (!quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<2>, i64) -> !quake.ref
    %cst = arith.constant 2.590000e+00 : f64
    quake.rx (%cst) %7 : (f64, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<2>, i64) -> !quake.ref
    quake.y %8 : (!quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %9 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<2>, i64) -> !quake.ref
    %c1_i64_7 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_7] : (!quake.veq<2>, i64) -> !quake.ref
    quake.x [%9] %10 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %11 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %11 : (!quake.ref) -> !quake.measure
    %12 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_9 = arith.constant 1 : i64
    %13 = quake.extract_ref %0[%c1_i64_9] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_10 = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    return
  }
}
