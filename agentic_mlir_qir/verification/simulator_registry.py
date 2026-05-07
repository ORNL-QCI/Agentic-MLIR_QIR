"""Registry for quantum circuit execution backends."""

from typing import Dict, Type, List, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseRunner(ABC):
    """Abstract base class for circuit execution backends."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available on the system."""
        pass

    @abstractmethod
    def run(self, code: str, shots: int = 1000) -> Dict[str, int]:
        """Execute circuit and return measurement distribution.

        Args:
            code: Circuit code (QIR, MLIR, or other format)
            shots: Number of shots to run

        Returns:
            Dictionary mapping measurement outcomes to counts
            Example: {"00": 489, "11": 511}
        """
        pass

    @abstractmethod
    def get_circuit_info(self, code: str) -> Dict:
        """Extract circuit information (qubits, gates, depth).

        Args:
            code: Circuit code

        Returns:
            Dictionary with circuit information
        """
        pass

    def run_probs(self, code: str) -> Optional[Dict[str, float]]:
        """Return exact probability distribution (no shot noise).

        Override in subclasses that support state-vector simulation.
        Returns None if not supported by this backend.

        Returns:
            Dictionary mapping measurement outcomes to exact probabilities
            Example: {"00": 0.5, "11": 0.5}
        """
        return None

    def can_handle(self, dialect: str) -> bool:
        """Check if this backend can execute circuits from the given MLIR dialect.

        Override in subclasses. Default returns False.
        """
        return False


class SimulatorRegistry:
    """Registry for quantum simulator backends."""

    _backends: Dict[str, Type[BaseRunner]] = {}
    _instances: Dict[str, BaseRunner] = {}

    @classmethod
    def register(cls, backend_class: Type[BaseRunner]):
        """Register a backend class.

        Args:
            backend_class: Backend class to register
        """
        backend_name = backend_class().name
        cls._backends[backend_name] = backend_class
        logger.info(f"Registered backend: {backend_name}")

    @classmethod
    def get_backend(cls, name: str) -> BaseRunner:
        """Get backend instance by name.

        Args:
            name: Backend name

        Returns:
            Backend instance

        Raises:
            ValueError: If backend not found or not available
        """
        # Check if already instantiated
        if name in cls._instances:
            return cls._instances[name]

        # Check if registered
        if name not in cls._backends:
            available = cls.list_available()
            raise ValueError(
                f"Backend '{name}' not found. "
                f"Available backends: {', '.join(available)}"
            )

        # Create instance
        backend_class = cls._backends[name]
        instance = backend_class()

        # Check if available
        if not instance.is_available():
            raise ValueError(
                f"Backend '{name}' is not available on this system. "
                f"Please install required dependencies."
            )

        # Cache instance
        cls._instances[name] = instance

        return instance

    @classmethod
    def list_all(cls) -> List[str]:
        """List all registered backends.

        Returns:
            List of backend names
        """
        return list(cls._backends.keys())

    @classmethod
    def list_available(cls) -> List[str]:
        """List available backends (registered and available on system).

        Returns:
            List of available backend names
        """
        available = []
        for name, backend_class in cls._backends.items():
            try:
                instance = backend_class()
                if instance.is_available():
                    available.append(name)
            except Exception:
                continue

        return available

    @classmethod
    def find_runner_for_dialect(cls, dialect: str) -> Optional[BaseRunner]:
        """Find an available runner that can handle the given MLIR dialect.

        Returns the first available runner whose can_handle(dialect) is True,
        or None if no matching runner is found.
        """
        for name, backend_class in cls._backends.items():
            try:
                instance = backend_class()
                if instance.can_handle(dialect) and instance.is_available():
                    cls._instances[name] = instance
                    return instance
            except Exception:
                continue
        return None

    @classmethod
    def get_status(cls) -> Dict[str, Dict]:
        """Get status of all backends.

        Returns:
            Dict mapping backend names to status info
        """
        status = {}

        for name, backend_class in cls._backends.items():
            try:
                instance = backend_class()
                is_available = instance.is_available()

                status[name] = {
                    'registered': True,
                    'available': is_available,
                    'class': backend_class.__name__
                }
            except Exception as e:
                status[name] = {
                    'registered': True,
                    'available': False,
                    'error': str(e)
                }

        return status
