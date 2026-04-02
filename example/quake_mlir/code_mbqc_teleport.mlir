module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI = "__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
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
    quake.h %4 : (!quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %5 : (!quake.ref) -> !quake.measure
    %6 = quake.discriminate %measOut : (!quake.measure) -> i1
    cc.if(%6) {
      %c1_i64_6 = arith.constant 1 : i64
      %10 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<2>, i64) -> !quake.ref
      quake.x %10 : (!quake.ref) -> ()
    }
    %c1_i64_3 = arith.constant 1 : i64
    %7 = quake.extract_ref %0[%c1_i64_3] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c1_i64_4 = arith.constant 1 : i64
    %8 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_5 = quake.mz %8 : (!quake.ref) -> !quake.measure
    %9 = quake.discriminate %measOut_5 : (!quake.measure) -> i1
    return
  }
}
