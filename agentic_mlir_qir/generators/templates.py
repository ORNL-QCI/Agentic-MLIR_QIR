"""QIR code templates for generation."""

from typing import List


class QIRTemplates:
    """Templates for generating QIR code components."""

    # Module header with type definitions
    HEADER = '''; ModuleID = '{module_id}'
source_filename = "{source_filename}"

%Qubit = type opaque
%Result = type opaque
'''

    # Entry point function template
    ENTRY_FUNCTION = '''define void @{function_name}() #0 {{
entry:
  call void @__quantum__rt__initialize(i8* null)
{gate_operations}
{measurements}
{output_recording}
  ret void
}}
'''

    # Gate operation template (single qubit)
    SINGLE_QUBIT_GATE = '  call void @{function_name}(%Qubit* {qubit_ptr})'

    # Gate operation template (two qubits)
    TWO_QUBIT_GATE = '  call void @{function_name}(%Qubit* {control_ptr}, %Qubit* {target_ptr})'

    # Parameterized gate template
    PARAM_GATE = '  call void @{function_name}(double {param}, %Qubit* {qubit_ptr})'

    # Measurement operation
    MEASUREMENT = '  call void @__quantum__qis__mz__body(%Qubit* {qubit_ptr}, %Result* {result_ptr})'

    # Measurement with result read (for conditionals)
    MEASUREMENT_WITH_READ = '''  call void @__quantum__qis__mz__body(%Qubit* {qubit_ptr}, %Result* {result_ptr})
  %{result_var} = call i1 @__quantum__qis__read_result__body(%Result* {result_ptr})'''

    # Conditional branch template
    CONDITIONAL = '''  br i1 %{condition}, label %then{label_id}, label %else{label_id}

then{label_id}:
{then_ops}
  br label %continue{label_id}

else{label_id}:
{else_ops}
  br label %continue{label_id}

continue{label_id}:'''

    # Output recording template
    OUTPUT_RECORDING = '''  call void @__quantum__rt__array_record_output(i64 {num_results}, i8* null)
{result_outputs}'''

    # Single result output
    RESULT_OUTPUT = '  call void @__quantum__rt__result_record_output(%Result* {result_ptr}, i8* null)'

    # Function declarations
    DECLARATIONS = '''
declare void @__quantum__rt__initialize(i8*)

{gate_declarations}

declare void @__quantum__qis__mz__body(%Qubit*, %Result* writeonly) #1

{conditional_declarations}

declare void @__quantum__rt__array_record_output(i64, i8*)

declare void @__quantum__rt__result_record_output(%Result*, i8*)
'''

    # Individual gate declaration
    GATE_DECLARATION = 'declare void @{function_name}({params})'

    # Conditional-specific declarations
    CONDITIONAL_DECLARATIONS = '''declare i1 @__quantum__qis__read_result__body(%Result*)'''

    # Attributes section
    ATTRIBUTES = '''
attributes #0 = {{ "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="{num_qubits}" "required_num_results"="{num_results}" }}
attributes #1 = {{ "irreversible" }}
'''

    # Metadata section
    METADATA = '''
!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
'''

    @staticmethod
    def get_qubit_pointer(index: int) -> str:
        """Generate qubit pointer for given index.

        Args:
            index: Qubit index (0-based)

        Returns:
            QIR pointer string
        """
        if index == 0:
            return "null"
        return f"inttoptr (i64 {index} to %Qubit*)"

    @staticmethod
    def get_result_pointer(index: int) -> str:
        """Generate result pointer for given index.

        Args:
            index: Result index (0-based)

        Returns:
            QIR pointer string
        """
        if index == 0:
            return "null"
        return f"inttoptr (i64 {index} to %Result*)"

    @staticmethod
    def get_gate_param_signature(gate_name: str, num_qubits: int, has_param: bool = False) -> str:
        """Get parameter signature for gate declaration.

        Args:
            gate_name: QIR gate function name
            num_qubits: Number of qubits gate operates on
            has_param: Whether gate has a parameter (like RX, RY, RZ)

        Returns:
            Parameter signature string
        """
        params = []

        # Add parameter first if present
        if has_param:
            params.append("double")

        # Add qubits
        params.extend(["%Qubit*"] * num_qubits)

        return ", ".join(params)
