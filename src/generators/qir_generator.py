"""QIR code generation from parsed MLIR circuits."""

from typing import List, Set, Dict
from ..dialects.base_dialect import MLIRCircuit, GateOperation
from .templates import QIRTemplates


class QIRGenerator:
    """Generate QIR code from parsed MLIR circuits."""

    def __init__(self):
        self.templates = QIRTemplates()
        self.conditional_counter = 0  # For generating unique labels

    def generate(self, circuit: MLIRCircuit, module_id: str = "circuit",
                 function_name: str = "main") -> str:
        """Generate complete QIR code from MLIR circuit.

        Args:
            circuit: Parsed MLIRCircuit object
            module_id: Module identifier
            function_name: Entry function name

        Returns:
            Complete QIR code as string
        """
        # Generate each section
        header = self._generate_header(module_id)
        entry_function = self._generate_entry_function(circuit, function_name)
        declarations = self._generate_declarations(circuit)
        attributes = self._generate_attributes(circuit)
        metadata = self.templates.METADATA

        # Combine all sections
        qir_code = f"{header}\n{entry_function}\n{declarations}\n{attributes}\n{metadata}"

        return qir_code

    def _generate_header(self, module_id: str) -> str:
        """Generate QIR module header."""
        return self.templates.HEADER.format(
            module_id=module_id,
            source_filename=module_id
        )

    def _generate_entry_function(self, circuit: MLIRCircuit, function_name: str) -> str:
        """Generate entry point function with all operations."""
        # Generate gate operations
        gate_ops = []
        for gate in circuit.gates:
            gate_code = self._generate_gate_call(gate, circuit)
            gate_ops.append(gate_code)

        gate_operations = "\n".join(gate_ops)

        # Generate measurements
        meas_ops = []
        for i, meas in enumerate(circuit.measurements):
            meas_code = self._generate_measurement(meas.qubit, i)
            meas_ops.append(meas_code)

        measurements = "\n".join(meas_ops)

        # Generate output recording
        output_recording = self._generate_output_recording(len(circuit.measurements))

        return self.templates.ENTRY_FUNCTION.format(
            function_name=function_name,
            gate_operations=gate_operations,
            measurements=measurements,
            output_recording=output_recording
        )

    def _generate_gate_call(self, gate: GateOperation, circuit: MLIRCircuit) -> str:
        """Generate QIR code for a single gate operation."""
        # Get QIR function name from dialect
        # For now, we'll use a simple mapping
        qir_function = self._get_qir_function_name(gate.name)

        if len(gate.qubits) == 1:
            # Single-qubit gate
            qubit_ptr = self.templates.get_qubit_pointer(gate.qubits[0])

            if gate.params:
                # Parameterized gate (RX, RY, RZ)
                return self.templates.PARAM_GATE.format(
                    function_name=qir_function,
                    param=gate.params[0],
                    qubit_ptr=qubit_ptr
                )
            else:
                # Non-parameterized gate
                return self.templates.SINGLE_QUBIT_GATE.format(
                    function_name=qir_function,
                    qubit_ptr=qubit_ptr
                )

        elif len(gate.qubits) == 2:
            # Two-qubit gate
            control_ptr = self.templates.get_qubit_pointer(gate.qubits[0])
            target_ptr = self.templates.get_qubit_pointer(gate.qubits[1])

            return self.templates.TWO_QUBIT_GATE.format(
                function_name=qir_function,
                control_ptr=control_ptr,
                target_ptr=target_ptr
            )

        else:
            # Multi-qubit gates (not yet supported)
            raise NotImplementedError(f"Gates with {len(gate.qubits)} qubits not yet supported")

    def _generate_measurement(self, qubit_index: int, result_index: int) -> str:
        """Generate measurement operation."""
        qubit_ptr = self.templates.get_qubit_pointer(qubit_index)
        result_ptr = self.templates.get_result_pointer(result_index)

        return self.templates.MEASUREMENT.format(
            qubit_ptr=qubit_ptr,
            result_ptr=result_ptr
        )

    def _generate_output_recording(self, num_results: int) -> str:
        """Generate output recording section."""
        if num_results == 0:
            return ""

        # Generate result outputs
        result_outputs = []
        for i in range(num_results):
            result_ptr = self.templates.get_result_pointer(i)
            result_outputs.append(
                self.templates.RESULT_OUTPUT.format(result_ptr=result_ptr)
            )

        return self.templates.OUTPUT_RECORDING.format(
            num_results=num_results,
            result_outputs="\n".join(result_outputs)
        )

    def _generate_declarations(self, circuit: MLIRCircuit) -> str:
        """Generate function declarations section."""
        # Collect unique gates used
        gate_functions = self._collect_gate_functions(circuit)

        # Generate declarations for each gate
        gate_decls = []
        for func_name, (num_qubits, has_param) in gate_functions.items():
            param_sig = self.templates.get_gate_param_signature(
                func_name, num_qubits, has_param
            )
            gate_decls.append(
                self.templates.GATE_DECLARATION.format(
                    function_name=func_name,
                    params=param_sig
                )
            )

        gate_declarations = "\n".join(gate_decls)

        # Add conditional declarations if needed
        conditional_declarations = ""
        if circuit.has_conditionals:
            conditional_declarations = self.templates.CONDITIONAL_DECLARATIONS

        return self.templates.DECLARATIONS.format(
            gate_declarations=gate_declarations,
            conditional_declarations=conditional_declarations
        )

    def _generate_attributes(self, circuit: MLIRCircuit) -> str:
        """Generate attributes section."""
        return self.templates.ATTRIBUTES.format(
            num_qubits=circuit.num_qubits,
            num_results=len(circuit.measurements)
        )

    def _collect_gate_functions(self, circuit: MLIRCircuit) -> Dict[str, tuple]:
        """Collect unique gate functions used in circuit.

        Returns:
            Dict mapping function_name -> (num_qubits, has_param)
        """
        gate_functions = {}

        for gate in circuit.gates:
            func_name = self._get_qir_function_name(gate.name)
            num_qubits = len(gate.qubits)
            has_param = len(gate.params) > 0

            gate_functions[func_name] = (num_qubits, has_param)

        return gate_functions

    def _get_qir_function_name(self, gate_name: str) -> str:
        """Map gate name to QIR function name.

        This uses standard mappings. In a full implementation,
        this would query the dialect's gate mapping.
        """
        # Standard mappings
        mappings = {
            "Hadamard": "__quantum__qis__h__body",
            "CNOT": "__quantum__qis__cnot__body",
            "PauliX": "__quantum__qis__x__body",
            "PauliY": "__quantum__qis__y__body",
            "PauliZ": "__quantum__qis__z__body",
            "S": "__quantum__qis__s__body",
            "T": "__quantum__qis__t__body",
            "RX": "__quantum__qis__rx__body",
            "RY": "__quantum__qis__ry__body",
            "RZ": "__quantum__qis__rz__body",
            "CZ": "__quantum__qis__cz__body",
            "SWAP": "__quantum__qis__swap__body",
        }

        return mappings.get(gate_name, f"__quantum__qis__{gate_name.lower()}__body")
