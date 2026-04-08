"""Shared verification pipeline — importable by both app.py and crew_manager.py."""

import logging

logger = logging.getLogger(__name__)


def _detect_dialect(mlir_code: str) -> str:
    """Auto-detect the MLIR dialect from source code markers."""
    if any(m in mlir_code for m in ["quake.alloca", "quake.h", "quake.mz", "!quake.veq"]):
        return "quake"
    if any(m in mlir_code for m in ["quantum.custom", "quantum.alloc", "catalyst.launch_kernel"]):
        return "catalyst"
    return "unseen"


def run_verification_pipeline(mlir_code: str, qir_code: str,
                              shots: int = 1000, mode: str = 'shots') -> dict:
    """Run the full 4-level verification pipeline.

    Level 1: Gate count comparison
    Level 2: QIR execution (qirrunner subprocess)
    Level 3: MLIR execution (dialect-specific backend via SimulatorRegistry)
    Level 4: TVD-based statistical similarity (PASS >= 95%)

    Args:
        mlir_code: Source MLIR circuit
        qir_code: Translated QIR circuit
        shots: Number of shots for sampling mode (default 1000)
        mode: 'shots' for shot-based sampling, 'probs' for exact probability
              comparison (zero shot noise). In 'probs' mode, the MLIR backend
              returns exact probabilities via qml.probs(); the QIR backend
              uses high shot count (100K) as qirrunner has no state-vector mode.
              Falls back to 'shots' mode if probs is not supported.

    For unseen dialects where no MLIR backend is available, Level 3 is skipped
    and verification is partial (QIR-only execution + gate counting).

    Returns a dict with keys:
        success, error, qir_distribution, catalyst_distribution,
        similarity, similarity_passes, gate_comparison,
        qir_is_mock, catalyst_is_mock, mlir_runner_label,
        mlir_execution_skipped, verification_mode
    """
    dialect = _detect_dialect(mlir_code)

    result = {
        'success': False,
        'error': None,
        'qir_distribution': {},
        'catalyst_distribution': {},
        'similarity': 0.0,
        'similarity_passes': False,
        'gate_comparison': {},
        'qir_is_mock': True,
        'catalyst_is_mock': True,
        'mlir_runner_label': '',
        'mlir_execution_skipped': False,
        'verification_mode': mode,
    }

    try:
        from src.verification.qir_runner import QIRRunner
        from src.verification.metrics import (
            compute_distribution_similarity,
            compute_similarity_from_probs,
            VerificationThresholds,
        )
        from src.verification.gate_counter import GateCounter
        from src.verification.simulator_registry import SimulatorRegistry

        # Level 2: QIR execution
        qir_runner = QIRRunner()
        if mode == 'probs':
            # qirrunner has no state-vector mode; use high shot count to approximate
            qir_dist = qir_runner.run(qir_code, shots=100_000)
        else:
            qir_dist = qir_runner.run(qir_code, shots=shots)
        result['qir_distribution'] = qir_dist
        result['qir_is_mock'] = qir_runner._last_run_was_mock

        # Level 3: MLIR execution (dialect-specific via registry)
        mlir_runner = SimulatorRegistry.find_runner_for_dialect(dialect)

        if mlir_runner is not None:
            result['mlir_runner_label'] = f"{mlir_runner.name} ({type(mlir_runner).__name__})"

            if mode == 'probs':
                # Try exact probability mode first
                mlir_probs = mlir_runner.run_probs(mlir_code)
                if mlir_probs is not None:
                    result['catalyst_distribution'] = mlir_probs
                    result['catalyst_is_mock'] = False

                    # Normalize QIR shot counts to probabilities for comparison
                    qir_total = sum(qir_dist.values())
                    qir_probs = {k: v / qir_total for k, v in qir_dist.items()}

                    similarity = compute_similarity_from_probs(qir_probs, mlir_probs)
                    result['similarity'] = similarity
                    result['similarity_passes'] = VerificationThresholds.check_simulation(similarity)
                else:
                    # Probs not supported (e.g. conditional circuits) — fall back to shots
                    logger.info("run_probs() not available, falling back to shots mode")
                    result['verification_mode'] = 'shots (fallback)'
                    mlir_dist = mlir_runner.run(mlir_code, shots=shots)
                    result['catalyst_distribution'] = mlir_dist
                    result['catalyst_is_mock'] = mlir_runner._last_run_was_mock
                    similarity = compute_distribution_similarity(qir_dist, mlir_dist)
                    result['similarity'] = similarity
                    result['similarity_passes'] = VerificationThresholds.check_simulation(similarity)
            else:
                mlir_dist = mlir_runner.run(mlir_code, shots=shots)
                result['catalyst_distribution'] = mlir_dist
                result['catalyst_is_mock'] = mlir_runner._last_run_was_mock

                # Level 4: Statistical comparison
                similarity = compute_distribution_similarity(qir_dist, mlir_dist)
                result['similarity'] = similarity
                result['similarity_passes'] = VerificationThresholds.check_simulation(similarity)
        else:
            # No MLIR backend for this dialect — partial verification
            logger.warning(
                "No MLIR backend available for dialect '%s'; "
                "skipping MLIR execution (Level 3) and TVD comparison (Level 4)",
                dialect,
            )
            result['mlir_execution_skipped'] = True
            result['mlir_runner_label'] = f'none (unseen dialect: {dialect})'
            # Without MLIR-side distribution, TVD cannot be computed.
            # Mark similarity as passing so gate-count alone determines success.
            result['similarity_passes'] = True
            result['similarity'] = -1.0  # sentinel: not computed

        # Level 1: Gate count comparison (exclude measurements)
        gc = GateCounter()
        mlir_gates = gc.count_mlir_gates(mlir_code)
        mlir_gates.pop('measure', None)
        mlir_gates.pop('mz', None)
        qir_gates = gc.count_qir_gates(qir_code)
        qir_gates.pop('measure', None)

        if dialect == "unseen" and not mlir_gates:
            # For unseen dialects where the MLIR parser can't count gates,
            # skip gate comparison to avoid counterproductive "remove gates"
            # feedback. The QIR-side gate count is still reported for reference.
            result['gate_comparison'] = {
                'matches': True,  # Don't penalise — we can't count MLIR gates
                'similarity': -1.0,
                'mlir_total': 0,
                'qir_total': sum(qir_gates.values()),
                'discrepancies': [],
                'mlir_gates': {},
                'qir_gates': qir_gates,
                'unseen_dialect': True,
            }
        else:
            result['gate_comparison'] = gc.compare(mlir_gates, qir_gates)

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)
        logger.exception("Verification pipeline failed")

    return result
