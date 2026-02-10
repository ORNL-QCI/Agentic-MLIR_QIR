// Bell State Circuit - Creates entangled pair |00⟩ + |11⟩
// Catalyst dialect (PennyLane)

func.func @bell_state() {
  %0 = quantum.alloc( 2) : !quantum.reg
  %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
  %out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
  %2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
  %out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
  %3 = quantum.measure %out_qubits_0#0 : !quantum.meas
  %4 = quantum.measure %out_qubits_0#1 : !quantum.meas
  func.return
}
