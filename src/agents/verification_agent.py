"""Verification agent for validating QIR translations."""

from crewai import Agent, Task
import logging

logger = logging.getLogger(__name__)


class VerificationAgent:
    """AI agent specialized in verifying QIR translations."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        self.agent = Agent(
            role="Quantum Circuit Verification Specialist",

            goal=(
                "Verify QIR translation correctness through comprehensive validation. "
                "Check gate counts, circuit structure, and provide actionable feedback "
                "for improvements."
            ),

            backstory=(
                "You are an expert in quantum circuit analysis and verification. "
                "You have deep knowledge of quantum computing principles and can identify "
                "discrepancies between circuit representations.\n\n"
                "Your verification process includes:\n"
                "- Gate count comparison (must match exactly)\n"
                "- Circuit structure analysis\n"
                "- Qubit usage verification\n"
                "- Measurement operation validation\n\n"
                "You use specialized tools to count gates in both MLIR and QIR, "
                "compare circuit properties, and identify missing or extra operations.\n\n"
                "When verification fails, you provide specific, actionable feedback: "
                "which gates are missing or incorrect, what needs to be fixed, "
                "and the exact changes required.\n\n"
                "You are thorough and precise, ensuring quantum circuits are translated correctly."
            ),

            tools=tools,
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=10,
        )

    def verify(self, mlir_code: str, qir_code: str) -> dict:
        """Verify QIR translation against MLIR source.

        Returns:
            dict with keys: passed (bool), gate_count_match (bool), feedback (str)
        """
        task_description = (
            "Verify that the QIR translation correctly represents the MLIR circuit.\n\n"
            f"MLIR Circuit:\n```mlir\n{mlir_code}\n```\n\n"
            f"QIR Translation:\n```llvm\n{qir_code}\n```\n\n"
            "Verification Steps:\n"
            "1. Use the Gate Counter tool to compare gate counts (input format: MLIR_CODE|||QIR_CODE)\n"
            "2. Analyse the comparison results\n"
            "3. Determine if translation is correct\n\n"
            "Provide your result in EXACTLY this format:\n"
            "RESULT: PASS or FAIL\n"
            "GATE_COUNT_MATCH: true or false\n"
            "FEEDBACK: <specific feedback if failed, or 'Translation verified' if passed>"
        )

        logger.info("Verification agent starting...")

        task = Task(
            description=task_description,
            expected_output="Verification result with RESULT, GATE_COUNT_MATCH, and FEEDBACK",
            agent=self.agent,
        )
        result = self.agent.execute_task(task)
        return self._parse_result(str(result))

    def _parse_result(self, result: str) -> dict:
        verification = {
            'passed': False,
            'gate_count_match': False,
            'feedback': result,
        }
        for line in result.split('\n'):
            if line.startswith('RESULT:'):
                verification['passed'] = line.split(':', 1)[1].strip().upper() == 'PASS'
            elif line.startswith('GATE_COUNT_MATCH:'):
                verification['gate_count_match'] = (
                    line.split(':', 1)[1].strip().lower() == 'true'
                )
            elif line.startswith('FEEDBACK:'):
                verification['feedback'] = line.split(':', 1)[1].strip()
        return verification
