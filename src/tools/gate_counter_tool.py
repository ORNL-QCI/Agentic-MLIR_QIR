"""Gate counter tool for CrewAI agents."""

from crewai_tools import BaseTool
import logging

logger = logging.getLogger(__name__)


class GateCounterTool(BaseTool):
    """Tool for counting and comparing gates between MLIR and QIR."""

    name: str = "Gate Counter"
    description: str = """
    Counts and compares quantum gates between MLIR and QIR circuits.

    Input: Two circuits separated by '|||' marker:
    <MLIR_CODE>|||<QIR_CODE>

    Output: Gate count comparison with:
    - Gate counts for each circuit
    - Match status (pass/fail)
    - Discrepancies if any
    - Missing or extra gates

    Use this to verify gate translation accuracy.
    """

    def _run(self, input_str: str) -> str:
        """Execute gate counting and comparison.

        Args:
            input_str: MLIR and QIR code separated by '|||'

        Returns:
            Formatted comparison result
        """
        from ..verification.gate_counter import GateCounter

        try:
            # Split input
            if '|||' not in input_str:
                return "Error: Input must contain MLIR and QIR separated by '|||'"

            parts = input_str.split('|||', 1)
            mlir_code = parts[0].strip()
            qir_code = parts[1].strip()

            # Count gates
            counter = GateCounter()
            mlir_counts = counter.count_mlir_gates(mlir_code)
            qir_counts = counter.count_qir_gates(qir_code)

            # Compare
            comparison = counter.compare(mlir_counts, qir_counts)

            # Format output
            output = "=== Gate Count Analysis ===\n\n"

            output += f"MLIR Gates (Total: {comparison['mlir_total']}):\n"
            for gate, count in comparison['mlir_gates'].items():
                output += f"  {gate}: {count}\n"

            output += f"\nQIR Gates (Total: {comparison['qir_total']}):\n"
            for gate, count in comparison['qir_gates'].items():
                output += f"  {gate}: {count}\n"

            output += f"\nMatch: {'✓ PASS' if comparison['matches'] else '✗ FAIL'}\n"
            output += f"Similarity: {comparison['similarity']:.2%}\n"

            if comparison['discrepancies']:
                output += "\nDiscrepancies:\n"
                for disc in comparison['discrepancies']:
                    output += f"  {disc['gate']}: MLIR={disc['mlir_count']}, QIR={disc['qir_count']}\n"

            # Missing/extra gates
            missing = counter.get_missing_gates(mlir_counts, qir_counts)
            extra = counter.get_extra_gates(mlir_counts, qir_counts)

            if missing:
                output += f"\nMissing in QIR: {', '.join(missing)}\n"

            if extra:
                output += f"Extra in QIR: {', '.join(extra)}\n"

            return output

        except Exception as e:
            logger.error(f"Gate counter error: {e}")
            return f"Error: {str(e)}"
