"""Translation agent for MLIR to QIR conversion."""

from crewai import Agent, Task
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TranslationAgent:
    """AI agent specialized in MLIR to QIR translation."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        self.agent = Agent(
            role="MLIR to QIR Translation Specialist",

            goal=(
                "Convert MLIR quantum circuits to valid QIR format with high accuracy. "
                "Use the knowledge base to retrieve translation patterns and examples. "
                "Generate QIR code that matches the MLIR circuit's quantum operations exactly."
            ),

            backstory=(
                "You are an expert in quantum circuit representations with deep knowledge "
                "of MLIR dialects (Catalyst, Quake) and QIR specifications. You have extensive "
                "experience translating between quantum intermediate representations.\n\n"
                "Your expertise includes:\n"
                "- Understanding MLIR quantum dialect syntax and semantics\n"
                "- QIR specification and LLVM IR conventions\n"
                "- Quantum gate mappings and transformations\n"
                "- Qubit indexing and pointer representation\n"
                "- Measurement operations and classical control flow\n\n"
                "You use the knowledge base to retrieve relevant documentation and examples "
                "to ensure accurate translation. When translating:\n"
                "1. First, understand the MLIR circuit structure\n"
                "2. Query knowledge base for relevant gate mappings and patterns\n"
                "3. Generate QIR with correct syntax and structure\n"
                "4. Include all required declarations and metadata"
            ),

            tools=tools,
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=15,
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def translate(self, mlir_code: str, dialect: Optional[str] = None) -> str:
        """Translate MLIR to QIR (first attempt, no prior feedback)."""
        return self.translate_with_feedback(mlir_code, dialect, iteration=1)

    def translate_with_feedback(
        self,
        mlir_code: str,
        dialect: Optional[str],
        feedback: Optional[str] = None,
        previous_qir: Optional[str] = None,
        iteration: int = 1,
    ) -> str:
        """Translate MLIR to QIR, optionally incorporating feedback from a prior attempt.

        Args:
            mlir_code:     MLIR source code.
            dialect:       Detected dialect name, or None / "unknown" for unrecognised.
            feedback:      Structured failure feedback from the previous iteration.
            previous_qir:  The QIR produced in the previous iteration.
            iteration:     Current iteration number (1-based).

        Returns:
            Generated QIR code string.
        """
        dialect_is_unknown = dialect is None or dialect.lower() == "unknown"
        dialect_info = f" ({dialect} dialect)" if dialect and not dialect_is_unknown else ""

        # ---- Build task description ----------------------------------------
        parts = []

        if dialect_is_unknown:
            parts.append(
                "UNRECOGNIZED DIALECT DETECTED.\n\n"
                "Step 1 — RESEARCH: Use the 'Read website content' tool to fetch "
                "official documentation for the namespace prefixes you see in the code below "
                "(e.g. search mlir.llvm.org, GitHub, or the dialect's GitHub repo). "
                "Look specifically for: gate names, qubit allocation syntax, measurement ops.\n"
                "Step 2 — CROSS-REFERENCE: Use the Knowledge Base Retrieval tool to check "
                "if any of these gates are already documented locally.\n"
                "Step 3 — TRANSLATE: Using what you have learned, generate complete valid QIR.\n\n"
            )

        parts.append(
            f"Translate the following MLIR quantum circuit{dialect_info} to QIR format:\n\n"
            f"```mlir\n{mlir_code}\n```\n\n"
            "Requirements:\n"
            "1. Use the Knowledge Base Retrieval tool to find relevant gate mappings\n"
            "2. Generate complete QIR including: module header, type definitions, "
            "entry function with all operations, function declarations, attributes, metadata\n"
            "3. Ensure all gate names are correctly mapped to __quantum__qis__*__body calls\n"
            "4. Use correct qubit pointer syntax (null for qubit 0, inttoptr for others)\n"
            "5. Follow QIR specification standards\n\n"
            "Return ONLY the complete QIR code, no explanations."
        )

        if iteration > 1 and previous_qir and feedback:
            parts.append(
                f"\n\n--- PREVIOUS ATTEMPT (iteration {iteration - 1}) ---\n"
                f"The previous QIR had the following issues:\n\n{feedback}\n\n"
                f"Previous QIR code:\n```llvm\n{previous_qir}\n```\n\n"
                "Fix EVERY issue listed above. Do not repeat the same mistakes."
            )

        task_description = "".join(parts)

        logger.info(f"Translation agent starting (iteration {iteration})...")

        task = Task(
            description=task_description,
            expected_output="Complete QIR LLVM IR code",
            agent=self.agent,
        )
        result = self.agent.execute_task(task)
        return str(result)
