"""Agentic MLIR-to-QIR translator.

A hybrid deterministic + LLM-based system that converts MLIR quantum circuits
to QIR (LLVM IR) format, with dual-backend simulation verification.

Quick start
-----------

>>> from agentic_mlir_qir import translate
>>> mlir_source = open("circuit.mlir").read()
>>> result = translate(mlir_source)
>>> print(result.qir)
>>> print(result.dialect, result.translation_path, result.success)

For agentic (LLM) translation of unseen dialects, install the ``agentic``
extra and pass a ``model`` key:

>>> result = translate(mlir_source, model="llama3.1-8b")    # local Ollama
>>> result = translate(mlir_source, model="gpt-oss-20b")    # HuggingFace cloud

For full verification (gate counts + dual-backend simulation + TVD), install
the ``verify`` extra (and optionally ``quake`` for the CUDA-Q backend):

>>> result = translate(mlir_source, verify=True, shots=1024)
>>> print(result.verification.similarity, result.verification.passes)

See :func:`translate` for the full parameter list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "translate",
    "translate_qasm",
    "TranslateResult",
    "VerificationSummary",
    # Lower-level building blocks (re-exported for advanced users)
    "MLIRParser",
    "QIRGenerator",
    "DialectDetector",
    "run_verification_pipeline",
    "GateCounter",
    "compute_distribution_similarity",
    "VerificationThresholds",
    "UnsupportedDialectError",
]


# -----------------------------------------------------------------------------
# Lower-level re-exports (lazy: importing this package must NOT pull in the
# heavy verification / agent stacks until the user asks for them).
# -----------------------------------------------------------------------------

# Cheap imports — no native runtimes touched.
from .parsers.mlir_parser import MLIRParser
from .generators.qir_generator import QIRGenerator
from .dialects.dialect_detector import DialectDetector
from .dialects.base_dialect import UnsupportedDialectError


def __getattr__(name: str) -> Any:
    """Lazy attribute resolver for heavy submodules.

    This keeps ``import agentic_mlir_qir`` cheap — verification backends
    (qirrunner, pennylane-catalyst, cudaq) and CrewAI are only loaded when
    a function that needs them is actually called.
    """
    if name in ("run_verification_pipeline",):
        from .verification.pipeline import run_verification_pipeline as _f
        return _f
    if name in ("GateCounter",):
        from .verification.gate_counter import GateCounter as _c
        return _c
    if name in ("compute_distribution_similarity", "VerificationThresholds"):
        from .verification import metrics as _m
        return getattr(_m, name)
    raise AttributeError(f"module 'agentic_mlir_qir' has no attribute {name!r}")


# -----------------------------------------------------------------------------
# High-level public API
# -----------------------------------------------------------------------------


@dataclass
class VerificationSummary:
    """Compact, JSON-serialisable summary of the verification pipeline result."""

    similarity: float = 0.0
    passes: bool = False
    gate_match: bool = False
    qir_distribution: dict = field(default_factory=dict)
    mlir_distribution: dict = field(default_factory=dict)
    qir_is_mock: bool = True
    mlir_is_mock: bool = True
    mlir_runner_label: str = ""
    error: Optional[str] = None
    raw: Optional[dict] = None  # full pipeline dict for advanced consumers


@dataclass
class TranslateResult:
    """Result of :func:`translate`.

    Attributes
    ----------
    qir : str
        Generated QIR (LLVM IR) source.
    dialect : str
        Detected MLIR dialect ('catalyst', 'quake', 'unknown', or an
        agent-inferred prefix for unseen dialects).
    translation_path : str
        One of ``"deterministic"``, ``"ai_agent"``, ``"deterministic+repair"``.
    success : bool
        ``True`` iff verification (when run) passed; ``True`` for any
        deterministic translation when ``verify=False``.
    iterations : int
        Number of agent refinement iterations (1 for the deterministic path).
    error : Optional[str]
        Error message if translation or verification failed.
    verification : Optional[VerificationSummary]
        Verification result, or ``None`` if ``verify=False``.
    """

    qir: str = ""
    dialect: str = "unknown"
    translation_path: str = "deterministic"
    success: bool = False
    iterations: int = 1
    error: Optional[str] = None
    verification: Optional[VerificationSummary] = None
    source_format: str = "mlir"  # "mlir", "openqasm2", or "openqasm3"


def _wrap_verification(vr: Optional[dict]) -> Optional[VerificationSummary]:
    if not vr:
        return None
    return VerificationSummary(
        similarity=float(vr.get("similarity", 0.0) or 0.0),
        passes=bool(vr.get("similarity_passes", False)
                    and vr.get("gate_comparison", {}).get("matches", False)),
        gate_match=bool(vr.get("gate_comparison", {}).get("matches", False)),
        qir_distribution=dict(vr.get("qir_distribution", {})),
        mlir_distribution=dict(vr.get("catalyst_distribution", {})),
        qir_is_mock=bool(vr.get("qir_is_mock", True)),
        mlir_is_mock=bool(vr.get("catalyst_is_mock", True)),
        mlir_runner_label=str(vr.get("mlir_runner_label", "")),
        error=vr.get("error"),
        raw=vr,
    )


def translate(
    mlir_source: str,
    *,
    model: Optional[str] = None,
    verify: bool = False,
    shots: int = 1000,
    mode: str = "shots",
    max_iterations: int = 5,
    force_agentic: bool = False,
) -> TranslateResult:
    """Translate an MLIR quantum circuit to QIR.

    This is the high-level one-call entry point. It picks the cheapest
    reliable translation path:

    * Known dialect (Catalyst, Quake) and ``model is None`` →
      pure-Python deterministic parser + QIR generator.
    * Known dialect with ``model`` set + ``force_agentic=True`` →
      forces the LLM path (useful for benchmarking).
    * Unknown dialect → requires ``model`` to be set; routes to the
      LLM-driven agentic path (CrewAI). Raises
      :class:`UnsupportedDialectError` if ``model is None``.

    Parameters
    ----------
    mlir_source : str
        MLIR source code (the contents of a .mlir file, not a path).
    model : str, optional
        LLM model key (see :class:`agentic_mlir_qir.config.llm_config.LLMConfig.MODELS`),
        e.g. ``"llama3.1-8b"`` or ``"gpt-oss-20b"``. ``None`` (default) means
        deterministic-only. Requires the ``agentic`` extra:
        ``pip install 'agentic-mlir-qir[agentic]'``.
    verify : bool, default False
        Run the dual-backend verification pipeline after translation.
        Requires the ``verify`` extra (and optionally ``quake`` for Quake
        circuits): ``pip install 'agentic-mlir-qir[verify,quake]'``.
    shots : int, default 1000
        Number of shots for sampled simulation verification.
    mode : {"shots", "probs"}, default "shots"
        Verification mode. ``"probs"`` uses exact probabilities on the MLIR
        side (zero shot noise); ``"shots"`` is sample-based on both sides.
    max_iterations : int, default 5
        Maximum LLM repair iterations (only used when ``model`` is set).
    force_agentic : bool, default False
        Skip the deterministic parser even on known dialects. Requires
        ``model``. Useful for benchmarking the LLM in isolation.

    Returns
    -------
    TranslateResult
        See :class:`TranslateResult`.

    Raises
    ------
    UnsupportedDialectError
        Dialect not recognised AND no ``model`` provided.
    RuntimeError
        ``model`` was provided but the ``agentic`` extra is not installed,
        or the LLM backend (Ollama, HuggingFace) is unreachable.
    """
    if not mlir_source or not mlir_source.strip():
        raise ValueError("mlir_source is empty")

    # ---- Path A: model + verify  →  full agentic+verification pipeline ----
    if model is not None:
        try:
            from .agents.crew_manager import CrewManager
            from .config.llm_config import LLMConfig
            from .config import settings as _settings  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Agentic translation requires the 'agentic' extra. "
                "Install with: pip install 'agentic-mlir-qir[agentic]'"
            ) from exc

        # Build the LLM via the same path translate.py uses.
        from . import _llm_factory
        llm = _llm_factory.build_llm(model)

        manager = CrewManager(llm=llm, max_iterations=max_iterations, verbose=False)

        if verify:
            tr = manager.translate_with_verification(
                mlir_source, shots=shots, force_agentic=force_agentic,
            )
            return TranslateResult(
                qir=tr.qir_code or "",
                dialect=tr.dialect or "unknown",
                translation_path=tr.translation_path,
                iterations=tr.iterations,
                success=tr.success,
                error=tr.error_message,
                verification=_wrap_verification(tr.verification_result),
            )
        else:
            tr = manager.translate(mlir_source)  # legacy agent-only path
            return TranslateResult(
                qir=tr.qir_code or "",
                dialect=tr.dialect or "unknown",
                translation_path=tr.translation_path,
                iterations=tr.iterations,
                success=tr.success,
                error=tr.error_message,
                verification=None,
            )

    # ---- Path B: deterministic-only  →  parser + generator ----------------
    parser = MLIRParser()
    try:
        circuit = parser.parse(mlir_source)
    except UnsupportedDialectError:
        raise UnsupportedDialectError(
            "Dialect not recognised by the deterministic parser. Pass model='...' "
            "to enable the agentic pipeline (requires the 'agentic' extra)."
        )

    qir = QIRGenerator().generate(circuit, module_id="translated-circuit")

    result = TranslateResult(
        qir=qir,
        dialect=circuit.dialect_name,
        translation_path="deterministic",
        success=True,  # provisional; possibly downgraded by verification below
    )

    if verify:
        try:
            from .verification.pipeline import run_verification_pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Verification requires the 'verify' extra. "
                "Install with: pip install 'agentic-mlir-qir[verify]'"
            ) from exc

        vr = run_verification_pipeline(mlir_source, qir, shots=shots, mode=mode)
        result.verification = _wrap_verification(vr)
        result.success = bool(result.verification and result.verification.passes)
        if vr.get("error"):
            result.error = vr["error"]

    return result


def translate_qasm(
    qasm_source: str,
    *,
    verify: bool = False,
    shots: int = 1000,
    mode: str = "shots",
) -> TranslateResult:
    """Translate an OpenQASM 2.0/3.0 circuit to QIR.

    The QASM source is converted to Quake-dialect MLIR using the existing
    Qiskit + CUDA-Q toolchain (see
    :mod:`agentic_mlir_qir.frontends.qasm_frontend`), then handed to the same
    deterministic :func:`translate` pipeline as native MLIR input. The result's
    :attr:`TranslateResult.source_format` records the detected QASM version.

    Parameters
    ----------
    qasm_source : str
        OpenQASM source code (the contents of a .qasm file, not a path).
    verify : bool, default False
        Run the dual-backend verification pipeline (Quake-side CUDA-Q
        simulator vs. QIR runner). Requires the ``verify`` and ``quake`` extras.
    shots : int, default 1000
        Number of shots for sampled simulation verification.
    mode : {"shots", "probs"}, default "shots"
        Verification mode, forwarded to :func:`translate`.

    Returns
    -------
    TranslateResult
        With ``dialect == "quake"`` and ``source_format`` in
        ``{"openqasm2", "openqasm3"}``.

    Raises
    ------
    ValueError
        ``qasm_source`` is empty or is not a recognisable OpenQASM program.
    RuntimeError
        The ``qasm`` extra (qiskit / qiskit-qasm3-import / cuda-quantum) is not
        installed.
    UnsupportedQASMGateError
        A gate in the program has no CUDA-Q kernel-builder mapping.
    """
    if not qasm_source or not qasm_source.strip():
        raise ValueError("qasm_source is empty")

    from .frontends.qasm_frontend import detect_qasm_version, qasm_to_mlir

    version = detect_qasm_version(qasm_source)  # raises ValueError if not QASM
    mlir_source = qasm_to_mlir(qasm_source)

    result = translate(mlir_source, verify=verify, shots=shots, mode=mode)
    result.source_format = f"openqasm{version}"
    return result
