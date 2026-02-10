"""Catalyst dialect adapter for PennyLane Catalyst MLIR."""

import re
from typing import List, Dict
from .base_dialect import (
    BaseDialect,
    GateOperation,
    QubitAllocation,
    MeasurementOperation,
    MLIRCircuit,
    ParsingError
)


class CatalystDialect(BaseDialect):
    """Adapter for PennyLane Catalyst MLIR dialect.

    Catalyst uses value semantics with quantum.custom operations for gates.
    Example: quantum.custom "Hadamard"() %qubit : !quantum.bit
    """

    @property
    def name(self) -> str:
        return "catalyst"

    # Gate mappings from Catalyst to QIR
    GATE_MAPPING = {
        # Single-qubit gates
        "Hadamard": "__quantum__qis__h__body",
        "PauliX": "__quantum__qis__x__body",
        "PauliY": "__quantum__qis__y__body",
        "PauliZ": "__quantum__qis__z__body",
        "S": "__quantum__qis__s__body",
        "T": "__quantum__qis__t__body",
        "Sdg": "__quantum__qis__sdg__body",
        "Tdg": "__quantum__qis__tdg__body",

        # Parameterized single-qubit gates
        "RX": "__quantum__qis__rx__body",
        "RY": "__quantum__qis__ry__body",
        "RZ": "__quantum__qis__rz__body",
        "PhaseShift": "__quantum__qis__rz__body",  # Alias

        # Two-qubit gates
        "CNOT": "__quantum__qis__cnot__body",
        "CZ": "__quantum__qis__cz__body",
        "SWAP": "__quantum__qis__swap__body",
        "CY": "__quantum__qis__cy__body",

        # Three-qubit gates
        "Toffoli": "__quantum__qis__ccx__body",
        "CSWAP": "__quantum__qis__cswap__body",
    }

    def can_parse(self, mlir_code: str) -> bool:
        """Check if code contains Catalyst dialect markers."""
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
        """Parse complete Catalyst MLIR code."""
        try:
            qubit_alloc = self.parse_qubits(mlir_code)
            gates = self.parse_gates(mlir_code)
            measurements = self.parse_measurements(mlir_code)
            has_conditionals = "scf.if" in mlir_code

            return MLIRCircuit(
                dialect_name=self.name,
                num_qubits=qubit_alloc.num_qubits,
                gates=gates,
                measurements=measurements,
                qubit_allocation=qubit_alloc,
                has_conditionals=has_conditionals,
                metadata={"source": "catalyst"}
            )
        except Exception as e:
            raise ParsingError(f"Failed to parse Catalyst MLIR: {str(e)}") from e

    def parse_gates(self, mlir_code: str) -> List[GateOperation]:
        """Extract gate operations from Catalyst MLIR.

        Catalyst gate pattern: quantum.custom "GateName"([params]) %qubit1[, %qubit2]
        """
        gates = []

        # Pattern for quantum.custom gates
        # Matches: quantum.custom "GateName"() %qubit
        # or: quantum.custom "GateName"(%param) %qubit
        # or: quantum.custom "CNOT"() %q1, %q2
        gate_pattern = r'quantum\.custom "(\w+)"(?:\(([^)]*)\))?\s+([^:]+)'

        # Track qubit variable mappings
        qubit_vars = self._extract_qubit_variables(mlir_code)

        for match in re.finditer(gate_pattern, mlir_code):
            gate_name = match.group(1)
            params_str = match.group(2) or ""
            qubits_str = match.group(3)

            # Parse parameters
            params = self._parse_parameters(params_str)

            # Parse qubits
            qubit_indices = self._parse_qubit_indices(qubits_str, qubit_vars)

            gates.append(GateOperation(
                name=gate_name,
                qubits=qubit_indices,
                params=params
            ))

        return gates

    def parse_qubits(self, mlir_code: str) -> QubitAllocation:
        """Extract qubit allocation from Catalyst MLIR.

        Pattern: %reg = quantum.alloc( N) : !quantum.reg
        """
        # Find quantum.alloc statement
        alloc_pattern = r'quantum\.alloc\(\s*(\d+)\s*\)'
        match = re.search(alloc_pattern, mlir_code)

        if not match:
            raise ParsingError("Could not find quantum.alloc statement")

        num_qubits = int(match.group(1))

        # Extract qubit variable mappings
        qubit_vars = self._extract_qubit_variables(mlir_code)

        return QubitAllocation(
            num_qubits=num_qubits,
            allocation_type="static",
            qubit_vars=qubit_vars
        )

    def parse_measurements(self, mlir_code: str) -> List[MeasurementOperation]:
        """Extract measurement operations from Catalyst MLIR.

        Pattern: %mres, %out_qubit = quantum.measure %qubit
        """
        measurements = []

        meas_pattern = r'%(\w+),\s*%\w+\s*=\s*quantum\.measure\s+%(\w+)'
        qubit_vars = self._extract_qubit_variables(mlir_code)

        for match in re.finditer(meas_pattern, mlir_code):
            result_var = match.group(1)
            qubit_var = match.group(2)

            # Try to resolve qubit index
            qubit_index = qubit_vars.get(qubit_var, 0)

            measurements.append(MeasurementOperation(
                qubit=qubit_index,
                result_var=result_var
            ))

        return measurements

    def get_gate_mapping(self) -> Dict[str, str]:
        """Return Catalyst gate to QIR function mapping."""
        return self.GATE_MAPPING

    def _extract_qubit_variables(self, mlir_code: str) -> Dict[str, int]:
        """Extract mapping from MLIR variable names to qubit indices.

        Pattern: %qubit = quantum.extract %reg[ INDEX]
        """
        qubit_vars = {}

        extract_pattern = r'%(\w+)\s*=\s*quantum\.extract\s+%\w+\[\s*(\d+)\s*\]'

        for match in re.finditer(extract_pattern, mlir_code):
            var_name = match.group(1)
            index = int(match.group(2))
            qubit_vars[var_name] = index

        return qubit_vars

    def _parse_parameters(self, params_str: str) -> List[float]:
        """Parse gate parameters from string."""
        if not params_str.strip():
            return []

        params = []

        # Match floating point numbers (including scientific notation)
        param_pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'

        for match in re.finditer(param_pattern, params_str):
            try:
                params.append(float(match.group()))
            except ValueError:
                continue

        return params

    def _parse_qubit_indices(self, qubits_str: str, qubit_vars: Dict[str, int]) -> List[int]:
        """Parse qubit indices from qubit variable string."""
        indices = []

        # Extract variable names (starts with %)
        var_pattern = r'%(\w+)'

        for match in re.finditer(var_pattern, qubits_str):
            var_name = match.group(1)

            # Look up in qubit_vars, or try to parse from output variables
            if var_name in qubit_vars:
                indices.append(qubit_vars[var_name])
            elif "qubit" in var_name.lower():
                # Try to extract index from variable name like "out_qubits_0"
                num_match = re.search(r'_(\d+)$', var_name)
                if num_match:
                    indices.append(int(num_match.group(1)))
                else:
                    # Default to 0 if can't determine
                    indices.append(0)

        return indices
