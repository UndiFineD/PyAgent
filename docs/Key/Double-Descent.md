# Double Descent

## Overview
**Double Descent** is a phenomenon observed in modern Deep Learning that contradicts the classical Bias-Variance Tradeoff.

## The Classical View (U-Curve)
Traditionally, as model complexity increases:
1.  Training error goes down.
2.  Test error goes down initially (underfitting $\to$ optimal).
3.  Test error goes back up (overfitting).

## The Modern View (Double Descent)
In Deep Learning, as we continue to increase model size (or training time) *beyond* the point of overfitting:
1.  **First Descent**: The classical U-curve. Test error decreases then increases.
2.  **Interpolation Threshold**: The point where the model is large enough to achieve 0% training error (perfectly memorizing the data).
3.  **Second Descent**: Surprisingly, if we make the model *even larger*, the test error starts to decrease again!

## Why?
The theory is that highly over-parameterized models (where parameters >> data points) act as "smooth" interpolators.
*   Instead of memorizing the data in a "jagged" way (high variance), the optimization algorithm (SGD) finds a solution that fits the training data perfectly but has the smallest norm (smoothest function).
*   This smoothness allows the model to generalize well, even though it has memorized the training set.

## Implications
"Bigger is Better". This justifies the trend of training massive models (LLMs) that are vastly larger than the amount of data required to fit them.
