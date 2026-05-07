from qiskit import QuantumCircuit

# 25-qubit GHZ state
qc_ghz25 = QuantumCircuit(25)
qc_ghz25.h(0)
for i in range(1, 25):
    qc_ghz25.cx(0, i)
qc_ghz25.measure_all()

# print("25-qubit GHZ:")
# qc_ghz25.draw('mpl')

from qiskit_qir import to_qir_module
module, entry_points = to_qir_module(qc_ghz25)
bitcode = module.bitcode
ir = str(module)
print(ir)