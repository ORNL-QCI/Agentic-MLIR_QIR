# OpenQASM → Quake MLIR: How It Works

## Why Do We Need a Regex Parser?

CUDA-Q v0.13 has **no built-in OpenQASM 3.0 importer**.

The `cudaq.translate` function only works in the **outbound** direction — converting a cudaq kernel *to* another format (e.g. QIR):

```python
cudaq.translate(kernel, format='qir')  # ✅ works in v0.13
```

The reverse direction is **not available**:

```python
cudaq.translate(source=qasm_str, format='quake', from_source='OpenQASM3')  # ❌ not in v0.13
```

So to go from OpenQASM text to a cudaq kernel, we must manually parse the OpenQASM source and call the cudaq builder API gate by gate. That's what the regex parser does.

---

## Flow: OpenQASM → Quake MLIR

```
OpenQASM text
    │
    ▼
regex parser  (qasm3_to_cudaq_kernel)
    │  - finds qubit[2] q   → records register, total_q = 2
    │  - finds h q[0]       → kernel.h(q[0])
    │  - finds cx q[0],q[1] → kernel.cx(q[0], q[1])
    │  - finds measure       → kernel.mz(q[i])
    ▼
cudaq kernel  (in-memory builder object)
    │
    ▼
kernel.module  →  Quake MLIR string  (cudaq generates this internally)
```

---

## Concrete Example: Bell State

**Input (OpenQASM 3.0)**

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[2] q;
bit[2] c;

h q[0];
cx q[0], q[1];

c[0] = measure q[0];
c[1] = measure q[1];
```

**What the regex parser does**

```python
kernel = cudaq.make_kernel()
q = kernel.qalloc(2)   # qubit[2] q

kernel.h(q[0])         # h q[0]
kernel.cx(q[0], q[1])  # cx q[0], q[1]
kernel.mz(q[0])        # c[0] = measure q[0]
kernel.mz(q[1])        # c[1] = measure q[1]
```

**Extract Quake MLIR**

```python
quake_mlir = str(kernel.module)
```

cudaq maintains an internal MLIR representation as you add gates. `kernel.module` serializes it to a Quake MLIR string.

**Output (Quake MLIR)**

```mlir
module attributes {...} {
  func.func @__nvqpp__mlirgen____nvqppBuilderKernel_...() attributes {...} {
    %0 = quake.alloca !quake.veq<2>
    %1 = quake.extract_ref %0[0] : (!quake.veq<2>) -> !quake.ref
    quake.h %1 : (!quake.ref) -> ()
    %2 = quake.extract_ref %0[1] : (!quake.veq<2>) -> !quake.ref
    quake.x [%1] %2 : (!quake.ref, !quake.ref) -> ()
    %3 = quake.mz %1 : (!quake.ref) -> !quake.measure
    %4 = quake.mz %2 : (!quake.ref) -> !quake.measure
    return
  }
}
```

---

## Summary

| Step | Tool | What happens |
|------|------|--------------|
| Parse registers & gates | regex | OpenQASM text → structured gate list |
| Build kernel | cudaq builder API | Gate list → in-memory cudaq kernel |
| Extract MLIR | `kernel.module` | cudaq serializes kernel → Quake MLIR string |
| (Optional) Get QIR | `cudaq.translate` | cudaq kernel → QIR LLVM IR |
