# Synapse Models & Plasticity

Standard Deep Learning models rely on **Backpropagation** to update weights (synapses) during training. Once training is done, the weights are frozen. **Synapse Models** explore how to make these connections dynamic, adaptive, and more biologically plausible.

## 1. The Biological Inspiration

In the human brain, synapses are not static scalars. They are complex biological machines that change based on activity.
*   **Hebbian Learning**: "Neurons that fire together, wire together."
*   **Short-Term Plasticity**: Synapses can temporarily strengthen or weaken based on recent activity (milliseconds to seconds).
*   **Long-Term Potentiation (LTP)**: Permanent strengthening of connections (learning).

## 2. Artificial Synapse Models

### A. Fast Weights (Dynamic Evaluation)
Standard RNNs/Transformers have "Slow Weights" (learned over the whole dataset) and "State" (activations that change every step).
**Fast Weights** are a middle ground: a matrix of weights that changes quickly during inference to store temporary memory.
*   Instead of just $y = \sigma(Wx)$, we use $y = \sigma((W + A(t))x)$.
*   $A(t)$ is a fast-weight matrix that updates based on the outer product of recent inputs. This allows the network to "remember" the immediate context better than standard attention.

### B. Hebbian Softmax
Replacing the standard dot-product attention with Hebbian update rules. This allows the model to perform associative recall more efficiently, mimicking how the hippocampus retrieves memories.

### C. Differentiable Plasticity
Meta-learning algorithms where the *learning rule itself* is learned.
*   Instead of hardcoding "update weight by gradient descent," the network learns a local update rule for each synapse.
*   This allows networks to adapt to new tasks at test time without a full training loop (Few-Shot Learning).

## 3. Spiking Neural Networks (SNNs)

SNNs model the temporal aspect of synapses. Neurons don't output a continuous number; they output discrete **spikes** over time.
*   **Energy Efficiency**: SNNs are extremely efficient (neuromorphic hardware) because computation only happens when a spike occurs.
*   **STDP (Spike-Timing-Dependent Plasticity)**: The weight update depends on the precise timing difference between the input spike and the output spike.

## 4. Summary

Synapse models attempt to break the rigid "Train then Freeze" paradigm of current AI. By introducing plasticity, we aim to create **Lifelong Learning** agents that can adapt to a changing world without forgetting what they previously learned (Catastrophic Forgetting).
