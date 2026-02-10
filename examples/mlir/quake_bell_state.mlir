// Bell State Circuit - Quake dialect (CUDA Quantum)

func.func @bell_state() {
  %0 = quake.alloca !quake.veq<2>
  %1 = quake.extract_ref %0[0] : (!quake.veq<2>) -> !quake.ref
  %2 = quake.extract_ref %0[1] : (!quake.veq<2>) -> !quake.ref
  quake.h %1
  quake.cnot %1, %2
  %3 = quake.mz %1 : (!quake.ref) -> !quake.measure
  %4 = quake.mz %2 : (!quake.ref) -> !quake.measure
  return
}
