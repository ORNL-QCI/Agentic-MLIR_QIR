"""
OpenQASM 3.0 → Quake MLIR conversion using CUDA Quantum.

Usage:
    python openqasm_to_quake_mlir.py

Output:
    examples/quake_mlir/<variable_name>.mlir  (one file per code_* variable)

How it works:
    1. All module-level variables whose names start with ``code_`` are treated
       as OpenQASM 3.0 source strings.
    2. Each string is parsed by the built-in qasm3_to_cudaq_kernel() converter.
    3. The resulting cudaq kernel exposes its Quake MLIR via kernel.module.
    4. The MLIR text is written to examples/quake_mlir/<var_name>.mlir.

cudaq 0.13 API notes:
    - cudaq.make_kernel()   → builder API
    - kernel.module         → Quake MLIR string
    - cudaq.translate(kernel, format='qir') → QIR LLVM IR string
    - cudaq.translate(source=..., from_source=OpenQASM3) is NOT available in v0.13
"""

import math
import re
import sys
from pathlib import Path

try:
    import cudaq
except ImportError:
    print("ERROR: cudaq not installed. Run: pip install cudaq")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# OpenQASM 3.0 source strings  (add / edit circuits here)
# ══════════════════════════════════════════════════════════════════════════════

code_bell = """\
OPENQASM 3.0;
include "stdgates.inc";

qubit[2] q;
bit[2] c;

h q[0];
cx q[0], q[1];

c[0] = measure q[0];
c[1] = measure q[1];
"""

code_ghz_5 = """\
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
"""

code_random_circuit_6994 = """\
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
"""

code_classic_teleportation = """\
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[3] q;
bit[3] c;

// Eve creates EPR pair, sends q[1] to Alice and q[2] to Bob
h q[1];
cx q[1], q[2];

// Alice entangles the unknown state (q[0]) with her EPR qubit (q[1])
cx q[0], q[1];
h q[0];

// Alice measures her two qubits
c[0] = measure q[0];
c[1] = measure q[1];

// Bob applies corrections based on Alice's measurement results
if (c[0] == 1) z q[2];
if (c[1] == 1) x q[2];

// Measure Bob's qubit
c[2] = measure q[2];
"""

code_random_circuit_3990 = """\
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
"""

code_random_circuit_658 = """\
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[2] q;
bit[2] cb;

// Apply gates in sequence
cx q[1], q[0];
swap q[0], q[1];
s q[0];
h q[1];
rx(2.59) q[0];
y q[0];
cx q[0], q[1];

// Measure both qubits
cb[0] = measure q[0];
cb[1] = measure q[1];
"""

code_random_circuit_1847 = """\
OPENQASM 3.0;
include "stdgates.inc";

// Registers
qubit[7] q;
bit[4] cb;

// Apply gates in sequence
t q[4];
z q[3];
cx q[0], q[4];
rz(2.53) q[5];
cz q[6], q[2];
h q[0];
x q[0];
cx q[2], q[3];
cx q[4], q[1];
cx q[5], q[2];

// Measure qubits 1, 4, 5, and 6 into cb
cb[0] = measure q[1];
cb[1] = measure q[4];
cb[2] = measure q[5];
cb[3] = measure q[6];
"""

code_random_circuit_2449 = """\
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
"""


# ══════════════════════════════════════════════════════════════════════════════
# OpenQASM 3.0 → cudaq kernel converter
# ══════════════════════════════════════════════════════════════════════════════

def qasm3_to_cudaq_kernel(qasm_str: str):
    """
    Parse a subset of OpenQASM 3.0 and build an equivalent cudaq kernel.

    Supported constructs:
      Registers  : qubit[N] name;  bit[N] name;
      1-q gates  : h x y z s t sdg tdg
      Param 1-q  : rx(θ) ry(θ) rz(θ) r1(θ) p(θ)
      2-q gates  : cx cz swap
      Param 2-q  : cp(θ) (mapped to cudaq cr1)
      Measure    : reg = measure qreg;  or  reg[i] = measure qreg[j];
      Conditional: if (c[i] == 1) gate q[j];
    """
    def strip_comment(line: str) -> str:
        return re.sub(r'//.*', '', line).strip()

    lines = [strip_comment(l) for l in qasm_str.splitlines()]
    lines = [l for l in lines if l]

    # ── Pass 1: collect register declarations ─────────────────────────────────
    qubit_regs: dict[str, tuple[int, int]] = {}   # name → (size, global_offset)
    bit_regs:   dict[str, int] = {}               # name → size
    total_q = 0

    for line in lines:
        m = re.match(r'qubit\[(\d+)\]\s+(\w+)\s*;', line)
        if m:
            size, name = int(m.group(1)), m.group(2)
            qubit_regs[name] = (size, total_q)
            total_q += size
            continue
        m = re.match(r'bit\[(\d+)\]\s+(\w+)\s*;', line)
        if m:
            bit_regs[m.group(2)] = int(m.group(1))

    if total_q == 0:
        raise ValueError("No qubit registers found in OpenQASM source")

    # ── Build cudaq kernel ────────────────────────────────────────────────────
    kernel = cudaq.make_kernel()
    q = kernel.qalloc(total_q)

    def qi(reg: str, idx: int) -> int:
        """Resolve a register-local index to a global qubit index."""
        size, offset = qubit_regs[reg]
        if idx >= size:
            raise IndexError(f"{reg}[{idx}] out of bounds (size={size})")
        return offset + idx

    def parse_angle(expr: str) -> float:
        return float(eval(expr, {'pi': math.pi, '__builtins__': {}}))

    ONE_Q = {
        'h':   kernel.h,   'x': kernel.x,   'y': kernel.y,   'z': kernel.z,
        's':   kernel.s,   't': kernel.t,
        'sdg': kernel.sdg, 'tdg': kernel.tdg,
    }
    PARAM_ONE_Q = {
        'rx': kernel.rx, 'ry': kernel.ry, 'rz': kernel.rz, 'r1': kernel.r1,
    }

    # Measurement results: (bit_reg, bit_idx) → QuakeValue
    mvals: dict[tuple[str, int], object] = {}

    SKIP_PREFIXES = ('OPENQASM', 'include', 'qubit', 'bit')

    for line in lines:
        if any(line.startswith(p) for p in SKIP_PREFIXES):
            continue

        # measure: c = measure q;
        m = re.match(r'(\w+)\s*=\s*measure\s+(\w+)\s*;', line)
        if m:
            breg, qreg = m.group(1), m.group(2)
            size, offset = qubit_regs[qreg]
            for i in range(size):
                mvals[(breg, i)] = kernel.mz(q[offset + i])
            continue

        # measure: c[i] = measure q[j];
        m = re.match(r'(\w+)\[(\d+)\]\s*=\s*measure\s+(\w+)\[(\d+)\]\s*;', line)
        if m:
            breg, bi = m.group(1), int(m.group(2))
            qreg, qidx = m.group(3), int(m.group(4))
            mvals[(breg, bi)] = kernel.mz(q[qi(qreg, qidx)])
            continue

        # conditional: if (c[i] == 1) gate q[j];
        m = re.match(
            r'if\s*\(\s*(\w+)\[(\d+)\]\s*==\s*1\s*\)\s+(\w+)\s+(\w+)\[(\d+)\]\s*;',
            line)
        if m:
            breg, bi    = m.group(1), int(m.group(2))
            gate_name   = m.group(3)
            qreg, qidx  = m.group(4), int(m.group(5))
            target      = qi(qreg, qidx)
            mval        = mvals.get((breg, bi))
            if mval is not None and gate_name in ONE_Q:
                gfn = ONE_Q[gate_name]
                kernel.c_if(mval, lambda gf=gfn, t=target: gf(q[t]))
            continue

        # cp(θ) q[i], q[j];  (controlled phase → cudaq cr1)
        m = re.match(
            r'cp\s*\(([^)]+)\)\s+(\w+)\[(\d+)\]\s*,\s*(\w+)\[(\d+)\]\s*;', line)
        if m:
            angle = parse_angle(m.group(1))
            c_idx = qi(m.group(2), int(m.group(3)))
            t_idx = qi(m.group(4), int(m.group(5)))
            kernel.cr1(angle, q[c_idx], q[t_idx])
            continue

        # parametric 1-q: rx(θ) q[i];  ry  rz  r1  p
        m = re.match(r'(rx|ry|rz|r1|p)\s*\(([^)]+)\)\s+(\w+)\[(\d+)\]\s*;', line)
        if m:
            gname  = m.group(1)
            angle  = parse_angle(m.group(2))
            target = qi(m.group(3), int(m.group(4)))
            gkey   = 'r1' if gname == 'p' else gname
            if gkey in PARAM_ONE_Q:
                PARAM_ONE_Q[gkey](angle, q[target])
            continue

        # 2-q: cx q[i], q[j];  cz  swap
        m = re.match(
            r'(cx|cz|swap)\s+(\w+)\[(\d+)\]\s*,\s*(\w+)\[(\d+)\]\s*;', line)
        if m:
            gname = m.group(1)
            idx1  = qi(m.group(2), int(m.group(3)))
            idx2  = qi(m.group(4), int(m.group(5)))
            if gname == 'cx':
                kernel.cx(q[idx1], q[idx2])
            elif gname == 'cz':
                kernel.cz(q[idx1], q[idx2])
            elif gname == 'swap':
                kernel.swap(q[idx1], q[idx2])
            continue

        # 1-q: h q[0];  x y z s t sdg tdg
        m = re.match(r'(h|x|y|z|s|t|sdg|tdg)\s+(\w+)\[(\d+)\]\s*;', line)
        if m:
            gname  = m.group(1)
            target = qi(m.group(2), int(m.group(3)))
            if gname in ONE_Q:
                ONE_Q[gname](q[target])
            continue

    return kernel


# ══════════════════════════════════════════════════════════════════════════════
# Main: auto-discover code_* variables, convert, and save
# ══════════════════════════════════════════════════════════════════════════════

def _write_md(out_dir: Path, var_name: str, qasm_str: str,
              quake_mlir: str, qir: str) -> Path:
    """Write a Markdown file containing all three representations."""
    title = var_name.replace('_', ' ').title()
    md = f"# {title}\n\n"

    md += "## OpenQASM 3.0 Source\n\n"
    md += f"```qasm\n{qasm_str.strip()}\n```\n\n"

    md += "## Quake MLIR\n\n"
    md += f"```mlir\n{quake_mlir.strip()}\n```\n\n"

    md += "## QIR (LLVM IR via cudaq.translate)\n\n"
    md += f"```llvm\n{qir.strip()}\n```\n"

    out_path = out_dir / f"{var_name}.md"
    out_path.write_text(md)
    return out_path


if __name__ == "__main__":
    # Collect all code_* string variables defined in this module
    this_module = sys.modules[__name__]
    circuits = {
        name: val
        for name, val in vars(this_module).items()
        if name.startswith('code_') and isinstance(val, str)
    }

    if not circuits:
        print("No code_* variables found in this file.")
        sys.exit(0)

    out_dir = Path(__file__).parent.parent / 'examples' / 'quake_mlir'
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {out_dir}\n")

    ok, failed = 0, []

    for var_name in sorted(circuits):
        qasm_str = circuits[var_name]
        print(f"  {var_name} ... ", end='', flush=True)
        try:
            kernel     = qasm3_to_cudaq_kernel(qasm_str)
            quake_mlir = str(kernel.module)
            qir        = cudaq.translate(kernel, format='qir')

            # .mlir file
            (out_dir / f'{var_name}.mlir').write_text(quake_mlir)

            # .md file with all three representations
            md_path = _write_md(out_dir, var_name, qasm_str, quake_mlir, qir)

            print(f"saved → {md_path.relative_to(Path.cwd())}")
            ok += 1
        except Exception as exc:
            print(f"FAILED  ({exc})")
            failed.append((var_name, str(exc)))

    print(f"\nDone: {ok}/{len(circuits)} circuits converted successfully.")
    if failed:
        print("Failed:")
        for name, msg in failed:
            print(f"  - {name}: {msg}")
