// GHZ State Circuit - Creates 3-qubit entangled state |000⟩ + |111⟩
// Catalyst dialect (PennyLane)

func.func @ghz_state() {
  %0 = quantum.alloc( 3) : !quantum.reg
  %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
  %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
  %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
  %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
  %3 = quantum.extract %0[ 2] : !quantum.reg -> !quantum.bit
  %out_qubits_1:2 = quantum.custom "CNOT"() %out_qubits_0#0, %3 : !quantum.bit, !quantum.bit
  %4 = quantum.measure %out_qubits_1#0 : !quantum.meas
  %5 = quantum.measure %out_qubits_0#1 : !quantum.meas
  %6 = quantum.measure %out_qubits_1#1 : !quantum.meas
  func.return
}
