"""Shared verification pipeline — importable by both app.py and crew_manager.py."""

import logging

logger = logging.getLogger(__name__)


def run_verification_pipeline(mlir_code: str, qir_code: str, shots: int = 1000) -> dict:
    """Run the full 4-level verification pipeline.

    Level 1: Gate count comparison
    Level 2: QIR execution (qirrunner subprocess)
    Level 3: MLIR execution (CatalystRunner or QuakeRunner, dialect-detected)
    Level 4: TVD-based statistical similarity (PASS >= 95%)

    Returns a dict with keys:
        success, error, qir_distribution, catalyst_distribution,
        similarity, similarity_passes, gate_comparison,
        qir_is_mock, catalyst_is_mock, mlir_runner_label
    """
    is_quake = any(m in mlir_code for m in
                   ["quake.alloca", "quake.h", "quake.mz", "!quake.veq"])

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
        'mlir_runner_label': 'cudaq (QuakeRunner)' if is_quake else 'Catalyst (qjit)',
    }

    try:
        from src.verification.qir_runner import QIRRunner
        from src.verification.metrics import compute_distribution_similarity, VerificationThresholds
        from src.verification.gate_counter import GateCounter

        # Level 2: QIR execution
        qir_runner = QIRRunner()
        qir_dist = qir_runner.run(qir_code, shots=shots)
        result['qir_distribution'] = qir_dist
        result['qir_is_mock'] = qir_runner._last_run_was_mock

        # Level 3: MLIR execution (dialect-specific)
        if is_quake:
            from src.verification.quake_runner import QuakeRunner
            mlir_runner = QuakeRunner()
        else:
            from src.verification.catalyst_runner import CatalystRunner
            mlir_runner = CatalystRunner()

        mlir_dist = mlir_runner.run(mlir_code, shots=shots)
        result['catalyst_distribution'] = mlir_dist
        result['catalyst_is_mock'] = mlir_runner._last_run_was_mock

        # Level 4: Statistical comparison
        similarity = compute_distribution_similarity(qir_dist, mlir_dist)
        result['similarity'] = similarity
        result['similarity_passes'] = VerificationThresholds.check_simulation(similarity)

        # Level 1: Gate count comparison (exclude measurements)
        gc = GateCounter()
        mlir_gates = gc.count_mlir_gates(mlir_code)
        mlir_gates.pop('measure', None)
        mlir_gates.pop('mz', None)
        qir_gates = gc.count_qir_gates(qir_code)
        qir_gates.pop('measure', None)
        result['gate_comparison'] = gc.compare(mlir_gates, qir_gates)

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)
        logger.exception("Verification pipeline failed")

    return result
