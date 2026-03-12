"""Verification agent for validating QIR translations."""

import logging
from crewai import Agent, Task

logger = logging.getLogger(__name__)


class VerificationAgent:
    """AI agent specialized in verifying QIR translations."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        self.llm = llm
        self.verbose = verbose
        # Agent is only used for qualitative structural feedback (not gate counting)
        self.agent = Agent(
            role="Quantum Circuit Verification Specialist",

            goal=(
                "Analyse a QIR translation and explain any structural or semantic "
                "problems compared to the original MLIR circuit. "
                "Do NOT count gates — gate counts are provided to you already."
            ),

            backstory=(
                "You are an expert in quantum circuit analysis. "
                "You receive a pre-computed gate-count diff and the two circuit listings. "
                "Your job is to explain WHY the translation is wrong and give the "
                "translator SPECIFIC instructions on what to fix (gate order, qubit "
                "indices, missing operations, wrong parameters, etc.)."
            ),

            tools=[],          # no tools needed — gate counting is done in Python
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=5,
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def verify(self, mlir_code: str, qir_code: str) -> dict:
        """Verify QIR translation against MLIR source.

        Gate counting is performed directly in Python (reliable).
        The LLM is only called when gate counts mismatch, to generate
        qualitative repair feedback.

        Returns:
            dict: passed (bool), gate_count_match (bool), feedback (str)
        """
        from ..verification.gate_counter import GateCounter

        # ---- Step 1: deterministic gate count (Python, always correct) ----
        counter = GateCounter()
        mlir_counts = counter.count_mlir_gates(mlir_code)
        qir_counts  = counter.count_qir_gates(qir_code)
        comparison  = counter.compare(mlir_counts, qir_counts)

        gates_match = comparison['matches']
        missing     = counter.get_missing_gates(mlir_counts, qir_counts)
        extra       = counter.get_extra_gates(mlir_counts, qir_counts)

        logger.info(
            "Gate counter (Python): MLIR=%d QIR=%d match=%s",
            comparison['mlir_total'], comparison['qir_total'], gates_match,
        )

        if gates_match:
            return {
                'passed': True,
                'gate_count_match': True,
                'feedback': 'Translation verified',
            }

        # ---- Step 2: build a concise diff summary -------------------------
        diff_lines = []
        for d in comparison['discrepancies']:
            diff_lines.append(
                f"  {d['gate']}: MLIR={d['mlir_count']}, QIR={d['qir_count']}"
            )
        if missing:
            diff_lines.append(f"Missing in QIR: {', '.join(missing)}")
        if extra:
            diff_lines.append(f"Extra in QIR (remove): {', '.join(extra)}")
        diff_summary = "\n".join(diff_lines)

        # ---- Step 3: ask LLM for qualitative repair advice ----------------
        llm_feedback = self._get_llm_feedback(mlir_code, qir_code, diff_summary)

        return {
            'passed': False,
            'gate_count_match': False,
            'feedback': f"Gate count mismatch:\n{diff_summary}\n\n{llm_feedback}".strip(),
        }

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _get_llm_feedback(self, mlir_code: str, qir_code: str, diff: str) -> str:
        """Ask the LLM to explain the diff and suggest concrete repairs."""
        task_description = (
            "The gate-count comparison between an MLIR circuit and its QIR translation "
            "has failed. Here is the diff:\n\n"
            f"{diff}\n\n"
            "MLIR source:\n"
            f"{mlir_code}\n\n"
            "QIR translation:\n"
            f"{qir_code}\n\n"
            "Provide a SHORT, specific list of changes the translator must make to the "
            "QIR to fix the gate count mismatch. Be concrete: name the exact gate, "
            "the qubit index, and the fix required. No preamble, no JSON."
        )
        try:
            task = Task(
                description=task_description,
                expected_output="Bulleted list of specific QIR fixes needed.",
                agent=self.agent,
            )
            result = self.agent.execute_task(task)
            return str(result).strip()
        except Exception as e:
            logger.warning("LLM feedback call failed: %s", e)
            return ""
