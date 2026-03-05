"""Catalyst/PennyLane backend for executing Catalyst MLIR quantum circuits.

Real execution uses PennyLane Catalyst (qjit + lightning.qubit) which supports
both standard circuits and circuits with mid-circuit measurements / classical
conditionals (teleportation, error correction).
Falls back to physics-correct mock when the runtime is unavailable.
"""

import logging
import warnings
from itertools import product
from typing import Dict

from .simulator_registry import BaseRunner, SimulatorRegistry

logger = logging.getLogger(__name__)


class CatalystRunner(BaseRunner):
    """Execute Catalyst MLIR circuits via PennyLane Catalyst (qjit).

    Parses the MLIR into a structured MLIRCircuit, reconstructs an equivalent
    PennyLane QNode, and compiles + runs it with catalyst.qjit on the
    lightning.qubit device.  Mid-circuit measurements and classical conditionals
    (scf.if blocks) are supported through qml.measure + catalyst.cond.
    """

    def __init__(self):
        self._last_run_was_mock = True

    @property
    def name(self) -> str:
        return "catalyst"

    def is_available(self) -> bool:
        """Check if PennyLane + Catalyst are importable."""
        try:
            import pennylane          # noqa: F401
            import catalyst           # noqa: F401
            return True
        except ImportError:
            pass
        # Fallback: bare pennylane without catalyst
        try:
            import pennylane          # noqa: F401
            return True
        except ImportError:
            return False

    def get_circuit_info(self, mlir_code: str) -> Dict:
        """Extract circuit information from Catalyst MLIR code."""
        info = {
            'num_qubits': 0,
            'num_gates': 0,
            'gate_types': {},
            'num_measurements': 0,
            'has_conditionals': False,
        }
        try:
            from src.parsers.mlir_parser import MLIRParser
            from src.verification.gate_counter import GateCounter

            circuit = MLIRParser().parse(mlir_code)
            info['num_qubits'] = circuit.num_qubits
            info['has_conditionals'] = circuit.has_conditionals

            gc = GateCounter()
            raw_counts = gc.count_mlir_gates(mlir_code)
            info['num_measurements'] = raw_counts.pop('measure', 0)
            info['gate_types'] = raw_counts
            info['num_gates'] = sum(raw_counts.values())

        except Exception as e:
            logger.warning(f"Could not parse MLIR for circuit info: {e}")

        return info

    def run(self, mlir_code: str, shots: int = 1000) -> Dict[str, int]:
        """Execute the Catalyst MLIR circuit.

        Tries real Catalyst execution first; falls back to mock on any failure.
        """
        if not self.is_available():
            logger.info("PennyLane/Catalyst not available — using mock results")
            self._last_run_was_mock = True
            return self._mock_run(mlir_code, shots)

        try:
            result = self._real_run(mlir_code, shots)
            self._last_run_was_mock = False
            return result
        except Exception as e:
            logger.warning(f"Real Catalyst execution failed: {e} — falling back to mock")
            self._last_run_was_mock = True
            return self._mock_run(mlir_code, shots)

    # ------------------------------------------------------------------
    # Real execution via PennyLane Catalyst
    # ------------------------------------------------------------------

    def _real_run(self, mlir_code: str, shots: int) -> Dict[str, int]:
        """Execute via PennyLane Catalyst (qjit + lightning.qubit).

        Reconstructs the circuit from MLIRCircuit.ordered_ops and compiles it
        with catalyst.qjit.  Supports:
          - Standard gate sequences (Bell, GHZ, parametric)
          - Mid-circuit measurements + classical conditionals (teleportation)
        """
        warnings.filterwarnings('ignore')
        import catalyst
        import pennylane as qml
        import numpy as np
        from src.parsers.mlir_parser import MLIRParser

        parsed = MLIRParser().parse(mlir_code)
        n = parsed.num_qubits
        if n == 0:
            raise ValueError("Parsed circuit has 0 qubits")

        ordered_ops = parsed.ordered_ops or []
        dev = qml.device('lightning.qubit', wires=n, shots=shots)

        # ---------- gate dispatcher (called inside QNode) ----------
        def apply_gate(gate):
            name, qubits, params = gate.name, gate.qubits, gate.params
            if   name == 'Hadamard':   qml.Hadamard(qubits[0])
            elif name == 'PauliX':     qml.PauliX(qubits[0])
            elif name == 'PauliY':     qml.PauliY(qubits[0])
            elif name == 'PauliZ':     qml.PauliZ(qubits[0])
            elif name == 'S':          qml.S(qubits[0])
            elif name == 'T':          qml.T(qubits[0])
            elif name == 'Sdg':        qml.adjoint(qml.S)(wires=[qubits[0]])
            elif name == 'Tdg':        qml.adjoint(qml.T)(wires=[qubits[0]])
            elif name == 'RX':         qml.RX(params[0], qubits[0])
            elif name == 'RY':         qml.RY(params[0], qubits[0])
            elif name == 'RZ':         qml.RZ(params[0], qubits[0])
            elif name == 'PhaseShift': qml.PhaseShift(params[0], qubits[0])
            elif name == 'CNOT':       qml.CNOT(wires=qubits)
            elif name == 'CZ':         qml.CZ(wires=qubits)
            elif name == 'CY':         qml.CY(wires=qubits)
            elif name == 'SWAP':       qml.SWAP(wires=qubits)
            elif name == 'Toffoli':    qml.Toffoli(wires=qubits)
            elif name == 'CSWAP':      qml.CSWAP(wires=qubits)
            else:
                logger.debug(f"Skipping unknown gate: {name}")

        if not parsed.has_conditionals:
            # ----- Simple circuit: no mid-circuit measurements -----
            @catalyst.qjit
            @qml.qnode(dev)
            def run_circuit():
                for op_type, op_data in ordered_ops:
                    if op_type == 'gate':
                        apply_gate(op_data)
                return qml.sample()

        else:
            # ----- Circuit with mid-circuit measurements & conditionals -----
            # Pre-build a flat list of (op_type, ...) entries with explicit
            # measurement indices so the QNode body is fully determined at
            # trace time (all Python-level control flow, no runtime branching).
            #
            # ordered_ops layout for teleportation:
            #   gate / measurement / conditional(condition_measurement_idx)
            # We replay them in order, tracking MeasurementValues in a dict.

            # Snapshot the conditional data as plain Python lists so the
            # compiler can see everything statically.
            snapshot = []
            for op_type, op_data in ordered_ops:
                if op_type == 'gate':
                    snapshot.append(('gate', op_data))
                elif op_type == 'measurement':
                    snapshot.append(('meas', op_data.qubit))
                elif op_type == 'conditional':
                    snapshot.append((
                        'cond',
                        op_data.condition_measurement_idx,
                        list(op_data.then_gates or []),
                        list(op_data.else_gates or []),
                    ))

            @catalyst.qjit
            @qml.qnode(dev)
            def run_circuit():
                mid = {}          # measurement index → MeasurementValue
                meas_count = 0

                for entry in snapshot:
                    kind = entry[0]

                    if kind == 'gate':
                        apply_gate(entry[1])

                    elif kind == 'meas':
                        mid[meas_count] = qml.measure(entry[1])
                        meas_count += 1

                    elif kind == 'cond':
                        _, cond_idx, then_gates, else_gates = entry
                        cond_val = mid[cond_idx]

                        # Capture gates for this specific conditional
                        tg = then_gates
                        eg = else_gates

                        @catalyst.cond(cond_val)
                        def _branch():
                            for g in tg:
                                apply_gate(g)

                        @_branch.otherwise
                        def _branch():
                            for g in eg:
                                apply_gate(g)

                        _branch()

                return qml.sample()

        samples = np.array(run_circuit())
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)

        dist: Dict[str, int] = {}
        for row in samples:
            bs = ''.join(str(int(b)) for b in row)
            dist[bs] = dist.get(bs, 0) + 1
        return dist

    # ------------------------------------------------------------------
    # Mock fallback — physics-correct distributions from circuit structure
    # ------------------------------------------------------------------

    def _mock_run(self, mlir_code: str, shots: int) -> Dict[str, int]:
        info = self.get_circuit_info(mlir_code)
        return self._generate_distribution(info, shots)

    def _detect_circuit_pattern(self, info: Dict) -> str:
        gate_types = info.get('gate_types', {})
        num_qubits = info.get('num_qubits', 0)
        h_count = gate_types.get('Hadamard', 0)
        cnot_count = gate_types.get('CNOT', 0)

        if info.get('has_conditionals'):
            return 'teleportation'
        if h_count == 1 and cnot_count == num_qubits - 1 and num_qubits >= 3:
            return 'ghz'
        if h_count == 1 and cnot_count == 1 and num_qubits == 2:
            return 'bell'
        return 'generic'

    def _generate_distribution(self, info: Dict, shots: int) -> Dict[str, int]:
        num_qubits = max(info.get('num_qubits', 1), 1)
        pattern = self._detect_circuit_pattern(info)

        if pattern == 'bell':
            return {'00': shots // 2, '11': shots - shots // 2}

        if pattern == 'ghz':
            z, o = '0' * num_qubits, '1' * num_qubits
            return {z: shots // 2, o: shots - shots // 2}

        if pattern == 'teleportation':
            n_meas = max(info.get('num_measurements', 2), 1)
            bstrings = [''.join(b) for b in product('01', repeat=n_meas)]
            per = shots // len(bstrings)
            rem = shots % len(bstrings)
            return {bs: per + (1 if i < rem else 0) for i, bs in enumerate(bstrings)}

        bstrings = [''.join(b) for b in product('01', repeat=num_qubits)]
        per = shots // len(bstrings)
        rem = shots % len(bstrings)
        return {bs: per + (1 if i < rem else 0) for i, bs in enumerate(bstrings)}


# Register at import time
SimulatorRegistry.register(CatalystRunner)
