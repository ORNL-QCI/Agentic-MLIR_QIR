# Code Random Circuit 6994

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[4] qb;
bit[4] cb;

// Apply gates in sequence
y qb[0];
t qb[3];
rx(1.72) qb[0];
cx qb[2], qb[0];
z qb[0];
h qb[1];
swap qb[0], qb[2];
y qb[1];
s qb[1];
s qb[3];

// Measure all qubits
cb[0] = measure qb[0];
cb[1] = measure qb[1];
cb[2] = measure qb[2];
cb[3] = measure qb[3];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS = "__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<4>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.y %1 : (!quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %2 = quake.extract_ref %0[%c3_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.t %2 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<4>, i64) -> !quake.ref
    %cst = arith.constant 1.720000e+00 : f64
    quake.rx (%cst) %3 : (f64, !quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %4 = quake.extract_ref %0[%c2_i64] : (!quake.veq<4>, i64) -> !quake.ref
    %c0_i64_1 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<4>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<4>, i64) -> !quake.ref
    quake.z %6 : (!quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %7 = quake.extract_ref %0[%c1_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<4>, i64) -> !quake.ref
    %c2_i64_4 = arith.constant 2 : i64
    %9 = quake.extract_ref %0[%c2_i64_4] : (!quake.veq<4>, i64) -> !quake.ref
    quake.swap %8, %9 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_5 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<4>, i64) -> !quake.ref
    quake.y %10 : (!quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %11 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<4>, i64) -> !quake.ref
    quake.s %11 : (!quake.ref) -> ()
    %c3_i64_7 = arith.constant 3 : i64
    %12 = quake.extract_ref %0[%c3_i64_7] : (!quake.veq<4>, i64) -> !quake.ref
    quake.s %12 : (!quake.ref) -> ()
    %c0_i64_8 = arith.constant 0 : i64
    %13 = quake.extract_ref %0[%c0_i64_8] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_9 = arith.constant 1 : i64
    %15 = quake.extract_ref %0[%c1_i64_9] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_10 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    %c2_i64_11 = arith.constant 2 : i64
    %17 = quake.extract_ref %0[%c2_i64_11] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_12 = quake.mz %17 : (!quake.ref) -> !quake.measure
    %18 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
    %c3_i64_13 = arith.constant 3 : i64
    %19 = quake.extract_ref %0[%c3_i64_13] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_14 = quake.mz %19 : (!quake.ref) -> !quake.measure
    %20 = quake.discriminate %measOut_14 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_AUGR21F7HS() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 4)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__y(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 3)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void @__quantum__qis__t(%Qubit* %5)
  tail call void @__quantum__qis__rx(double 1.720000e+00, %Qubit* %3)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %7, %Qubit* %3)
  tail call void @__quantum__qis__z(%Qubit* %3)
  %8 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %9 = load %Qubit*, %Qubit** %8, align 8
  tail call void @__quantum__qis__h(%Qubit* %9)
  tail call void @__quantum__qis__swap(%Qubit* %3, %Qubit* %7)
  tail call void @__quantum__qis__y(%Qubit* %9)
  tail call void @__quantum__qis__s(%Qubit* %9)
  tail call void @__quantum__qis__s(%Qubit* %5)
  %10 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %11 = tail call %Result* @__quantum__qis__mz(%Qubit* %9)
  %12 = tail call %Result* @__quantum__qis__mz(%Qubit* %7)
  %13 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  tail call void @__quantum__rt__qubit_release_array(%Array* %1)
  ret void
}

declare %Array* @__quantum__rt__qubit_allocate_array(i64) local_unnamed_addr

declare void @__quantum__rt__qubit_release_array(%Array*) local_unnamed_addr

declare %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array*, i64) local_unnamed_addr

declare void @__quantum__qis__x__ctl(%Array*, %Qubit*)

declare void @generalizedInvokeWithRotationsControlsTargets(i64, i64, i64, i64, i8*, ...) local_unnamed_addr

declare void @__quantum__qis__h(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__y(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__z(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__s(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__t(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__swap(%Qubit*, %Qubit*) local_unnamed_addr

declare void @__quantum__qis__rx(double, %Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
