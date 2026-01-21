# Quantum Machine Learning (QML)

Using Quantum Computers to accelerate or improve Machine Learning algorithms.

## 1. The Promise

*   **Superposition**: A Qubit can be 0 and 1 at the same time.
*   **Entanglement**: Qubits can be linked; changing one instantly affects the other.
*   **Hilbert Space**: Quantum states exist in a massive vector space ($2^N$ dimensions for $N$ qubits). This is naturally similar to the high-dimensional vector spaces used in ML.

## 2. Algorithms

*   **VQC (Variational Quantum Circuits)**: The quantum equivalent of a Neural Network.
    *   Parameters are rotation angles of quantum gates.
    *   Optimized using classical gradient descent (Hybrid Classical-Quantum).
*   **QSVM (Quantum SVM)**: Using a quantum computer to calculate the "Kernel" (similarity) between data points in a space that is too complex for classical computers.
*   **QGAN**: Quantum Generative Adversarial Networks.

## 3. Current State (NISQ Era)

We are in the **Noisy Intermediate-Scale Quantum** era.
*   Real quantum computers are noisy and error-prone.
*   QML is currently mostly theoretical or proof-of-concept.
*   **Quantum Advantage**: We have not yet proven that QML is strictly better than Classical ML for practical problems, but research is exploding.

## 4. Libraries

*   **PennyLane**: Python library for differentiable quantum programming (integrates with PyTorch/TensorFlow).
*   **Qiskit (IBM)**: The standard SDK for working with IBM's quantum processors.
*   **TensorFlow Quantum**: Google's library for hybrid quantum-classical ML.
