module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_7EZS25QL27 = "__nvqpp__mlirgen____nvqppBuilderKernel_7EZS25QL27_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_7EZS25QL27() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<3>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c1_i64_0 = arith.constant 1 : i64
    %2 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<3>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %3 = quake.extract_ref %0[%c2_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64] : (!quake.veq<3>, i64) -> !quake.ref
    %c1_i64_1 = arith.constant 1 : i64
    %5 = quake.extract_ref %0[%c1_i64_1] : (!quake.veq<3>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %6 : (!quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut = quake.mz %7 : (!quake.ref) -> !quake.measure
    %8 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_4 = arith.constant 1 : i64
    %9 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_5 = quake.mz %9 : (!quake.ref) -> !quake.measure
    %10 = quake.discriminate %measOut_5 : (!quake.measure) -> i1
    cc.if(%8) {
      %c2_i64_8 = arith.constant 2 : i64
      %13 = quake.extract_ref %0[%c2_i64_8] : (!quake.veq<3>, i64) -> !quake.ref
      quake.z %13 : (!quake.ref) -> ()
    }
    cc.if(%10) {
      %c2_i64_8 = arith.constant 2 : i64
      %13 = quake.extract_ref %0[%c2_i64_8] : (!quake.veq<3>, i64) -> !quake.ref
      quake.x %13 : (!quake.ref) -> ()
    }
    %c2_i64_6 = arith.constant 2 : i64
    %11 = quake.extract_ref %0[%c2_i64_6] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_7 = quake.mz %11 : (!quake.ref) -> !quake.measure
    %12 = quake.discriminate %measOut_7 : (!quake.measure) -> i1
    return
  }
}
