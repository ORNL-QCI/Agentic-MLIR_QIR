module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_YZ06F4QQB6 = "__nvqpp__mlirgen____nvqppBuilderKernel_YZ06F4QQB6_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_YZ06F4QQB6() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<1>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<1>, i64) -> !quake.ref
    %cst = arith.constant 1.5707963 : f64
    quake.rz (%cst) %1 : (f64, !quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<1>, i64) -> !quake.ref
    %measOut = quake.mz %2 : (!quake.ref) -> !quake.measure
    %3 = quake.discriminate %measOut : (!quake.measure) -> i1
    return
  }
}
