# Code Mbqc Teleport

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[2] q;
bit[2] c;

h q[1];
cz q[0], q[1];
h q[0];

c[0] = measure q[0];
if (c[0] == true) {
  x q[1];
}

h q[1];
c[1] = measure q[1];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI = "__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<2>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref
    %c1_i64_0 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<2>, i64) -> !quake.ref
    quake.z [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %4 : (!quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %5 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %5 : (!quake.ref) -> !quake.measure
    %6 = quake.discriminate %measOut : (!quake.measure) -> i1
    cc.if(%6) {
      %c1_i64_6 = arith.constant 1 : i64
      %10 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<2>, i64) -> !quake.ref
      quake.x %10 : (!quake.ref) -> ()
    }
    %c1_i64_3 = arith.constant 1 : i64
    %7 = quake.extract_ref %0[%c1_i64_3] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %7 : (!quake.ref) -> ()
    %c1_i64_4 = arith.constant 1 : i64
    %8 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_5 = quake.mz %8 : (!quake.ref) -> !quake.measure
    %9 = quake.discriminate %measOut_5 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_UOA0X76QEI() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 2)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__h(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %5, %Qubit* %3)
  tail call void @__quantum__qis__h(%Qubit* %5)
  %6 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  %7 = bitcast %Result* %6 to i1*
  %8 = load i1, i1* %7, align 1
  br i1 %8, label %9, label %10

9:                                                ; preds = %0
  tail call void @__quantum__qis__x(%Qubit* %3)
  br label %10

10:                                               ; preds = %9, %0
  tail call void @__quantum__qis__h(%Qubit* %3)
  %11 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
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

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
