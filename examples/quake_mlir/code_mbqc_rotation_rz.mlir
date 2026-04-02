module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_UAXUSQVHUB = "__nvqpp__mlirgen____nvqppBuilderKernel_UAXUSQVHUB_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_UAXUSQVHUB() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<2>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref
    %c1_i64_0 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<2>, i64) -> !quake.ref
    quake.z [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<2>, i64) -> !quake.ref
    %cst = arith.constant 0.78539816339744828 : f64
    quake.rz (%cst) %4 : (f64, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %5 : (!quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %6 : (!quake.ref) -> !quake.measure
    %7 = quake.discriminate %measOut : (!quake.measure) -> i1
    cc.if(%7) {
      %c1_i64_7 = arith.constant 1 : i64
      %11 = quake.extract_ref %0[%c1_i64_7] : (!quake.veq<2>, i64) -> !quake.ref
      quake.x %11 : (!quake.ref) -> ()
    }
    %c1_i64_4 = arith.constant 1 : i64
    %8 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %8 : (!quake.ref) -> ()
    %c1_i64_5 = arith.constant 1 : i64
    %9 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_6 = quake.mz %9 : (!quake.ref) -> !quake.measure
    %10 = quake.discriminate %measOut_6 : (!quake.measure) -> i1
    return
  }
}
