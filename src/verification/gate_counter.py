"""Gate counting and comparison for verification."""

import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class GateCounter:
    """Count and compare gates in MLIR and QIR circuits."""

    # MLIR gate patterns (Catalyst dialect)
    MLIR_GATE_PATTERN = r'quantum\.custom "(\w+)"'

    # QIR gate patterns
    QIR_GATE_PATTERN = r'call void @__quantum__qis__(\w+)__body'

    # Gate name mappings (MLIR -> QIR)
    GATE_MAPPINGS = {
        'Hadamard': 'h',
        'CNOT': 'cnot',
        'PauliX': 'x',
        'PauliY': 'y',
        'PauliZ': 'z',
        'S': 's',
        'T': 't',
        'RX': 'rx',
        'RY': 'ry',
        'RZ': 'rz',
        'CZ': 'cz',
        'SWAP': 'swap',
    }

    def count_mlir_gates(self, mlir_code: str) -> Dict[str, int]:
        """Count gates in MLIR code.

        Args:
            mlir_code: MLIR source code

        Returns:
            Dictionary mapping gate names to counts
        """
        counts = {}

        # Find all quantum.custom gates
        matches = re.findall(self.MLIR_GATE_PATTERN, mlir_code)

        for gate_name in matches:
            counts[gate_name] = counts.get(gate_name, 0) + 1

        # Count measurements separately
        meas_matches = re.findall(r'quantum\.measure', mlir_code)
        if meas_matches:
            counts['measure'] = len(meas_matches)

        return counts

    def count_qir_gates(self, qir_code: str) -> Dict[str, int]:
        """Count gates in QIR code.

        Args:
            qir_code: QIR source code

        Returns:
            Dictionary mapping gate names to counts
        """
        counts = {}

        # Find all __quantum__qis__ function calls
        matches = re.findall(self.QIR_GATE_PATTERN, qir_code)

        for gate_name in matches:
            # Skip measurement in gate counting
            if gate_name == 'mz':
                counts['measure'] = counts.get('measure', 0) + 1
            else:
                counts[gate_name] = counts.get(gate_name, 0) + 1

        return counts

    def compare(self, mlir_counts: Dict[str, int],
                qir_counts: Dict[str, int]) -> Dict:
        """Compare gate counts between MLIR and QIR.

        Args:
            mlir_counts: MLIR gate counts
            qir_counts: QIR gate counts

        Returns:
            Comparison result with matches, discrepancies, etc.
        """
        # Normalize MLIR gate names to QIR format
        mlir_normalized = {}
        for gate, count in mlir_counts.items():
            qir_name = self.GATE_MAPPINGS.get(gate, gate.lower())
            mlir_normalized[qir_name] = mlir_normalized.get(qir_name, 0) + count

        # Find all unique gates
        all_gates = set(mlir_normalized.keys()) | set(qir_counts.keys())

        # Compare counts
        matches = True
        discrepancies = []

        for gate in all_gates:
            mlir_count = mlir_normalized.get(gate, 0)
            qir_count = qir_counts.get(gate, 0)

            if mlir_count != qir_count:
                matches = False
                discrepancies.append({
                    'gate': gate,
                    'mlir_count': mlir_count,
                    'qir_count': qir_count,
                    'difference': qir_count - mlir_count
                })

        # Calculate similarity
        total_gates = sum(mlir_normalized.values()) + sum(qir_counts.values())
        if total_gates == 0:
            similarity = 1.0
        else:
            matching_gates = sum(
                min(mlir_normalized.get(g, 0), qir_counts.get(g, 0))
                for g in all_gates
            )
            similarity = (2 * matching_gates) / total_gates

        return {
            'matches': matches,
            'similarity': similarity,
            'mlir_total': sum(mlir_normalized.values()),
            'qir_total': sum(qir_counts.values()),
            'discrepancies': discrepancies,
            'mlir_gates': mlir_normalized,
            'qir_gates': qir_counts
        }

    def get_missing_gates(self, mlir_counts: Dict[str, int],
                          qir_counts: Dict[str, int]) -> List[str]:
        """Get gates present in MLIR but missing in QIR.

        Args:
            mlir_counts: MLIR gate counts
            qir_counts: QIR gate counts

        Returns:
            List of missing gate names
        """
        mlir_normalized = {
            self.GATE_MAPPINGS.get(g, g.lower()): c
            for g, c in mlir_counts.items()
        }

        missing = []
        for gate in mlir_normalized:
            if gate not in qir_counts and mlir_normalized[gate] > 0:
                missing.append(gate)

        return missing

    def get_extra_gates(self, mlir_counts: Dict[str, int],
                        qir_counts: Dict[str, int]) -> List[str]:
        """Get gates present in QIR but not in MLIR.

        Args:
            mlir_counts: MLIR gate counts
            qir_counts: QIR gate counts

        Returns:
            List of extra gate names
        """
        mlir_normalized = {
            self.GATE_MAPPINGS.get(g, g.lower()): c
            for g, c in mlir_counts.items()
        }

        extra = []
        for gate in qir_counts:
            if gate not in mlir_normalized and qir_counts[gate] > 0:
                extra.append(gate)

        return extra
