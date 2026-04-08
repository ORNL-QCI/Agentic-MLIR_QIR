"""CrewAI orchestration for multi-agent translation system."""

import logging
import re
from typing import Optional

from crewai.hooks import before_tool_call, ToolCallHookContext

from .translation_agent import TranslationAgent
from .verification_agent import VerificationAgent
from ..tools.qir_search_tool import QIRSearchTool
from ..tools.gate_counter_tool import GateCounterTool
from ..tools.web_fetch_tool import get_web_tools
from ..tools.simulator_discovery_tool import get_simulator_discovery_tool

logger = logging.getLogger(__name__)

# ── Dedup tool hook: prevent identical consecutive tool calls ──────────────────
# Smaller models (e.g. llama3.1-8b) tend to call the same search tool 5+ times
# with the exact same query, wasting iterations. This hook blocks duplicates.

_recent_tool_queries: dict[str, str] = {}  # tool_name -> last query string


@before_tool_call
def _dedup_tool_calls(context: ToolCallHookContext) -> bool | None:
    """Block repeated identical tool calls that waste agent iterations."""
    query = str(context.tool_input.get("query", "") or
                context.tool_input.get("search_query", "") or
                context.tool_input.get("url", ""))
    if not query:
        return None  # Allow non-query tools

    last = _recent_tool_queries.get(context.tool_name)
    if last == query:
        logger.info("Dedup hook: blocking duplicate %s call with query=%r",
                     context.tool_name, query[:80])
        return False  # Block duplicate call

    _recent_tool_queries[context.tool_name] = query
    return None  # Allow

# Namespace prefixes that belong to standard MLIR dialects — excluded from
# unknown-dialect detection.
_KNOWN_NAMESPACES = {
    'quantum', 'quake', 'func', 'scf', 'arith', 'tensor',
    'stablehlo', 'cc', 'memref', 'cf', 'llvm', 'oq3',
}


class TranslationResult:
    """Result from the translation + verification process."""

    def __init__(self):
        self.qir_code: Optional[str] = None
        self.verification: Optional[dict] = None        # agent-level check (lightweight)
        self.verification_result: Optional[dict] = None # full 4-level pipeline result
        self.iterations: int = 0
        self.iteration_history: list = []
        self.success: bool = False
        self.error_message: Optional[str] = None
        self.translation_path: str = "deterministic"   # deterministic | ai_agent | deterministic+repair
        self.dialect: Optional[str] = None


class CrewManager:
    """Manages multi-agent translation + verification workflow."""

    def __init__(self, llm, knowledge_base=None, max_iterations: int = 5, verbose: bool = True):
        self.llm = llm
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Tools — lightweight search replaces heavy ChromaDB RAG
        self.qir_search_tool = QIRSearchTool()
        self.gate_counter_tool = GateCounterTool()
        self.web_tools = get_web_tools()
        self.simulator_discovery_tool = get_simulator_discovery_tool()

        # Agents (translation gets search tool; context is injected inline in prompt)
        self.translation_agent = TranslationAgent(
            llm=llm,
            tools=[self.qir_search_tool],
            verbose=verbose,
        )
        self.verification_agent = VerificationAgent(
            llm=llm,
            tools=[self.gate_counter_tool],
            verbose=verbose,
        )

        logger.info("CrewManager initialised")

    # ------------------------------------------------------------------ #
    #  Main entry point                                                    #
    # ------------------------------------------------------------------ #

    def translate_with_verification(
        self,
        mlir_code: str,
        shots: int = 1000,
        force_agentic: bool = False,
    ) -> TranslationResult:
        """Full pipeline: dialect routing → QIR generation → verification loop.

        Known dialects (Catalyst / Quake):
            1. Deterministic QIR via MLIRParser + QIRGenerator
            2. Verify; if FAIL → agent repairs up to max_iterations times

        Unknown dialects (or force_agentic=True):
            1. Translation Specialist with web-search tools generates QIR agentically
            2. Verify; if FAIL → agent retranslates with feedback

        Args:
            force_agentic: Skip the deterministic parser even for known dialects.
                           Useful for benchmarking LLM translation time/iterations.
        """
        from src.parsers.mlir_parser import MLIRParser
        from src.generators.qir_generator import QIRGenerator
        from src.dialects.base_dialect import UnsupportedDialectError
        from src.verification.pipeline import run_verification_pipeline

        result = TranslationResult()

        # ---- Phase 0: dialect detection --------------------------------
        try:
            detected_dialect = MLIRParser().get_detected_dialect(mlir_code)
            is_known = True
        except UnsupportedDialectError:
            detected_dialect = self._infer_dialect_hint(mlir_code)
            is_known = False

        result.dialect = detected_dialect

        # ---- Phase 1: initial QIR generation ---------------------------
        if is_known and not force_agentic:
            try:
                circuit = MLIRParser().parse(mlir_code)
                qir_code = QIRGenerator().generate(circuit, module_id="translated-circuit")
                result.translation_path = "deterministic"
            except Exception as e:
                result.error_message = f"Deterministic parse failed: {e}"
                logger.error(result.error_message)
                return result
        else:
            self._attach_web_tools()
            try:
                qir_code = self.translation_agent.translate_with_feedback(
                    mlir_code, dialect=detected_dialect, iteration=1,
                    is_known_dialect=is_known,
                )
                if not qir_code or not qir_code.strip():
                    result.error_message = (
                        "LLM did not produce valid QIR (likely emitted a tool-call "
                        "JSON instead of LLVM IR). Try a different model or use the "
                        "deterministic path."
                    )
                    logger.error(result.error_message)
                    return result
                result.translation_path = "ai_agent"
            except Exception as e:
                result.error_message = f"Agentic translation failed: {e}"
                logger.error(result.error_message)
                return result

        # ---- Phase 2: verification + refinement loop -------------------
        feedback_str: Optional[str] = None
        previous_qir: Optional[str] = None

        # Track the best attempt: prefer gate_match=True, then highest TVD similarity
        best_attempt: dict = {'qir_code': qir_code, 'score': (-1, -1.0), 'vr': None}

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"=== Verification iteration {iteration}/{self.max_iterations} ===")

            # Full 4-level deterministic check
            vr = run_verification_pipeline(mlir_code, qir_code, shots)
            result.verification_result = vr
            result.iterations = iteration

            gate_ok = vr['gate_comparison'].get('matches', False)
            tvd_ok = vr['similarity_passes']
            similarity = vr.get('similarity', 0.0) or 0.0

            # Update best attempt (score: gate_ok as int first, then similarity)
            score = (int(gate_ok), similarity)
            if score > best_attempt['score']:
                best_attempt = {'qir_code': qir_code, 'score': score, 'vr': vr}
                logger.debug(
                    f"New best attempt at iteration {iteration}: "
                    f"gate_ok={gate_ok}, similarity={similarity:.3f}"
                )

            # Exit early — no LLM call needed when the pipeline already passes
            if gate_ok and tvd_ok:
                logger.info(f"✓ Verification PASSED in {iteration} iteration(s)")
                result.success = True
                result.qir_code = qir_code
                result.iteration_history.append({
                    'iteration': iteration,
                    'qir_code': qir_code,
                    'gate_match': gate_ok,
                    'tvd_pass': tvd_ok,
                    'agent_feedback': None,
                    'verification': vr,
                })
                return result

            if iteration == self.max_iterations:
                logger.warning(f"Max iterations ({self.max_iterations}) reached without passing")
                result.iteration_history.append({
                    'iteration': iteration,
                    'qir_code': qir_code,
                    'gate_match': gate_ok,
                    'tvd_pass': tvd_ok,
                    'agent_feedback': None,
                    'verification': vr,
                })
                break

            # Pipeline failed and retries remain — call agent for targeted feedback
            try:
                agent_check = self.verification_agent.verify(mlir_code, qir_code)
            except Exception as e:
                logger.warning(f"Verification agent failed: {e}; using deterministic results only")
                agent_check = {'passed': False, 'gate_count_match': False, 'feedback': ''}

            result.verification = agent_check
            result.iteration_history.append({
                'iteration': iteration,
                'qir_code': qir_code,
                'gate_match': gate_ok,
                'tvd_pass': tvd_ok,
                'agent_feedback': agent_check.get('feedback'),
                'verification': vr,
            })

            # Build feedback and retry
            feedback_str = self._build_feedback_string(vr, agent_check)
            logger.info(f"Feedback for iteration {iteration + 1}:\n{feedback_str}")
            previous_qir = qir_code

            if is_known and not force_agentic:
                result.translation_path = "deterministic+repair"

            try:
                new_qir = self.translation_agent.translate_with_feedback(
                    mlir_code,
                    dialect=detected_dialect,
                    feedback=feedback_str,
                    previous_qir=previous_qir,
                    iteration=iteration + 1,
                    is_known_dialect=is_known,
                )
                if new_qir and new_qir.strip():
                    qir_code = new_qir
                else:
                    logger.warning(
                        "Iteration %d produced empty QIR (tool-call JSON?); "
                        "retrying with previous QIR", iteration + 1
                    )
            except Exception as e:
                logger.error(f"Agent repair failed on iteration {iteration + 1}: {e}")
                break

        # Return the best-scoring attempt, not necessarily the last one
        best_gate_ok = best_attempt['score'][0] == 1
        best_sim = best_attempt['score'][1]
        logger.info(
            f"Returning best attempt: gate_ok={best_gate_ok}, similarity={best_sim:.3f}"
        )
        result.qir_code = best_attempt['qir_code']
        if best_attempt['vr'] is not None:
            result.verification_result = best_attempt['vr']
        result.error_message = (
            f"Did not pass full verification after {result.iterations} iteration(s)"
        )
        return result

    # ------------------------------------------------------------------ #
    #  Legacy method (kept for backward compatibility)                     #
    # ------------------------------------------------------------------ #

    def translate(self, mlir_code: str, dialect: Optional[str] = None) -> TranslationResult:
        """Execute translation with iterative refinement (legacy, agent-only path)."""
        result = TranslationResult()
        result.dialect = dialect

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"=== Iteration {iteration}/{self.max_iterations} ===")

            try:
                qir_code = self.translation_agent.translate(mlir_code, dialect)
                result.qir_code = qir_code
            except Exception as e:
                result.error_message = f"Translation failed: {e}"
                return result

            try:
                verification = self.verification_agent.verify(mlir_code, qir_code)
                result.verification = verification
            except Exception as e:
                verification = {'passed': False, 'feedback': f"Verification error: {e}"}
                result.verification = verification

            result.iteration_history.append({
                'iteration': iteration,
                'qir_code': qir_code,
                'verification': verification,
            })
            result.iterations = iteration

            if verification.get('passed', False):
                logger.info(f"✓ Translation verified in {iteration} iteration(s)")
                result.success = True
                return result

            if iteration < self.max_iterations:
                logger.info(f"Feedback: {verification.get('feedback')}")
        else:
            result.error_message = f"Failed to verify after {self.max_iterations} iterations"

        return result

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _build_feedback_string(self, vr: dict, agent_check: dict) -> str:
        """Synthesise deterministic + agent verification into repair instructions."""
        parts = []

        gate_comp = vr.get('gate_comparison', {})

        # For unseen dialects, gate comparison is unreliable (MLIR parser can't
        # count gates for unknown ops), so provide QIR-side info only.
        if gate_comp.get('unseen_dialect'):
            qir_gates = gate_comp.get('qir_gates', {})
            if qir_gates:
                gate_str = ", ".join(f"{g}={c}" for g, c in sorted(qir_gates.items()))
                parts.append(
                    f"UNSEEN DIALECT: Gate comparison unavailable (MLIR parser "
                    f"cannot count gates for this dialect). QIR gates produced: {gate_str}. "
                    f"Verify the translation is semantically correct by re-reading the MLIR."
                )
        elif not gate_comp.get('matches', True):
            parts.append("GATE COUNT MISMATCH:")
            for disc in gate_comp.get('discrepancies', []):
                parts.append(
                    f"  Gate '{disc['gate']}': MLIR has {disc['mlir_count']}, "
                    f"QIR has {disc['qir_count']} (diff {disc['difference']:+d})"
                )
            missing = [
                d['gate'] for d in gate_comp.get('discrepancies', [])
                if d.get('mlir_count', 0) > d.get('qir_count', 0)
            ]
            extra = [
                d['gate'] for d in gate_comp.get('discrepancies', [])
                if d.get('qir_count', 0) > d.get('mlir_count', 0)
            ]
            if missing:
                parts.append(f"  Missing in QIR: {', '.join(missing)}")
            if extra:
                parts.append(f"  Extra in QIR (remove): {', '.join(extra)}")

        if not vr.get('similarity_passes', True):
            sim_pct = vr.get('similarity', 0) * 100
            parts.append(
                f"SIMULATION MISMATCH: TVD similarity is {sim_pct:.1f}% (need >= 95%). "
                "The quantum operations are producing a different probability distribution "
                "than the MLIR circuit. Check gate order, parameters, and qubit indexing."
            )

        agent_fb = agent_check.get('feedback', '')
        if agent_fb and agent_fb.lower() not in ('translation verified', ''):
            parts.append(f"AGENT ANALYSIS: {agent_fb}")

        return "\n".join(parts) if parts else "Unknown verification failure."

    def _attach_web_tools(self) -> None:
        """Append web-search and simulator discovery tools to the translation agent (idempotent)."""
        current = list(self.translation_agent.agent.tools or [])
        current_names = {t.name for t in current}
        for tool in self.web_tools:
            if tool.name not in current_names:
                current.append(tool)
                current_names.add(tool.name)
        if self.simulator_discovery_tool and self.simulator_discovery_tool.name not in current_names:
            current.append(self.simulator_discovery_tool)
            current_names.add(self.simulator_discovery_tool.name)
        self.translation_agent.agent.tools = current
        logger.debug(f"Translation agent tools: {[t.name for t in current]}")

    @staticmethod
    def _infer_dialect_hint(mlir_code: str) -> str:
        """Scan MLIR for the most common unknown namespace prefix."""
        prefixes = re.findall(r'\b([a-z][a-z0-9_]*)\.', mlir_code)
        counts: dict = {}
        for p in prefixes:
            if p not in _KNOWN_NAMESPACES:
                counts[p] = counts.get(p, 0) + 1
        return max(counts, key=counts.get) if counts else "unknown"
