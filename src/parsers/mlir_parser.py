"""Main MLIR parser using dialect detection."""

from typing import Optional
from ..dialects.base_dialect import MLIRCircuit, BaseDialect
from ..dialects.dialect_detector import detector


class MLIRParser:
    """Main parser for MLIR quantum circuits.

    Automatically detects dialect and delegates parsing to
    the appropriate dialect adapter.
    """

    def __init__(self, dialect: Optional[BaseDialect] = None):
        """Initialize parser.

        Args:
            dialect: Specific dialect to use. If None, auto-detect.
        """
        self.dialect = dialect

    def parse(self, mlir_code: str) -> MLIRCircuit:
        """Parse MLIR code into structured circuit representation.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            MLIRCircuit object

        Raises:
            UnsupportedDialectError: If dialect cannot be detected
            ParsingError: If code cannot be parsed
        """
        # Detect or use specified dialect
        if self.dialect is None:
            dialect = detector.detect(mlir_code)
        else:
            dialect = self.dialect

        # Parse using detected dialect
        circuit = dialect.parse_circuit(mlir_code)

        # Validate circuit
        is_valid, errors = dialect.validate_circuit(circuit)
        if not is_valid:
            raise ValueError(f"Invalid circuit: {'; '.join(errors)}")

        return circuit

    def get_detected_dialect(self, mlir_code: str) -> str:
        """Detect dialect name without parsing.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            Dialect name
        """
        dialect = detector.detect(mlir_code)
        return dialect.name
