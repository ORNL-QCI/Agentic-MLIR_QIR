"""Lightweight QIR search tool for agentic translation.

Replaces the heavy ChromaDB RAG tool with a simple keyword-based lookup
over the inline reference material. The agent already has the full reference
in its prompt context; this tool lets it do targeted lookups when needed.
"""

import logging
from crewai.tools import BaseTool
from .qir_reference import (
    GATE_MAPPINGS,
    QIR_TEMPLATE,
    CORE_PATTERNS,
    CATALYST_PATTERNS,
    QUAKE_PATTERNS,
)

logger = logging.getLogger(__name__)

# Pre-built searchable sections for fast keyword matching
_SECTIONS = {
    "gate_mappings": GATE_MAPPINGS,
    "qir_template": QIR_TEMPLATE,
    "translation_patterns": CORE_PATTERNS,
    "catalyst_patterns": CATALYST_PATTERNS,
    "quake_patterns": QUAKE_PATTERNS,
}


class QIRSearchTool(BaseTool):
    """Search the QIR reference material by keyword.

    Returns matching sections from the gate mapping table,
    QIR template, or translation patterns.
    """

    name: str = "QIR Reference Search"
    description: str = (
        "Search the QIR reference for gate mappings, syntax, or translation patterns. "
        "Input: a keyword like 'Hadamard', 'CNOT', 'measurement', 'conditional', 'template'. "
        "Returns matching reference sections."
    )

    def _run(self, query: str) -> str:
        query_lower = query.lower()
        matches = []

        for section_name, content in _SECTIONS.items():
            # Split into lines and find matching ones with context
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Return the matching line plus a few lines of context
                    start = max(0, i - 1)
                    end = min(len(lines), i + 3)
                    snippet = "\n".join(lines[start:end])
                    matches.append(f"[{section_name}]\n{snippet}")
                    break  # one match per section is enough

        if not matches:
            return f"No matches for '{query}'. Available topics: gate names (Hadamard, CNOT, RX, etc.), measurement, conditional, template, qubit pointer."

        return "\n\n---\n\n".join(matches)
