"""Catalyst dialect adapter for PennyLane Catalyst MLIR."""

import re
from typing import List, Dict, Optional, Tuple
from .base_dialect import (
    BaseDialect,
    GateOperation,
    QubitAllocation,
    MeasurementOperation,
    ConditionalBlock,
    MLIRCircuit,
    ParsingError
)


class CatalystDialect(BaseDialect):
    """Adapter for PennyLane Catalyst MLIR dialect.

    Uses SSA-aware single-pass parsing to correctly track qubit indices
    through multi-result operations like CNOT.
    """

    @property
    def name(self) -> str:
        return "catalyst"

    # Gate mappings from Catalyst to QIR
    GATE_MAPPING = {
        "Hadamard": "__quantum__qis__h__body",
        "PauliX": "__quantum__qis__x__body",
        "PauliY": "__quantum__qis__y__body",
        "PauliZ": "__quantum__qis__z__body",
        "S": "__quantum__qis__s__body",
        "T": "__quantum__qis__t__body",
        "Sdg": "__quantum__qis__sdg__body",
        "Tdg": "__quantum__qis__tdg__body",
        "RX": "__quantum__qis__rx__body",
        "RY": "__quantum__qis__ry__body",
        "RZ": "__quantum__qis__rz__body",
        "PhaseShift": "__quantum__qis__rz__body",
        "CNOT": "__quantum__qis__cnot__body",
        "CZ": "__quantum__qis__cz__body",
        "SWAP": "__quantum__qis__swap__body",
        "CY": "__quantum__qis__cy__body",
        "Toffoli": "__quantum__qis__ccx__body",
        "CSWAP": "__quantum__qis__cswap__body",
    }

    def can_parse(self, mlir_code: str) -> bool:
        catalyst_markers = [
            "quantum.custom",
            "catalyst.launch_kernel",
            "quantum.alloc",
            "quantum.extract",
            "quantum.measure",
            "!quantum.bit",
            "!quantum.reg",
        ]
        return any(marker in mlir_code for marker in catalyst_markers)

    def parse_circuit(self, mlir_code: str) -> MLIRCircuit:
        """Parse complete Catalyst MLIR with SSA-aware tracking."""
        try:
            num_qubits = self._parse_num_qubits(mlir_code)
            qubit_alloc = QubitAllocation(
                num_qubits=num_qubits,
                allocation_type="static",
                qubit_vars={}
            )

            # Single-pass SSA-aware parse
            ordered_ops, gates, measurements, conditionals = self._ssa_parse(mlir_code, num_qubits)
            has_conditionals = len(conditionals) > 0

            return MLIRCircuit(
                dialect_name=self.name,
                num_qubits=num_qubits,
                gates=gates,
                measurements=measurements,
                qubit_allocation=qubit_alloc,
                has_conditionals=has_conditionals,
                metadata={"source": "catalyst"},
                conditionals=conditionals,
                ordered_ops=ordered_ops
            )
        except Exception as e:
            raise ParsingError(f"Failed to parse Catalyst MLIR: {str(e)}") from e

    def _parse_num_qubits(self, mlir_code: str) -> int:
        alloc_pattern = r'quantum\.alloc\(\s*(\d+)\s*\)'
        match = re.search(alloc_pattern, mlir_code)
        if not match:
            raise ParsingError("Could not find quantum.alloc statement")
        return int(match.group(1))

    def _ssa_parse(self, mlir_code: str, num_qubits: int):
        """SSA-aware single-pass parse of Catalyst MLIR.

        Tracks every SSA variable to its physical qubit index as values
        flow through extract, gate, and measurement operations.

        Returns:
            (ordered_ops, gates, measurements, conditionals)
        """
        # SSA variable -> physical qubit index
        ssa_qubit: Dict[str, int] = {}
        # SSA variable -> constant float value (for gate parameters like RX angle)
        ssa_constants: Dict[str, float] = {}
        # SSA variable -> measurement result index (for tracing conditionals)
        ssa_meas_source: Dict[str, int] = {}

        ordered_ops = []
        gates = []
        measurements = []
        conditionals = []
        meas_counter = 0

        lines = mlir_code.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # --- arith.constant: track constant values for gate parameters ---
            m = re.match(r'%(\w+)\s*=\s*arith\.constant\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*:\s*f\d+', stripped)
            if m:
                ssa_constants[m.group(1)] = float(m.group(2))
                i += 1
                continue

            # --- quantum.extract: maps variable to physical qubit index ---
            m = re.match(r'%(\w+)\s*=\s*quantum\.extract\s+%\w+\[\s*(\d+)\s*\]', stripped)
            if m:
                ssa_qubit[m.group(1)] = int(m.group(2))
                i += 1
                continue

            # --- quantum.custom: multi-result (2-qubit gate like CNOT) ---
            m = re.match(
                r'%(\w+):(\d+)\s*=\s*quantum\.custom\s+"(\w+)"\(([^)]*)\)\s+(.+?)\s*:\s*',
                stripped
            )
            if m:
                out_var = m.group(1)
                gate_name = m.group(3)
                params_str = m.group(4)
                operands_str = m.group(5)

                operand_vars = self._extract_operand_vars(operands_str)
                qubit_indices = [self._resolve_qubit(v, ssa_qubit) for v in operand_vars]

                # Map output#N to the same physical qubit as input N
                for idx, q in enumerate(qubit_indices):
                    ssa_qubit[f"{out_var}#{idx}"] = q

                params = self._parse_parameters(params_str, ssa_constants)
                gate = GateOperation(name=gate_name, qubits=qubit_indices, params=params)
                gates.append(gate)
                ordered_ops.append(("gate", gate))
                i += 1
                continue

            # --- quantum.custom: single-result (1-qubit gate like Hadamard) ---
            m = re.match(
                r'%(\w+)\s*=\s*quantum\.custom\s+"(\w+)"\(([^)]*)\)\s+(.+?)\s*:\s*',
                stripped
            )
            if m:
                out_var = m.group(1)
                gate_name = m.group(2)
                params_str = m.group(3)
                operands_str = m.group(4)

                operand_vars = self._extract_operand_vars(operands_str)
                qubit_indices = [self._resolve_qubit(v, ssa_qubit) for v in operand_vars]

                # Single output maps to the same physical qubit as input
                if qubit_indices:
                    ssa_qubit[out_var] = qubit_indices[0]

                params = self._parse_parameters(params_str, ssa_constants)
                gate = GateOperation(name=gate_name, qubits=qubit_indices, params=params)
                gates.append(gate)
                ordered_ops.append(("gate", gate))
                i += 1
                continue

            # --- quantum.measure ---
            m = re.match(r'%(\w+),\s*%(\w+)\s*=\s*quantum\.measure\s+%(\S+)', stripped)
            if m:
                meas_result_var = m.group(1)
                out_qubit_var = m.group(2)
                input_var = m.group(3)

                qubit_idx = self._resolve_qubit(input_var, ssa_qubit)
                # The output qubit variable maps to the same physical qubit
                ssa_qubit[out_qubit_var] = qubit_idx
                # Track measurement result for conditional tracing
                ssa_meas_source[meas_result_var] = meas_counter

                meas = MeasurementOperation(qubit=qubit_idx, result_var=meas_result_var)
                measurements.append(meas)
                ordered_ops.append(("measurement", meas))
                meas_counter += 1
                i += 1
                continue

            # --- Trace measurement results through tensor/stablehlo ops ---
            # tensor.from_elements %var -> propagate source
            m = re.match(r'%(\w+)\s*=\s*tensor\.from_elements\s+%(\w+)', stripped)
            if m:
                dst, src = m.group(1), m.group(2)
                if src in ssa_meas_source:
                    ssa_meas_source[dst] = ssa_meas_source[src]
                i += 1
                continue

            # stablehlo.convert %var -> propagate source
            m = re.match(r'%(\w+)\s*=\s*stablehlo\.convert\s+%(\w+)', stripped)
            if m:
                dst, src = m.group(1), m.group(2)
                if src in ssa_meas_source:
                    ssa_meas_source[dst] = ssa_meas_source[src]
                i += 1
                continue

            # stablehlo.compare ... %var1, %var2 -> propagate from var1
            m = re.match(r'%(\w+)\s*=\s*stablehlo\.compare\s+\w+,\s*%(\w+),', stripped)
            if m:
                dst, src = m.group(1), m.group(2)
                if src in ssa_meas_source:
                    ssa_meas_source[dst] = ssa_meas_source[src]
                i += 1
                continue

            # tensor.extract %var[] -> propagate source
            m = re.match(r'%(\w+)\s*=\s*tensor\.extract\s+%(\w+)\s*\[', stripped)
            if m:
                dst, src = m.group(1), m.group(2)
                if src in ssa_meas_source:
                    ssa_meas_source[dst] = ssa_meas_source[src]
                i += 1
                continue

            # --- scf.if conditional block ---
            m = re.match(r'%\w+\s*=\s*scf\.if\s+%(\w+)', stripped)
            if m:
                cond_var = m.group(1)
                cond_meas_idx = ssa_meas_source.get(cond_var, 0)

                # Parse the then block (look for quantum.custom inside)
                then_gates = []
                else_gates = []
                in_then = True
                i += 1
                brace_depth = 1

                while i < len(lines) and brace_depth > 0:
                    inner = lines[i].strip()

                    if '{' in inner:
                        brace_depth += inner.count('{')
                    if '}' in inner:
                        brace_depth -= inner.count('}')

                    if '} else {' in inner or inner == '} else {':
                        in_then = False
                        i += 1
                        continue

                    if brace_depth <= 0:
                        i += 1
                        break

                    # Look for quantum.extract inside conditional
                    im = re.match(r'%(\w+)\s*=\s*quantum\.extract\s+%\w+\[\s*(\d+)\s*\]', inner)
                    if im:
                        ssa_qubit[im.group(1)] = int(im.group(2))

                    # Look for quantum.custom inside conditional
                    gm = re.match(
                        r'%(\w+)\s*=\s*quantum\.custom\s+"(\w+)"\(([^)]*)\)\s+(.+?)\s*:\s*',
                        inner
                    )
                    if gm:
                        g_out = gm.group(1)
                        g_name = gm.group(2)
                        g_params_str = gm.group(3)
                        g_operands_str = gm.group(4)

                        g_operand_vars = self._extract_operand_vars(g_operands_str)
                        g_qubit_indices = [self._resolve_qubit(v, ssa_qubit) for v in g_operand_vars]

                        if g_qubit_indices:
                            ssa_qubit[g_out] = g_qubit_indices[0]

                        g_params = self._parse_parameters(g_params_str, ssa_constants)
                        g = GateOperation(name=g_name, qubits=g_qubit_indices, params=g_params)

                        if in_then:
                            then_gates.append(g)
                        else:
                            else_gates.append(g)

                    i += 1

                cond = ConditionalBlock(
                    condition_measurement_idx=cond_meas_idx,
                    then_gates=then_gates,
                    else_gates=else_gates
                )
                conditionals.append(cond)
                ordered_ops.append(("conditional", cond))
                # Don't increment i here, already advanced in the while loop
                continue

            i += 1

        return ordered_ops, gates, measurements, conditionals

    def _extract_operand_vars(self, operands_str: str) -> List[str]:
        """Extract SSA variable names from an operands string.

        Handles: %out_qubits, %2, %out_qubits_0#0, %out_qubits_0#1
        """
        vars_found = []
        # Match %varname or %varname#N
        for m in re.finditer(r'%(\w+(?:#\d+)?)', operands_str):
            vars_found.append(m.group(1))
        return vars_found

    def _resolve_qubit(self, var_name: str, ssa_qubit: Dict[str, int]) -> int:
        """Resolve an SSA variable name to its physical qubit index."""
        # Strip leading % if present
        var_name = var_name.lstrip('%')

        # Direct lookup
        if var_name in ssa_qubit:
            return ssa_qubit[var_name]

        # Try without #N suffix (shouldn't normally happen)
        base = var_name.split('#')[0]
        if base in ssa_qubit:
            return ssa_qubit[base]

        raise ParsingError(f"Cannot resolve qubit for SSA variable '%{var_name}'. "
                          f"Known variables: {list(ssa_qubit.keys())}")

    def parse_gates(self, mlir_code: str) -> List[GateOperation]:
        num_qubits = self._parse_num_qubits(mlir_code)
        _, gates, _, _ = self._ssa_parse(mlir_code, num_qubits)
        return gates

    def parse_qubits(self, mlir_code: str) -> QubitAllocation:
        num_qubits = self._parse_num_qubits(mlir_code)
        return QubitAllocation(num_qubits=num_qubits, allocation_type="static", qubit_vars={})

    def parse_measurements(self, mlir_code: str) -> List[MeasurementOperation]:
        num_qubits = self._parse_num_qubits(mlir_code)
        _, _, measurements, _ = self._ssa_parse(mlir_code, num_qubits)
        return measurements

    def get_gate_mapping(self) -> Dict[str, str]:
        return self.GATE_MAPPING

    def _parse_parameters(self, params_str: str, ssa_constants: Dict[str, float] = None) -> List[float]:
        if not params_str.strip():
            return []
        params = []
        # First, resolve SSA variable references (e.g., %cst)
        if ssa_constants:
            for m in re.finditer(r'%(\w+)', params_str):
                var_name = m.group(1)
                if var_name in ssa_constants:
                    params.append(ssa_constants[var_name])
        # If no SSA vars resolved, try literal floats
        if not params:
            param_pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
            for match in re.finditer(param_pattern, params_str):
                try:
                    params.append(float(match.group()))
                except ValueError:
                    continue
        return params
