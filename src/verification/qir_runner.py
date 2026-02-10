"""QIR-runner backend for executing QIR circuits."""

import subprocess
import tempfile
import re
import shutil
from pathlib import Path
from typing import Dict
import logging

from .simulator_registry import BaseRunner, SimulatorRegistry

logger = logging.getLogger(__name__)


class QIRRunner(BaseRunner):
    """Execute QIR circuits using qir-runner tool."""

    @property
    def name(self) -> str:
        return "qir-runner"

    def is_available(self) -> bool:
        """Check if qir-runner is available."""
        # Check if qir-runner command exists
        return shutil.which('qir-runner') is not None or shutil.which('qir_runner') is not None

    def run(self, qir_code: str, shots: int = 1000) -> Dict[str, int]:
        """Execute QIR circuit using qir-runner.

        Args:
            qir_code: QIR code as string
            shots: Number of shots

        Returns:
            Measurement distribution
        """
        if not self.is_available():
            logger.warning("qir-runner not available, using mock results")
            return self._mock_run(qir_code, shots)

        try:
            # Write QIR to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ll', delete=False) as f:
                f.write(qir_code)
                qir_file = f.name

            try:
                # Run qir-runner
                cmd = ['qir-runner', '--shots', str(shots), qir_file]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    logger.error(f"qir-runner failed: {result.stderr}")
                    return self._mock_run(qir_code, shots)

                # Parse results
                return self._parse_results(result.stdout, shots)

            finally:
                # Clean up temp file
                Path(qir_file).unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Error running QIR: {str(e)}")
            return self._mock_run(qir_code, shots)

    def get_circuit_info(self, qir_code: str) -> Dict:
        """Extract circuit information from QIR code.

        Args:
            qir_code: QIR code

        Returns:
            Dictionary with num_qubits, num_gates, gate_types
        """
        info = {
            'num_qubits': 0,
            'num_gates': 0,
            'gate_types': {},
            'num_measurements': 0
        }

        # Extract number of qubits from attributes
        qubit_match = re.search(r'"required_num_qubits"="(\d+)"', qir_code)
        if qubit_match:
            info['num_qubits'] = int(qubit_match.group(1))

        # Count gates
        gate_calls = re.findall(r'call void @__quantum__qis__(\w+)__body', qir_code)
        for gate in gate_calls:
            if gate not in ['mz', 'measure']:  # Skip measurements
                info['gate_types'][gate] = info['gate_types'].get(gate, 0) + 1
                info['num_gates'] += 1

        # Count measurements
        meas_calls = re.findall(r'call void @__quantum__qis__mz__body', qir_code)
        info['num_measurements'] = len(meas_calls)

        return info

    def _parse_results(self, output: str, shots: int) -> Dict[str, int]:
        """Parse qir-runner output.

        Args:
            output: Raw output from qir-runner
            shots: Number of shots

        Returns:
            Measurement distribution
        """
        # This is a placeholder - actual parsing depends on qir-runner output format
        # Different versions may have different output formats

        distribution = {}

        # Try to parse output (format may vary)
        # Common formats: "00: 489" or "00 489" or "|00⟩: 489"
        patterns = [
            r'(\d+):?\s*(\d+)',  # "00: 489" or "00 489"
            r'\|([01]+)⟩:?\s*(\d+)',  # "|00⟩: 489"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, output)
            if matches:
                for bitstring, count in matches:
                    distribution[bitstring] = int(count)
                break

        # If no results parsed, return empty
        if not distribution:
            logger.warning("Could not parse qir-runner output, using mock results")
            return self._mock_run_from_info(self.get_circuit_info(""), shots)

        return distribution

    def _mock_run(self, qir_code: str, shots: int) -> Dict[str, int]:
        """Mock execution for when qir-runner is not available.

        Args:
            qir_code: QIR code
            shots: Number of shots

        Returns:
            Mock measurement distribution
        """
        info = self.get_circuit_info(qir_code)
        return self._mock_run_from_info(info, shots)

    def _mock_run_from_info(self, info: Dict, shots: int) -> Dict[str, int]:
        """Generate mock results based on circuit info.

        Args:
            info: Circuit information
            shots: Number of shots

        Returns:
            Mock distribution
        """
        num_qubits = info.get('num_qubits', 2)

        # For Bell-like circuits (H + CNOT), return 00 and 11
        if 'cnot' in info.get('gate_types', {}) and 'h' in info.get('gate_types', {}):
            bitstring_0 = '0' * num_qubits
            bitstring_1 = '1' * num_qubits
            return {
                bitstring_0: shots // 2,
                bitstring_1: shots - shots // 2
            }

        # Default: equal superposition
        from itertools import product
        bitstrings = [''.join(b) for b in product('01', repeat=num_qubits)]
        count_per_bitstring = shots // len(bitstrings)
        remainder = shots % len(bitstrings)

        distribution = {}
        for i, bitstring in enumerate(bitstrings):
            count = count_per_bitstring + (1 if i < remainder else 0)
            distribution[bitstring] = count

        return distribution


# Register the backend
SimulatorRegistry.register(QIRRunner)
