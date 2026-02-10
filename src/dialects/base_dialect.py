"""Abstract base class for MLIR dialect adapters."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class GateOperation:
    """Represents a quantum gate operation."""
    name: str  # Gate name (e.g., "Hadamard", "CNOT")
    qubits: List[int]  # Qubit indices
    params: List[float]  # Gate parameters (for parameterized gates)
    line_number: Optional[int] = None  # Source line number for debugging


@dataclass
class QubitAllocation:
    """Represents qubit allocation information."""
    num_qubits: int
    allocation_type: str  # "static" or "dynamic"
    qubit_vars: Dict[str, int]  # Maps MLIR variable names to qubit indices


@dataclass
class MeasurementOperation:
    """Represents a measurement operation."""
    qubit: int
    result_var: str  # Variable name for measurement result
    line_number: Optional[int] = None


@dataclass
class MLIRCircuit:
    """Structured representation of an MLIR quantum circuit."""
    dialect_name: str
    num_qubits: int
    gates: List[GateOperation]
    measurements: List[MeasurementOperation]
    qubit_allocation: QubitAllocation
    has_conditionals: bool = False
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseDialect(ABC):
    """Abstract base class for MLIR dialect adapters.

    This provides a plugin architecture for supporting different MLIR
    quantum dialects (Catalyst, Quake, etc.). Each dialect implements
    this interface to provide dialect-specific parsing and gate mapping.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the dialect name (e.g., 'catalyst', 'quake')."""
        pass

    @abstractmethod
    def can_parse(self, mlir_code: str) -> bool:
        """Check if this dialect can parse the given MLIR code.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            True if this dialect can handle the code, False otherwise
        """
        pass

    @abstractmethod
    def parse_circuit(self, mlir_code: str) -> MLIRCircuit:
        """Parse complete MLIR code into structured circuit representation.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            MLIRCircuit object with all circuit information

        Raises:
            ParsingError: If code cannot be parsed
        """
        pass

    @abstractmethod
    def parse_gates(self, mlir_code: str) -> List[GateOperation]:
        """Extract gate operations from MLIR code.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            List of GateOperation objects in execution order
        """
        pass

    @abstractmethod
    def parse_qubits(self, mlir_code: str) -> QubitAllocation:
        """Extract qubit allocation information from MLIR code.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            QubitAllocation object with allocation details
        """
        pass

    @abstractmethod
    def parse_measurements(self, mlir_code: str) -> List[MeasurementOperation]:
        """Extract measurement operations from MLIR code.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            List of MeasurementOperation objects
        """
        pass

    @abstractmethod
    def get_gate_mapping(self) -> Dict[str, str]:
        """Get dialect-specific gate name to QIR function mapping.

        Returns:
            Dictionary mapping gate names to QIR function names
            Example: {"Hadamard": "__quantum__qis__h__body", ...}
        """
        pass

    def get_qir_function_name(self, gate_name: str) -> Optional[str]:
        """Get QIR function name for a gate.

        Args:
            gate_name: Dialect-specific gate name

        Returns:
            QIR function name, or None if not found
        """
        mapping = self.get_gate_mapping()
        return mapping.get(gate_name)

    def validate_circuit(self, circuit: MLIRCircuit) -> Tuple[bool, List[str]]:
        """Validate parsed circuit for correctness.

        Args:
            circuit: Parsed MLIRCircuit object

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check qubit indices are valid
        for gate in circuit.gates:
            for qubit in gate.qubits:
                if qubit < 0 or qubit >= circuit.num_qubits:
                    errors.append(
                        f"Gate {gate.name} uses invalid qubit index {qubit} "
                        f"(circuit has {circuit.num_qubits} qubits)"
                    )

        # Check measurements use valid qubits
        for meas in circuit.measurements:
            if meas.qubit < 0 or meas.qubit >= circuit.num_qubits:
                errors.append(
                    f"Measurement uses invalid qubit index {meas.qubit} "
                    f"(circuit has {circuit.num_qubits} qubits)"
                )

        return len(errors) == 0, errors


class UnsupportedDialectError(Exception):
    """Raised when MLIR dialect is not supported."""
    pass


class ParsingError(Exception):
    """Raised when MLIR code cannot be parsed."""
    pass
