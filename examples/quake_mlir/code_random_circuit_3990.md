# Code Random Circuit 3990

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[2] q;
bit[2] c;

// Apply gates in sequence
cz q[1], q[0];
h q[1];
z q[1];
t q[1];
z q[1];
cx q[1], q[0];
rz(1.66) q[1];
t q[1];
ry(2.23) q[1];
s q[0];

// Measure both qubits
c[0] = measure q[0];
c[1] = measure q[1];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_RJHKJR3TOM = "__nvqpp__mlirgen____nvqppBuilderKernel_RJHKJR3TOM_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_RJHKJR3TOM() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<2>
    %c1_i64 = arith.constant 1 : i64
    %1 = quake.extract_ref %0[%c1_i64] : (!quake.veq<2>, i64) -> !quake.ref
    %c0_i64 = arith.constant 0 : i64
    %2 = quake.extract_ref %0[%c0_i64] : (!quake.veq<2>, i64) -> !quake.ref
    quake.z [%1] %2 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_0 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64_0] : (!quake.veq<2>, i64) -> !quake.ref
    quake.h %3 : (!quake.ref) -> ()
    %c1_i64_1 = arith.constant 1 : i64
    %4 = quake.extract_ref %0[%c1_i64_1] : (!quake.veq<2>, i64) -> !quake.ref
    quake.z %4 : (!quake.ref) -> ()
    %c1_i64_2 = arith.constant 1 : i64
    %5 = quake.extract_ref %0[%c1_i64_2] : (!quake.veq<2>, i64) -> !quake.ref
    quake.t %5 : (!quake.ref) -> ()
    %c1_i64_3 = arith.constant 1 : i64
    %6 = quake.extract_ref %0[%c1_i64_3] : (!quake.veq<2>, i64) -> !quake.ref
    quake.z %6 : (!quake.ref) -> ()
    %c1_i64_4 = arith.constant 1 : i64
    %7 = quake.extract_ref %0[%c1_i64_4] : (!quake.veq<2>, i64) -> !quake.ref
    %c0_i64_5 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_5] : (!quake.veq<2>, i64) -> !quake.ref
    quake.x [%7] %8 : (!quake.ref, !quake.ref) -> ()
    %c1_i64_6 = arith.constant 1 : i64
    %9 = quake.extract_ref %0[%c1_i64_6] : (!quake.veq<2>, i64) -> !quake.ref
    %cst = arith.constant 1.660000e+00 : f64
    quake.rz (%cst) %9 : (f64, !quake.ref) -> ()
    %c1_i64_7 = arith.constant 1 : i64
    %10 = quake.extract_ref %0[%c1_i64_7] : (!quake.veq<2>, i64) -> !quake.ref
    quake.t %10 : (!quake.ref) -> ()
    %c1_i64_8 = arith.constant 1 : i64
    %11 = quake.extract_ref %0[%c1_i64_8] : (!quake.veq<2>, i64) -> !quake.ref
    %cst_9 = arith.constant 2.230000e+00 : f64
    quake.ry (%cst_9) %11 : (f64, !quake.ref) -> ()
    %c0_i64_10 = arith.constant 0 : i64
    %12 = quake.extract_ref %0[%c0_i64_10] : (!quake.veq<2>, i64) -> !quake.ref
    quake.s %12 : (!quake.ref) -> ()
    %c0_i64_11 = arith.constant 0 : i64
    %13 = quake.extract_ref %0[%c0_i64_11] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c1_i64_12 = arith.constant 1 : i64
    %15 = quake.extract_ref %0[%c1_i64_12] : (!quake.veq<2>, i64) -> !quake.ref
    %measOut_13 = quake.mz %15 : (!quake.ref) -> !quake.measure
    %16 = quake.discriminate %measOut_13 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_RJHKJR3TOM() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 2)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %3 = load %Qubit*, %Qubit** %2, align 8
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__z__ctl to i8*), %Qubit* %3, %Qubit* %5)
  tail call void @__quantum__qis__h(%Qubit* %3)
  tail call void @__quantum__qis__z(%Qubit* %3)
  tail call void @__quantum__qis__t(%Qubit* %3)
  tail call void @__quantum__qis__z(%Qubit* %3)
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), %Qubit* %3, %Qubit* %5)
  tail call void @__quantum__qis__rz(double 1.660000e+00, %Qubit* %3)
  tail call void @__quantum__qis__t(%Qubit* %3)
  tail call void @__quantum__qis__ry(double 2.230000e+00, %Qubit* %3)
  tail call void @__quantum__qis__s(%Qubit* %5)
  %6 = tail call %Result* @__quantum__qis__mz(%Qubit* %5)
  %7 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
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

declare void @__quantum__qis__z(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__s(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__t(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__ry(double, %Qubit*) local_unnamed_addr

declare void @__quantum__qis__rz(double, %Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
