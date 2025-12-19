# Information Theory for AI

## Overview
**Information Theory** studies the quantification, storage, and communication of information. In AI, it provides the metrics we use to measure how "surprised" a model is by the data.

## Key Concepts

### 1. Entropy ($H$)
A measure of uncertainty or "surprise". High entropy means the outcome is unpredictable (uniform distribution). Low entropy means the outcome is certain.
$$ H(P) = -\sum P(x) \log P(x) $$
*   **Significance**: In Reinforcement Learning, we often add an "Entropy Bonus" to encourage exploration (preventing the agent from becoming too confident too early).

### 2. Cross-Entropy Loss
Measures the difference between two probability distributions: the true distribution $P$ (one-hot label) and the predicted distribution $Q$ (softmax output).
$$ H(P, Q) = -\sum P(x) \log Q(x) $$
*   **Significance**: The standard loss function for classification and LLM training. Minimizing Cross-Entropy is equivalent to maximizing the likelihood of the correct class.

### 3. Kullback-Leibler (KL) Divergence
A measure of how one probability distribution $Q$ diverges from a second, expected probability distribution $P$.
$$ D_{KL}(P || Q) = \sum P(x) \log \frac{P(x)}{Q(x)} $$
*   **Significance**: Used in Variational Autoencoders (VAEs) to force the learned latent distribution to approximate a standard Gaussian distribution. Also used in RL (PPO) to prevent the policy from changing too drastically.

### 4. Mutual Information ($I$)
Measures how much information one random variable tells us about another.
$$ I(X; Y) = H(X) - H(X|Y) $$
*   **Significance**: Used in feature selection and contrastive learning (maximizing mutual information between different views of the same image).

### 5. Perplexity
A measurement of how well a probability model predicts a sample.
$$ PP(P) = 2^{H(P)} $$
*   **Significance**: The standard metric for evaluating LLMs. A perplexity of 10 means the model is as confused as if it had to choose uniformly from 10 options. Lower is better.
