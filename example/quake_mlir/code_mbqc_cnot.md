# Code Mbqc Cnot

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[4] q;
bit[3] m;

h q[2];
h q[3];

cz q[0], q[2];
cz q[1], q[2];
cz q[2], q[3];

h q[1];
m[0] = measure q[1];

h q[2];
m[1] = measure q[2];

if (m[0] == true) {
  z q[0];
}
if (m[1] == true) {
  x q[3];
}
if (m[0] == true) {
  z q[3];
}
m[2] = measure q[3];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_IPKO5YG98P = "__nvqpp__mlirgen____nvqppBuilderKernel_IPKO5YG98P_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_IPKO5YG98P() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<4>
    %c2_i64 = arith.constant 2 : i64
    %1 = quake.extract_ref %0[%c2_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %2 = quake.extract_ref %0[%c3_i64] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %2 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %3 = quake.extract_ref %0[%c0_i64] : (!quake.veq<4>, i64) -> !quake.ref
    %c2_i64_0 = arith.constant 2 : i64
    %4 = quake.extract_ref %0[%c2_i64_0] : (!quake.veq<4>, i64) -> !quake.ref
    quake.z [%3] %4 : (!quake.ref, !quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %5 = quake.extract_ref %0[%c1_i64] : (!quake.veq<4>, i64) -> !quake.ref
    %c2_i64_1 = arith.constant 2 : i64
    %6 = quake.extract_ref %0[%c2_i64_1] : (!quake.veq<4>, i64) -> !quake.ref
    quake.z [%5] %6 : (!quake.ref, !quake.ref) -> ()
    %c2_i64_2 = arith.constant 2 : i64
    %7 = quake.extract_ref %0[%c2_i64_2] : (!quake.veq<4>, i64) -> !quake.ref
    %c3_i64_3 = arith.constant 3 : i64
    %8 = quake.extract_ref %0[%c3_i64_3] : (!quake.veq<4>, i64) -> !quake.ref
    quake.z [%7] %8 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_4 = arith.constant 1 : i64
    %9 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %9 : (!quake.ref) -> ()
    %c1_i64_5 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut = quake.mz %10 : (!quake.ref) -> !quake.measure
    %11 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c2_i64_6 = arith.constant 2 : i64
    %12 = quake.extract_ref %0[%c2_i64_6] : (!quake.veq<4>, i64) -> !quake.ref
    quake.h %12 : (!quake.ref) -> ()
    %c2_i64_7 = arith.constant 2 : i64
    %13 = quake.extract_ref %0[%c2_i64_7] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_8 = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    cc.if(%11) {
      %c0_i64_11 = arith.constant 0 : i64
      %17 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<4>, i64) -> !quake.ref
      quake.z %17 : (!quake.ref) -> ()
    }
    cc.if(%14) {
      %c3_i64_11 = arith.constant 3 : i64
      %17 = quake.extract_ref %0[%c3_i64_11] : (!quake.veq<4>, i64) -> !quake.ref
      quake.x %17 : (!quake.ref) -> ()
    }
    cc.if(%11) {
      %c3_i64_11 = arith.constant 3 : i64
      %17 = quake.extract_ref %0[%c3_i64_11] : (!quake.veq<4>, i64) -> !quake.ref
      quake.z %17 : (!quake.ref) -> ()
    }
    %c3_i64_9 = arith.constant 3 : i64
    %15 = quake.extract_ref %0[%c3_i64_9] : (!quake.veq<4>, i64) -> !quake.ref
    %measOut_10 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_IPKO5YG98P() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 4)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__h(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 3)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void @__quantum__qis__h(%Qubit* %5)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %7, %Qubit* %3)
  %8 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %9 = load %Qubit*, %Qubit** %8, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %9, %Qubit* %3)
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %3, %Qubit* %5)
  tail call void @__quantum__qis__h(%Qubit* %9)
  %10 = tail call %Result* @__quantum__qis__mz(%Qubit* %9)
  %11 = bitcast %Result* %10 to i1*
  %12 = load i1, i1* %11, align 1
  tail call void @__quantum__qis__h(%Qubit* %3)
  %13 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %14 = bitcast %Result* %13 to i1*
  %15 = load i1, i1* %14, align 1
  br i1 %12, label %16, label %17

16:                                               ; preds = %0
  tail call void @__quantum__qis__z(%Qubit* %7)
  br label %17

17:                                               ; preds = %16, %0
  br i1 %15, label %18, label %19

18:                                               ; preds = %17
  tail call void @__quantum__qis__x(%Qubit* %5)
  br label %19

19:                                               ; preds = %18, %17
  br i1 %12, label %20, label %21

20:                                               ; preds = %19
  tail call void @__quantum__qis__z(%Qubit* %5)
  br label %21

21:                                               ; preds = %20, %19
  %22 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
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

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
