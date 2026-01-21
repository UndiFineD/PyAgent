# Spiking Neural Networks (SNNs)

Standard Artificial Neural Networks (ANNs) are "Second Generation" models. They use continuous values (floating point numbers) to represent neuron activation.
**Spiking Neural Networks (SNNs)** are "Third Generation" models. They mimic the biological brain more closely by using discrete **spikes** (events) over time.

## 1. How it Works

### The Leaky Integrate-and-Fire (LIF) Neuron
Instead of $y = \sigma(Wx + b)$, an SNN neuron has a membrane potential $V(t)$.
1.  **Integrate**: Incoming spikes increase the potential.
2.  **Leak**: The potential decays over time (like a leaky bucket).
3.  **Fire**: If $V(t)$ crosses a threshold $V_{th}$, the neuron emits a spike and resets.

### Information Coding
Information is encoded in the timing of spikes:
- **Rate Coding**: High frequency = high value.
- **Temporal Coding**: The exact timing of the spike carries meaning (e.g., time-to-first-spike).

## 2. Training SNNs

Training is hard because the spiking operation is non-differentiable (a step function).
- **Surrogate Gradients**: During backpropagation, we approximate the derivative of the spike function with a smooth curve (like a sigmoid), allowing us to use standard SGD.
- **STDP (Spike-Timing-Dependent Plasticity)**: A biological learning rule. If neuron A spikes just before neuron B, the connection strengthens (Hebbian learning). If B spikes before A, it weakens.

## 3. Neuromorphic Hardware

SNNs are designed to run on specialized hardware, not GPUs.
- **Event-Driven**: The hardware only consumes power when a spike occurs. If nothing changes, power consumption is near zero.
- **Chips**: Intel Loihi, IBM TrueNorth.

## 4. Pros and Cons

| Feature | ANN | SNN |
| :--- | :--- | :--- |
| **Precision** | High (Float32) | Low (Binary Spikes) |
| **Energy Efficiency** | Low (Always active) | High (Event-driven) |
| **Latency** | Batch-dependent | Ultra-low (Real-time) |
| **Training** | Easy (Backprop) | Hard (Non-differentiable) |

## Summary

SNNs are the future of **Edge AI** and ultra-low-power robotics, offering a path to brain-like efficiency.
