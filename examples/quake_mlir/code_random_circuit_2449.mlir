module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_T2GYCKBVE3 = "__nvqpp__mlirgen____nvqppBuilderKernel_T2GYCKBVE3_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_T2GYCKBVE3() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<6>
    %c5_i64 = arith.constant 5 : i64
    %1 = quake.extract_ref %0[%c5_i64] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x %1 : (!quake.ref) -> ()
    %c5_i64_0 = arith.constant 5 : i64
    %2 = quake.extract_ref %0[%c5_i64_0] : (!quake.veq<6>, i64) -> !quake.ref
    quake.y %2 : (!quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst = arith.constant 3.000000e-02 : f64
    quake.rz (%cst) %3 : (f64, !quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %4 = quake.extract_ref %0[%c2_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst_1 = arith.constant 1.080000e+00 : f64
    quake.rz (%cst_1) %4 : (f64, !quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %5 = quake.extract_ref %0[%c3_i64] : (!quake.veq<6>, i64) -> !quake.ref
    quake.t %5 : (!quake.ref) -> ()
    %c2_i64_2 = arith.constant 2 : i64
    %6 = quake.extract_ref %0[%c2_i64_2] : (!quake.veq<6>, i64) -> !quake.ref
    quake.s %6 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst_3 = arith.constant 2.410000e+00 : f64
    quake.rx (%cst_3) %7 : (f64, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x %8 : (!quake.ref) -> ()
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %c2_i64_5 = arith.constant 2 : i64
    %10 = quake.extract_ref %0[%c2_i64_5] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x [%9] %10 : (!quake.ref, !quake.ref) -> ()
    %c2_i64_6 = arith.constant 2 : i64
    %11 = quake.extract_ref %0[%c2_i64_6] : (!quake.veq<6>, i64) -> !quake.ref
    %measOut = quake.mz %11 : (!quake.ref) -> !quake.measure
    %12 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c5_i64_7 = arith.constant 5 : i64
    %13 = quake.extract_ref %0[%c5_i64_7] : (!quake.veq<6>, i64) -> !quake.ref
    %measOut_8 = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    return
  }
}
