// Parametric Rotation Circuit - Single qubit with RX, RY, RZ gates
// Catalyst dialect (PennyLane)

func.func @parametric_rotation(%theta: f64) {
  %0 = quantum.alloc( 1) : !quantum.reg
  %1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
  %pi_4 = arith.constant 0.785398163397448 : f64  // π/4
  %out_qubits = quantum.custom "RX"(%pi_4) %1 : !quantum.bit
  %pi_2 = arith.constant 1.57079632679490 : f64  // π/2
  %out_qubits_0 = quantum.custom "RY"(%pi_2) %out_qubits : !quantum.bit
  %out_qubits_1 = quantum.custom "RZ"(%theta) %out_qubits_0 : !quantum.bit
  %2 = quantum.measure %out_qubits_1 : !quantum.meas
  func.return
}
