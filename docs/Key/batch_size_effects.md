# Batch Size Effects

## Overview
The **Batch Size** is the number of training examples used in one iteration of model training. It is a crucial hyperparameter that affects training speed, memory usage, and model performance.

## Small Batch Size (e.g., 32, 64)
*   **Noise**: Gradients are noisy because they are estimated from a few samples.
*   **Generalization**: This noise acts as a form of regularization, often helping the model escape sharp local minima and find flatter minima (which generalize better).
*   **Speed**: Slower training (wall-clock time) because the GPU is not fully utilized (less parallelism).

## Large Batch Size (e.g., 4096, 8192)
*   **Stability**: Gradients are very accurate approximations of the true gradient.
*   **Speed**: Much faster training per epoch due to massive parallelization on GPUs/TPUs.
*   **Generalization Gap**: Large batches tend to converge to "sharp" minima, which leads to worse generalization on unseen data.

## The Linear Scaling Rule
When increasing the batch size, you must adjust the learning rate to maintain convergence speed.
*   **Rule**: If you multiply the batch size by $k$, multiply the learning rate by $k$.
    $$\eta_{new} = k \cdot \eta_{base}$$
*   **Caveat**: This works up to a point. For extremely large batches, you may need warmup or more complex scaling (like Square Root Scaling).

## Gradient Accumulation
If your GPU memory is too small for your desired batch size:
1.  Run multiple small batches (micro-batches) sequentially.
2.  Accumulate (sum) their gradients.
3.  Perform one optimizer step.
This simulates a large batch size without needing massive VRAM.
