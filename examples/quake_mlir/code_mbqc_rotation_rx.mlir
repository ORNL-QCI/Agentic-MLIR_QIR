module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9 = "__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<3>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %2 = quake.extract_ref %0[%c2_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %2 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64] : (!quake.veq<3>, i64) -> !quake.ref
    %c1_i64_0 = arith.constant 1 : i64
    %4 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<3>, i64) -> !quake.ref
    quake.z [%3] %4 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_1 = arith.constant 1 : i64
    %5 = quake.extract_ref %0[%c1_i64_1] : (!quake.veq<3>, i64) -> !quake.ref
    %c2_i64_2 = arith.constant 2 : i64
    %6 = quake.extract_ref %0[%c2_i64_2] : (!quake.veq<3>, i64) -> !quake.ref
    quake.z [%5] %6 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut = quake.mz %8 : (!quake.ref) -> !quake.measure
    %9 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_5 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<3>, i64) -> !quake.ref
    %cst = arith.constant 0.78539816339744828 : f64
    quake.rz (%cst) %10 : (f64, !quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %11 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %11 : (!quake.ref) -> ()
    %c1_i64_7 = arith.constant 1 : i64
    %12 = quake.extract_ref %0[%c1_i64_7] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_8 = quake.mz %12 : (!quake.ref) -> !quake.measure
    %13 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    %c2_i64_9 = arith.constant 2 : i64
    %14 = quake.extract_ref %0[%c2_i64_9] : (!quake.veq<3>, i64) -> !quake.ref
    %cst_10 = arith.constant -1.5707963 : f64
    quake.rx (%cst_10) %14 : (f64, !quake.ref) -> ()
    cc.if(%9) {
      %c2_i64_13 = arith.constant 2 : i64
      %17 = quake.extract_ref %0[%c2_i64_13] : (!quake.veq<3>, i64) -> !quake.ref
      quake.x %17 : (!quake.ref) -> ()
    }
    cc.if(%13) {
      %c2_i64_13 = arith.constant 2 : i64
      %17 = quake.extract_ref %0[%c2_i64_13] : (!quake.veq<3>, i64) -> !quake.ref
      quake.z %17 : (!quake.ref) -> ()
    }
    %c2_i64_11 = arith.constant 2 : i64
    %15 = quake.extract_ref %0[%c2_i64_11] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_12 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
    return
  }
}
