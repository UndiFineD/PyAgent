# Universal Approximation Theorem

## Overview
The **Universal Approximation Theorem (UAT)** is the theoretical foundation that explains *why* Neural Networks are so powerful. It states that a feedforward neural network with a single hidden layer containing a finite number of neurons can approximate any continuous function on compact subsets of $\mathbb{R}^n$, under mild assumptions on the activation function.

## The Statement
Let $\varphi(\cdot)$ be a non-constant, bounded, and continuous activation function (like Sigmoid or Tanh).
Then, for any continuous function $f: [0, 1]^n \to \mathbb{R}$ and any error tolerance $\epsilon > 0$, there exists a neural network $F(x)$ with one hidden layer such that:
$$|F(x) - f(x)| < \epsilon$$
for all $x$ in the input space.

## Implications
1.  **Expressive Power**: Neural Networks are "Universal Function Approximators". There is no function (that we care about in practice) that a neural network *cannot* represent.
2.  **Existence vs. Learnability**: The theorem guarantees that a network *exists*, but it does not tell us:
    *   How to find the weights (training).
    *   How many neurons are needed (efficiency).
    *   Whether it will generalize to unseen data.

## Width vs. Depth
*   **Original UAT (Cybenko, 1989)**: Proved for arbitrary **width** (one hidden layer, infinite neurons).
*   **Deep UAT (Lu et al., 2017)**: Proved for arbitrary **depth** (bounded width, infinite layers). Deep networks are often exponentially more efficient at approximating complex functions than shallow, wide networks.
