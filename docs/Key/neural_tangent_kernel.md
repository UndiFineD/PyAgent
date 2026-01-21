# Neural Tangent Kernel (NTK)

## Overview
The **Neural Tangent Kernel (NTK)** is a theoretical tool used to analyze the training dynamics of Deep Neural Networks. It describes how a neural network evolves during training with Gradient Descent.

## The Infinite Width Limit
When the width of a neural network (number of neurons per layer) goes to infinity:
1.  **Initialization**: The network behaves like a Gaussian Process.
2.  **Training**: The network behaves like a **Linear Model** (Kernel Method) with a specific kernel called the Neural Tangent Kernel.
3.  **Dynamics**: The weights change very little, but the output changes significantly. The training dynamics can be solved exactly analytically.

## Why is it Important?
*   **Understanding**: It provides a rigorous mathematical framework to understand why over-parameterized networks converge to global minima.
*   **Kernel Methods**: It bridges the gap between Deep Learning and classical Kernel Methods (like SVMs).
*   **Limitations**: While NTK explains the "lazy training" regime (where features don't change much), it fails to explain "feature learning" (where the model learns complex representations), which is crucial for the success of modern Deep Learning.

## Formula
For a network $f(x; \theta)$, the NTK is defined as:
$$\Theta(x, x') = \langle \nabla_\theta f(x; \theta), \nabla_\theta f(x'; \theta) \rangle$$
This kernel measures the similarity between two inputs $x$ and $x'$ based on how the network's gradients align.
