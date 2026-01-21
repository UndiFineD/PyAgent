# Sparse Autoencoders (SAEs)

Sparse Autoencoders have emerged as the leading technique for **Mechanistic Interpretability** in Large Language Models. They aim to solve the "Superposition Hypothesis" and decompose the dense, unintelligible activations of a neural network into human-understandable features.

## 1. The Problem: Polysemanticity & Superposition

- **Polysemantic Neurons**: In a standard LLM, a single neuron might fire for "cats," "cars," and "geometry." It has multiple meanings.
- **Superposition**: Because the model has more "concepts" to learn than it has neurons, it packs multiple concepts into the same linear subspace. This makes reading the "mind" of the LLM impossible by just looking at neuron activations.

## 2. The Solution: Dictionary Learning

An SAE is trained to take the activation vector of a layer (e.g., the output of an MLP block in GPT-4) and decompose it into a linear combination of "sparse features."

### Architecture
1.  **Encoder**: Takes the dense model activation $x$ and maps it to a much larger, sparse hidden layer $f$.
    $$ f = \text{ReLU}(W_e x + b_e) $$
2.  **Decoder**: Reconstructs the original activation $\hat{x}$ from the sparse features.
    $$ \hat{x} = W_d f + b_d $$

### Training Objective
Minimize reconstruction error + L1 penalty (sparsity).
$$ L = ||x - \hat{x}||^2 + \lambda ||f||_1 $$
The L1 penalty forces most elements of $f$ to be zero.

## 3. The Result: Monosemantic Features

When trained correctly (often with a hidden dimension 10x-100x larger than the input), the features in the SAE become **Monosemantic**.
- **Feature 1245**: Fires *only* for references to the Golden Gate Bridge.
- **Feature 892**: Fires *only* for code syntax errors in Python.
- **Feature 33**: Fires *only* for the concept of "sadness."

## 4. Applications

- **Circuit Analysis**: Tracing how "sadness" flows through the network to influence the output.
- **Steering**: Manually clamping the "Golden Gate Bridge" feature to high to force the model to talk about it (Golden Gate Claude).
- **Safety**: Detecting if a "deception" or "bias" feature is active before the model outputs text.

## Summary

| Concept | Standard LLM Neuron | SAE Feature |
| :--- | :--- | :--- |
| **Meaning** | Polysemantic (Many concepts) | Monosemantic (One concept) |
| **Activation** | Dense (Always firing a little) | Sparse (Rarely fires) |
| **Count** | Fixed (e.g., 4096) | Massive (e.g., 100k+) |
| **Interpretability** | Low | High |
