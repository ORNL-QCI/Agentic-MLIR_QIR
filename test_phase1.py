#!/usr/bin/env python3
"""Test Phase 1: Core infrastructure with Bell state example."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.parsers.mlir_parser import MLIRParser
from src.generators.qir_generator import QIRGenerator


def test_bell_state():
    """Test parsing and QIR generation for Bell state circuit."""
    print("=" * 60)
    print("Phase 1 Test: Bell State MLIR to QIR Translation")
    print("=" * 60)

    # Load Bell state MLIR
    mlir_file = Path("examples/mlir/bell_state.mlir")
    if not mlir_file.exists():
        print(f"ERROR: {mlir_file} not found!")
        return False

    with open(mlir_file, 'r') as f:
        mlir_code = f.read()

    print(f"\n✓ Loaded MLIR code ({len(mlir_code)} characters)")

    # Parse MLIR
    try:
        parser = MLIRParser()
        print("\n[1/4] Detecting dialect...")
        dialect_name = parser.get_detected_dialect(mlir_code)
        print(f"✓ Detected dialect: {dialect_name}")

        print("\n[2/4] Parsing MLIR circuit...")
        circuit = parser.parse(mlir_code)
        print(f"✓ Parsed circuit successfully!")
        print(f"  - Dialect: {circuit.dialect_name}")
        print(f"  - Qubits: {circuit.num_qubits}")
        print(f"  - Gates: {len(circuit.gates)}")
        print(f"  - Measurements: {len(circuit.measurements)}")

        # Print gate details
        print("\n  Gate sequence:")
        for i, gate in enumerate(circuit.gates):
            print(f"    {i+1}. {gate.name} on qubits {gate.qubits}")

    except Exception as e:
        print(f"✗ Parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Generate QIR
    try:
        generator = QIRGenerator()
        print("\n[3/4] Generating QIR code...")
        qir_code = generator.generate(circuit, module_id="bell-state")
        print(f"✓ Generated QIR code ({len(qir_code)} characters)")

    except Exception as e:
        print(f"✗ QIR generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Save QIR output
    try:
        print("\n[4/4] Saving QIR output...")
        output_file = Path("examples/qir/bell_state_generated.ll")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(qir_code)
        print(f"✓ Saved to {output_file}")

    except Exception as e:
        print(f"✗ Failed to save QIR: {e}")
        return False

    # Display generated QIR
    print("\n" + "=" * 60)
    print("Generated QIR Code:")
    print("=" * 60)
    print(qir_code)

    # Verification
    print("\n" + "=" * 60)
    print("Verification:")
    print("=" * 60)
    print(f"✓ Circuit has {circuit.num_qubits} qubits (expected: 2)")
    print(f"✓ Circuit has {len(circuit.gates)} gates (expected: 2 - H + CNOT)")
    print(f"✓ Circuit has {len(circuit.measurements)} measurements (expected: 2)")

    # Check for expected QIR functions
    expected_functions = [
        "__quantum__qis__h__body",  # Hadamard
        "__quantum__qis__cnot__body",  # CNOT
        "__quantum__qis__mz__body",  # Measurements
    ]

    print("\nExpected QIR functions:")
    for func in expected_functions:
        if func in qir_code:
            print(f"  ✓ {func}")
        else:
            print(f"  ✗ {func} NOT FOUND!")
            return False

    print("\n" + "=" * 60)
    print("✓ Phase 1 Test PASSED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_bell_state()
    sys.exit(0 if success else 1)
