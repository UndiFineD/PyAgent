# Initialization Methods

## Overview
**Weight Initialization** is the process of setting the initial values of the neural network parameters before training begins.
*   **Bad Initialization**: Can lead to vanishing/exploding gradients, causing the network to never learn.
*   **Good Initialization**: Ensures gradients flow properly through the network, speeding up convergence.

## The Problem with Zero or Random
*   **All Zeros**: If all weights are zero, all neurons in a layer compute the same output and get the same gradient update. The symmetry is never broken.
*   **Random Normal (Gaussian)**: If the variance is too high, activations explode. If too low, they vanish.

## Xavier (Glorot) Initialization
*   **Designed for**: Sigmoid or Tanh activation functions.
*   **Goal**: Keep the variance of activations the same across every layer.
*   **Formula**: Draw weights from a distribution with variance:
    $$Var(W) = \frac{2}{n_{in} + n_{out}}$$
    Where $n_{in}$ is the number of input units and $n_{out}$ is the number of output units.

## He (Kaiming) Initialization
*   **Designed for**: ReLU (Rectified Linear Unit) and its variants (Leaky ReLU).
*   **Why**: ReLU kills half the activations (sets them to zero). Xavier initialization doesn't account for this and leads to vanishing signals in deep ReLU networks.
*   **Formula**: Draw weights from a distribution with variance:
    $$Var(W) = \frac{2}{n_{in}}$$

## Orthogonal Initialization
*   **Designed for**: RNNs (Recurrent Neural Networks).
*   **Mechanism**: Initialize the weight matrix as an orthogonal matrix (eigenvalues have absolute value 1).
*   **Effect**: Preserves the norm of the gradient vector over many time steps, helping with the vanishing gradient problem in RNNs.
