# Neuron-Level Models & Mechanistic Interpretability

**Mechanistic Interpretability** is the field of AI research dedicated to reverse-engineering neural networks. Instead of treating the model as a "Black Box," researchers attempt to understand the algorithms implemented by the weights and neurons.

## 1. The Neuron as the Atomic Unit

In a standard Transformer, the Multi-Layer Perceptron (MLP) layers consist of thousands of individual neurons.
*   **Hypothesis**: Each neuron detects a specific feature.
*   **Reality**: It's complicated.

### Monosemanticity
A **Monosemantic Neuron** is one that fires for exactly one concept.
*   *Example*: The "Curve Detector" in a vision model (fires only for curves).
*   *Example*: The "Base64 Detector" in an LLM (fires only for base64 strings).

### Polysemanticity
Most neurons in large models are **Polysemantic**. They fire for multiple, seemingly unrelated concepts.
*   *Example*: A single neuron might fire for "The color blue" AND "Historical French Literature".
*   **Why?**: **Superposition**. The model wants to represent more concepts than it has neurons. It compresses these concepts into the available space by assigning multiple meanings to each neuron, relying on the fact that "Blue" and "French Literature" rarely appear in the same context, so it can distinguish them later.

## 2. Circuits

Neurons do not act alone. They form **Circuits**: sub-graphs of the network that perform a specific task.

### Induction Heads
One of the most famous discovered circuits.
*   **Task**: Copying patterns. If the sequence is "A B ... A", the Induction Head predicts "B".
*   **Mechanism**:
    1.  **Previous Token Head**: Attends to the previous token.
    2.  **Induction Head**: Attends to the token *before* the previous occurrence of the current token.
*   **Significance**: This circuit is responsible for "In-Context Learning" (the ability of LLMs to learn from examples in the prompt).

## 3. Sparse Autoencoders (SAEs)

To solve the Polysemanticity problem, researchers (like Anthropic) use **Sparse Autoencoders**.
*   **Idea**: Train a separate, much larger (sparse) network to decompose the activations of the dense model.
*   **Result**: This breaks apart the polysemantic neurons into "monosemantic features".
*   **Discovery**: Using SAEs, researchers found features for "Golden Gate Bridge", "Code Errors", and even "Deception".

## 4. Summary

Neuron-level modeling is moving AI from alchemy to biology. By mapping the "genome" of the model (its circuits and features), we hope to build safer, more controllable AI systems.
