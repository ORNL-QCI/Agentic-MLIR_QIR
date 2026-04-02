# Code Random Circuit 1847

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[7] q;
bit[4] cb;

// Apply gates in sequence
t q[4];
z q[3];
cx q[0], q[4];
rz(2.53) q[5];
cz q[6], q[2];
h q[0];
x q[0];
cx q[2], q[3];
cx q[4], q[1];
cx q[5], q[2];

// Measure qubits 1, 4, 5, and 6 into cb
cb[0] = measure q[1];
cb[1] = measure q[4];
cb[2] = measure q[5];
cb[3] = measure q[6];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_4EST6TURAJ = "__nvqpp__mlirgen____nvqppBuilderKernel_4EST6TURAJ_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_4EST6TURAJ() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<7>
    %c4_i64 = arith.constant 4 : i64
    %1 = quake.extract_ref %0[%c4_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.t %1 : (!quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %2 = quake.extract_ref %0[%c3_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.z %2 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64] : (!quake.veq<7>, i64) -> !quake.ref
    %c4_i64_0 = arith.constant 4 : i64
    %4 = quake.extract_ref %0[%c4_i64_0] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%3] %4 : (!quake.ref, !quake.ref) -> ()
    %c5_i64 = arith.constant 5 : i64
    %5 = quake.extract_ref %0[%c5_i64] : (!quake.veq<7>, i64) -> !quake.ref
    %cst = arith.constant 2.530000e+00 : f64
    quake.rz (%cst) %5 : (f64, !quake.ref) -> ()
    %c6_i64 = arith.constant 6 : i64
    %6 = quake.extract_ref %0[%c6_i64] : (!quake.veq<7>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %7 = quake.extract_ref %0[%c2_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.z [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<7>, i64) -> !quake.ref
    quake.h %8 : (!quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %9 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x %9 : (!quake.ref) -> ()
    %c2_i64_3 = arith.constant 2 : i64
    %10 = quake.extract_ref %0[%c2_i64_3] : (!quake.veq<7>, i64) -> !quake.ref
    %c3_i64_4 = arith.constant 3 : i64
    %11 = quake.extract_ref %0[%c3_i64_4] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%10] %11 : (!quake.ref, !quake.ref) -> ()
    %c4_i64_5 = arith.constant 4 : i64
    %12 = quake.extract_ref %0[%c4_i64_5] : (!quake.veq<7>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %13 = quake.extract_ref %0[%c1_i64] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%12] %13 : (!quake.ref, !quake.ref) -> ()
    %c5_i64_6 = arith.constant 5 : i64
    %14 = quake.extract_ref %0[%c5_i64_6] : (!quake.veq<7>, i64) -> !quake.ref
    %c2_i64_7 = arith.constant 2 : i64
    %15 = quake.extract_ref %0[%c2_i64_7] : (!quake.veq<7>, i64) -> !quake.ref
    quake.x [%14] %15 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_8 = arith.constant 1 : i64
    %16 = quake.extract_ref %0[%c1_i64_8] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut = quake.mz %16 : (!quake.ref) -> !quake.measure
    %17 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c4_i64_9 = arith.constant 4 : i64
    %18 = quake.extract_ref %0[%c4_i64_9] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_10 = quake.mz %18 : (!quake.ref) -> !quake.measure
    %19 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    %c5_i64_11 = arith.constant 5 : i64
    %20 = quake.extract_ref %0[%c5_i64_11] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_12 = quake.mz %20 : (!quake.ref) -> !quake.measure
    %21 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
    %c6_i64_13 = arith.constant 6 : i64
    %22 = quake.extract_ref %0[%c6_i64_13] : (!quake.veq<7>, i64) -> !quake.ref
    %measOut_14 = quake.mz %22 : (!quake.ref) -> !quake.measure
    %23 = quake.discriminate %measOut_14 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_4EST6TURAJ() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 7)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 4)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__t(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 3)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void @__quantum__qis__z(%Qubit* %5)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %7, %Qubit* %3)
  %8 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 5)
  %9 = load %Qubit*, %Qubit** %8, align 8
  tail call void @__quantum__qis__rz(double 2.530000e+00, %Qubit* %9)
  %10 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 6)
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %13 = bitcast %Qubit** %12 to i8**
  %14 = load i8*, i8** %13, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %11, i8* %14)
  tail call void @__quantum__qis__h(%Qubit* %7)
  tail call void @__quantum__qis__x(%Qubit* %7)
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), i8* %14, %Qubit* %5)
  %15 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %16 = load %Qubit*, %Qubit** %15, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %16)
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %9, i8* %14)
  %17 = tail call %Result* @__quantum__qis__mz(%Qubit* %16)
  %18 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %19 = tail call %Result* @__quantum__qis__mz(%Qubit* %9)
  %20 = tail call %Result* @__quantum__qis__mz(%Qubit* %11)
  tail call void @__quantum__rt__qubit_release_array(%Array* %1)
  ret void
}

declare %Array* @__quantum__rt__qubit_allocate_array(i64) local_unnamed_addr

declare void @__quantum__rt__qubit_release_array(%Array*) local_unnamed_addr

declare %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array*, i64) local_unnamed_addr

declare void @__quantum__qis__x__ctl(%Array*, %Qubit*)

declare void @__quantum__qis__z__ctl(%Array*, %Qubit*)

declare void @generalizedInvokeWithRotationsControlsTargets(i64, i64, i64, i64, i8*, ...) local_unnamed_addr

declare void @__quantum__qis__h(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__x(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__z(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__t(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__rz(double, %Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
