# Code Ghz 100

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[100] q;
bit[100] c;

// 100-qubit GHZ state
h q[0];
cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[0], q[4];
cx q[0], q[5];
cx q[0], q[6];
cx q[0], q[7];
cx q[0], q[8];
cx q[0], q[9];
cx q[0], q[10];
cx q[0], q[11];
cx q[0], q[12];
cx q[0], q[13];
cx q[0], q[14];
cx q[0], q[15];
cx q[0], q[16];
cx q[0], q[17];
cx q[0], q[18];
cx q[0], q[19];
cx q[0], q[20];
cx q[0], q[21];
cx q[0], q[22];
cx q[0], q[23];
cx q[0], q[24];
cx q[0], q[25];
cx q[0], q[26];
cx q[0], q[27];
cx q[0], q[28];
cx q[0], q[29];
cx q[0], q[30];
cx q[0], q[31];
cx q[0], q[32];
cx q[0], q[33];
cx q[0], q[34];
cx q[0], q[35];
cx q[0], q[36];
cx q[0], q[37];
cx q[0], q[38];
cx q[0], q[39];
cx q[0], q[40];
cx q[0], q[41];
cx q[0], q[42];
cx q[0], q[43];
cx q[0], q[44];
cx q[0], q[45];
cx q[0], q[46];
cx q[0], q[47];
cx q[0], q[48];
cx q[0], q[49];
cx q[0], q[50];
cx q[0], q[51];
cx q[0], q[52];
cx q[0], q[53];
cx q[0], q[54];
cx q[0], q[55];
cx q[0], q[56];
cx q[0], q[57];
cx q[0], q[58];
cx q[0], q[59];
cx q[0], q[60];
cx q[0], q[61];
cx q[0], q[62];
cx q[0], q[63];
cx q[0], q[64];
cx q[0], q[65];
cx q[0], q[66];
cx q[0], q[67];
cx q[0], q[68];
cx q[0], q[69];
cx q[0], q[70];
cx q[0], q[71];
cx q[0], q[72];
cx q[0], q[73];
cx q[0], q[74];
cx q[0], q[75];
cx q[0], q[76];
cx q[0], q[77];
cx q[0], q[78];
cx q[0], q[79];
cx q[0], q[80];
cx q[0], q[81];
cx q[0], q[82];
cx q[0], q[83];
cx q[0], q[84];
cx q[0], q[85];
cx q[0], q[86];
cx q[0], q[87];
cx q[0], q[88];
cx q[0], q[89];
cx q[0], q[90];
cx q[0], q[91];
cx q[0], q[92];
cx q[0], q[93];
cx q[0], q[94];
cx q[0], q[95];
cx q[0], q[96];
cx q[0], q[97];
cx q[0], q[98];
cx q[0], q[99];

// Measure all qubits
c = measure q;
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_4RIYR1Q4F7 = "__nvqpp__mlirgen____nvqppBuilderKernel_4RIYR1Q4F7_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_4RIYR1Q4F7() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<100>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<100>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<100>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<100>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<100>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<100>, i64) -> !quake.ref
    %c5_i64 = arith.constant 5 : i64
    %11 = quake.extract_ref %0[%c5_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_5 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<100>, i64) -> !quake.ref
    %c6_i64 = arith.constant 6 : i64
    %13 = quake.extract_ref %0[%c6_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_6 = arith.constant 0 : i64
    %14 = quake.extract_ref %0[%c0_i64_6] : (!quake.veq<100>, i64) -> !quake.ref
    %c7_i64 = arith.constant 7 : i64
    %15 = quake.extract_ref %0[%c7_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_7 = arith.constant 0 : i64
    %16 = quake.extract_ref %0[%c0_i64_7] : (!quake.veq<100>, i64) -> !quake.ref
    %c8_i64 = arith.constant 8 : i64
    %17 = quake.extract_ref %0[%c8_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%16] %17 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %18 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<100>, i64) -> !quake.ref
    %c9_i64 = arith.constant 9 : i64
    %19 = quake.extract_ref %0[%c9_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%18] %19 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_9 = arith.constant 0 : i64
    %20 = quake.extract_ref %0[%c0_i64_9] : (!quake.veq<100>, i64) -> !quake.ref
    %c10_i64 = arith.constant 10 : i64
    %21 = quake.extract_ref %0[%c10_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%20] %21 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %22 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<100>, i64) -> !quake.ref
    %c11_i64 = arith.constant 11 : i64
    %23 = quake.extract_ref %0[%c11_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%22] %23 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %24 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<100>, i64) -> !quake.ref
    %c12_i64 = arith.constant 12 : i64
    %25 = quake.extract_ref %0[%c12_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%24] %25 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_12 = arith.constant 0 : i64
    %26 = quake.extract_ref %0[%c0_i64_12] : (!quake.veq<100>, i64) -> !quake.ref
    %c13_i64 = arith.constant 13 : i64
    %27 = quake.extract_ref %0[%c13_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%26] %27 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_13 = arith.constant 0 : i64
    %28 = quake.extract_ref %0[%c0_i64_13] : (!quake.veq<100>, i64) -> !quake.ref
    %c14_i64 = arith.constant 14 : i64
    %29 = quake.extract_ref %0[%c14_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%28] %29 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_14 = arith.constant 0 : i64
    %30 = quake.extract_ref %0[%c0_i64_14] : (!quake.veq<100>, i64) -> !quake.ref
    %c15_i64 = arith.constant 15 : i64
    %31 = quake.extract_ref %0[%c15_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%30] %31 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_15 = arith.constant 0 : i64
    %32 = quake.extract_ref %0[%c0_i64_15] : (!quake.veq<100>, i64) -> !quake.ref
    %c16_i64 = arith.constant 16 : i64
    %33 = quake.extract_ref %0[%c16_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%32] %33 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_16 = arith.constant 0 : i64
    %34 = quake.extract_ref %0[%c0_i64_16] : (!quake.veq<100>, i64) -> !quake.ref
    %c17_i64 = arith.constant 17 : i64
    %35 = quake.extract_ref %0[%c17_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%34] %35 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_17 = arith.constant 0 : i64
    %36 = quake.extract_ref %0[%c0_i64_17] : (!quake.veq<100>, i64) -> !quake.ref
    %c18_i64 = arith.constant 18 : i64
    %37 = quake.extract_ref %0[%c18_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%36] %37 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_18 = arith.constant 0 : i64
    %38 = quake.extract_ref %0[%c0_i64_18] : (!quake.veq<100>, i64) -> !quake.ref
    %c19_i64 = arith.constant 19 : i64
    %39 = quake.extract_ref %0[%c19_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%38] %39 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_19 = arith.constant 0 : i64
    %40 = quake.extract_ref %0[%c0_i64_19] : (!quake.veq<100>, i64) -> !quake.ref
    %c20_i64 = arith.constant 20 : i64
    %41 = quake.extract_ref %0[%c20_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%40] %41 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_20 = arith.constant 0 : i64
    %42 = quake.extract_ref %0[%c0_i64_20] : (!quake.veq<100>, i64) -> !quake.ref
    %c21_i64 = arith.constant 21 : i64
    %43 = quake.extract_ref %0[%c21_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%42] %43 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_21 = arith.constant 0 : i64
    %44 = quake.extract_ref %0[%c0_i64_21] : (!quake.veq<100>, i64) -> !quake.ref
    %c22_i64 = arith.constant 22 : i64
    %45 = quake.extract_ref %0[%c22_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%44] %45 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_22 = arith.constant 0 : i64
    %46 = quake.extract_ref %0[%c0_i64_22] : (!quake.veq<100>, i64) -> !quake.ref
    %c23_i64 = arith.constant 23 : i64
    %47 = quake.extract_ref %0[%c23_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%46] %47 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_23 = arith.constant 0 : i64
    %48 = quake.extract_ref %0[%c0_i64_23] : (!quake.veq<100>, i64) -> !quake.ref
    %c24_i64 = arith.constant 24 : i64
    %49 = quake.extract_ref %0[%c24_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%48] %49 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_24 = arith.constant 0 : i64
    %50 = quake.extract_ref %0[%c0_i64_24] : (!quake.veq<100>, i64) -> !quake.ref
    %c25_i64 = arith.constant 25 : i64
    %51 = quake.extract_ref %0[%c25_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%50] %51 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_25 = arith.constant 0 : i64
    %52 = quake.extract_ref %0[%c0_i64_25] : (!quake.veq<100>, i64) -> !quake.ref
    %c26_i64 = arith.constant 26 : i64
    %53 = quake.extract_ref %0[%c26_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%52] %53 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_26 = arith.constant 0 : i64
    %54 = quake.extract_ref %0[%c0_i64_26] : (!quake.veq<100>, i64) -> !quake.ref
    %c27_i64 = arith.constant 27 : i64
    %55 = quake.extract_ref %0[%c27_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%54] %55 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_27 = arith.constant 0 : i64
    %56 = quake.extract_ref %0[%c0_i64_27] : (!quake.veq<100>, i64) -> !quake.ref
    %c28_i64 = arith.constant 28 : i64
    %57 = quake.extract_ref %0[%c28_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%56] %57 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_28 = arith.constant 0 : i64
    %58 = quake.extract_ref %0[%c0_i64_28] : (!quake.veq<100>, i64) -> !quake.ref
    %c29_i64 = arith.constant 29 : i64
    %59 = quake.extract_ref %0[%c29_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%58] %59 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_29 = arith.constant 0 : i64
    %60 = quake.extract_ref %0[%c0_i64_29] : (!quake.veq<100>, i64) -> !quake.ref
    %c30_i64 = arith.constant 30 : i64
    %61 = quake.extract_ref %0[%c30_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%60] %61 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_30 = arith.constant 0 : i64
    %62 = quake.extract_ref %0[%c0_i64_30] : (!quake.veq<100>, i64) -> !quake.ref
    %c31_i64 = arith.constant 31 : i64
    %63 = quake.extract_ref %0[%c31_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%62] %63 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_31 = arith.constant 0 : i64
    %64 = quake.extract_ref %0[%c0_i64_31] : (!quake.veq<100>, i64) -> !quake.ref
    %c32_i64 = arith.constant 32 : i64
    %65 = quake.extract_ref %0[%c32_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%64] %65 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_32 = arith.constant 0 : i64
    %66 = quake.extract_ref %0[%c0_i64_32] : (!quake.veq<100>, i64) -> !quake.ref
    %c33_i64 = arith.constant 33 : i64
    %67 = quake.extract_ref %0[%c33_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%66] %67 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_33 = arith.constant 0 : i64
    %68 = quake.extract_ref %0[%c0_i64_33] : (!quake.veq<100>, i64) -> !quake.ref
    %c34_i64 = arith.constant 34 : i64
    %69 = quake.extract_ref %0[%c34_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%68] %69 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_34 = arith.constant 0 : i64
    %70 = quake.extract_ref %0[%c0_i64_34] : (!quake.veq<100>, i64) -> !quake.ref
    %c35_i64 = arith.constant 35 : i64
    %71 = quake.extract_ref %0[%c35_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%70] %71 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_35 = arith.constant 0 : i64
    %72 = quake.extract_ref %0[%c0_i64_35] : (!quake.veq<100>, i64) -> !quake.ref
    %c36_i64 = arith.constant 36 : i64
    %73 = quake.extract_ref %0[%c36_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%72] %73 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_36 = arith.constant 0 : i64
    %74 = quake.extract_ref %0[%c0_i64_36] : (!quake.veq<100>, i64) -> !quake.ref
    %c37_i64 = arith.constant 37 : i64
    %75 = quake.extract_ref %0[%c37_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%74] %75 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_37 = arith.constant 0 : i64
    %76 = quake.extract_ref %0[%c0_i64_37] : (!quake.veq<100>, i64) -> !quake.ref
    %c38_i64 = arith.constant 38 : i64
    %77 = quake.extract_ref %0[%c38_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%76] %77 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_38 = arith.constant 0 : i64
    %78 = quake.extract_ref %0[%c0_i64_38] : (!quake.veq<100>, i64) -> !quake.ref
    %c39_i64 = arith.constant 39 : i64
    %79 = quake.extract_ref %0[%c39_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%78] %79 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_39 = arith.constant 0 : i64
    %80 = quake.extract_ref %0[%c0_i64_39] : (!quake.veq<100>, i64) -> !quake.ref
    %c40_i64 = arith.constant 40 : i64
    %81 = quake.extract_ref %0[%c40_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%80] %81 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_40 = arith.constant 0 : i64
    %82 = quake.extract_ref %0[%c0_i64_40] : (!quake.veq<100>, i64) -> !quake.ref
    %c41_i64 = arith.constant 41 : i64
    %83 = quake.extract_ref %0[%c41_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%82] %83 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_41 = arith.constant 0 : i64
    %84 = quake.extract_ref %0[%c0_i64_41] : (!quake.veq<100>, i64) -> !quake.ref
    %c42_i64 = arith.constant 42 : i64
    %85 = quake.extract_ref %0[%c42_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%84] %85 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_42 = arith.constant 0 : i64
    %86 = quake.extract_ref %0[%c0_i64_42] : (!quake.veq<100>, i64) -> !quake.ref
    %c43_i64 = arith.constant 43 : i64
    %87 = quake.extract_ref %0[%c43_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%86] %87 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_43 = arith.constant 0 : i64
    %88 = quake.extract_ref %0[%c0_i64_43] : (!quake.veq<100>, i64) -> !quake.ref
    %c44_i64 = arith.constant 44 : i64
    %89 = quake.extract_ref %0[%c44_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%88] %89 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_44 = arith.constant 0 : i64
    %90 = quake.extract_ref %0[%c0_i64_44] : (!quake.veq<100>, i64) -> !quake.ref
    %c45_i64 = arith.constant 45 : i64
    %91 = quake.extract_ref %0[%c45_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%90] %91 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_45 = arith.constant 0 : i64
    %92 = quake.extract_ref %0[%c0_i64_45] : (!quake.veq<100>, i64) -> !quake.ref
    %c46_i64 = arith.constant 46 : i64
    %93 = quake.extract_ref %0[%c46_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%92] %93 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_46 = arith.constant 0 : i64
    %94 = quake.extract_ref %0[%c0_i64_46] : (!quake.veq<100>, i64) -> !quake.ref
    %c47_i64 = arith.constant 47 : i64
    %95 = quake.extract_ref %0[%c47_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%94] %95 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_47 = arith.constant 0 : i64
    %96 = quake.extract_ref %0[%c0_i64_47] : (!quake.veq<100>, i64) -> !quake.ref
    %c48_i64 = arith.constant 48 : i64
    %97 = quake.extract_ref %0[%c48_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%96] %97 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_48 = arith.constant 0 : i64
    %98 = quake.extract_ref %0[%c0_i64_48] : (!quake.veq<100>, i64) -> !quake.ref
    %c49_i64 = arith.constant 49 : i64
    %99 = quake.extract_ref %0[%c49_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%98] %99 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_49 = arith.constant 0 : i64
    %100 = quake.extract_ref %0[%c0_i64_49] : (!quake.veq<100>, i64) -> !quake.ref
    %c50_i64 = arith.constant 50 : i64
    %101 = quake.extract_ref %0[%c50_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%100] %101 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_50 = arith.constant 0 : i64
    %102 = quake.extract_ref %0[%c0_i64_50] : (!quake.veq<100>, i64) -> !quake.ref
    %c51_i64 = arith.constant 51 : i64
    %103 = quake.extract_ref %0[%c51_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%102] %103 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_51 = arith.constant 0 : i64
    %104 = quake.extract_ref %0[%c0_i64_51] : (!quake.veq<100>, i64) -> !quake.ref
    %c52_i64 = arith.constant 52 : i64
    %105 = quake.extract_ref %0[%c52_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%104] %105 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_52 = arith.constant 0 : i64
    %106 = quake.extract_ref %0[%c0_i64_52] : (!quake.veq<100>, i64) -> !quake.ref
    %c53_i64 = arith.constant 53 : i64
    %107 = quake.extract_ref %0[%c53_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%106] %107 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_53 = arith.constant 0 : i64
    %108 = quake.extract_ref %0[%c0_i64_53] : (!quake.veq<100>, i64) -> !quake.ref
    %c54_i64 = arith.constant 54 : i64
    %109 = quake.extract_ref %0[%c54_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%108] %109 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_54 = arith.constant 0 : i64
    %110 = quake.extract_ref %0[%c0_i64_54] : (!quake.veq<100>, i64) -> !quake.ref
    %c55_i64 = arith.constant 55 : i64
    %111 = quake.extract_ref %0[%c55_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%110] %111 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_55 = arith.constant 0 : i64
    %112 = quake.extract_ref %0[%c0_i64_55] : (!quake.veq<100>, i64) -> !quake.ref
    %c56_i64 = arith.constant 56 : i64
    %113 = quake.extract_ref %0[%c56_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%112] %113 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_56 = arith.constant 0 : i64
    %114 = quake.extract_ref %0[%c0_i64_56] : (!quake.veq<100>, i64) -> !quake.ref
    %c57_i64 = arith.constant 57 : i64
    %115 = quake.extract_ref %0[%c57_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%114] %115 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_57 = arith.constant 0 : i64
    %116 = quake.extract_ref %0[%c0_i64_57] : (!quake.veq<100>, i64) -> !quake.ref
    %c58_i64 = arith.constant 58 : i64
    %117 = quake.extract_ref %0[%c58_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%116] %117 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_58 = arith.constant 0 : i64
    %118 = quake.extract_ref %0[%c0_i64_58] : (!quake.veq<100>, i64) -> !quake.ref
    %c59_i64 = arith.constant 59 : i64
    %119 = quake.extract_ref %0[%c59_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%118] %119 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_59 = arith.constant 0 : i64
    %120 = quake.extract_ref %0[%c0_i64_59] : (!quake.veq<100>, i64) -> !quake.ref
    %c60_i64 = arith.constant 60 : i64
    %121 = quake.extract_ref %0[%c60_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%120] %121 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_60 = arith.constant 0 : i64
    %122 = quake.extract_ref %0[%c0_i64_60] : (!quake.veq<100>, i64) -> !quake.ref
    %c61_i64 = arith.constant 61 : i64
    %123 = quake.extract_ref %0[%c61_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%122] %123 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_61 = arith.constant 0 : i64
    %124 = quake.extract_ref %0[%c0_i64_61] : (!quake.veq<100>, i64) -> !quake.ref
    %c62_i64 = arith.constant 62 : i64
    %125 = quake.extract_ref %0[%c62_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%124] %125 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_62 = arith.constant 0 : i64
    %126 = quake.extract_ref %0[%c0_i64_62] : (!quake.veq<100>, i64) -> !quake.ref
    %c63_i64 = arith.constant 63 : i64
    %127 = quake.extract_ref %0[%c63_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%126] %127 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_63 = arith.constant 0 : i64
    %128 = quake.extract_ref %0[%c0_i64_63] : (!quake.veq<100>, i64) -> !quake.ref
    %c64_i64 = arith.constant 64 : i64
    %129 = quake.extract_ref %0[%c64_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%128] %129 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_64 = arith.constant 0 : i64
    %130 = quake.extract_ref %0[%c0_i64_64] : (!quake.veq<100>, i64) -> !quake.ref
    %c65_i64 = arith.constant 65 : i64
    %131 = quake.extract_ref %0[%c65_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%130] %131 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_65 = arith.constant 0 : i64
    %132 = quake.extract_ref %0[%c0_i64_65] : (!quake.veq<100>, i64) -> !quake.ref
    %c66_i64 = arith.constant 66 : i64
    %133 = quake.extract_ref %0[%c66_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%132] %133 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_66 = arith.constant 0 : i64
    %134 = quake.extract_ref %0[%c0_i64_66] : (!quake.veq<100>, i64) -> !quake.ref
    %c67_i64 = arith.constant 67 : i64
    %135 = quake.extract_ref %0[%c67_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%134] %135 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_67 = arith.constant 0 : i64
    %136 = quake.extract_ref %0[%c0_i64_67] : (!quake.veq<100>, i64) -> !quake.ref
    %c68_i64 = arith.constant 68 : i64
    %137 = quake.extract_ref %0[%c68_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%136] %137 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_68 = arith.constant 0 : i64
    %138 = quake.extract_ref %0[%c0_i64_68] : (!quake.veq<100>, i64) -> !quake.ref
    %c69_i64 = arith.constant 69 : i64
    %139 = quake.extract_ref %0[%c69_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%138] %139 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_69 = arith.constant 0 : i64
    %140 = quake.extract_ref %0[%c0_i64_69] : (!quake.veq<100>, i64) -> !quake.ref
    %c70_i64 = arith.constant 70 : i64
    %141 = quake.extract_ref %0[%c70_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%140] %141 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_70 = arith.constant 0 : i64
    %142 = quake.extract_ref %0[%c0_i64_70] : (!quake.veq<100>, i64) -> !quake.ref
    %c71_i64 = arith.constant 71 : i64
    %143 = quake.extract_ref %0[%c71_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%142] %143 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_71 = arith.constant 0 : i64
    %144 = quake.extract_ref %0[%c0_i64_71] : (!quake.veq<100>, i64) -> !quake.ref
    %c72_i64 = arith.constant 72 : i64
    %145 = quake.extract_ref %0[%c72_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%144] %145 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_72 = arith.constant 0 : i64
    %146 = quake.extract_ref %0[%c0_i64_72] : (!quake.veq<100>, i64) -> !quake.ref
    %c73_i64 = arith.constant 73 : i64
    %147 = quake.extract_ref %0[%c73_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%146] %147 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_73 = arith.constant 0 : i64
    %148 = quake.extract_ref %0[%c0_i64_73] : (!quake.veq<100>, i64) -> !quake.ref
    %c74_i64 = arith.constant 74 : i64
    %149 = quake.extract_ref %0[%c74_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%148] %149 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_74 = arith.constant 0 : i64
    %150 = quake.extract_ref %0[%c0_i64_74] : (!quake.veq<100>, i64) -> !quake.ref
    %c75_i64 = arith.constant 75 : i64
    %151 = quake.extract_ref %0[%c75_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%150] %151 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_75 = arith.constant 0 : i64
    %152 = quake.extract_ref %0[%c0_i64_75] : (!quake.veq<100>, i64) -> !quake.ref
    %c76_i64 = arith.constant 76 : i64
    %153 = quake.extract_ref %0[%c76_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%152] %153 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_76 = arith.constant 0 : i64
    %154 = quake.extract_ref %0[%c0_i64_76] : (!quake.veq<100>, i64) -> !quake.ref
    %c77_i64 = arith.constant 77 : i64
    %155 = quake.extract_ref %0[%c77_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%154] %155 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_77 = arith.constant 0 : i64
    %156 = quake.extract_ref %0[%c0_i64_77] : (!quake.veq<100>, i64) -> !quake.ref
    %c78_i64 = arith.constant 78 : i64
    %157 = quake.extract_ref %0[%c78_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%156] %157 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_78 = arith.constant 0 : i64
    %158 = quake.extract_ref %0[%c0_i64_78] : (!quake.veq<100>, i64) -> !quake.ref
    %c79_i64 = arith.constant 79 : i64
    %159 = quake.extract_ref %0[%c79_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%158] %159 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_79 = arith.constant 0 : i64
    %160 = quake.extract_ref %0[%c0_i64_79] : (!quake.veq<100>, i64) -> !quake.ref
    %c80_i64 = arith.constant 80 : i64
    %161 = quake.extract_ref %0[%c80_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%160] %161 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_80 = arith.constant 0 : i64
    %162 = quake.extract_ref %0[%c0_i64_80] : (!quake.veq<100>, i64) -> !quake.ref
    %c81_i64 = arith.constant 81 : i64
    %163 = quake.extract_ref %0[%c81_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%162] %163 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_81 = arith.constant 0 : i64
    %164 = quake.extract_ref %0[%c0_i64_81] : (!quake.veq<100>, i64) -> !quake.ref
    %c82_i64 = arith.constant 82 : i64
    %165 = quake.extract_ref %0[%c82_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%164] %165 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_82 = arith.constant 0 : i64
    %166 = quake.extract_ref %0[%c0_i64_82] : (!quake.veq<100>, i64) -> !quake.ref
    %c83_i64 = arith.constant 83 : i64
    %167 = quake.extract_ref %0[%c83_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%166] %167 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_83 = arith.constant 0 : i64
    %168 = quake.extract_ref %0[%c0_i64_83] : (!quake.veq<100>, i64) -> !quake.ref
    %c84_i64 = arith.constant 84 : i64
    %169 = quake.extract_ref %0[%c84_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%168] %169 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_84 = arith.constant 0 : i64
    %170 = quake.extract_ref %0[%c0_i64_84] : (!quake.veq<100>, i64) -> !quake.ref
    %c85_i64 = arith.constant 85 : i64
    %171 = quake.extract_ref %0[%c85_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%170] %171 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_85 = arith.constant 0 : i64
    %172 = quake.extract_ref %0[%c0_i64_85] : (!quake.veq<100>, i64) -> !quake.ref
    %c86_i64 = arith.constant 86 : i64
    %173 = quake.extract_ref %0[%c86_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%172] %173 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_86 = arith.constant 0 : i64
    %174 = quake.extract_ref %0[%c0_i64_86] : (!quake.veq<100>, i64) -> !quake.ref
    %c87_i64 = arith.constant 87 : i64
    %175 = quake.extract_ref %0[%c87_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%174] %175 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_87 = arith.constant 0 : i64
    %176 = quake.extract_ref %0[%c0_i64_87] : (!quake.veq<100>, i64) -> !quake.ref
    %c88_i64 = arith.constant 88 : i64
    %177 = quake.extract_ref %0[%c88_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%176] %177 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_88 = arith.constant 0 : i64
    %178 = quake.extract_ref %0[%c0_i64_88] : (!quake.veq<100>, i64) -> !quake.ref
    %c89_i64 = arith.constant 89 : i64
    %179 = quake.extract_ref %0[%c89_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%178] %179 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_89 = arith.constant 0 : i64
    %180 = quake.extract_ref %0[%c0_i64_89] : (!quake.veq<100>, i64) -> !quake.ref
    %c90_i64 = arith.constant 90 : i64
    %181 = quake.extract_ref %0[%c90_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%180] %181 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_90 = arith.constant 0 : i64
    %182 = quake.extract_ref %0[%c0_i64_90] : (!quake.veq<100>, i64) -> !quake.ref
    %c91_i64 = arith.constant 91 : i64
    %183 = quake.extract_ref %0[%c91_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%182] %183 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_91 = arith.constant 0 : i64
    %184 = quake.extract_ref %0[%c0_i64_91] : (!quake.veq<100>, i64) -> !quake.ref
    %c92_i64 = arith.constant 92 : i64
    %185 = quake.extract_ref %0[%c92_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%184] %185 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_92 = arith.constant 0 : i64
    %186 = quake.extract_ref %0[%c0_i64_92] : (!quake.veq<100>, i64) -> !quake.ref
    %c93_i64 = arith.constant 93 : i64
    %187 = quake.extract_ref %0[%c93_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%186] %187 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_93 = arith.constant 0 : i64
    %188 = quake.extract_ref %0[%c0_i64_93] : (!quake.veq<100>, i64) -> !quake.ref
    %c94_i64 = arith.constant 94 : i64
    %189 = quake.extract_ref %0[%c94_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%188] %189 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_94 = arith.constant 0 : i64
    %190 = quake.extract_ref %0[%c0_i64_94] : (!quake.veq<100>, i64) -> !quake.ref
    %c95_i64 = arith.constant 95 : i64
    %191 = quake.extract_ref %0[%c95_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%190] %191 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_95 = arith.constant 0 : i64
    %192 = quake.extract_ref %0[%c0_i64_95] : (!quake.veq<100>, i64) -> !quake.ref
    %c96_i64 = arith.constant 96 : i64
    %193 = quake.extract_ref %0[%c96_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%192] %193 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_96 = arith.constant 0 : i64
    %194 = quake.extract_ref %0[%c0_i64_96] : (!quake.veq<100>, i64) -> !quake.ref
    %c97_i64 = arith.constant 97 : i64
    %195 = quake.extract_ref %0[%c97_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%194] %195 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_97 = arith.constant 0 : i64
    %196 = quake.extract_ref %0[%c0_i64_97] : (!quake.veq<100>, i64) -> !quake.ref
    %c98_i64 = arith.constant 98 : i64
    %197 = quake.extract_ref %0[%c98_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%196] %197 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_98 = arith.constant 0 : i64
    %198 = quake.extract_ref %0[%c0_i64_98] : (!quake.veq<100>, i64) -> !quake.ref
    %c99_i64 = arith.constant 99 : i64
    %199 = quake.extract_ref %0[%c99_i64] : (!quake.veq<100>, i64) -> !quake.ref
    quake.x [%198] %199 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_99 = arith.constant 0 : i64
    %200 = quake.extract_ref %0[%c0_i64_99] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut = quake.mz %200 : (!quake.ref) -> !quake.measure
    %201 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_100 = arith.constant 1 : i64
    %202 = quake.extract_ref %0[%c1_i64_100] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_101 = quake.mz %202 : (!quake.ref) -> !quake.measure
    %203 = quake.discriminate %measOut_101 : (!quake.measure) -> i1
    %c2_i64_102 = arith.constant 2 : i64
    %204 = quake.extract_ref %0[%c2_i64_102] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_103 = quake.mz %204 : (!quake.ref) -> !quake.measure
    %205 = quake.discriminate %measOut_103 : (!quake.measure) -> i1
    %c3_i64_104 = arith.constant 3 : i64
    %206 = quake.extract_ref %0[%c3_i64_104] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_105 = quake.mz %206 : (!quake.ref) -> !quake.measure
    %207 = quake.discriminate %measOut_105 : (!quake.measure) -> i1
    %c4_i64_106 = arith.constant 4 : i64
    %208 = quake.extract_ref %0[%c4_i64_106] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_107 = quake.mz %208 : (!quake.ref) -> !quake.measure
    %209 = quake.discriminate %measOut_107 : (!quake.measure) -> i1
    %c5_i64_108 = arith.constant 5 : i64
    %210 = quake.extract_ref %0[%c5_i64_108] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_109 = quake.mz %210 : (!quake.ref) -> !quake.measure
    %211 = quake.discriminate %measOut_109 : (!quake.measure) -> i1
    %c6_i64_110 = arith.constant 6 : i64
    %212 = quake.extract_ref %0[%c6_i64_110] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_111 = quake.mz %212 : (!quake.ref) -> !quake.measure
    %213 = quake.discriminate %measOut_111 : (!quake.measure) -> i1
    %c7_i64_112 = arith.constant 7 : i64
    %214 = quake.extract_ref %0[%c7_i64_112] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_113 = quake.mz %214 : (!quake.ref) -> !quake.measure
    %215 = quake.discriminate %measOut_113 : (!quake.measure) -> i1
    %c8_i64_114 = arith.constant 8 : i64
    %216 = quake.extract_ref %0[%c8_i64_114] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_115 = quake.mz %216 : (!quake.ref) -> !quake.measure
    %217 = quake.discriminate %measOut_115 : (!quake.measure) -> i1
    %c9_i64_116 = arith.constant 9 : i64
    %218 = quake.extract_ref %0[%c9_i64_116] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_117 = quake.mz %218 : (!quake.ref) -> !quake.measure
    %219 = quake.discriminate %measOut_117 : (!quake.measure) -> i1
    %c10_i64_118 = arith.constant 10 : i64
    %220 = quake.extract_ref %0[%c10_i64_118] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_119 = quake.mz %220 : (!quake.ref) -> !quake.measure
    %221 = quake.discriminate %measOut_119 : (!quake.measure) -> i1
    %c11_i64_120 = arith.constant 11 : i64
    %222 = quake.extract_ref %0[%c11_i64_120] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_121 = quake.mz %222 : (!quake.ref) -> !quake.measure
    %223 = quake.discriminate %measOut_121 : (!quake.measure) -> i1
    %c12_i64_122 = arith.constant 12 : i64
    %224 = quake.extract_ref %0[%c12_i64_122] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_123 = quake.mz %224 : (!quake.ref) -> !quake.measure
    %225 = quake.discriminate %measOut_123 : (!quake.measure) -> i1
    %c13_i64_124 = arith.constant 13 : i64
    %226 = quake.extract_ref %0[%c13_i64_124] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_125 = quake.mz %226 : (!quake.ref) -> !quake.measure
    %227 = quake.discriminate %measOut_125 : (!quake.measure) -> i1
    %c14_i64_126 = arith.constant 14 : i64
    %228 = quake.extract_ref %0[%c14_i64_126] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_127 = quake.mz %228 : (!quake.ref) -> !quake.measure
    %229 = quake.discriminate %measOut_127 : (!quake.measure) -> i1
    %c15_i64_128 = arith.constant 15 : i64
    %230 = quake.extract_ref %0[%c15_i64_128] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_129 = quake.mz %230 : (!quake.ref) -> !quake.measure
    %231 = quake.discriminate %measOut_129 : (!quake.measure) -> i1
    %c16_i64_130 = arith.constant 16 : i64
    %232 = quake.extract_ref %0[%c16_i64_130] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_131 = quake.mz %232 : (!quake.ref) -> !quake.measure
    %233 = quake.discriminate %measOut_131 : (!quake.measure) -> i1
    %c17_i64_132 = arith.constant 17 : i64
    %234 = quake.extract_ref %0[%c17_i64_132] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_133 = quake.mz %234 : (!quake.ref) -> !quake.measure
    %235 = quake.discriminate %measOut_133 : (!quake.measure) -> i1
    %c18_i64_134 = arith.constant 18 : i64
    %236 = quake.extract_ref %0[%c18_i64_134] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_135 = quake.mz %236 : (!quake.ref) -> !quake.measure
    %237 = quake.discriminate %measOut_135 : (!quake.measure) -> i1
    %c19_i64_136 = arith.constant 19 : i64
    %238 = quake.extract_ref %0[%c19_i64_136] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_137 = quake.mz %238 : (!quake.ref) -> !quake.measure
    %239 = quake.discriminate %measOut_137 : (!quake.measure) -> i1
    %c20_i64_138 = arith.constant 20 : i64
    %240 = quake.extract_ref %0[%c20_i64_138] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_139 = quake.mz %240 : (!quake.ref) -> !quake.measure
    %241 = quake.discriminate %measOut_139 : (!quake.measure) -> i1
    %c21_i64_140 = arith.constant 21 : i64
    %242 = quake.extract_ref %0[%c21_i64_140] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_141 = quake.mz %242 : (!quake.ref) -> !quake.measure
    %243 = quake.discriminate %measOut_141 : (!quake.measure) -> i1
    %c22_i64_142 = arith.constant 22 : i64
    %244 = quake.extract_ref %0[%c22_i64_142] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_143 = quake.mz %244 : (!quake.ref) -> !quake.measure
    %245 = quake.discriminate %measOut_143 : (!quake.measure) -> i1
    %c23_i64_144 = arith.constant 23 : i64
    %246 = quake.extract_ref %0[%c23_i64_144] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_145 = quake.mz %246 : (!quake.ref) -> !quake.measure
    %247 = quake.discriminate %measOut_145 : (!quake.measure) -> i1
    %c24_i64_146 = arith.constant 24 : i64
    %248 = quake.extract_ref %0[%c24_i64_146] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_147 = quake.mz %248 : (!quake.ref) -> !quake.measure
    %249 = quake.discriminate %measOut_147 : (!quake.measure) -> i1
    %c25_i64_148 = arith.constant 25 : i64
    %250 = quake.extract_ref %0[%c25_i64_148] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_149 = quake.mz %250 : (!quake.ref) -> !quake.measure
    %251 = quake.discriminate %measOut_149 : (!quake.measure) -> i1
    %c26_i64_150 = arith.constant 26 : i64
    %252 = quake.extract_ref %0[%c26_i64_150] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_151 = quake.mz %252 : (!quake.ref) -> !quake.measure
    %253 = quake.discriminate %measOut_151 : (!quake.measure) -> i1
    %c27_i64_152 = arith.constant 27 : i64
    %254 = quake.extract_ref %0[%c27_i64_152] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_153 = quake.mz %254 : (!quake.ref) -> !quake.measure
    %255 = quake.discriminate %measOut_153 : (!quake.measure) -> i1
    %c28_i64_154 = arith.constant 28 : i64
    %256 = quake.extract_ref %0[%c28_i64_154] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_155 = quake.mz %256 : (!quake.ref) -> !quake.measure
    %257 = quake.discriminate %measOut_155 : (!quake.measure) -> i1
    %c29_i64_156 = arith.constant 29 : i64
    %258 = quake.extract_ref %0[%c29_i64_156] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_157 = quake.mz %258 : (!quake.ref) -> !quake.measure
    %259 = quake.discriminate %measOut_157 : (!quake.measure) -> i1
    %c30_i64_158 = arith.constant 30 : i64
    %260 = quake.extract_ref %0[%c30_i64_158] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_159 = quake.mz %260 : (!quake.ref) -> !quake.measure
    %261 = quake.discriminate %measOut_159 : (!quake.measure) -> i1
    %c31_i64_160 = arith.constant 31 : i64
    %262 = quake.extract_ref %0[%c31_i64_160] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_161 = quake.mz %262 : (!quake.ref) -> !quake.measure
    %263 = quake.discriminate %measOut_161 : (!quake.measure) -> i1
    %c32_i64_162 = arith.constant 32 : i64
    %264 = quake.extract_ref %0[%c32_i64_162] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_163 = quake.mz %264 : (!quake.ref) -> !quake.measure
    %265 = quake.discriminate %measOut_163 : (!quake.measure) -> i1
    %c33_i64_164 = arith.constant 33 : i64
    %266 = quake.extract_ref %0[%c33_i64_164] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_165 = quake.mz %266 : (!quake.ref) -> !quake.measure
    %267 = quake.discriminate %measOut_165 : (!quake.measure) -> i1
    %c34_i64_166 = arith.constant 34 : i64
    %268 = quake.extract_ref %0[%c34_i64_166] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_167 = quake.mz %268 : (!quake.ref) -> !quake.measure
    %269 = quake.discriminate %measOut_167 : (!quake.measure) -> i1
    %c35_i64_168 = arith.constant 35 : i64
    %270 = quake.extract_ref %0[%c35_i64_168] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_169 = quake.mz %270 : (!quake.ref) -> !quake.measure
    %271 = quake.discriminate %measOut_169 : (!quake.measure) -> i1
    %c36_i64_170 = arith.constant 36 : i64
    %272 = quake.extract_ref %0[%c36_i64_170] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_171 = quake.mz %272 : (!quake.ref) -> !quake.measure
    %273 = quake.discriminate %measOut_171 : (!quake.measure) -> i1
    %c37_i64_172 = arith.constant 37 : i64
    %274 = quake.extract_ref %0[%c37_i64_172] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_173 = quake.mz %274 : (!quake.ref) -> !quake.measure
    %275 = quake.discriminate %measOut_173 : (!quake.measure) -> i1
    %c38_i64_174 = arith.constant 38 : i64
    %276 = quake.extract_ref %0[%c38_i64_174] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_175 = quake.mz %276 : (!quake.ref) -> !quake.measure
    %277 = quake.discriminate %measOut_175 : (!quake.measure) -> i1
    %c39_i64_176 = arith.constant 39 : i64
    %278 = quake.extract_ref %0[%c39_i64_176] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_177 = quake.mz %278 : (!quake.ref) -> !quake.measure
    %279 = quake.discriminate %measOut_177 : (!quake.measure) -> i1
    %c40_i64_178 = arith.constant 40 : i64
    %280 = quake.extract_ref %0[%c40_i64_178] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_179 = quake.mz %280 : (!quake.ref) -> !quake.measure
    %281 = quake.discriminate %measOut_179 : (!quake.measure) -> i1
    %c41_i64_180 = arith.constant 41 : i64
    %282 = quake.extract_ref %0[%c41_i64_180] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_181 = quake.mz %282 : (!quake.ref) -> !quake.measure
    %283 = quake.discriminate %measOut_181 : (!quake.measure) -> i1
    %c42_i64_182 = arith.constant 42 : i64
    %284 = quake.extract_ref %0[%c42_i64_182] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_183 = quake.mz %284 : (!quake.ref) -> !quake.measure
    %285 = quake.discriminate %measOut_183 : (!quake.measure) -> i1
    %c43_i64_184 = arith.constant 43 : i64
    %286 = quake.extract_ref %0[%c43_i64_184] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_185 = quake.mz %286 : (!quake.ref) -> !quake.measure
    %287 = quake.discriminate %measOut_185 : (!quake.measure) -> i1
    %c44_i64_186 = arith.constant 44 : i64
    %288 = quake.extract_ref %0[%c44_i64_186] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_187 = quake.mz %288 : (!quake.ref) -> !quake.measure
    %289 = quake.discriminate %measOut_187 : (!quake.measure) -> i1
    %c45_i64_188 = arith.constant 45 : i64
    %290 = quake.extract_ref %0[%c45_i64_188] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_189 = quake.mz %290 : (!quake.ref) -> !quake.measure
    %291 = quake.discriminate %measOut_189 : (!quake.measure) -> i1
    %c46_i64_190 = arith.constant 46 : i64
    %292 = quake.extract_ref %0[%c46_i64_190] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_191 = quake.mz %292 : (!quake.ref) -> !quake.measure
    %293 = quake.discriminate %measOut_191 : (!quake.measure) -> i1
    %c47_i64_192 = arith.constant 47 : i64
    %294 = quake.extract_ref %0[%c47_i64_192] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_193 = quake.mz %294 : (!quake.ref) -> !quake.measure
    %295 = quake.discriminate %measOut_193 : (!quake.measure) -> i1
    %c48_i64_194 = arith.constant 48 : i64
    %296 = quake.extract_ref %0[%c48_i64_194] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_195 = quake.mz %296 : (!quake.ref) -> !quake.measure
    %297 = quake.discriminate %measOut_195 : (!quake.measure) -> i1
    %c49_i64_196 = arith.constant 49 : i64
    %298 = quake.extract_ref %0[%c49_i64_196] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_197 = quake.mz %298 : (!quake.ref) -> !quake.measure
    %299 = quake.discriminate %measOut_197 : (!quake.measure) -> i1
    %c50_i64_198 = arith.constant 50 : i64
    %300 = quake.extract_ref %0[%c50_i64_198] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_199 = quake.mz %300 : (!quake.ref) -> !quake.measure
    %301 = quake.discriminate %measOut_199 : (!quake.measure) -> i1
    %c51_i64_200 = arith.constant 51 : i64
    %302 = quake.extract_ref %0[%c51_i64_200] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_201 = quake.mz %302 : (!quake.ref) -> !quake.measure
    %303 = quake.discriminate %measOut_201 : (!quake.measure) -> i1
    %c52_i64_202 = arith.constant 52 : i64
    %304 = quake.extract_ref %0[%c52_i64_202] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_203 = quake.mz %304 : (!quake.ref) -> !quake.measure
    %305 = quake.discriminate %measOut_203 : (!quake.measure) -> i1
    %c53_i64_204 = arith.constant 53 : i64
    %306 = quake.extract_ref %0[%c53_i64_204] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_205 = quake.mz %306 : (!quake.ref) -> !quake.measure
    %307 = quake.discriminate %measOut_205 : (!quake.measure) -> i1
    %c54_i64_206 = arith.constant 54 : i64
    %308 = quake.extract_ref %0[%c54_i64_206] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_207 = quake.mz %308 : (!quake.ref) -> !quake.measure
    %309 = quake.discriminate %measOut_207 : (!quake.measure) -> i1
    %c55_i64_208 = arith.constant 55 : i64
    %310 = quake.extract_ref %0[%c55_i64_208] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_209 = quake.mz %310 : (!quake.ref) -> !quake.measure
    %311 = quake.discriminate %measOut_209 : (!quake.measure) -> i1
    %c56_i64_210 = arith.constant 56 : i64
    %312 = quake.extract_ref %0[%c56_i64_210] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_211 = quake.mz %312 : (!quake.ref) -> !quake.measure
    %313 = quake.discriminate %measOut_211 : (!quake.measure) -> i1
    %c57_i64_212 = arith.constant 57 : i64
    %314 = quake.extract_ref %0[%c57_i64_212] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_213 = quake.mz %314 : (!quake.ref) -> !quake.measure
    %315 = quake.discriminate %measOut_213 : (!quake.measure) -> i1
    %c58_i64_214 = arith.constant 58 : i64
    %316 = quake.extract_ref %0[%c58_i64_214] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_215 = quake.mz %316 : (!quake.ref) -> !quake.measure
    %317 = quake.discriminate %measOut_215 : (!quake.measure) -> i1
    %c59_i64_216 = arith.constant 59 : i64
    %318 = quake.extract_ref %0[%c59_i64_216] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_217 = quake.mz %318 : (!quake.ref) -> !quake.measure
    %319 = quake.discriminate %measOut_217 : (!quake.measure) -> i1
    %c60_i64_218 = arith.constant 60 : i64
    %320 = quake.extract_ref %0[%c60_i64_218] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_219 = quake.mz %320 : (!quake.ref) -> !quake.measure
    %321 = quake.discriminate %measOut_219 : (!quake.measure) -> i1
    %c61_i64_220 = arith.constant 61 : i64
    %322 = quake.extract_ref %0[%c61_i64_220] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_221 = quake.mz %322 : (!quake.ref) -> !quake.measure
    %323 = quake.discriminate %measOut_221 : (!quake.measure) -> i1
    %c62_i64_222 = arith.constant 62 : i64
    %324 = quake.extract_ref %0[%c62_i64_222] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_223 = quake.mz %324 : (!quake.ref) -> !quake.measure
    %325 = quake.discriminate %measOut_223 : (!quake.measure) -> i1
    %c63_i64_224 = arith.constant 63 : i64
    %326 = quake.extract_ref %0[%c63_i64_224] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_225 = quake.mz %326 : (!quake.ref) -> !quake.measure
    %327 = quake.discriminate %measOut_225 : (!quake.measure) -> i1
    %c64_i64_226 = arith.constant 64 : i64
    %328 = quake.extract_ref %0[%c64_i64_226] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_227 = quake.mz %328 : (!quake.ref) -> !quake.measure
    %329 = quake.discriminate %measOut_227 : (!quake.measure) -> i1
    %c65_i64_228 = arith.constant 65 : i64
    %330 = quake.extract_ref %0[%c65_i64_228] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_229 = quake.mz %330 : (!quake.ref) -> !quake.measure
    %331 = quake.discriminate %measOut_229 : (!quake.measure) -> i1
    %c66_i64_230 = arith.constant 66 : i64
    %332 = quake.extract_ref %0[%c66_i64_230] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_231 = quake.mz %332 : (!quake.ref) -> !quake.measure
    %333 = quake.discriminate %measOut_231 : (!quake.measure) -> i1
    %c67_i64_232 = arith.constant 67 : i64
    %334 = quake.extract_ref %0[%c67_i64_232] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_233 = quake.mz %334 : (!quake.ref) -> !quake.measure
    %335 = quake.discriminate %measOut_233 : (!quake.measure) -> i1
    %c68_i64_234 = arith.constant 68 : i64
    %336 = quake.extract_ref %0[%c68_i64_234] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_235 = quake.mz %336 : (!quake.ref) -> !quake.measure
    %337 = quake.discriminate %measOut_235 : (!quake.measure) -> i1
    %c69_i64_236 = arith.constant 69 : i64
    %338 = quake.extract_ref %0[%c69_i64_236] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_237 = quake.mz %338 : (!quake.ref) -> !quake.measure
    %339 = quake.discriminate %measOut_237 : (!quake.measure) -> i1
    %c70_i64_238 = arith.constant 70 : i64
    %340 = quake.extract_ref %0[%c70_i64_238] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_239 = quake.mz %340 : (!quake.ref) -> !quake.measure
    %341 = quake.discriminate %measOut_239 : (!quake.measure) -> i1
    %c71_i64_240 = arith.constant 71 : i64
    %342 = quake.extract_ref %0[%c71_i64_240] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_241 = quake.mz %342 : (!quake.ref) -> !quake.measure
    %343 = quake.discriminate %measOut_241 : (!quake.measure) -> i1
    %c72_i64_242 = arith.constant 72 : i64
    %344 = quake.extract_ref %0[%c72_i64_242] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_243 = quake.mz %344 : (!quake.ref) -> !quake.measure
    %345 = quake.discriminate %measOut_243 : (!quake.measure) -> i1
    %c73_i64_244 = arith.constant 73 : i64
    %346 = quake.extract_ref %0[%c73_i64_244] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_245 = quake.mz %346 : (!quake.ref) -> !quake.measure
    %347 = quake.discriminate %measOut_245 : (!quake.measure) -> i1
    %c74_i64_246 = arith.constant 74 : i64
    %348 = quake.extract_ref %0[%c74_i64_246] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_247 = quake.mz %348 : (!quake.ref) -> !quake.measure
    %349 = quake.discriminate %measOut_247 : (!quake.measure) -> i1
    %c75_i64_248 = arith.constant 75 : i64
    %350 = quake.extract_ref %0[%c75_i64_248] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_249 = quake.mz %350 : (!quake.ref) -> !quake.measure
    %351 = quake.discriminate %measOut_249 : (!quake.measure) -> i1
    %c76_i64_250 = arith.constant 76 : i64
    %352 = quake.extract_ref %0[%c76_i64_250] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_251 = quake.mz %352 : (!quake.ref) -> !quake.measure
    %353 = quake.discriminate %measOut_251 : (!quake.measure) -> i1
    %c77_i64_252 = arith.constant 77 : i64
    %354 = quake.extract_ref %0[%c77_i64_252] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_253 = quake.mz %354 : (!quake.ref) -> !quake.measure
    %355 = quake.discriminate %measOut_253 : (!quake.measure) -> i1
    %c78_i64_254 = arith.constant 78 : i64
    %356 = quake.extract_ref %0[%c78_i64_254] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_255 = quake.mz %356 : (!quake.ref) -> !quake.measure
    %357 = quake.discriminate %measOut_255 : (!quake.measure) -> i1
    %c79_i64_256 = arith.constant 79 : i64
    %358 = quake.extract_ref %0[%c79_i64_256] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_257 = quake.mz %358 : (!quake.ref) -> !quake.measure
    %359 = quake.discriminate %measOut_257 : (!quake.measure) -> i1
    %c80_i64_258 = arith.constant 80 : i64
    %360 = quake.extract_ref %0[%c80_i64_258] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_259 = quake.mz %360 : (!quake.ref) -> !quake.measure
    %361 = quake.discriminate %measOut_259 : (!quake.measure) -> i1
    %c81_i64_260 = arith.constant 81 : i64
    %362 = quake.extract_ref %0[%c81_i64_260] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_261 = quake.mz %362 : (!quake.ref) -> !quake.measure
    %363 = quake.discriminate %measOut_261 : (!quake.measure) -> i1
    %c82_i64_262 = arith.constant 82 : i64
    %364 = quake.extract_ref %0[%c82_i64_262] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_263 = quake.mz %364 : (!quake.ref) -> !quake.measure
    %365 = quake.discriminate %measOut_263 : (!quake.measure) -> i1
    %c83_i64_264 = arith.constant 83 : i64
    %366 = quake.extract_ref %0[%c83_i64_264] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_265 = quake.mz %366 : (!quake.ref) -> !quake.measure
    %367 = quake.discriminate %measOut_265 : (!quake.measure) -> i1
    %c84_i64_266 = arith.constant 84 : i64
    %368 = quake.extract_ref %0[%c84_i64_266] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_267 = quake.mz %368 : (!quake.ref) -> !quake.measure
    %369 = quake.discriminate %measOut_267 : (!quake.measure) -> i1
    %c85_i64_268 = arith.constant 85 : i64
    %370 = quake.extract_ref %0[%c85_i64_268] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_269 = quake.mz %370 : (!quake.ref) -> !quake.measure
    %371 = quake.discriminate %measOut_269 : (!quake.measure) -> i1
    %c86_i64_270 = arith.constant 86 : i64
    %372 = quake.extract_ref %0[%c86_i64_270] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_271 = quake.mz %372 : (!quake.ref) -> !quake.measure
    %373 = quake.discriminate %measOut_271 : (!quake.measure) -> i1
    %c87_i64_272 = arith.constant 87 : i64
    %374 = quake.extract_ref %0[%c87_i64_272] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_273 = quake.mz %374 : (!quake.ref) -> !quake.measure
    %375 = quake.discriminate %measOut_273 : (!quake.measure) -> i1
    %c88_i64_274 = arith.constant 88 : i64
    %376 = quake.extract_ref %0[%c88_i64_274] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_275 = quake.mz %376 : (!quake.ref) -> !quake.measure
    %377 = quake.discriminate %measOut_275 : (!quake.measure) -> i1
    %c89_i64_276 = arith.constant 89 : i64
    %378 = quake.extract_ref %0[%c89_i64_276] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_277 = quake.mz %378 : (!quake.ref) -> !quake.measure
    %379 = quake.discriminate %measOut_277 : (!quake.measure) -> i1
    %c90_i64_278 = arith.constant 90 : i64
    %380 = quake.extract_ref %0[%c90_i64_278] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_279 = quake.mz %380 : (!quake.ref) -> !quake.measure
    %381 = quake.discriminate %measOut_279 : (!quake.measure) -> i1
    %c91_i64_280 = arith.constant 91 : i64
    %382 = quake.extract_ref %0[%c91_i64_280] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_281 = quake.mz %382 : (!quake.ref) -> !quake.measure
    %383 = quake.discriminate %measOut_281 : (!quake.measure) -> i1
    %c92_i64_282 = arith.constant 92 : i64
    %384 = quake.extract_ref %0[%c92_i64_282] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_283 = quake.mz %384 : (!quake.ref) -> !quake.measure
    %385 = quake.discriminate %measOut_283 : (!quake.measure) -> i1
    %c93_i64_284 = arith.constant 93 : i64
    %386 = quake.extract_ref %0[%c93_i64_284] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_285 = quake.mz %386 : (!quake.ref) -> !quake.measure
    %387 = quake.discriminate %measOut_285 : (!quake.measure) -> i1
    %c94_i64_286 = arith.constant 94 : i64
    %388 = quake.extract_ref %0[%c94_i64_286] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_287 = quake.mz %388 : (!quake.ref) -> !quake.measure
    %389 = quake.discriminate %measOut_287 : (!quake.measure) -> i1
    %c95_i64_288 = arith.constant 95 : i64
    %390 = quake.extract_ref %0[%c95_i64_288] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_289 = quake.mz %390 : (!quake.ref) -> !quake.measure
    %391 = quake.discriminate %measOut_289 : (!quake.measure) -> i1
    %c96_i64_290 = arith.constant 96 : i64
    %392 = quake.extract_ref %0[%c96_i64_290] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_291 = quake.mz %392 : (!quake.ref) -> !quake.measure
    %393 = quake.discriminate %measOut_291 : (!quake.measure) -> i1
    %c97_i64_292 = arith.constant 97 : i64
    %394 = quake.extract_ref %0[%c97_i64_292] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_293 = quake.mz %394 : (!quake.ref) -> !quake.measure
    %395 = quake.discriminate %measOut_293 : (!quake.measure) -> i1
    %c98_i64_294 = arith.constant 98 : i64
    %396 = quake.extract_ref %0[%c98_i64_294] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_295 = quake.mz %396 : (!quake.ref) -> !quake.measure
    %397 = quake.discriminate %measOut_295 : (!quake.measure) -> i1
    %c99_i64_296 = arith.constant 99 : i64
    %398 = quake.extract_ref %0[%c99_i64_296] : (!quake.veq<100>, i64) -> !quake.ref
    %measOut_297 = quake.mz %398 : (!quake.ref) -> !quake.measure
    %399 = quake.discriminate %measOut_297 : (!quake.measure) -> i1
    return
  }
}
```

## QIR (LLVM IR via cudaq.translate)

```llvm
; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"

%Array = type opaque
%Qubit = type opaque
%Result = type opaque

define void @__nvqpp__mlirgen____nvqppBuilderKernel_4RIYR1Q4F7() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 100)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__h(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %5)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %7)
  %8 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 3)
  %9 = load %Qubit*, %Qubit** %8, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %9)
  %10 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 4)
  %11 = load %Qubit*, %Qubit** %10, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %11)
  %12 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 5)
  %13 = load %Qubit*, %Qubit** %12, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %13)
  %14 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 6)
  %15 = load %Qubit*, %Qubit** %14, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %15)
  %16 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 7)
  %17 = load %Qubit*, %Qubit** %16, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %17)
  %18 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 8)
  %19 = load %Qubit*, %Qubit** %18, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %19)
  %20 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 9)
  %21 = load %Qubit*, %Qubit** %20, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %21)
  %22 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 10)
  %23 = load %Qubit*, %Qubit** %22, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %23)
  %24 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 11)
  %25 = load %Qubit*, %Qubit** %24, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %25)
  %26 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 12)
  %27 = load %Qubit*, %Qubit** %26, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %27)
  %28 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 13)
  %29 = load %Qubit*, %Qubit** %28, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %29)
  %30 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 14)
  %31 = load %Qubit*, %Qubit** %30, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %31)
  %32 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 15)
  %33 = load %Qubit*, %Qubit** %32, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %33)
  %34 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 16)
  %35 = load %Qubit*, %Qubit** %34, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %35)
  %36 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 17)
  %37 = load %Qubit*, %Qubit** %36, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %37)
  %38 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 18)
  %39 = load %Qubit*, %Qubit** %38, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %39)
  %40 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 19)
  %41 = load %Qubit*, %Qubit** %40, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %41)
  %42 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 20)
  %43 = load %Qubit*, %Qubit** %42, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %43)
  %44 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 21)
  %45 = load %Qubit*, %Qubit** %44, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %45)
  %46 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 22)
  %47 = load %Qubit*, %Qubit** %46, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %47)
  %48 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 23)
  %49 = load %Qubit*, %Qubit** %48, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %49)
  %50 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 24)
  %51 = load %Qubit*, %Qubit** %50, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %51)
  %52 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 25)
  %53 = load %Qubit*, %Qubit** %52, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %53)
  %54 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 26)
  %55 = load %Qubit*, %Qubit** %54, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %55)
  %56 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 27)
  %57 = load %Qubit*, %Qubit** %56, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %57)
  %58 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 28)
  %59 = load %Qubit*, %Qubit** %58, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %59)
  %60 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 29)
  %61 = load %Qubit*, %Qubit** %60, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %61)
  %62 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 30)
  %63 = load %Qubit*, %Qubit** %62, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %63)
  %64 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 31)
  %65 = load %Qubit*, %Qubit** %64, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %65)
  %66 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 32)
  %67 = load %Qubit*, %Qubit** %66, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %67)
  %68 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 33)
  %69 = load %Qubit*, %Qubit** %68, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %69)
  %70 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 34)
  %71 = load %Qubit*, %Qubit** %70, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %71)
  %72 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 35)
  %73 = load %Qubit*, %Qubit** %72, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %73)
  %74 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 36)
  %75 = load %Qubit*, %Qubit** %74, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %75)
  %76 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 37)
  %77 = load %Qubit*, %Qubit** %76, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %77)
  %78 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 38)
  %79 = load %Qubit*, %Qubit** %78, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %79)
  %80 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 39)
  %81 = load %Qubit*, %Qubit** %80, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %81)
  %82 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 40)
  %83 = load %Qubit*, %Qubit** %82, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %83)
  %84 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 41)
  %85 = load %Qubit*, %Qubit** %84, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %85)
  %86 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 42)
  %87 = load %Qubit*, %Qubit** %86, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %87)
  %88 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 43)
  %89 = load %Qubit*, %Qubit** %88, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %89)
  %90 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 44)
  %91 = load %Qubit*, %Qubit** %90, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %91)
  %92 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 45)
  %93 = load %Qubit*, %Qubit** %92, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %93)
  %94 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 46)
  %95 = load %Qubit*, %Qubit** %94, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %95)
  %96 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 47)
  %97 = load %Qubit*, %Qubit** %96, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %97)
  %98 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 48)
  %99 = load %Qubit*, %Qubit** %98, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %99)
  %100 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 49)
  %101 = load %Qubit*, %Qubit** %100, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %101)
  %102 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 50)
  %103 = load %Qubit*, %Qubit** %102, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %103)
  %104 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 51)
  %105 = load %Qubit*, %Qubit** %104, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %105)
  %106 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 52)
  %107 = load %Qubit*, %Qubit** %106, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %107)
  %108 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 53)
  %109 = load %Qubit*, %Qubit** %108, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %109)
  %110 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 54)
  %111 = load %Qubit*, %Qubit** %110, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %111)
  %112 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 55)
  %113 = load %Qubit*, %Qubit** %112, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %113)
  %114 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 56)
  %115 = load %Qubit*, %Qubit** %114, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %115)
  %116 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 57)
  %117 = load %Qubit*, %Qubit** %116, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %117)
  %118 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 58)
  %119 = load %Qubit*, %Qubit** %118, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %119)
  %120 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 59)
  %121 = load %Qubit*, %Qubit** %120, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %121)
  %122 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 60)
  %123 = load %Qubit*, %Qubit** %122, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %123)
  %124 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 61)
  %125 = load %Qubit*, %Qubit** %124, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %125)
  %126 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 62)
  %127 = load %Qubit*, %Qubit** %126, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %127)
  %128 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 63)
  %129 = load %Qubit*, %Qubit** %128, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %129)
  %130 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 64)
  %131 = load %Qubit*, %Qubit** %130, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %131)
  %132 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 65)
  %133 = load %Qubit*, %Qubit** %132, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %133)
  %134 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 66)
  %135 = load %Qubit*, %Qubit** %134, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %135)
  %136 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 67)
  %137 = load %Qubit*, %Qubit** %136, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %137)
  %138 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 68)
  %139 = load %Qubit*, %Qubit** %138, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %139)
  %140 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 69)
  %141 = load %Qubit*, %Qubit** %140, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %141)
  %142 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 70)
  %143 = load %Qubit*, %Qubit** %142, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %143)
  %144 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 71)
  %145 = load %Qubit*, %Qubit** %144, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %145)
  %146 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 72)
  %147 = load %Qubit*, %Qubit** %146, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %147)
  %148 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 73)
  %149 = load %Qubit*, %Qubit** %148, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %149)
  %150 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 74)
  %151 = load %Qubit*, %Qubit** %150, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %151)
  %152 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 75)
  %153 = load %Qubit*, %Qubit** %152, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %153)
  %154 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 76)
  %155 = load %Qubit*, %Qubit** %154, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %155)
  %156 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 77)
  %157 = load %Qubit*, %Qubit** %156, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %157)
  %158 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 78)
  %159 = load %Qubit*, %Qubit** %158, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %159)
  %160 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 79)
  %161 = load %Qubit*, %Qubit** %160, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %161)
  %162 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 80)
  %163 = load %Qubit*, %Qubit** %162, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %163)
  %164 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 81)
  %165 = load %Qubit*, %Qubit** %164, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %165)
  %166 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 82)
  %167 = load %Qubit*, %Qubit** %166, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %167)
  %168 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 83)
  %169 = load %Qubit*, %Qubit** %168, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %169)
  %170 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 84)
  %171 = load %Qubit*, %Qubit** %170, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %171)
  %172 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 85)
  %173 = load %Qubit*, %Qubit** %172, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %173)
  %174 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 86)
  %175 = load %Qubit*, %Qubit** %174, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %175)
  %176 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 87)
  %177 = load %Qubit*, %Qubit** %176, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %177)
  %178 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 88)
  %179 = load %Qubit*, %Qubit** %178, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %179)
  %180 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 89)
  %181 = load %Qubit*, %Qubit** %180, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %181)
  %182 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 90)
  %183 = load %Qubit*, %Qubit** %182, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %183)
  %184 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 91)
  %185 = load %Qubit*, %Qubit** %184, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %185)
  %186 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 92)
  %187 = load %Qubit*, %Qubit** %186, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %187)
  %188 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 93)
  %189 = load %Qubit*, %Qubit** %188, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %189)
  %190 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 94)
  %191 = load %Qubit*, %Qubit** %190, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %191)
  %192 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 95)
  %193 = load %Qubit*, %Qubit** %192, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %193)
  %194 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 96)
  %195 = load %Qubit*, %Qubit** %194, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %195)
  %196 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 97)
  %197 = load %Qubit*, %Qubit** %196, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %197)
  %198 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 98)
  %199 = load %Qubit*, %Qubit** %198, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %199)
  %200 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 99)
  %201 = load %Qubit*, %Qubit** %200, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %201)
  %202 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %203 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  %204 = tail call %Result* @__quantum__qis__mz(%Qubit* %7)
  %205 = tail call %Result* @__quantum__qis__mz(%Qubit* %9)
  %206 = tail call %Result* @__quantum__qis__mz(%Qubit* %11)
  %207 = tail call %Result* @__quantum__qis__mz(%Qubit* %13)
  %208 = tail call %Result* @__quantum__qis__mz(%Qubit* %15)
  %209 = tail call %Result* @__quantum__qis__mz(%Qubit* %17)
  %210 = tail call %Result* @__quantum__qis__mz(%Qubit* %19)
  %211 = tail call %Result* @__quantum__qis__mz(%Qubit* %21)
  %212 = tail call %Result* @__quantum__qis__mz(%Qubit* %23)
  %213 = tail call %Result* @__quantum__qis__mz(%Qubit* %25)
  %214 = tail call %Result* @__quantum__qis__mz(%Qubit* %27)
  %215 = tail call %Result* @__quantum__qis__mz(%Qubit* %29)
  %216 = tail call %Result* @__quantum__qis__mz(%Qubit* %31)
  %217 = tail call %Result* @__quantum__qis__mz(%Qubit* %33)
  %218 = tail call %Result* @__quantum__qis__mz(%Qubit* %35)
  %219 = tail call %Result* @__quantum__qis__mz(%Qubit* %37)
  %220 = tail call %Result* @__quantum__qis__mz(%Qubit* %39)
  %221 = tail call %Result* @__quantum__qis__mz(%Qubit* %41)
  %222 = tail call %Result* @__quantum__qis__mz(%Qubit* %43)
  %223 = tail call %Result* @__quantum__qis__mz(%Qubit* %45)
  %224 = tail call %Result* @__quantum__qis__mz(%Qubit* %47)
  %225 = tail call %Result* @__quantum__qis__mz(%Qubit* %49)
  %226 = tail call %Result* @__quantum__qis__mz(%Qubit* %51)
  %227 = tail call %Result* @__quantum__qis__mz(%Qubit* %53)
  %228 = tail call %Result* @__quantum__qis__mz(%Qubit* %55)
  %229 = tail call %Result* @__quantum__qis__mz(%Qubit* %57)
  %230 = tail call %Result* @__quantum__qis__mz(%Qubit* %59)
  %231 = tail call %Result* @__quantum__qis__mz(%Qubit* %61)
  %232 = tail call %Result* @__quantum__qis__mz(%Qubit* %63)
  %233 = tail call %Result* @__quantum__qis__mz(%Qubit* %65)
  %234 = tail call %Result* @__quantum__qis__mz(%Qubit* %67)
  %235 = tail call %Result* @__quantum__qis__mz(%Qubit* %69)
  %236 = tail call %Result* @__quantum__qis__mz(%Qubit* %71)
  %237 = tail call %Result* @__quantum__qis__mz(%Qubit* %73)
  %238 = tail call %Result* @__quantum__qis__mz(%Qubit* %75)
  %239 = tail call %Result* @__quantum__qis__mz(%Qubit* %77)
  %240 = tail call %Result* @__quantum__qis__mz(%Qubit* %79)
  %241 = tail call %Result* @__quantum__qis__mz(%Qubit* %81)
  %242 = tail call %Result* @__quantum__qis__mz(%Qubit* %83)
  %243 = tail call %Result* @__quantum__qis__mz(%Qubit* %85)
  %244 = tail call %Result* @__quantum__qis__mz(%Qubit* %87)
  %245 = tail call %Result* @__quantum__qis__mz(%Qubit* %89)
  %246 = tail call %Result* @__quantum__qis__mz(%Qubit* %91)
  %247 = tail call %Result* @__quantum__qis__mz(%Qubit* %93)
  %248 = tail call %Result* @__quantum__qis__mz(%Qubit* %95)
  %249 = tail call %Result* @__quantum__qis__mz(%Qubit* %97)
  %250 = tail call %Result* @__quantum__qis__mz(%Qubit* %99)
  %251 = tail call %Result* @__quantum__qis__mz(%Qubit* %101)
  %252 = tail call %Result* @__quantum__qis__mz(%Qubit* %103)
  %253 = tail call %Result* @__quantum__qis__mz(%Qubit* %105)
  %254 = tail call %Result* @__quantum__qis__mz(%Qubit* %107)
  %255 = tail call %Result* @__quantum__qis__mz(%Qubit* %109)
  %256 = tail call %Result* @__quantum__qis__mz(%Qubit* %111)
  %257 = tail call %Result* @__quantum__qis__mz(%Qubit* %113)
  %258 = tail call %Result* @__quantum__qis__mz(%Qubit* %115)
  %259 = tail call %Result* @__quantum__qis__mz(%Qubit* %117)
  %260 = tail call %Result* @__quantum__qis__mz(%Qubit* %119)
  %261 = tail call %Result* @__quantum__qis__mz(%Qubit* %121)
  %262 = tail call %Result* @__quantum__qis__mz(%Qubit* %123)
  %263 = tail call %Result* @__quantum__qis__mz(%Qubit* %125)
  %264 = tail call %Result* @__quantum__qis__mz(%Qubit* %127)
  %265 = tail call %Result* @__quantum__qis__mz(%Qubit* %129)
  %266 = tail call %Result* @__quantum__qis__mz(%Qubit* %131)
  %267 = tail call %Result* @__quantum__qis__mz(%Qubit* %133)
  %268 = tail call %Result* @__quantum__qis__mz(%Qubit* %135)
  %269 = tail call %Result* @__quantum__qis__mz(%Qubit* %137)
  %270 = tail call %Result* @__quantum__qis__mz(%Qubit* %139)
  %271 = tail call %Result* @__quantum__qis__mz(%Qubit* %141)
  %272 = tail call %Result* @__quantum__qis__mz(%Qubit* %143)
  %273 = tail call %Result* @__quantum__qis__mz(%Qubit* %145)
  %274 = tail call %Result* @__quantum__qis__mz(%Qubit* %147)
  %275 = tail call %Result* @__quantum__qis__mz(%Qubit* %149)
  %276 = tail call %Result* @__quantum__qis__mz(%Qubit* %151)
  %277 = tail call %Result* @__quantum__qis__mz(%Qubit* %153)
  %278 = tail call %Result* @__quantum__qis__mz(%Qubit* %155)
  %279 = tail call %Result* @__quantum__qis__mz(%Qubit* %157)
  %280 = tail call %Result* @__quantum__qis__mz(%Qubit* %159)
  %281 = tail call %Result* @__quantum__qis__mz(%Qubit* %161)
  %282 = tail call %Result* @__quantum__qis__mz(%Qubit* %163)
  %283 = tail call %Result* @__quantum__qis__mz(%Qubit* %165)
  %284 = tail call %Result* @__quantum__qis__mz(%Qubit* %167)
  %285 = tail call %Result* @__quantum__qis__mz(%Qubit* %169)
  %286 = tail call %Result* @__quantum__qis__mz(%Qubit* %171)
  %287 = tail call %Result* @__quantum__qis__mz(%Qubit* %173)
  %288 = tail call %Result* @__quantum__qis__mz(%Qubit* %175)
  %289 = tail call %Result* @__quantum__qis__mz(%Qubit* %177)
  %290 = tail call %Result* @__quantum__qis__mz(%Qubit* %179)
  %291 = tail call %Result* @__quantum__qis__mz(%Qubit* %181)
  %292 = tail call %Result* @__quantum__qis__mz(%Qubit* %183)
  %293 = tail call %Result* @__quantum__qis__mz(%Qubit* %185)
  %294 = tail call %Result* @__quantum__qis__mz(%Qubit* %187)
  %295 = tail call %Result* @__quantum__qis__mz(%Qubit* %189)
  %296 = tail call %Result* @__quantum__qis__mz(%Qubit* %191)
  %297 = tail call %Result* @__quantum__qis__mz(%Qubit* %193)
  %298 = tail call %Result* @__quantum__qis__mz(%Qubit* %195)
  %299 = tail call %Result* @__quantum__qis__mz(%Qubit* %197)
  %300 = tail call %Result* @__quantum__qis__mz(%Qubit* %199)
  %301 = tail call %Result* @__quantum__qis__mz(%Qubit* %201)
  tail call void @__quantum__rt__qubit_release_array(%Array* %1)
  ret void
}

declare %Array* @__quantum__rt__qubit_allocate_array(i64) local_unnamed_addr

declare void @__quantum__rt__qubit_release_array(%Array*) local_unnamed_addr

declare %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array*, i64) local_unnamed_addr

declare void @__quantum__qis__x__ctl(%Array*, %Qubit*)

declare void @generalizedInvokeWithRotationsControlsTargets(i64, i64, i64, i64, i8*, ...) local_unnamed_addr

declare void @__quantum__qis__h(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
