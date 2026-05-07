"""Verification metrics for circuit comparison."""

from typing import Dict, List
from dataclasses import dataclass
import math


@dataclass
class VerificationMetrics:
    """Container for verification metrics."""

    # Gate counting
    gate_count_match: bool
    gate_count_similarity: float
    mlir_gate_count: int
    qir_gate_count: int

    # Circuit depth
    depth_match: bool
    mlir_depth: int
    qir_depth: int
    depth_difference: int

    # Simulation
    simulation_similarity: float
    simulation_passed: bool

    # Overall
    overall_pass: bool

    # Detailed info
    missing_gates: List[str] = None
    extra_gates: List[str] = None
    gate_discrepancies: List[Dict] = None

    def __post_init__(self):
        if self.missing_gates is None:
            self.missing_gates = []
        if self.extra_gates is None:
            self.extra_gates = []
        if self.gate_discrepancies is None:
            self.gate_discrepancies = []


def compute_distribution_similarity(dist1: Dict[str, int],
                                     dist2: Dict[str, int]) -> float:
    """Compute similarity between two probability distributions.

    Uses Total Variation Distance converted to similarity.

    Args:
        dist1: First distribution
        dist2: Second distribution

    Returns:
        Similarity score between 0 and 1
    """
    # Normalize distributions
    total1 = sum(dist1.values())
    total2 = sum(dist2.values())

    if total1 == 0 or total2 == 0:
        return 0.0

    prob1 = {k: v / total1 for k, v in dist1.items()}
    prob2 = {k: v / total2 for k, v in dist2.items()}

    # Get all outcomes
    all_outcomes = set(prob1.keys()) | set(prob2.keys())

    # Compute Total Variation Distance
    tvd = 0.5 * sum(
        abs(prob1.get(outcome, 0) - prob2.get(outcome, 0))
        for outcome in all_outcomes
    )

    # Convert to similarity (0 = completely different, 1 = identical)
    similarity = 1.0 - tvd

    return similarity


def compute_similarity_from_probs(probs1: Dict[str, float],
                                   probs2: Dict[str, float]) -> float:
    """Compute TVD similarity from exact probability distributions (no shot noise).

    Args:
        probs1: First probability distribution (values sum to ~1.0)
        probs2: Second probability distribution (values sum to ~1.0)

    Returns:
        Similarity score between 0 and 1 (1.0 = identical distributions)
    """
    all_outcomes = set(probs1.keys()) | set(probs2.keys())
    tvd = 0.5 * sum(
        abs(probs1.get(outcome, 0.0) - probs2.get(outcome, 0.0))
        for outcome in all_outcomes
    )
    return 1.0 - tvd


def compute_kl_divergence(dist1: Dict[str, int],
                          dist2: Dict[str, int]) -> float:
    """Compute KL divergence between two distributions.

    Args:
        dist1: First distribution (P)
        dist2: Second distribution (Q)

    Returns:
        KL divergence D_KL(P||Q)
    """
    # Normalize distributions
    total1 = sum(dist1.values())
    total2 = sum(dist2.values())

    if total1 == 0 or total2 == 0:
        return float('inf')

    prob1 = {k: v / total1 for k, v in dist1.items()}
    prob2 = {k: v / total2 for k, v in dist2.items()}

    # Get all outcomes
    all_outcomes = set(prob1.keys()) | set(prob2.keys())

    # Compute KL divergence with numerically stable epsilon
    eps = 1e-10
    kl_div = 0.0
    for outcome in all_outcomes:
        p = prob1.get(outcome, eps)
        q = prob2.get(outcome, eps)

        if p > eps:
            kl_div += p * math.log(p / max(q, eps))

    return kl_div


def estimate_circuit_depth(gate_sequence: List[Dict]) -> int:
    """Estimate circuit depth from gate sequence.

    Args:
        gate_sequence: List of gate operations with qubit indices

    Returns:
        Estimated circuit depth
    """
    if not gate_sequence:
        return 0

    # Track latest time each qubit was used
    qubit_times = {}

    for gate in gate_sequence:
        qubits = gate.get('qubits', [])

        # Get maximum time across qubits this gate acts on
        max_time = max((qubit_times.get(q, 0) for q in qubits), default=0)

        # Update all qubits to new time
        new_time = max_time + 1
        for qubit in qubits:
            qubit_times[qubit] = new_time

    # Circuit depth is maximum time
    return max(qubit_times.values()) if qubit_times else 0


class VerificationThresholds:
    """Thresholds for verification metrics."""

    GATE_COUNT_TOLERANCE = 0.0  # Exact match required
    DEPTH_TOLERANCE = 1  # Allow ±1 difference
    SIMULATION_SIMILARITY_THRESHOLD = 0.95  # 95% similarity required

    @classmethod
    def check_gate_count(cls, mlir_count: int, qir_count: int) -> bool:
        """Check if gate counts match within tolerance."""
        if cls.GATE_COUNT_TOLERANCE == 0.0:
            return mlir_count == qir_count

        diff = abs(mlir_count - qir_count)
        avg = (mlir_count + qir_count) / 2

        if avg == 0:
            return diff == 0

        return diff / avg <= cls.GATE_COUNT_TOLERANCE

    @classmethod
    def check_depth(cls, mlir_depth: int, qir_depth: int) -> bool:
        """Check if depths match within tolerance."""
        return abs(mlir_depth - qir_depth) <= cls.DEPTH_TOLERANCE

    @classmethod
    def check_simulation(cls, similarity: float) -> bool:
        """Check if simulation similarity meets threshold."""
        return similarity >= cls.SIMULATION_SIMILARITY_THRESHOLD
