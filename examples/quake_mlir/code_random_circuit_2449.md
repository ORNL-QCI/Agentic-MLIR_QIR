# Code Random Circuit 2449

## OpenQASM 3.0 Source

```qasm
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[6] q;
bit[2] cbit;

// Apply gates in sequence
x q[5];
y q[5];
rz(0.03) q[1];
rz(1.08) q[2];
t q[3];
s q[2];
rx(2.41) q[0];
x q[0];
cx q[4], q[2];

// Measure qubits 2 and 5 into cbit
cbit[0] = measure q[2];
cbit[1] = measure q[5];
```

## Quake MLIR

```mlir
module attributes {quake.mangled_name_map = {__nvqpp__mlirgen____nvqppBuilderKernel_30RI7CYVW2 = "__nvqpp__mlirgen____nvqppBuilderKernel_30RI7CYVW2_PyKernelEntryPointRewrite"}} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_30RI7CYVW2() attributes {"cudaq-entrypoint", "cudaq-kernel"} {
    %0 = quake.alloca !quake.veq<6>
    %c5_i64 = arith.constant 5 : i64
    %1 = quake.extract_ref %0[%c5_i64] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x %1 : (!quake.ref) -> ()
    %c5_i64_0 = arith.constant 5 : i64
    %2 = quake.extract_ref %0[%c5_i64_0] : (!quake.veq<6>, i64) -> !quake.ref
    quake.y %2 : (!quake.ref) -> ()
    %c1_i64 = arith.constant 1 : i64
    %3 = quake.extract_ref %0[%c1_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst = arith.constant 3.000000e-02 : f64
    quake.rz (%cst) %3 : (f64, !quake.ref) -> ()
    %c2_i64 = arith.constant 2 : i64
    %4 = quake.extract_ref %0[%c2_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst_1 = arith.constant 1.080000e+00 : f64
    quake.rz (%cst_1) %4 : (f64, !quake.ref) -> ()
    %c3_i64 = arith.constant 3 : i64
    %5 = quake.extract_ref %0[%c3_i64] : (!quake.veq<6>, i64) -> !quake.ref
    quake.t %5 : (!quake.ref) -> ()
    %c2_i64_2 = arith.constant 2 : i64
    %6 = quake.extract_ref %0[%c2_i64_2] : (!quake.veq<6>, i64) -> !quake.ref
    quake.s %6 : (!quake.ref) -> ()
    %c0_i64 = arith.constant 0 : i64
    %7 = quake.extract_ref %0[%c0_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %cst_3 = arith.constant 2.410000e+00 : f64
    quake.rx (%cst_3) %7 : (f64, !quake.ref) -> ()
    %c0_i64_4 = arith.constant 0 : i64
    %8 = quake.extract_ref %0[%c0_i64_4] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x %8 : (!quake.ref) -> ()
    %c4_i64 = arith.constant 4 : i64
    %9 = quake.extract_ref %0[%c4_i64] : (!quake.veq<6>, i64) -> !quake.ref
    %c2_i64_5 = arith.constant 2 : i64
    %10 = quake.extract_ref %0[%c2_i64_5] : (!quake.veq<6>, i64) -> !quake.ref
    quake.x [%9] %10 : (!quake.ref, !quake.ref) -> ()
    %c2_i64_6 = arith.constant 2 : i64
    %11 = quake.extract_ref %0[%c2_i64_6] : (!quake.veq<6>, i64) -> !quake.ref
    %measOut = quake.mz %11 : (!quake.ref) -> !quake.measure
    %12 = quake.discriminate %measOut : (!quake.measure) -> i1
    %c5_i64_7 = arith.constant 5 : i64
    %13 = quake.extract_ref %0[%c5_i64_7] : (!quake.veq<6>, i64) -> !quake.ref
    %measOut_8 = quake.mz %13 : (!quake.ref) -> !quake.measure
    %14 = quake.discriminate %measOut_8 : (!quake.measure) -> i1
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

define void @__nvqpp__mlirgen____nvqppBuilderKernel_30RI7CYVW2() local_unnamed_addr {
  %1 = tail call %Array* @__quantum__rt__qubit_allocate_array(i64 6)
  %2 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 5)
  %3 = load %Qubit*, %Qubit** %2, align 8
  tail call void @__quantum__qis__x(%Qubit* %3)
  tail call void @__quantum__qis__y(%Qubit* %3)
  %4 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 1)
  %5 = load %Qubit*, %Qubit** %4, align 8
  tail call void @__quantum__qis__rz(double 3.000000e-02, %Qubit* %5)
  %6 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 2)
  %7 = load %Qubit*, %Qubit** %6, align 8
  tail call void @__quantum__qis__rz(double 1.080000e+00, %Qubit* %7)
  %8 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 3)
  %9 = load %Qubit*, %Qubit** %8, align 8
  tail call void @__quantum__qis__t(%Qubit* %9)
  tail call void @__quantum__qis__s(%Qubit* %7)
  %10 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %11 = load %Qubit*, %Qubit** %10, align 8
  tail call void @__quantum__qis__rx(double 2.410000e+00, %Qubit* %11)
  tail call void @__quantum__qis__x(%Qubit* %11)
  %12 = tail call %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 4)
  %13 = bitcast %Qubit** %12 to i8**
  %14 = load i8*, i8** %13, align 8
  tail call void (i64, i64, i64, i64, i8*, ...) @generalizedInvokeWithRotationsControlsTargets(i64 0, i64 0, i64 1, i64 1, i8* nonnull bitcast (void (%Array*, %Qubit*)* @__quantum__qis__x__ctl to i8*), i8* %14, %Qubit* %7)
  %15 = tail call %Result* @__quantum__qis__mz(%Qubit* %7)
  %16 = tail call %Result* @__quantum__qis__mz(%Qubit* %3)
  tail call void @__quantum__rt__qubit_release_array(%Array* %1)
  ret void
}

declare %Array* @__quantum__rt__qubit_allocate_array(i64) local_unnamed_addr

declare void @__quantum__rt__qubit_release_array(%Array*) local_unnamed_addr

declare %Qubit** @__quantum__rt__array_get_element_ptr_1d(%Array*, i64) local_unnamed_addr

declare void @__quantum__qis__x__ctl(%Array*, %Qubit*)

declare void @generalizedInvokeWithRotationsControlsTargets(i64, i64, i64, i64, i8*, ...) local_unnamed_addr

declare void @__quantum__qis__x(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__y(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__s(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__t(%Qubit*) local_unnamed_addr

declare %Result* @__quantum__qis__mz(%Qubit*) local_unnamed_addr

declare void @__quantum__qis__rx(double, %Qubit*) local_unnamed_addr

declare void @__quantum__qis__rz(double, %Qubit*) local_unnamed_addr

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
```
