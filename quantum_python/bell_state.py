# The below is from here: https://www.freecodecamp.org/news/how-to-write-your-first-quantum-circuit-in-python-a-beginner-s-step-by-step-guide/
import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

print(qiskit.__version__)

# Create a Quantum Circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

qc.h(0)

qc.cx(0, 1)

qc.measure([0, 1], [0, 1])

print(qc)

simulator = AerSimulator()

result = simulator.run(
    qc,
    shots=1024
).result()

counts = result.get_counts()

print(counts)
plot_histogram(counts) 
plt.show()
