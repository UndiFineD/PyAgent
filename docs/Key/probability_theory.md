# Probability Theory for AI

## Overview
**Probability Theory** provides the framework for quantifying uncertainty. In AI, models don't just predict "Yes" or "No"; they predict "80% probability of Yes".

## Key Concepts

### 1. Random Variables
A variable whose value depends on the outcome of a random phenomenon.
*   **Discrete**: Takes specific values (e.g., Token ID in an LLM).
*   **Continuous**: Takes any value in a range (e.g., Pixel intensity in a Diffusion model).

### 2. Probability Distributions
*   **Bernoulli**: Binary outcome (0 or 1). Used for binary classification.
*   **Categorical (Multinoulli)**: One of $K$ outcomes. Used for next-token prediction (Softmax).
*   **Gaussian (Normal)**: Bell curve. Used in VAEs and Diffusion models to model noise.
    $$ p(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}(\frac{x-\mu}{\sigma})^2} $$

### 3. Bayes' Theorem
Describes how to update the probability of a hypothesis based on new evidence.
$$ P(A|B) = \frac{P(B|A)P(A)}{P(B)} $$
*   **Posterior**: $P(A|B)$ - Probability after seeing data.
*   **Likelihood**: $P(B|A)$ - How well the model explains the data.
*   **Prior**: $P(A)$ - Initial belief.
*   **Significance**: Fundamental to Bayesian Neural Networks and understanding how models learn from data.

### 4. Maximum Likelihood Estimation (MLE)
A method to estimate the parameters of a probability distribution by maximizing a likelihood function.
*   **Significance**: Training a neural network (minimizing Cross-Entropy Loss) is mathematically equivalent to performing MLE. We are finding the weights that make the training data "most probable".

### 5. Expectation and Variance
*   **Expectation ($E[x]$)**: The weighted average value.
*   **Variance ($\sigma^2$)**: How spread out the data is.
