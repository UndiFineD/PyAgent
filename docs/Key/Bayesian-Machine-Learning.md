# Bayesian Machine Learning

A probabilistic approach to Machine Learning. Instead of learning a single "best" value for a parameter (Point Estimate), we learn a **Distribution** of possible values.

## 1. The Core Idea (Bayes' Theorem)

$$ P(Model | Data) = \frac{P(Data | Model) \cdot P(Model)}{P(Data)} $$

*   **Prior $P(Model)$**: What we believe about the model *before* seeing data.
*   **Likelihood $P(Data | Model)$**: How well the model explains the data.
*   **Posterior $P(Model | Data)$**: Our updated belief *after* seeing the data.

## 2. Uncertainty Quantification

Standard Neural Networks are often "confidently wrong."
*   **Aleatoric Uncertainty**: Noise in the data (e.g., blurry image). Irreducible.
*   **Epistemic Uncertainty**: Lack of knowledge (e.g., the model has never seen a kangaroo). Reducible with more data.
*   **Bayesian NNs**: Weights are distributions (Mean $\mu$, Variance $\sigma$). If the variance is high, the model says "I don't know."

## 3. Gaussian Processes (GPs)

A non-parametric Bayesian method.
*   Instead of fitting a function, it defines a distribution over *all possible functions* that fit the data points.
*   Provides exact confidence intervals.
*   **Drawback**: Scales poorly ($O(N^3)$) with the number of data points.
