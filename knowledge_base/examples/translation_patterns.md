# Common Translation Patterns

## Pattern 1: Qubit Allocation

### MLIR (Catalyst)
```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
%2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
```

### QIR
```llvm
; Qubits are statically allocated
; Qubit 0: null
; Qubit 1: inttoptr (i64 1 to %Qubit*)
```

## Pattern 2: Gate Sequencing

### MLIR (Catalyst)
```mlir
%out1 = quantum.custom "Hadamard"() %qubit0 : !quantum.bit
%out2:2 = quantum.custom "CNOT"() %out1, %qubit1 : !quantum.bit, !quantum.bit
```

### QIR
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
```

## Pattern 3: Measurements

### MLIR (Catalyst)
```mlir
%mres, %out_qubit = quantum.measure %qubit : i1, !quantum.bit
```

### QIR
```llvm
call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
```

## Pattern 4: Conditional Operations

### MLIR (Catalyst)
```mlir
%extracted = tensor.extract %condition[] : tensor<i1>
%result = scf.if %extracted -> (!quantum.reg) {
  %gate = quantum.custom "PauliZ"() %qubit : !quantum.bit
  scf.yield %new_reg : !quantum.reg
}
```

### QIR
```llvm
%0 = call i1 @__quantum__qis__read_result__body(%Result* null)
br i1 %0, label %then, label %else

then:
  call void @__quantum__qis__z__body(%Qubit* inttoptr (i64 2 to %Qubit*))
  br label %continue

else:
  br label %continue

continue:
  ; Continue execution
```
