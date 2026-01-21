# Optimization Algorithms

The engine of Machine Learning. These algorithms adjust the model's weights to minimize the Loss Function.

## 1. Gradient Descent (SGD)

*   **Concept**: Calculate the slope (gradient) of the loss landscape and take a step downhill.
*   **Stochastic Gradient Descent (SGD)**: Instead of calculating the gradient for the *entire* dataset (which is slow), calculate it for a small "batch" of data.
*   **Momentum**: Like a heavy ball rolling down a hill, it accumulates speed. Helps the optimizer plow through flat areas and local minima.

## 2. Adaptive Methods

*   **Adam (Adaptive Moment Estimation)**: The default optimizer for most Deep Learning.
    *   It adapts the learning rate for *each parameter* individually.
    *   Combines Momentum (First moment) and RMSprop (Second moment).
*   **AdamW**: A fix for Adam that decouples Weight Decay from the gradient update. Essential for training Transformers correctly.

## 3. Advanced Techniques

*   **Learning Rate Schedulers**: Changing the learning rate during training.
    *   **Warmup**: Start low, ramp up (stabilizes early training).
    *   **Cosine Decay**: Slowly lower the LR to zero (helps converge to a better solution).
*   **Schedule-Free Optimization**: New research (2024) that eliminates the need for LR schedules, simplifying the training pipeline.
