"""RAG tool for retrieving knowledge base context."""

from typing import Any, Optional
from crewai.tools import BaseTool
import logging

logger = logging.getLogger(__name__)


class RAGTool(BaseTool):
    """Tool for retrieving relevant documentation from knowledge base."""

    name: str = "Knowledge Base Retrieval"
    description: str = """
    Retrieves relevant documentation and examples from the MLIR/QIR knowledge base.

    Input: A query about MLIR gates, QIR syntax, translation patterns, or examples.
    Output: Relevant documentation snippets with sources.

    Example queries:
    - "How to translate Hadamard gate from MLIR to QIR?"
    - "QIR syntax for CNOT gate"
    - "Examples of conditional operations in QIR"
    - "MLIR Catalyst dialect gate syntax"
    """
    knowledge_base: Optional[Any] = None

    def __init__(self, knowledge_base=None, **kwargs):
        super().__init__(knowledge_base=knowledge_base, **kwargs)

        # Lazy load if not provided
        if self.knowledge_base is None:
            from ..rag.knowledge_base import KnowledgeBase
            try:
                self.knowledge_base = KnowledgeBase()
                logger.info("RAG tool initialized with knowledge base")
            except Exception as e:
                logger.warning(f"Could not initialize knowledge base: {e}")
                self.knowledge_base = None

    def _run(self, query: str) -> str:
        """Execute RAG retrieval.

        Args:
            query: Search query

        Returns:
            Formatted retrieval results
        """
        if self.knowledge_base is None:
            return "Knowledge base not available. Please initialize with 'python scripts/initialize_db.py'"

        try:
            # Query knowledge base
            results = self.knowledge_base.query(query, n_results=5)

            if not results:
                return f"No relevant documentation found for: {query}"

            # Format results
            output = f"Retrieved {len(results)} relevant documents:\n\n"

            for i, doc in enumerate(results, 1):
                source = doc.metadata.get('source', 'unknown')
                category = doc.metadata.get('category', 'unknown')

                output += f"[{i}] Source: {source} (Category: {category})\n"
                output += f"{doc.content[:500]}...\n\n"

            return output

        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")
            return f"Error retrieving knowledge: {str(e)}"
