# Energy-Based Models (EBMs)

Energy-Based Models represent a different paradigm from the standard probabilistic view of machine learning. Championed by Yann LeCun, they offer a unified framework for learning, particularly for tasks where the output is high-dimensional or structured (like images or text).

## 1. The Core Idea: The Energy Function

Instead of trying to estimate a normalized probability distribution $P(y|x)$ (which requires a difficult-to-compute partition function), EBMs learn an **Energy Function** $E(x, y)$.

- **Low Energy**: Compatible pairs of $(x, y)$ (e.g., a picture of a cat and the label "cat").
- **High Energy**: Incompatible pairs (e.g., a picture of a cat and the label "dog").

**Inference** becomes an optimization problem: Find the $y$ that minimizes the energy for a given $x$.
$$ y^* = \text{argmin}_y E(x, y) $$

## 2. Why EBMs?

### The Normalization Problem
In standard Softmax classification, you must sum over all possible classes to ensure probabilities sum to 1.
$$ P(y|x) = \frac{e^{-E(x,y)}}{\sum_{y'} e^{-E(x,y')}} $$
- For classification (1000 classes), this is fine.
- For generation (all possible images), the denominator (partition function) is intractable. EBMs skip this normalization step.

### Joint Embedding Architecture (JEPA)
A modern application of EBM principles.
- Instead of predicting the exact pixels of a missing part of an image (generative), JEPAs predict the *representation* of the missing part in an abstract space.
- **Goal**: Minimize the "energy" (distance) between the predicted representation and the actual representation.

## 3. Training EBMs

Training involves shaping the energy landscape:
1.  **Push Down**: Lower the energy of observed (training) data points.
2.  **Push Up**: Raise the energy of unobserved (incorrect) points.

### Contrastive Divergence
A common training method.
- Pick a real data point (positive sample).
- Generate a "fake" point nearby (negative sample) using the current model.
- Update weights to lower energy of positive and raise energy of negative.

## 4. Applications

- **Self-Supervised Learning**: Learning representations without labels (e.g., SimCLR, VICReg) can be viewed through the lens of EBMs.
- **Structured Prediction**: Handwriting recognition, protein folding, where the output has complex internal dependencies.
- **Out-of-Distribution Detection**: Samples with high energy are likely outliers.

## Summary

| Feature | Probabilistic Models | Energy-Based Models |
| :--- | :--- | :--- |
| **Output** | Probability $P(y\|x)$ | Energy Scalar $E(x, y)$ |
| **Constraint** | Must sum to 1 | No normalization required |
| **Inference** | Sampling / Argmax | Optimization (Gradient Descent on $y$) |
| **Philosophy** | Model the data distribution | Model the compatibility function |
