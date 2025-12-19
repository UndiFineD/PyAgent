# Bias-Variance Tradeoff

## Overview
The **Bias-Variance Tradeoff** is a fundamental concept in supervised learning that describes the tension between two sources of error that prevent supervised learning algorithms from generalizing beyond their training set.

## Error Decomposition
The total error of a model can be decomposed into three parts:
$$Error = Bias^2 + Variance + Irreducible Error$$

### 1. Bias (Underfitting)
*   **Definition**: The error introduced by approximating a real-world problem (which may be complex) by a simplified model.
*   **High Bias**: The model is too simple to capture the underlying patterns (e.g., using a linear regression for a quadratic relationship).
*   **Symptoms**: High training error and high validation error.

### 2. Variance (Overfitting)
*   **Definition**: The error introduced by the model's sensitivity to small fluctuations in the training set.
*   **High Variance**: The model captures random noise in the training data rather than the intended outputs.
*   **Symptoms**: Low training error but high validation error.

### 3. Irreducible Error (Noise)
*   The inherent noise in the data itself. No model can reduce this.

## The Tradeoff
*   **Simple Models**: High Bias, Low Variance.
*   **Complex Models**: Low Bias, High Variance.
*   **Goal**: Find the "Sweet Spot" (Goldilocks zone) where the sum of Bias and Variance is minimized.

## Modern Deep Learning View
In modern Deep Learning, we often observe that very large models (Low Bias) can also have Low Variance if trained with massive data and regularization. This challenges the classical U-shaped tradeoff curve (see **Double Descent**).
