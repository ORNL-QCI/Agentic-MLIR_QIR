"""Translation agent for MLIR to QIR conversion."""

from crewai import Agent
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TranslationAgent:
    """AI agent specialized in MLIR to QIR translation."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        """Initialize translation agent.

        Args:
            llm: Language model to use
            tools: List of tools available to agent
            verbose: Whether to show verbose output
        """
        self.agent = Agent(
            role="MLIR to QIR Translation Specialist",

            goal="""Convert MLIR quantum circuits to valid QIR format with high accuracy.
            Use the knowledge base to retrieve translation patterns and examples.
            Generate QIR code that matches the MLIR circuit's quantum operations exactly.""",

            backstory="""You are an expert in quantum circuit representations with deep knowledge
            of MLIR dialects (Catalyst, Quake) and QIR specifications. You have extensive
            experience translating between quantum intermediate representations.

            Your expertise includes:
            - Understanding MLIR quantum dialect syntax and semantics
            - QIR specification and LLVM IR conventions
            - Quantum gate mappings and transformations
            - Qubit indexing and pointer representation
            - Measurement operations and classical control flow

            You use the knowledge base to retrieve relevant documentation and examples
            to ensure accurate translation. You pay careful attention to:
            - Correct gate mappings (e.g., quantum.custom "Hadamard" -> __quantum__qis__h__body)
            - Proper qubit pointer generation (null for qubit 0, inttoptr for others)
            - Measurement result handling
            - QIR module structure and metadata

            When translating:
            1. First, understand the MLIR circuit structure
            2. Query knowledge base for relevant gate mappings and patterns
            3. Generate QIR with correct syntax and structure
            4. Include all required declarations and metadata
            """,

            tools=tools,
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=15
        )

    def translate(self, mlir_code: str, dialect: Optional[str] = None) -> str:
        """Translate MLIR to QIR.

        Args:
            mlir_code: MLIR source code
            dialect: MLIR dialect (if known)

        Returns:
            Generated QIR code
        """
        dialect_info = f" ({dialect} dialect)" if dialect else ""

        task_description = f"""
        Translate the following MLIR quantum circuit{dialect_info} to QIR format:

        ```mlir
        {mlir_code}
        ```

        Requirements:
        1. Use the Knowledge Base Retrieval tool to find relevant gate mappings and patterns
        2. Generate complete QIR code including:
           - Module header with type definitions
           - Entry function with all operations
           - Function declarations
           - Attributes
           - Metadata
        3. Ensure all gate names are correctly mapped
        4. Use correct qubit pointer syntax
        5. Follow QIR specification standards

        Return ONLY the complete QIR code, no explanations.
        """

        logger.info("Translation agent starting...")

        # Execute task
        result = self.agent.execute_task(task_description)

        return result
