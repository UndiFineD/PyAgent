# Label Smoothing

## Overview
**Label Smoothing** is a regularization technique used in classification tasks to prevent the model from becoming **overconfident**.

## The Problem: Hard Targets
In standard classification (Cross-Entropy Loss), the target is a "one-hot" vector.
*   Example (Cat, Dog, Bird): `[0, 1, 0]` (100% Dog).
*   To minimize loss, the model tries to push the predicted probability for "Dog" to 1.0 and others to 0.0.
*   **Issue**: This forces the logits (pre-softmax scores) to infinity. The model becomes extremely confident, even on ambiguous or mislabeled data, leading to overfitting.

## The Solution: Soft Targets
Instead of 0 and 1, we "smooth" the labels by stealing a little probability mass from the correct class and distributing it uniformly among the incorrect classes.

### Formula
$$y_{new} = (1 - \epsilon) \cdot y_{one\_hot} + \frac{\epsilon}{K}$$
Where:
*   $\epsilon$: Smoothing parameter (e.g., 0.1).
*   $K$: Number of classes.

### Example ($\epsilon = 0.1, K=3$)
*   **Hard Target**: `[0, 1, 0]`
*   **Soft Target**: `[0.033, 0.933, 0.033]`

## Effect
*   The model is no longer forced to predict 100% probability. It is satisfied with 93.3%.
*   This prevents the weights from growing too large.
*   **Result**: Better generalization and calibration (the predicted probabilities better reflect the true accuracy).
*   **Usage**: Standard in training Transformers (like the original "Attention Is All You Need" paper) and ImageNet models (Inception).
