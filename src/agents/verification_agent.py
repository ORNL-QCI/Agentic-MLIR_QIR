"""Verification agent for validating QIR translations."""

from crewai import Agent
import logging

logger = logging.getLogger(__name__)


class VerificationAgent:
    """AI agent specialized in verifying QIR translations."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        """Initialize verification agent.

        Args:
            llm: Language model to use
            tools: List of tools available to agent
            verbose: Whether to show verbose output
        """
        self.agent = Agent(
            role="Quantum Circuit Verification Specialist",

            goal="""Verify QIR translation correctness through comprehensive validation.
            Check gate counts, circuit structure, and provide actionable feedback for improvements.""",

            backstory="""You are an expert in quantum circuit analysis and verification.
            You have deep knowledge of quantum computing principles and can identify
            discrepancies between circuit representations.

            Your verification process includes:
            - Gate count comparison (must match exactly)
            - Circuit structure analysis
            - Qubit usage verification
            - Measurement operation validation

            You use specialized tools to:
            1. Count gates in both MLIR and QIR
            2. Compare circuit properties
            3. Identify missing or extra operations

            When verification fails, you provide specific, actionable feedback:
            - Which gates are missing or incorrect
            - What needs to be fixed
            - Exact changes required

            You are thorough and precise, ensuring quantum circuits are translated correctly.
            """,

            tools=tools,
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=10
        )

    def verify(self, mlir_code: str, qir_code: str) -> dict:
        """Verify QIR translation against MLIR source.

        Args:
            mlir_code: Original MLIR code
            qir_code: Generated QIR code

        Returns:
            Verification result dictionary
        """
        task_description = f"""
        Verify that the QIR translation correctly represents the MLIR circuit.

        MLIR Circuit:
        ```mlir
        {mlir_code}
        ```

        QIR Translation:
        ```llvm
        {qir_code}
        ```

        Verification Steps:
        1. Use Gate Counter tool to compare gate counts (input format: MLIR|||QIR)
        2. Analyze the comparison results
        3. Determine if translation is correct

        Provide verification result in this format:
        RESULT: PASS or FAIL
        GATE_COUNT_MATCH: true or false
        FEEDBACK: <specific feedback if failed, or "Translation verified" if passed>
        """

        logger.info("Verification agent starting...")

        # Execute verification task
        result = self.agent.execute_task(task_description)

        # Parse result
        verification = self._parse_result(result)

        return verification

    def _parse_result(self, result: str) -> dict:
        """Parse verification result from agent output.

        Args:
            result: Agent output string

        Returns:
            Parsed verification dictionary
        """
        lines = result.split('\n')

        verification = {
            'passed': False,
            'gate_count_match': False,
            'feedback': result
        }

        for line in lines:
            if line.startswith('RESULT:'):
                status = line.split(':', 1)[1].strip().upper()
                verification['passed'] = status == 'PASS'

            elif line.startswith('GATE_COUNT_MATCH:'):
                match_str = line.split(':', 1)[1].strip().lower()
                verification['gate_count_match'] = match_str == 'true'

            elif line.startswith('FEEDBACK:'):
                feedback = line.split(':', 1)[1].strip()
                verification['feedback'] = feedback

        return verification
