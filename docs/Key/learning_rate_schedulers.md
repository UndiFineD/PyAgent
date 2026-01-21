# Learning Rate Schedulers

## Overview
The **Learning Rate (LR)** is one of the most critical hyperparameters in training neural networks.
*   **Too High**: The model diverges or oscillates around the minimum.
*   **Too Low**: The model trains very slowly or gets stuck in a suboptimal local minimum.

**LR Schedulers** adjust the learning rate dynamically during training.

## Common Strategies

### 1. Step Decay
*   **Mechanism**: Reduce the LR by a factor (e.g., 0.1) every $N$ epochs.
*   **Pros**: Simple to implement.
*   **Cons**: Requires manual tuning of the step size and interval.

### 2. Linear Warmup
*   **Mechanism**: Start with a very small LR and linearly increase it to the target LR over the first few epochs (e.g., 5% of training).
*   **Why**: In the beginning, gradients can be very large and unstable. Warmup allows the model to stabilize before aggressive learning begins.

### 3. Cosine Annealing
*   **Mechanism**: The LR follows a cosine curve, starting high and decaying to near zero.
*   **Formula**: $\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(1 + \cos(\frac{T_{cur}}{T_{max}}\pi))$
*   **Pros**: Smooth decay, no abrupt drops. Often leads to better convergence than step decay.

### 4. ReduceLROnPlateau
*   **Mechanism**: Monitor a metric (e.g., Validation Loss). If it stops improving for a certain number of epochs ("patience"), reduce the LR.
*   **Pros**: Adaptive; only reduces LR when necessary.

### 5. One Cycle Policy
*   **Mechanism**: Rapidly increase LR to a maximum, then slowly decrease it.
*   **Impact**: Allows for "Super-Convergence" (training much faster than standard methods).

## Best Practices
*   **Transformers**: Almost always use **Linear Warmup** followed by **Cosine Decay**.
*   **Fine-Tuning**: Use a much lower LR than training from scratch (e.g., 1e-5 vs 1e-3).
