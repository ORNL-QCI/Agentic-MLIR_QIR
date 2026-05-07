"""QIR code generation from parsed MLIR circuits."""

from typing import List, Dict
from ..dialects.base_dialect import MLIRCircuit, GateOperation, ConditionalBlock
from .templates import QIRTemplates


class QIRGenerator:
    """Generate QIR code from parsed MLIR circuits."""

    def __init__(self):
        self.templates = QIRTemplates()
        self.conditional_counter = 0

    def generate(self, circuit: MLIRCircuit, module_id: str = "circuit",
                 function_name: str = "main") -> str:
        header = self._generate_header(module_id)
        entry_function = self._generate_entry_function(circuit, function_name)
        declarations = self._generate_declarations(circuit)
        attributes = self._generate_attributes(circuit)
        metadata = self.templates.METADATA

        return f"{header}\n{entry_function}\n{declarations}\n{attributes}\n{metadata}"

    def _generate_header(self, module_id: str) -> str:
        return self.templates.HEADER.format(
            module_id=module_id,
            source_filename=module_id
        )

    def _generate_entry_function(self, circuit: MLIRCircuit, function_name: str) -> str:
        """Generate entry point function with operations in correct order."""
        self.conditional_counter = 0
        body_lines = []
        body_lines.append("  call void @__quantum__rt__initialize(i8* null)")

        if circuit.ordered_ops:
            # Use ordered operations (SSA-aware parse)
            meas_idx = 0
            for op_type, op_data in circuit.ordered_ops:
                if op_type == "gate":
                    body_lines.append(self._generate_gate_call(op_data))
                elif op_type == "measurement":
                    body_lines.append(self._generate_measurement(op_data.qubit, meas_idx))
                    meas_idx += 1
                elif op_type == "conditional":
                    cond_lines = self._generate_conditional(op_data)
                    body_lines.extend(cond_lines)
        else:
            # Fallback: gates then measurements (old behavior)
            for gate in circuit.gates:
                body_lines.append(self._generate_gate_call(gate))
            for i, meas in enumerate(circuit.measurements):
                body_lines.append(self._generate_measurement(meas.qubit, i))

        # Output recording
        num_results = len(circuit.measurements)
        if num_results > 0:
            body_lines.append(f"  call void @__quantum__rt__array_record_output(i64 {num_results}, i8* null)")
            for i in range(num_results):
                result_ptr = self.templates.get_result_pointer(i)
                body_lines.append(f"  call void @__quantum__rt__result_record_output(%Result* {result_ptr}, i8* null)")

        body = "\n".join(body_lines)
        return f"define void @{function_name}() #0 {{\nentry:\n{body}\n  ret void\n}}\n"

    def _generate_gate_call(self, gate: GateOperation) -> str:
        qir_function = self._get_qir_function_name(gate.name)

        if len(gate.qubits) == 1:
            qubit_ptr = self.templates.get_qubit_pointer(gate.qubits[0])
            if gate.params:
                return self.templates.PARAM_GATE.format(
                    function_name=qir_function,
                    param=f"{gate.params[0]:.6e}",
                    qubit_ptr=qubit_ptr
                )
            else:
                return self.templates.SINGLE_QUBIT_GATE.format(
                    function_name=qir_function,
                    qubit_ptr=qubit_ptr
                )
        elif len(gate.qubits) == 2:
            control_ptr = self.templates.get_qubit_pointer(gate.qubits[0])
            target_ptr = self.templates.get_qubit_pointer(gate.qubits[1])
            return self.templates.TWO_QUBIT_GATE.format(
                function_name=qir_function,
                control_ptr=control_ptr,
                target_ptr=target_ptr
            )
        else:
            raise NotImplementedError(f"Gates with {len(gate.qubits)} qubits not yet supported")

    def _generate_measurement(self, qubit_index: int, result_index: int) -> str:
        qubit_ptr = self.templates.get_qubit_pointer(qubit_index)
        result_ptr = self.templates.get_result_pointer(result_index)
        return self.templates.MEASUREMENT.format(
            qubit_ptr=qubit_ptr,
            result_ptr=result_ptr
        )

    def _generate_conditional(self, cond: ConditionalBlock) -> List[str]:
        """Generate QIR conditional branch from a ConditionalBlock."""
        lines = []
        label_id = self.conditional_counter
        self.conditional_counter += 1

        result_ptr = self.templates.get_result_pointer(cond.condition_measurement_idx)
        result_var = f"%cond{label_id}"

        # Read the measurement result
        lines.append(f"  {result_var} = call i1 @__quantum__qis__read_result__body(%Result* {result_ptr})")
        # Branch
        suffix = "" if label_id == 0 else str(label_id)
        then_label = f"then{suffix}"
        else_label = f"else{suffix}"
        cont_label = f"continue{suffix}"

        lines.append(f"  br i1 {result_var}, label %{then_label}, label %{else_label}")
        lines.append("")

        # Then block
        lines.append(f"{then_label}:")
        for g in cond.then_gates:
            lines.append(self._generate_gate_call(g))
        lines.append(f"  br label %{cont_label}")
        lines.append("")

        # Else block
        lines.append(f"{else_label}:")
        for g in cond.else_gates:
            lines.append(self._generate_gate_call(g))
        lines.append(f"  br label %{cont_label}")
        lines.append("")

        # Continue block
        lines.append(f"{cont_label}:")

        return lines

    def _generate_declarations(self, circuit: MLIRCircuit) -> str:
        gate_functions = self._collect_gate_functions(circuit)

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

        conditional_declarations = ""
        if circuit.has_conditionals:
            conditional_declarations = self.templates.CONDITIONAL_DECLARATIONS

        return self.templates.DECLARATIONS.format(
            gate_declarations=gate_declarations,
            conditional_declarations=conditional_declarations
        )

    def _generate_attributes(self, circuit: MLIRCircuit) -> str:
        return self.templates.ATTRIBUTES.format(
            num_qubits=circuit.num_qubits,
            num_results=len(circuit.measurements)
        )

    def _collect_gate_functions(self, circuit: MLIRCircuit) -> Dict[str, tuple]:
        gate_functions = {}

        # Gates from main circuit
        for gate in circuit.gates:
            func_name = self._get_qir_function_name(gate.name)
            num_qubits = len(gate.qubits)
            has_param = len(gate.params) > 0
            gate_functions[func_name] = (num_qubits, has_param)

        # Gates from conditional blocks
        for cond in circuit.conditionals:
            for gate in cond.then_gates + cond.else_gates:
                func_name = self._get_qir_function_name(gate.name)
                num_qubits = len(gate.qubits)
                has_param = len(gate.params) > 0
                gate_functions[func_name] = (num_qubits, has_param)

        return gate_functions

    def _get_qir_function_name(self, gate_name: str) -> str:
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
