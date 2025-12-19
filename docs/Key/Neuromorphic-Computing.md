# Neuromorphic Computing

Traditional computers (Von Neumann architecture) separate memory (RAM) and processing (CPU). The brain mixes them (synapses store memory *and* compute). Neuromorphic chips try to mimic the brain.

## 1. Spiking Neural Networks (SNNs)

*   **Standard ANN**: Neurons send continuous values (0.75, -0.2).
*   **SNN**: Neurons send discrete "spikes" (0 or 1) over time.
*   **Efficiency**: If nothing changes, no spikes are sent. Extremely energy efficient (event-driven).
*   **Training**: Hard to train with Backpropagation (spikes are non-differentiable). Requires special algorithms (STDP - Spike-Timing-Dependent Plasticity).

## 2. Hardware

*   **Intel Loihi**: A research chip with 128 cores simulating 130,000 neurons.
*   **IBM TrueNorth**: Early neuromorphic chip inspired by the brain's structure.
*   **Event Cameras (DVS)**: Cameras that don't capture frames (FPS). They capture *changes* in brightness at the pixel level.
    *   Microsecond latency.
    *   High dynamic range.
    *   Perfect for SNNs.

## 3. Use Cases

*   **Ultra-low power robotics**: Drones that navigate like insects.
*   **Prosthetics**: Interfaces that speak the "language" of biological neurons (spikes).
*   **Edge Sensing**: Always-on keyword spotting with microwatt power consumption.
