"""Verification pipeline for MLIR to QIR translation correctness."""

from .metrics import (
    VerificationMetrics,
    VerificationThresholds,
    compute_distribution_similarity,
    compute_kl_divergence,
)
from .gate_counter import GateCounter
from .simulator_registry import SimulatorRegistry, BaseRunner

# Import runners to trigger self-registration into SimulatorRegistry as a side effect
from . import qir_runner       # noqa: F401
from . import catalyst_runner  # noqa: F401
from . import quake_runner     # noqa: F401

__all__ = [
    "VerificationMetrics",
    "VerificationThresholds",
    "compute_distribution_similarity",
    "compute_kl_divergence",
    "GateCounter",
    "SimulatorRegistry",
    "BaseRunner",
]
