"""CrewAI orchestration for multi-agent translation system."""

from crewai import Crew, Task
from typing import Optional
import logging

from .translation_agent import TranslationAgent
from .verification_agent import VerificationAgent
from ..tools.rag_tool import RAGTool
from ..tools.gate_counter_tool import GateCounterTool

logger = logging.getLogger(__name__)


class TranslationResult:
    """Result from translation process."""

    def __init__(self):
        self.qir_code: Optional[str] = None
        self.verification: Optional[dict] = None
        self.iterations: int = 0
        self.iteration_history: list = []
        self.success: bool = False
        self.error_message: Optional[str] = None


class CrewManager:
    """Manages multi-agent translation workflow."""

    def __init__(self, llm, knowledge_base=None, max_iterations: int = 3, verbose: bool = True):
        """Initialize crew manager.

        Args:
            llm: Language model to use
            knowledge_base: KnowledgeBase instance
            max_iterations: Maximum refinement iterations
            verbose: Whether to show verbose output
        """
        self.llm = llm
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Initialize tools
        self.rag_tool = RAGTool(knowledge_base=knowledge_base)
        self.gate_counter_tool = GateCounterTool()

        # Initialize agents
        self.translation_agent = TranslationAgent(
            llm=llm,
            tools=[self.rag_tool],
            verbose=verbose
        )

        self.verification_agent = VerificationAgent(
            llm=llm,
            tools=[self.gate_counter_tool],
            verbose=verbose
        )

        logger.info("CrewManager initialized")

    def translate(self, mlir_code: str, dialect: Optional[str] = None) -> TranslationResult:
        """Execute translation with iterative refinement.

        Args:
            mlir_code: MLIR source code
            dialect: MLIR dialect (if known)

        Returns:
            TranslationResult with QIR and verification info
        """
        result = TranslationResult()

        logger.info(f"Starting translation (max iterations: {self.max_iterations})...")

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"=== Iteration {iteration}/{self.max_iterations} ===")

            # Translation
            logger.info("Translating MLIR to QIR...")
            try:
                qir_code = self.translation_agent.translate(mlir_code, dialect)
                result.qir_code = qir_code
            except Exception as e:
                logger.error(f"Translation error: {e}")
                result.error_message = f"Translation failed: {str(e)}"
                return result

            # Verification
            logger.info("Verifying translation...")
            try:
                verification = self.verification_agent.verify(mlir_code, qir_code)
                result.verification = verification
            except Exception as e:
                logger.error(f"Verification error: {e}")
                verification = {
                    'passed': False,
                    'feedback': f"Verification error: {str(e)}"
                }
                result.verification = verification

            # Record iteration
            result.iteration_history.append({
                'iteration': iteration,
                'qir_code': qir_code,
                'verification': verification
            })

            result.iterations = iteration

            # Check if passed
            if verification.get('passed', False):
                logger.info(f"✓ Translation verified successfully in {iteration} iteration(s)!")
                result.success = True
                return result

            # Prepare for next iteration
            if iteration < self.max_iterations:
                logger.info(f"Verification failed. Feedback: {verification.get('feedback')}")
                logger.info("Refining translation...")

                # In a full implementation, we would pass feedback back to translation agent
                # For now, we'll just retry
            else:
                logger.warning(f"Max iterations ({self.max_iterations}) reached without passing verification")
                result.error_message = f"Failed to verify after {self.max_iterations} iterations"

        return result

    def translate_with_crew(self, mlir_code: str) -> str:
        """Alternative: Use CrewAI's native task system.

        Args:
            mlir_code: MLIR source code

        Returns:
            QIR code
        """
        # Define tasks
        translation_task = Task(
            description=f"""
            Translate this MLIR circuit to QIR:
            {mlir_code}

            Use knowledge base for gate mappings.
            Return complete QIR code.
            """,
            agent=self.translation_agent.agent,
            expected_output="Complete QIR code"
        )

        verification_task = Task(
            description="""
            Verify the QIR translation using gate counting.
            Ensure all gates match the MLIR circuit.
            """,
            agent=self.verification_agent.agent,
            expected_output="Verification result (PASS/FAIL)",
            context=[translation_task]
        )

        # Create crew
        crew = Crew(
            agents=[
                self.translation_agent.agent,
                self.verification_agent.agent
            ],
            tasks=[translation_task, verification_task],
            verbose=self.verbose
        )

        # Execute
        logger.info("Executing crew...")
        result = crew.kickoff()

        return result
