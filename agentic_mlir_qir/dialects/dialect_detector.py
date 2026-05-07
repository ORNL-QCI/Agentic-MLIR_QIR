"""Auto-detection of MLIR dialects."""

from typing import List
from .base_dialect import BaseDialect, UnsupportedDialectError
from .catalyst_dialect import CatalystDialect
from .quake_dialect import QuakeDialect


class DialectDetector:
    """Automatically detect which MLIR dialect to use for parsing.

    This allows the system to automatically handle different MLIR dialects
    without the user needing to specify which one they're using.
    """

    def __init__(self):
        """Initialize detector with all available dialects."""
        # Register all available dialects here
        # Order matters - dialects are checked in this order
        self.dialects: List[BaseDialect] = [
            CatalystDialect(),
            QuakeDialect(),
            # Future dialects can be added here:
            # OpenQASMDialect(),
            # etc.
        ]

    def detect(self, mlir_code: str) -> BaseDialect:
        """Auto-detect which dialect to use for parsing.

        Args:
            mlir_code: MLIR source code as string

        Returns:
            Appropriate BaseDialect instance

        Raises:
            UnsupportedDialectError: If no dialect can parse the code
        """
        for dialect in self.dialects:
            if dialect.can_parse(mlir_code):
                return dialect

        # If we get here, no dialect matched
        raise UnsupportedDialectError(
            "Cannot detect MLIR dialect. The code may use an unsupported dialect or be malformed."
        )

    def get_available_dialects(self) -> List[str]:
        """Get list of available dialect names."""
        return [d.name for d in self.dialects]

    def get_dialect_by_name(self, name: str) -> BaseDialect:
        """Get specific dialect by name.

        Args:
            name: Dialect name (e.g., 'catalyst', 'quake')

        Returns:
            BaseDialect instance

        Raises:
            UnsupportedDialectError: If dialect name not found
        """
        for dialect in self.dialects:
            if dialect.name.lower() == name.lower():
                return dialect

        raise UnsupportedDialectError(
            f"Dialect '{name}' not found. Available dialects: {self.get_available_dialects()}"
        )

    def register_dialect(self, dialect: BaseDialect):
        """Dynamically register a new dialect.

        This allows plugins to add new dialect support at runtime.

        Args:
            dialect: BaseDialect instance to register
        """
        # Check if dialect name already exists
        existing_names = [d.name for d in self.dialects]
        if dialect.name in existing_names:
            # Replace existing dialect
            self.dialects = [d for d in self.dialects if d.name != dialect.name]

        self.dialects.append(dialect)


# Global detector instance
detector = DialectDetector()
