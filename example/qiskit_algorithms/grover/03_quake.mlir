module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_4AIKVSVUWO = "__nvqpp__mlirgen____nvqppBuilderKernel_4AIKVSVUWO_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_4AIKVSVUWO() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %cst = arith.constant 0.78539816339744828 : f64
    %cst_0 = arith.constant -1.5707963267948966 : f64
    %cst_1 = arith.constant -3.1415926535897931 : f64
    %cst_2 = arith.constant 3.1415926535897931 : f64
    %cst_3 = arith.constant -2.3561944901923448 : f64
    %cst_4 = arith.constant -0.78539816339744828 : f64
    %cst_5 = arith.constant 1.5707963267948966 : f64
    %0 = quake.alloca !quake.veq<3>
    %1 = quake.extract_ref %0[0] : (!quake.veq<3>) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %2 = quake.extract_ref %0[1] : (!quake.veq<3>) -> !quake.ref
    quake.h %2 : (!quake.ref) -> ()
    %3 = quake.extract_ref %0[2] : (!quake.veq<3>) -> !quake.ref
    quake.ry (%cst_5) %3 : (f64, !quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %3 : (!quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %2 : (!quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.t %1 : (!quake.ref) -> ()
    quake.rz (%cst_4) %2 : (f64, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.x %1 : (!quake.ref) -> ()
    quake.x %2 : (!quake.ref) -> ()
    quake.rz (%cst_3) %3 : (f64, !quake.ref) -> ()
    quake.ry (%cst_2) %3 : (f64, !quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %3 : (!quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %2 : (!quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.t %1 : (!quake.ref) -> ()
    quake.rz (%cst_4) %2 : (f64, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.rz (%cst_1) %1 : (f64, !quake.ref) -> ()
    quake.ry (%cst_0) %1 : (f64, !quake.ref) -> ()
    quake.rz (%cst_1) %2 : (f64, !quake.ref) -> ()
    quake.ry (%cst_0) %2 : (f64, !quake.ref) -> ()
    quake.rz (%cst) %3 : (f64, !quake.ref) -> ()
    quake.ry (%cst_5) %3 : (f64, !quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %3 : (!quake.ref) -> ()
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    quake.t %2 : (!quake.ref) -> ()
    quake.rz (%cst_4) %3 : (f64, !quake.ref) -> ()
    quake.x [%1] %3 : (!quake.ref, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.t %1 : (!quake.ref) -> ()
    quake.rz (%cst_4) %2 : (f64, !quake.ref) -> ()
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    quake.ry (%cst_0) %1 : (f64, !quake.ref) -> ()
    quake.ry (%cst_0) %2 : (f64, !quake.ref) -> ()
    quake.rz (%cst) %3 : (f64, !quake.ref) -> ()
    quake.ry (%cst_0) %3 : (f64, !quake.ref) -> ()
    %measOut = quake.mz %0 : (!quake.veq<3>) -> !cc.stdvec<!quake.measure>
    return
  }
}
