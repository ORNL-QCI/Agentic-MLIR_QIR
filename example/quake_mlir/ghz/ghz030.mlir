module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_316ZPKL68D = "__nvqpp__mlirgen____nvqppBuilderKernel_316ZPKL68D_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_316ZPKL68D() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<30>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<30>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<30>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<30>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<30>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<30>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<30>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<30>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<30>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<30>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<30>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<30>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<30>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<30>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<30>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<30>, i64) -> !quake.ref
    %c15_i64 = arith.constant 15 : i64
    %31 = quake.extract_ref %0[%c15_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%30] %31 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_15 = arith.constant 0 : i64
    %32 = quake.extract_ref %0[%c0_i64_15] : (!quake.veq<30>, i64) -> !quake.ref
    %c16_i64 = arith.constant 16 : i64
    %33 = quake.extract_ref %0[%c16_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%32] %33 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_16 = arith.constant 0 : i64
    %34 = quake.extract_ref %0[%c0_i64_16] : (!quake.veq<30>, i64) -> !quake.ref
    %c17_i64 = arith.constant 17 : i64
    %35 = quake.extract_ref %0[%c17_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%34] %35 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_17 = arith.constant 0 : i64
    %36 = quake.extract_ref %0[%c0_i64_17] : (!quake.veq<30>, i64) -> !quake.ref
    %c18_i64 = arith.constant 18 : i64
    %37 = quake.extract_ref %0[%c18_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%36] %37 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_18 = arith.constant 0 : i64
    %38 = quake.extract_ref %0[%c0_i64_18] : (!quake.veq<30>, i64) -> !quake.ref
    %c19_i64 = arith.constant 19 : i64
    %39 = quake.extract_ref %0[%c19_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%38] %39 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_19 = arith.constant 0 : i64
    %40 = quake.extract_ref %0[%c0_i64_19] : (!quake.veq<30>, i64) -> !quake.ref
    %c20_i64 = arith.constant 20 : i64
    %41 = quake.extract_ref %0[%c20_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%40] %41 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_20 = arith.constant 0 : i64
    %42 = quake.extract_ref %0[%c0_i64_20] : (!quake.veq<30>, i64) -> !quake.ref
    %c21_i64 = arith.constant 21 : i64
    %43 = quake.extract_ref %0[%c21_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%42] %43 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_21 = arith.constant 0 : i64
    %44 = quake.extract_ref %0[%c0_i64_21] : (!quake.veq<30>, i64) -> !quake.ref
    %c22_i64 = arith.constant 22 : i64
    %45 = quake.extract_ref %0[%c22_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%44] %45 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_22 = arith.constant 0 : i64
    %46 = quake.extract_ref %0[%c0_i64_22] : (!quake.veq<30>, i64) -> !quake.ref
    %c23_i64 = arith.constant 23 : i64
    %47 = quake.extract_ref %0[%c23_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%46] %47 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_23 = arith.constant 0 : i64
    %48 = quake.extract_ref %0[%c0_i64_23] : (!quake.veq<30>, i64) -> !quake.ref
    %c24_i64 = arith.constant 24 : i64
    %49 = quake.extract_ref %0[%c24_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%48] %49 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_24 = arith.constant 0 : i64
    %50 = quake.extract_ref %0[%c0_i64_24] : (!quake.veq<30>, i64) -> !quake.ref
    %c25_i64 = arith.constant 25 : i64
    %51 = quake.extract_ref %0[%c25_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%50] %51 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_25 = arith.constant 0 : i64
    %52 = quake.extract_ref %0[%c0_i64_25] : (!quake.veq<30>, i64) -> !quake.ref
    %c26_i64 = arith.constant 26 : i64
    %53 = quake.extract_ref %0[%c26_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%52] %53 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_26 = arith.constant 0 : i64
    %54 = quake.extract_ref %0[%c0_i64_26] : (!quake.veq<30>, i64) -> !quake.ref
    %c27_i64 = arith.constant 27 : i64
    %55 = quake.extract_ref %0[%c27_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%54] %55 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_27 = arith.constant 0 : i64
    %56 = quake.extract_ref %0[%c0_i64_27] : (!quake.veq<30>, i64) -> !quake.ref
    %c28_i64 = arith.constant 28 : i64
    %57 = quake.extract_ref %0[%c28_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%56] %57 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_28 = arith.constant 0 : i64
    %58 = quake.extract_ref %0[%c0_i64_28] : (!quake.veq<30>, i64) -> !quake.ref
    %c29_i64 = arith.constant 29 : i64
    %59 = quake.extract_ref %0[%c29_i64] : (!quake.veq<30>, i64) -> !quake.ref
    quake.x [%58] %59 : (!quake.ref, !quake.ref) -> ()
    %measOut = quake.mz %0 : (!quake.veq<30>) -> !cc.stdvec<!quake.measure>
    %60 = quake.discriminate %measOut : (!cc.stdvec<!quake.measure>) -> !cc.stdvec<i1>
    return
  }
}
