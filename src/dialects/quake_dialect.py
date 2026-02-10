"""Quake dialect adapter for NVIDIA CUDA Quantum."""

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


class QuakeDialect(BaseDialect):
    """Adapter for NVIDIA CUDA Quantum Quake dialect.

    Quake uses different syntax than Catalyst:
    Example: quake.h %qubit  (instead of quantum.custom "Hadamard")
    """

    @property
    def name(self) -> str:
        return "quake"

    # Gate mappings from Quake to QIR
    GATE_MAPPING = {
        "h": "__quantum__qis__h__body",
        "x": "__quantum__qis__x__body",
        "y": "__quantum__qis__y__body",
        "z": "__quantum__qis__z__body",
        "s": "__quantum__qis__s__body",
        "t": "__quantum__qis__t__body",
        "rx": "__quantum__qis__rx__body",
        "ry": "__quantum__qis__ry__body",
        "rz": "__quantum__qis__rz__body",
        "cnot": "__quantum__qis__cnot__body",
        "cx": "__quantum__qis__cnot__body",  # Alias
        "cz": "__quantum__qis__cz__body",
        "swap": "__quantum__qis__swap__body",
    }

    def can_parse(self, mlir_code: str) -> bool:
        """Check if code contains Quake dialect markers."""
        quake_markers = [
            "quake.h",
            "quake.x",
            "quake.cnot",
            "quake.alloca",
            "quake.mz",
            "!quake.veq",
            "!quake.ref",
        ]
        return any(marker in mlir_code for marker in quake_markers)

    def parse_circuit(self, mlir_code: str) -> MLIRCircuit:
        """Parse complete Quake MLIR code."""
        try:
            qubit_alloc = self.parse_qubits(mlir_code)
            gates = self.parse_gates(mlir_code)
            measurements = self.parse_measurements(mlir_code)
            has_conditionals = "cf.cond_br" in mlir_code or "scf.if" in mlir_code

            return MLIRCircuit(
                dialect_name=self.name,
                num_qubits=qubit_alloc.num_qubits,
                gates=gates,
                measurements=measurements,
                qubit_allocation=qubit_alloc,
                has_conditionals=has_conditionals,
                metadata={"source": "quake"}
            )
        except Exception as e:
            raise ParsingError(f"Failed to parse Quake MLIR: {str(e)}") from e

    def parse_gates(self, mlir_code: str) -> List[GateOperation]:
        """Extract gate operations from Quake MLIR.

        Quake gate patterns:
        - Single qubit: quake.h %qubit
        - Two qubit: quake.cnot %control, %target
        - Parameterized: quake.rx(%param) %qubit
        """
        gates = []

        # Pattern for Quake gates
        # Single qubit gates
        single_gate_pattern = r'quake\.(\w+)\s+(%\S+)'

        # Two qubit gates
        two_gate_pattern = r'quake\.(\w+)\s+(%\S+),\s*(%\S+)'

        # Parameterized gates
        param_gate_pattern = r'quake\.(\w+)\(([^)]+)\)\s+(%\S+)'

        # Track qubit indices
        qubit_vars = self._extract_qubit_variables(mlir_code)

        # Parse two-qubit gates first (more specific pattern)
        for match in re.finditer(two_gate_pattern, mlir_code):
            gate_name = match.group(1)
            qubit1_var = match.group(2).strip('%')
            qubit2_var = match.group(3).strip('%')

            # Resolve qubit indices
            qubit1 = qubit_vars.get(qubit1_var, 0)
            qubit2 = qubit_vars.get(qubit2_var, 1)

            gates.append(GateOperation(
                name=gate_name,
                qubits=[qubit1, qubit2],
                params=[]
            ))

        # Parse parameterized gates
        for match in re.finditer(param_gate_pattern, mlir_code):
            gate_name = match.group(1)
            param_str = match.group(2)
            qubit_var = match.group(3).strip('%')

            # Parse parameter
            param = self._parse_parameter(param_str)
            qubit_idx = qubit_vars.get(qubit_var, 0)

            gates.append(GateOperation(
                name=gate_name,
                qubits=[qubit_idx],
                params=[param]
            ))

        # Parse single-qubit gates (excluding already parsed)
        for match in re.finditer(single_gate_pattern, mlir_code):
            gate_name = match.group(1)
            qubit_var = match.group(2).strip('%')

            # Skip if this is part of a two-qubit or parameterized gate
            full_match = match.group(0)
            if ',' in mlir_code[match.start():match.end()+20]:
                continue
            if '(' in mlir_code[match.start():match.start()+30]:
                continue

            # Skip measurement
            if gate_name == 'mz':
                continue

            qubit_idx = qubit_vars.get(qubit_var, 0)

            gates.append(GateOperation(
                name=gate_name,
                qubits=[qubit_idx],
                params=[]
            ))

        return gates

    def parse_qubits(self, mlir_code: str) -> QubitAllocation:
        """Extract qubit allocation from Quake MLIR.

        Pattern: %qubits = quake.alloca !quake.veq<N>
        """
        # Find quake.alloca statement
        alloc_pattern = r'quake\.alloca\s+!quake\.veq<(\d+)>'
        match = re.search(alloc_pattern, mlir_code)

        if not match:
            # Try alternative pattern
            alloc_pattern2 = r'quake\.alloca\s*\[\s*(\d+)\s*\]'
            match = re.search(alloc_pattern2, mlir_code)

        if not match:
            raise ParsingError("Could not find quake.alloca statement")

        num_qubits = int(match.group(1))

        # Extract qubit variable mappings
        qubit_vars = self._extract_qubit_variables(mlir_code)

        return QubitAllocation(
            num_qubits=num_qubits,
            allocation_type="static",
            qubit_vars=qubit_vars
        )

    def parse_measurements(self, mlir_code: str) -> List[MeasurementOperation]:
        """Extract measurement operations from Quake MLIR.

        Pattern: %result = quake.mz %qubit
        """
        measurements = []

        meas_pattern = r'%(\w+)\s*=\s*quake\.mz\s+(%\S+)'
        qubit_vars = self._extract_qubit_variables(mlir_code)

        for match in re.finditer(meas_pattern, mlir_code):
            result_var = match.group(1)
            qubit_var = match.group(2).strip('%')

            qubit_index = qubit_vars.get(qubit_var, 0)

            measurements.append(MeasurementOperation(
                qubit=qubit_index,
                result_var=result_var
            ))

        return measurements

    def get_gate_mapping(self) -> Dict[str, str]:
        """Return Quake gate to QIR function mapping."""
        return self.GATE_MAPPING

    def _extract_qubit_variables(self, mlir_code: str) -> Dict[str, int]:
        """Extract mapping from MLIR variable names to qubit indices.

        Quake pattern: %q0 = quake.extract_ref %qubits[0]
        """
        qubit_vars = {}

        extract_pattern = r'%(\w+)\s*=\s*quake\.extract_ref\s+%\w+\[(\d+)\]'

        for match in re.finditer(extract_pattern, mlir_code):
            var_name = match.group(1)
            index = int(match.group(2))
            qubit_vars[var_name] = index

        return qubit_vars

    def _parse_parameter(self, param_str: str) -> float:
        """Parse gate parameter from string."""
        # Extract floating point number
        param_pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
        match = re.search(param_pattern, param_str)

        if match:
            return float(match.group())

        return 0.0
