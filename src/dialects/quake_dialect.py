"""Quake dialect adapter for NVIDIA CUDA Quantum — SSA-aware parser.

Handles the cudaq-generated Quake MLIR format:

    module attributes {quake.mangled_name_map = {...}} {
      func.func @__nvqpp__mlirgen__...() attributes {"cudaq-entrypoint"} {
        %0   = quake.alloca !quake.veq<N>
        %c0  = arith.constant 0 : i64
        %1   = quake.extract_ref %0[%c0]  : (!quake.veq<N>, i64) -> !quake.ref
        quake.h   %1                      : (!quake.ref) -> ()
        quake.x   [%ctrl] %tgt            : (!quake.ref, !quake.ref) -> ()
        quake.rx  (%cst)  %ref            : (f64, !quake.ref) -> ()
        quake.r1  (%cst)  [%ctrl] %tgt   : (f64, !quake.ref, !quake.ref) -> ()
        quake.swap %a, %b                 : (!quake.ref, !quake.ref) -> ()
        quake.cz   %a, %b                : (!quake.ref, !quake.ref) -> ()
        %m  = quake.mz %ref              : (!quake.ref) -> !quake.measure
        %b  = quake.discriminate %m      : (!quake.measure) -> i1
        cc.if(%b) { ... }
        return
      }
    }
"""

import re
from typing import List, Dict, Optional, Tuple
from .base_dialect import (
    BaseDialect,
    GateOperation,
    QubitAllocation,
    MeasurementOperation,
    ConditionalBlock,
    MLIRCircuit,
    ParsingError,
)


class QuakeDialect(BaseDialect):
    """Adapter for NVIDIA CUDA Quantum Quake dialect."""

    @property
    def name(self) -> str:
        return "quake"

    # Quake gate name → QIR body function
    GATE_MAPPING: Dict[str, str] = {
        "h":    "__quantum__qis__h__body",
        "x":    "__quantum__qis__x__body",
        "y":    "__quantum__qis__y__body",
        "z":    "__quantum__qis__z__body",
        "s":    "__quantum__qis__s__body",
        "t":    "__quantum__qis__t__body",
        "sdg":  "__quantum__qis__sdg__body",
        "tdg":  "__quantum__qis__tdg__body",
        "rx":   "__quantum__qis__rx__body",
        "ry":   "__quantum__qis__ry__body",
        "rz":   "__quantum__qis__rz__body",
        "r1":   "__quantum__qis__r1__body",
        # two-qubit
        "cnot": "__quantum__qis__cnot__body",
        "cx":   "__quantum__qis__cnot__body",
        "cz":   "__quantum__qis__cz__body",
        "swap": "__quantum__qis__swap__body",
    }

    # ── BaseDialect API ────────────────────────────────────────────────────────

    def can_parse(self, mlir_code: str) -> bool:
        markers = [
            "quake.alloca", "quake.h", "quake.x", "quake.y", "quake.z",
            "quake.mz", "!quake.veq", "!quake.ref",
        ]
        return any(m in mlir_code for m in markers)

    def parse_circuit(self, mlir_code: str) -> MLIRCircuit:
        try:
            return self._ssa_parse(mlir_code)
        except ParsingError:
            raise
        except Exception as exc:
            raise ParsingError(f"Failed to parse Quake MLIR: {exc}") from exc

    def parse_qubits(self, mlir_code: str) -> QubitAllocation:
        m = re.search(r"quake\.alloca\s+!quake\.veq<(\d+)>", mlir_code)
        if not m:
            raise ParsingError("Cannot find quake.alloca statement")
        num_q = int(m.group(1))
        ref_map = self._build_ref_map(mlir_code)
        return QubitAllocation(
            num_qubits=num_q,
            allocation_type="static",
            qubit_vars=ref_map,
        )

    def parse_gates(self, mlir_code: str) -> List[GateOperation]:
        return self._ssa_parse(mlir_code).gates

    def parse_measurements(self, mlir_code: str) -> List[MeasurementOperation]:
        return self._ssa_parse(mlir_code).measurements

    def get_gate_mapping(self) -> Dict[str, str]:
        return self.GATE_MAPPING

    # ── SSA-aware single-pass parser ───────────────────────────────────────────

    def _ssa_parse(self, mlir_code: str) -> MLIRCircuit:
        """Single-pass SSA-aware parser that produces an ordered_ops list."""

        # ── num_qubits ──────────────────────────────────────────────────────
        m = re.search(r"quake\.alloca\s+!quake\.veq<(\d+)>", mlir_code)
        if not m:
            raise ParsingError("No quake.alloca found")
        num_qubits = int(m.group(1))

        # SSA state
        ssa_int:   Dict[str, int]   = {}   # %var → int   (arith.constant i64)
        ssa_float: Dict[str, float] = {}   # %var → float (arith.constant f64)
        ref_qubit: Dict[str, int]   = {}   # %var → qubit index (quake.extract_ref)
        meas_var_to_idx: Dict[str, int] = {}  # meas SSA var → meas list index
        discrim_to_meas_idx: Dict[str, int] = {}  # discrim SSA var → meas index

        ordered_ops: List[Tuple] = []
        all_gates:   List[GateOperation]       = []
        all_meas:    List[MeasurementOperation] = []
        all_conds:   List[ConditionalBlock]     = []

        lines = mlir_code.splitlines()
        i = 0
        while i < len(lines):
            raw = lines[i].strip()
            i += 1

            # Skip boilerplate lines
            if not raw or raw.startswith(("//", "module", "func.func", "}", "return")):
                continue

            # ── arith.constant N : i64 ──────────────────────────────────────
            m = re.match(
                r"%(\S+?)\s*=\s*arith\.constant\s+(\d+)\s*:\s*i64", raw)
            if m:
                ssa_int[m.group(1)] = int(m.group(2))
                continue

            # ── arith.constant X.X : f64 ────────────────────────────────────
            m = re.match(
                r"%(\S+?)\s*=\s*arith\.constant\s+([-+]?[\d.]+(?:[eE][-+]?\d+)?)\s*:\s*f64",
                raw)
            if m:
                try:
                    ssa_float[m.group(1)] = float(m.group(2))
                except ValueError:
                    pass
                continue

            # ── quake.extract_ref %0[%idx_var] → ref_qubit ─────────────────
            m = re.match(
                r"%(\S+?)\s*=\s*quake\.extract_ref\s+%\S+\[%(\S+?)\]", raw)
            if m:
                var, idx_var = m.group(1), m.group(2).rstrip(":)")
                ref_qubit[var] = ssa_int.get(idx_var, 0)
                continue

            # ── quake.discriminate ──────────────────────────────────────────
            m = re.match(
                r"%(\S+?)\s*=\s*quake\.discriminate\s+%(\S+?)[\s:]", raw)
            if m:
                dvar, mvar = m.group(1), m.group(2)
                if mvar in meas_var_to_idx:
                    discrim_to_meas_idx[dvar] = meas_var_to_idx[mvar]
                continue

            # ── quake.mz (single-qubit or register) ─────────────────────────
            m = re.match(
                r"%(\S+?)\s*=\s*quake\.mz\s+%(\S+?)\s*:", raw)
            if m:
                mvar, ref_or_reg = m.group(1), m.group(2).rstrip(":)")
                # Detect register mz: "-> !cc.stdvec" in the rest of the line
                is_register = "!cc.stdvec" in raw or "!quake.veq" in raw
                if is_register:
                    # Measure all N qubits in qubit-index order
                    for qi in range(num_qubits):
                        sub_var = f"{mvar}_q{qi}"
                        meas_op = MeasurementOperation(
                            qubit=qi,
                            result_var=sub_var,
                            line_number=i,
                        )
                        meas_var_to_idx[sub_var] = len(all_meas)
                        all_meas.append(meas_op)
                        ordered_ops.append(("measurement", meas_op))
                else:
                    qubit_idx = ref_qubit.get(ref_or_reg, 0)
                    meas_op = MeasurementOperation(
                        qubit=qubit_idx,
                        result_var=mvar,
                        line_number=i,
                    )
                    meas_var_to_idx[mvar] = len(all_meas)
                    all_meas.append(meas_op)
                    ordered_ops.append(("measurement", meas_op))
                continue

            # ── cc.if(%cond_var) { ... } ────────────────────────────────────
            m = re.match(r"cc\.if\s*\(%(\S+?)\)\s*\{", raw)
            if m:
                cond_var = m.group(1).rstrip(":)")
                meas_idx_for_cond = discrim_to_meas_idx.get(cond_var, 0)

                # Collect body until matching '}'
                body_lines: List[str] = []
                depth = 1
                while i < len(lines) and depth > 0:
                    bl = lines[i].strip()
                    i += 1
                    if "{" in bl:
                        depth += 1
                    if "}" in bl:
                        depth -= 1
                        if depth == 0:
                            break
                    body_lines.append(bl)

                then_gates = self._parse_block_gates(
                    body_lines, ref_qubit, ssa_int, ssa_float
                )
                cond = ConditionalBlock(
                    condition_measurement_idx=meas_idx_for_cond,
                    then_gates=then_gates,
                    else_gates=[],
                )
                all_conds.append(cond)
                ordered_ops.append(("conditional", cond))
                continue

            # ── quake.x [%ctrl] %tgt  (CNOT) ───────────────────────────────
            m = re.match(
                r"quake\.x\s+\[%(\S+?)\]\s+%(\S+?)\s*:", raw)
            if m:
                ctrl = m.group(1).rstrip(":)")
                tgt  = m.group(2).rstrip(":)")
                gate = GateOperation(
                    name="cnot",
                    qubits=[ref_qubit.get(ctrl, 0), ref_qubit.get(tgt, 1)],
                    params=[],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── quake.z [%ctrl] %tgt  (CZ) ─────────────────────────────────
            m = re.match(
                r"quake\.z\s+\[%(\S+?)\]\s+%(\S+?)\s*:", raw)
            if m:
                ctrl = m.group(1).rstrip(":)")
                tgt  = m.group(2).rstrip(":)")
                gate = GateOperation(
                    name="cz",
                    qubits=[ref_qubit.get(ctrl, 0), ref_qubit.get(tgt, 1)],
                    params=[],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── quake.r1 (%angle) [%ctrl] %tgt  (controlled-phase) ─────────
            m = re.match(
                r"quake\.r1\s+\(%(\S+?)\)\s+\[%(\S+?)\]\s+%(\S+?)\s*:", raw)
            if m:
                angle_var = m.group(1).rstrip(":)")
                ctrl      = m.group(2).rstrip(":)")
                tgt       = m.group(3).rstrip(":)")
                gate = GateOperation(
                    name="r1",
                    qubits=[ref_qubit.get(ctrl, 0), ref_qubit.get(tgt, 1)],
                    params=[ssa_float.get(angle_var, 0.0)],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── quake.<param> (%angle) %qubit  (parametric single-qubit) ────
            m = re.match(
                r"quake\.(rx|ry|rz|r1)\s+\(%(\S+?)\)\s+%(\S+?)\s*:", raw)
            if m:
                gname     = m.group(1)
                angle_var = m.group(2).rstrip(":)")
                qubit_var = m.group(3).rstrip(":)")
                gate = GateOperation(
                    name=gname,
                    qubits=[ref_qubit.get(qubit_var, 0)],
                    params=[ssa_float.get(angle_var, 0.0)],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── quake.swap %a, %b ───────────────────────────────────────────
            m = re.match(
                r"quake\.swap\s+%(\S+?),\s*%(\S+?)\s*:", raw)
            if m:
                av = m.group(1).rstrip(",:")
                bv = m.group(2).rstrip(":")
                gate = GateOperation(
                    name="swap",
                    qubits=[ref_qubit.get(av, 0), ref_qubit.get(bv, 1)],
                    params=[],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── quake.cz %a, %b ─────────────────────────────────────────────
            m = re.match(
                r"quake\.cz\s+%(\S+?),\s*%(\S+?)\s*:", raw)
            if m:
                av = m.group(1).rstrip(",:")
                bv = m.group(2).rstrip(":")
                gate = GateOperation(
                    name="cz",
                    qubits=[ref_qubit.get(av, 0), ref_qubit.get(bv, 1)],
                    params=[],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

            # ── single-qubit gate: quake.<g> %ref : (!quake.ref) -> () ──────
            m = re.match(
                r"quake\.(h|x|y|z|s|t|sdg|tdg)\s+%(\S+?)\s*:", raw)
            if m:
                gname     = m.group(1)
                qubit_var = m.group(2).rstrip(":)")
                gate = GateOperation(
                    name=gname,
                    qubits=[ref_qubit.get(qubit_var, 0)],
                    params=[],
                    line_number=i,
                )
                all_gates.append(gate)
                ordered_ops.append(("gate", gate))
                continue

        qubit_alloc = QubitAllocation(
            num_qubits=num_qubits,
            allocation_type="static",
            qubit_vars=ref_qubit,
        )
        return MLIRCircuit(
            dialect_name=self.name,
            num_qubits=num_qubits,
            gates=all_gates,
            measurements=all_meas,
            conditionals=all_conds if all_conds else None,
            ordered_ops=ordered_ops,
            has_conditionals=bool(all_conds),
            qubit_allocation=qubit_alloc,
            metadata={"source": "quake"},
        )

    # ── Helper: parse gates inside a cc.if body block ─────────────────────────

    def _parse_block_gates(
        self,
        lines: List[str],
        outer_ref_qubit: Dict[str, int],
        outer_ssa_int:   Dict[str, int],
        outer_ssa_float: Dict[str, float],
    ) -> List[GateOperation]:
        """Parse gate operations inside a cc.if { } body.

        May define local arith.constant + quake.extract_ref before the gate.
        Inherits the outer SSA state.
        """
        local_ints   = dict(outer_ssa_int)
        local_floats = dict(outer_ssa_float)
        local_refs   = dict(outer_ref_qubit)
        gates: List[GateOperation] = []

        for raw in lines:
            raw = raw.strip()
            if not raw:
                continue

            # arith.constant int
            m = re.match(
                r"%(\S+?)\s*=\s*arith\.constant\s+(\d+)\s*:\s*i64", raw)
            if m:
                local_ints[m.group(1)] = int(m.group(2))
                continue

            # arith.constant float
            m = re.match(
                r"%(\S+?)\s*=\s*arith\.constant\s+([-+]?[\d.]+(?:[eE][-+]?\d+)?)\s*:\s*f64",
                raw)
            if m:
                try:
                    local_floats[m.group(1)] = float(m.group(2))
                except ValueError:
                    pass
                continue

            # quake.extract_ref
            m = re.match(
                r"%(\S+?)\s*=\s*quake\.extract_ref\s+%\S+\[%(\S+?)\]", raw)
            if m:
                var, idx_var = m.group(1), m.group(2).rstrip(":)")
                local_refs[var] = local_ints.get(idx_var, 0)
                continue

            # single-qubit gate
            m = re.match(
                r"quake\.(h|x|y|z|s|t|sdg|tdg)\s+%(\S+?)\s*:", raw)
            if m:
                gname     = m.group(1)
                qubit_var = m.group(2).rstrip(":)")
                gates.append(GateOperation(
                    name=gname,
                    qubits=[local_refs.get(qubit_var, 0)],
                    params=[],
                ))
                continue

            # parametric single-qubit
            m = re.match(
                r"quake\.(rx|ry|rz|r1)\s+\(%(\S+?)\)\s+%(\S+?)\s*:", raw)
            if m:
                gname     = m.group(1)
                angle_var = m.group(2).rstrip(":)")
                qvar      = m.group(3).rstrip(":)")
                gates.append(GateOperation(
                    name=gname,
                    qubits=[local_refs.get(qvar, 0)],
                    params=[local_floats.get(angle_var, 0.0)],
                ))
                continue

        return gates

    # ── Legacy helper used by parse_qubits ────────────────────────────────────

    def _build_ref_map(self, mlir_code: str) -> Dict[str, int]:
        """Best-effort SSA→qubit index map (used by standalone parse_qubits)."""
        ssa_int: Dict[str, int] = {}
        ref_qubit: Dict[str, int] = {}
        for line in mlir_code.splitlines():
            line = line.strip()
            m = re.match(
                r"%(\S+?)\s*=\s*arith\.constant\s+(\d+)\s*:\s*i64", line)
            if m:
                ssa_int[m.group(1)] = int(m.group(2))
                continue
            m = re.match(
                r"%(\S+?)\s*=\s*quake\.extract_ref\s+%\S+\[%(\S+?)\]", line)
            if m:
                var, idx_var = m.group(1), m.group(2).rstrip(":)")
                ref_qubit[var] = ssa_int.get(idx_var, 0)
        return ref_qubit

    # kept for backward compat
    def _extract_qubit_variables(self, mlir_code: str) -> Dict[str, int]:
        return self._build_ref_map(mlir_code)

    def _parse_parameter(self, param_str: str) -> float:
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", param_str)
        return float(m.group()) if m else 0.0
