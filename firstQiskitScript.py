"""Run a Bell-state circuit on an available IBM Quantum device.

Set ``IBM_QUANTUM_TOKEN`` in the environment before running this example.
The token is passed directly to the service and is never written to source or
saved to the local Qiskit account configuration by this script.
"""

import os
import sys

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2


SHOTS = 1024


def main() -> int:
    token = os.environ.get("IBM_QUANTUM_TOKEN", "").strip()
    if not token:
        print(
            "Missing IBM_QUANTUM_TOKEN. Create an API key in IBM Quantum, "
            "then set it in your shell before running this script.",
            file=sys.stderr,
        )
        return 2

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    print("Bell-state circuit:")
    print(circuit.draw())

    try:
        service_options = {
            "channel": "ibm_quantum_platform",
            "token": token,
        }
        instance = os.environ.get("IBM_QUANTUM_INSTANCE", "").strip()
        if instance:
            service_options["instance"] = instance
        service = QiskitRuntimeService(**service_options)
        backend = service.least_busy(
            min_num_qubits=2,
            operational=True,
            simulator=False,
        )
        print(f"Selected device: {backend.name}")

        pass_manager = generate_preset_pass_manager(
            backend=backend,
            optimization_level=1,
        )
        isa_circuit = pass_manager.run(circuit)

        sampler = SamplerV2(mode=backend)
        job = sampler.run([isa_circuit], shots=SHOTS)
        print(f"Submitted job: {job.job_id()}")
        result = job.result()

    except Exception as error:
        print(f"IBM Quantum job failed: {error}", file=sys.stderr)
        return 1

    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    print("\nMeasurement results:")
    for outcome, count in sorted(counts.items()):
        probability = 100 * count / total_shots
        print(f"{outcome}: {count}/{total_shots} shots ({probability:.2f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
