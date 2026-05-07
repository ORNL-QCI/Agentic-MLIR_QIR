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
        # Catalyst dialect names (PascalCase)
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
        # Quake dialect adjoint gates → QIR adjoint names
        'sdg': 's_adj',
        'tdg': 't_adj',
    }

    def count_mlir_gates(self, mlir_code: str) -> Dict[str, int]:
        """Count gates in MLIR code.

        Supports both Catalyst dialect (quantum.custom "GateName") and
        Quake dialect (quake.h, quake.x [ctrl] tgt, etc.).

        Args:
            mlir_code: MLIR source code

        Returns:
            Dictionary mapping gate names to counts
        """
        counts = {}

        # Quake dialect: detect by presence of quake.* ops
        if any(m in mlir_code for m in ("quake.alloca", "!quake.veq", "!quake.ref")):
            # Single-qubit gates (not controlled)
            for gate in ('h', 'y', 'z', 's', 't', 'sdg', 'tdg'):
                n = len(re.findall(rf'quake\.{gate}\s+%', mlir_code))
                if n:
                    counts[gate] = n

            # X gate: distinguish controlled (CNOT) from plain X
            n_cnot = len(re.findall(r'quake\.x\s+\[', mlir_code))
            n_x = len(re.findall(r'quake\.x\s+%', mlir_code))
            if n_cnot:
                counts['cnot'] = n_cnot
            if n_x:
                counts['x'] = n_x

            # Z gate: distinguish controlled (CZ) from plain Z
            # In Quake dialect, controlled-Z is `quake.z [ctrl] target`, NOT `quake.cz`
            n_cz = len(re.findall(r'quake\.z\s+\[', mlir_code))
            if n_cz:
                counts['cz'] = n_cz

            # Two-qubit non-controlled gates (swap only — cz handled above)
            n_swap = len(re.findall(r'quake\.swap\s+%', mlir_code))
            if n_swap:
                counts['swap'] = n_swap

            # Parametric gates
            for gate in ('rx', 'ry', 'rz', 'r1'):
                n = len(re.findall(rf'quake\.{gate}\s*\(', mlir_code))
                if n:
                    counts[gate] = n

            # Measurements
            n_meas = len(re.findall(r'quake\.mz\s+%', mlir_code))
            if n_meas:
                counts['measure'] = n_meas

            return counts

        # Catalyst dialect: quantum.custom "GateName"
        matches = re.findall(self.MLIR_GATE_PATTERN, mlir_code)
        for gate_name in matches:
            counts[gate_name] = counts.get(gate_name, 0) + 1

        # Count measurements separately
        meas_matches = re.findall(r'quantum\.measure', mlir_code)
        if meas_matches:
            counts['measure'] = len(meas_matches)

        # If we didn't find any gates with the known-dialect patterns,
        # fall back to generic keyword extraction for unseen dialects.
        # Scan each MLIR operation line for a recognized gate keyword.
        if not counts:
            counts = self._count_gates_by_keyword(mlir_code)

        return counts

    # Gate keywords recognized in unseen-dialect op names.
    # Ordered so longest keywords are matched first (cnot before not, cx before x).
    _GATE_KEYWORDS_ORDERED = [
        'cnot', 'cx', 'cz', 'swap', 'measure',
        'rx', 'ry', 'rz', 'mz',
        'h', 'x', 'y', 'z', 's', 't',
    ]
    # Canonical gate name per keyword (some keywords alias).
    _KEYWORD_TO_GATE = {
        'cnot': 'cnot', 'cx': 'cnot',
        'cz': 'cz',
        'swap': 'swap',
        'rx': 'rx', 'ry': 'ry', 'rz': 'rz',
        'measure': 'measure', 'mz': 'measure',
        'h': 'h', 'x': 'x', 'y': 'y', 'z': 'z',
        's': 's', 't': 't',
    }

    def _count_gates_by_keyword(self, mlir_code: str) -> Dict[str, int]:
        """Generic gate-keyword extraction for unseen MLIR dialects.

        Scans each line for `<dialect>.<op_name>` patterns and identifies
        the gate by finding a recognized keyword as a substring (longest
        match wins). Matches the same rules used in the LLM prompt guidance
        so that MLIR-side and QIR-side counts are directly comparable.
        """
        counts: Dict[str, int] = {}
        # Match any dialect-prefixed op name: e.g. "ftqc.logical_cz", "myq.cnot_op"
        op_pattern = re.compile(r'\b([a-z][a-z0-9_]*)\.([a-z0-9_]+)')
        seen_ops = set()
        # Standard MLIR keywords that are not quantum ops
        _SKIP = {
            'func', 'arith', 'scf', 'cf', 'tensor', 'memref', 'llvm',
            'stablehlo', 'transform', 'builtin', 'cc',
        }
        for match in op_pattern.finditer(mlir_code):
            dialect, op_name = match.group(1), match.group(2)
            if dialect in _SKIP:
                continue
            # Only count operation lines — skip type references (e.g. !ftqc.logical_qubit)
            # by checking the character before the match: must not be '!' or '<'
            start = match.start()
            if start > 0 and mlir_code[start - 1] in '!<':
                continue
            # Find the longest keyword inside the op name.
            # Split op_name on '_' and check each token, plus the full name.
            tokens = op_name.split('_') + [op_name]
            best_kw = None
            for kw in self._GATE_KEYWORDS_ORDERED:
                if kw in tokens or kw == op_name:
                    best_kw = kw
                    break
            if best_kw is None:
                continue
            canonical = self._KEYWORD_TO_GATE[best_kw]
            counts[canonical] = counts.get(canonical, 0) + 1
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

    # Gates to exclude from missing/extra reporting (infrastructure, not unitary)
    _EXCLUDED_GATES = {'measure', 'mz'}

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
            if self.GATE_MAPPINGS.get(g, g.lower()) not in self._EXCLUDED_GATES
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
            if self.GATE_MAPPINGS.get(g, g.lower()) not in self._EXCLUDED_GATES
        }

        extra = []
        for gate in qir_counts:
            if gate in self._EXCLUDED_GATES:
                continue
            if gate not in mlir_normalized and qir_counts[gate] > 0:
                extra.append(gate)

        return extra
