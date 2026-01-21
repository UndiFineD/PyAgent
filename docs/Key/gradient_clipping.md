# Gradient Clipping

## Overview
**Gradient Clipping** is a technique used to prevent the **Exploding Gradient Problem**, which is common in Recurrent Neural Networks (RNNs) and very deep networks (like Transformers).

## The Problem: Exploding Gradients
During backpropagation, gradients are multiplied by the weight matrices at each layer. If the weights are large (e.g., > 1), the gradients can grow exponentially as they move backward.
*   **Result**: The gradient update becomes massive, causing the model weights to change drastically. The loss becomes `NaN` (Not a Number) or infinity, and training crashes.

## The Solution: Clipping
We artificially limit the magnitude of the gradients before the optimizer step.

### 1. Value Clipping
*   **Method**: Clip each element of the gradient vector to be within a range $[min, max]$ (e.g., $[-1, 1]$).
*   **Pros**: Simple.
*   **Cons**: Changes the direction of the gradient vector, which might lead the optimizer astray.

### 2. Norm Clipping (Standard)
*   **Method**: Scale the entire gradient vector $g$ so that its L2 norm (length) does not exceed a threshold $C$.
    $$if \ ||g|| > C: \ g \leftarrow g \cdot \frac{C}{||g||}$$
*   **Pros**: Preserves the **direction** of the gradient, only reducing its magnitude (step size).
*   **Usage**: This is the default method used in PyTorch (`torch.nn.utils.clip_grad_norm_`) and TensorFlow.

## When to Use
*   **RNNs/LSTMs**: Almost mandatory.
*   **Transformers**: Highly recommended (e.g., BERT, GPT training).
*   **ResNets**: Usually not needed due to Batch Normalization and skip connections.
