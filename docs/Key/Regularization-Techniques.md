# Regularization Techniques

## Overview
**Regularization** refers to any technique that prevents a model from **overfitting** (memorizing the training data) and encourages it to **generalize** to unseen data.

## L1 and L2 Regularization
These add a penalty term to the Loss function based on the magnitude of the weights.
*   **L2 Regularization (Ridge)**: Adds $\lambda \sum w^2$.
    *   Encourages small, diffuse weights.
    *   Equivalent to **Weight Decay** in SGD.
*   **L1 Regularization (Lasso)**: Adds $\lambda \sum |w|$.
    *   Encourages **sparsity** (driving many weights to exactly zero). Useful for feature selection.

## Dropout
*   **Mechanism**: During training, randomly "drop" (set to zero) a fraction $p$ of neurons in a layer (e.g., $p=0.5$).
*   **Effect**: Prevents neurons from co-adapting too much. Forces the network to learn redundant representations.
*   **Inference**: During testing, all neurons are active, but their weights are scaled by $(1-p)$ to match the expected magnitude.

## DropConnect
*   **Mechanism**: Similar to Dropout, but instead of dropping neurons (activations), it drops individual **weights** (connections) randomly.

## Early Stopping
*   **Mechanism**: Monitor validation loss during training. If it starts increasing (while training loss continues to decrease), stop training immediately.
*   **Effect**: Prevents the model from over-optimizing on the training set.

## Data Augmentation
*   **Mechanism**: Artificially increasing the size of the training set by transforming inputs (flipping, rotating, cropping images).
*   **Effect**: The model sees more diverse examples, making it harder to memorize specific pixels.
