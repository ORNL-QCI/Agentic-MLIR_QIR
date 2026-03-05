module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_F3RMW5EDHD = "__nvqpp__mlirgen____nvqppBuilderKernel_F3RMW5EDHD_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_F3RMW5EDHD() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<2>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<2>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %4 : (!quake.ref) -> !quake.measure
    %5 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_2 = arith.constant 1 : i64
    %6 = quake.extract_ref %0[%c1_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_3 = quake.mz %6 : (!quake.ref) -> !quake.measure
    %7 = quake.discriminate %measOut_3 : (!quake.measure) -> i1
    return
  }
}
