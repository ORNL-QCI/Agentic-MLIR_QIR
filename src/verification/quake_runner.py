"""QuakeRunner — executes Quake MLIR circuits via CUDA Quantum (cudaq).

Parses the Quake MLIR with QuakeDialect, rebuilds it as a cudaq kernel,
and runs cudaq.sample() to obtain a bitstring probability distribution.

cudaq and qirrunner share LLVM symbols and segfault when loaded together.
The real execution is therefore delegated to an isolated subprocess
(_quake_subprocess_runner.py) that imports only cudaq.

Self-registers into SimulatorRegistry on import.
"""

import json
import sys
from pathlib import Path
from .simulator_registry import BaseRunner, SimulatorRegistry

_SUBPROCESS_SCRIPT = Path(__file__).with_name("_quake_subprocess_runner.py")


class QuakeRunner(BaseRunner):
    """Execute Quake MLIR circuits using cudaq.sample() in a subprocess."""

    def __init__(self):
        self._last_run_was_mock = True

    @property
    def name(self) -> str:
        return "quake"

    # ── availability ──────────────────────────────────────────────────────────

    def is_available(self) -> bool:
        """Check if cudaq is installed WITHOUT importing it into this process.

        Importing cudaq in the same process as qirrunner causes a segfault
        due to conflicting LLVM shared libraries.  We check availability using
        importlib.util.find_spec, which locates the package without loading it.
        """
        import importlib.util
        return importlib.util.find_spec("cudaq") is not None

    def get_circuit_info(self, code: str) -> dict:
        import re
        m = re.search(r"quake\.alloca\s+!quake\.veq<(\d+)>", code)
        num_q = int(m.group(1)) if m else 0
        gates = re.findall(r"quake\.(h|x|y|z|s|t|rx|ry|rz|swap|cz)\b", code)
        return {"num_qubits": num_q, "gates": gates, "depth": len(gates)}

    # ── public run ────────────────────────────────────────────────────────────

    def run(self, quake_mlir_code: str, shots: int = 1000) -> dict:
        if not self.is_available():
            self._last_run_was_mock = True
            return self._mock_run(quake_mlir_code, shots)
        try:
            result = self._real_run(quake_mlir_code, shots)
            self._last_run_was_mock = False
            return result
        except Exception:
            self._last_run_was_mock = True
            return self._mock_run(quake_mlir_code, shots)

    # ── real execution (subprocess-isolated to avoid cudaq/qirrunner conflict) ─

    def _real_run(self, quake_mlir_code: str, shots: int) -> dict:
        """Run cudaq in a separate process to avoid shared-LLVM conflicts."""
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(_SUBPROCESS_SCRIPT), str(shots)],
            input=quake_mlir_code,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"QuakeRunner subprocess failed (exit {proc.returncode}):\n{proc.stderr}"
            )
        return json.loads(proc.stdout.strip())

    # ── mock fallback (uniform distribution) ─────────────────────────────────

    def _mock_run(self, quake_mlir_code: str, shots: int) -> dict:
        import re
        m = re.search(r"quake\.alloca\s+!quake\.veq<(\d+)>", quake_mlir_code)
        num_q = int(m.group(1)) if m else 2
        n_outcomes = 2 ** num_q
        per_outcome = shots // n_outcomes
        return {format(k, f"0{num_q}b"): per_outcome for k in range(n_outcomes)}


SimulatorRegistry.register(QuakeRunner)
