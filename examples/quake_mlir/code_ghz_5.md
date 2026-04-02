# Code Ghz 5

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[5] q;
bit[5] c;

// 5-qubit GHZ state: (|00000⟩ + |11111⟩)/√2
h q[0];
cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[0], q[4];

// Measure all qubits
c = measure q;
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21 = "__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<5>
    %c0_i64 = arith.constant 0 : i64
    %1 = quake.extract_ref %0[%c0_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %c0_i64_0 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64_0] : (!quake.veq<5>, i64) -> !quake.ref
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%2] %3 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_1 = arith.constant 0 : i64
    %4 = quake.extract_ref %0[%c0_i64_1] : (!quake.veq<5>, i64) -> !quake.ref
    %c2_i64 = arith.constant 2 : i64
    %5 = quake.extract_ref %0[%c2_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%4] %5 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_2 = arith.constant 0 : i64
    %6 = quake.extract_ref %0[%c0_i64_2] : (!quake.veq<5>, i64) -> !quake.ref
    %c3_i64 = arith.constant 3 : i64
    %7 = quake.extract_ref %0[%c3_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%6] %7 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_3 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_3] : (!quake.veq<5>, i64) -> !quake.ref
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<5>, i64) -> !quake.ref
    quake.x [%8] %9 : (!quake.ref, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %10 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut = quake.mz %10 : (!quake.ref) -> !quake.measure
    %11 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_5 = arith.constant 1 : i64
    %12 = quake.extract_ref %0[%c1_i64_5] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_6 = quake.mz %12 : (!quake.ref) -> !quake.measure
    %13 = quake.discriminate %measOut_6 : (!quake.measure) -> i1
    %c2_i64_7 = arith.constant 2 : i64
    %14 = quake.extract_ref %0[%c2_i64_7] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_8 = quake.mz %14 : (!quake.ref) -> !quake.measure
    %15 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
    %c3_i64_9 = arith.constant 3 : i64
    %16 = quake.extract_ref %0[%c3_i64_9] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_10 = quake.mz %16 : (!quake.ref) -> !quake.measure
    %17 = quake.discriminate %measOut_10 : (!quake.measure) -> i1
    %c4_i64_11 = arith.constant 4 : i64
    %18 = quake.extract_ref %0[%c4_i64_11] : (!quake.veq<5>, i64) -> !quake.ref
    %measOut_12 = quake.mz %18 : (!quake.ref) -> !quake.measure
    %19 = quake.discriminate %measOut_12 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_7VL23OIK21() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 5)
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
  %12 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  %13 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  %14 = tail call %Result* @__quantum__qis__mz(%Qubit* %7)
  %15 = tail call %Result* @__quantum__qis__mz(%Qubit* %9)
  %16 = tail call %Result* @__quantum__qis__mz(%Qubit* %11)
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
