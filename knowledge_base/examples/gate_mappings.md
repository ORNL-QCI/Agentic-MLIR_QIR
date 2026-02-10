# MLIR to QIR Gate Mappings

## Single-Qubit Gates

| MLIR Gate (Catalyst) | QIR Function | Parameters |
|---------------------|--------------|------------|
| Hadamard | `__quantum__qis__h__body` | `%Qubit*` |
| PauliX | `__quantum__qis__x__body` | `%Qubit*` |
| PauliY | `__quantum__qis__y__body` | `%Qubit*` |
| PauliZ | `__quantum__qis__z__body` | `%Qubit*` |
| S | `__quantum__qis__s__body` | `%Qubit*` |
| T | `__quantum__qis__t__body` | `%Qubit*` |

## Parameterized Gates

| MLIR Gate | QIR Function | Parameters |
|-----------|--------------|------------|
| RX | `__quantum__qis__rx__body` | `double, %Qubit*` |
| RY | `__quantum__qis__ry__body` | `double, %Qubit*` |
| RZ | `__quantum__qis__rz__body` | `double, %Qubit*` |

## Two-Qubit Gates

| MLIR Gate | QIR Function | Parameters |
|-----------|--------------|------------|
| CNOT | `__quantum__qis__cnot__body` | `%Qubit*, %Qubit*` |
| CZ | `__quantum__qis__cz__body` | `%Qubit*, %Qubit*` |
| SWAP | `__quantum__qis__swap__body` | `%Qubit*, %Qubit*` |

## Measurements

| MLIR Operation | QIR Function | Parameters |
|----------------|--------------|------------|
| quantum.measure | `__quantum__qis__mz__body` | `%Qubit*, %Result*` |

## Qubit Pointers

In QIR, qubits are represented as pointers:
- Qubit 0: `null`
- Qubit 1: `inttoptr (i64 1 to %Qubit*)`
- Qubit n: `inttoptr (i64 n to %Qubit*)`

## Examples

### Hadamard Gate

**MLIR (Catalyst):**
```mlir
%out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
```

**QIR:**
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
```

### CNOT Gate

**MLIR (Catalyst):**
```mlir
%out_qubits:2 = quantum.custom "CNOT"() %control, %target : !quantum.bit, !quantum.bit
```

**QIR:**
```llvm
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
```
