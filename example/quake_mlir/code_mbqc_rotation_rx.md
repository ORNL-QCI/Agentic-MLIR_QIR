# Code Mbqc Rotation Rx

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[3] q;
bit[3] m;

h q[1];
h q[2];

cz q[0], q[1];
cz q[1], q[2];

h q[0];
m[0] = measure q[0];

rz(pi/4) q[1];
h q[1];
m[1] = measure q[1];

rx(-1.5707963) q[2];

if (m[0] == true) {
  x q[2];
}
if (m[1] == true) {
  z q[2];
}
m[2] = measure q[2];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9 = "__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<3>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %2 = quake.extract_ref %0[%c2_i64] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %2 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64] : (!quake.veq<3>, i64) -> !quake.ref
    %c1_i64_0 = arith.constant 1 : i64
    %4 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<3>, i64) -> !quake.ref
    quake.z [%3] %4 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_1 = arith.constant 1 : i64
    %5 = quake.extract_ref %0[%c1_i64_1] : (!quake.veq<3>, i64) -> !quake.ref
    %c2_i64_2 = arith.constant 2 : i64
    %6 = quake.extract_ref %0[%c2_i64_2] : (!quake.veq<3>, i64) -> !quake.ref
    quake.z [%5] %6 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut = quake.mz %8 : (!quake.ref) -> !quake.measure
    %9 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_5 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<3>, i64) -> !quake.ref
    %cst = arith.constant 0.78539816339744828 : f64
    quake.rz (%cst) %10 : (f64, !quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %11 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<3>, i64) -> !quake.ref
    quake.h %11 : (!quake.ref) -> ()
    %c1_i64_7 = arith.constant 1 : i64
    %12 = quake.extract_ref %0[%c1_i64_7] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_8 = quake.mz %12 : (!quake.ref) -> !quake.measure
    %13 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    %c2_i64_9 = arith.constant 2 : i64
    %14 = quake.extract_ref %0[%c2_i64_9] : (!quake.veq<3>, i64) -> !quake.ref
    %cst_10 = arith.constant -1.5707963 : f64
    quake.rx (%cst_10) %14 : (f64, !quake.ref) -> ()
    cc.if(%9) {
      %c2_i64_13 = arith.constant 2 : i64
      %17 = quake.extract_ref %0[%c2_i64_13] : (!quake.veq<3>, i64) -> !quake.ref
      quake.x %17 : (!quake.ref) -> ()
    }
    cc.if(%13) {
      %c2_i64_13 = arith.constant 2 : i64
      %17 = quake.extract_ref %0[%c2_i64_13] : (!quake.veq<3>, i64) -> !quake.ref
      quake.z %17 : (!quake.ref) -> ()
    }
    %c2_i64_11 = arith.constant 2 : i64
    %15 = quake.extract_ref %0[%c2_i64_11] : (!quake.veq<3>, i64) -> !quake.ref
    %measOut_12 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_K93IOH09F9() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 3)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__h(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void @__quantum__qis__h(%Qubit* %5)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %7, %Qubit* %3)
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %3, %Qubit* %5)
  tail call void @__quantum__qis__h(%Qubit* %7)
  %8 = tail call %Result* @__quantum__qis__mz(%Qubit* %7)
  %9 = bitcast %Result* %8 to i1*
  %10 = load i1, i1* %9, align 1
  tail call void @__quantum__qis__rz(double 0x3FE921FB54442D18, %Qubit* %3)
  tail call void @__quantum__qis__h(%Qubit* %3)
  %11 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %12 = bitcast %Result* %11 to i1*
  %13 = load i1, i1* %12, align 1
  tail call void @__quantum__qis__rx(double 0xBFF921FB4D12D84A, %Qubit* %5)
  br i1 %10, label %14, label %15

14:                                               ; preds = %0
  tail call void @__quantum__qis__x(%Qubit* %5)
  br label %15

15:                                               ; preds = %14, %0
  br i1 %13, label %16, label %17

16:                                               ; preds = %15
  tail call void @__quantum__qis__z(%Qubit* %5)
  br label %17

17:                                               ; preds = %16, %15
  %18 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  tail call void @__quantum__rt__qubit_release_array(%Array* %1)
  ret void
}

declare %Array* @__quantum__rt__qubit_allocate_array(i64) local_unnamed_addr

declare void @__quantum__rt__qubit_release_array(%Array*) local_unnamed_addr

declare %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array*, i64) local_unnamed_addr

declare void @__quantum__qis__z__ctl(%Array*, %Qubit*)

declare void @generalizedInvokeWithRotationsControlsTargets(i64, i64, i64, i64, i8*, ...) local_unnamed_addr

declare void @__quantum__qis__h(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__x(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__z(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__rx(double, %Qubit*) local_unnamed_addr

declare void @__quantum__qis__rz(double, %Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
