# Kolmogorov-Arnold Networks (KANs)

Proposed in 2024, KANs are a fundamental rethinking of the neural network architecture. They challenge the Multi-Layer Perceptron (MLP) structure that has dominated AI for decades.

## 1. The Theorem: Kolmogorov-Arnold Representation

The theorem states that any multivariate continuous function can be represented as a superposition of continuous univariate functions.
$$ f(x_1, \dots, x_n) = \sum_{q=0}^{2n} \Phi_q \left( \sum_{p=1}^n \phi_{q,p}(x_p) \right) $$

## 2. MLP vs. KAN

### Multi-Layer Perceptron (MLP)
- **Nodes**: Have fixed activation functions (ReLU, Sigmoid).
- **Edges**: Have learnable linear weights ($w \cdot x$).
- **Structure**: Linear transform $\rightarrow$ Non-linearity.

### Kolmogorov-Arnold Network (KAN)
- **Nodes**: Just sum up incoming signals.
- **Edges**: Have **learnable activation functions** (Splines).
- **Structure**: Non-linear transform on every edge $\rightarrow$ Sum.

## 3. Why KANs?

### Accuracy & Efficiency
KANs can often achieve the same accuracy as MLPs with significantly fewer parameters.
- *Example*: A KAN might solve a partial differential equation with 100 parameters where an MLP needs 10,000.

### Interpretability
Because the functions are on the edges and are univariate (1D), you can visualize them.
- You can look at a KAN and see: "Oh, this edge learned a sine wave, and that edge learned a quadratic function."
- This allows scientists to **rediscover physical laws** (e.g., $E=mc^2$) by training a KAN on data and inspecting the learned functions.

### Catastrophic Forgetting
KANs appear to be more resistant to catastrophic forgetting than MLPs because the changes to the spline functions are local.

## 4. Challenges

- **Training Speed**: Currently, KANs are slower to train than MLPs because they cannot leverage the massive matrix-multiplication optimizations of modern GPUs as easily.
- **Scaling**: It is yet to be proven if KANs scale to the size of LLMs (billions of parameters).

## Summary

KANs place the "intelligence" (non-linearity) on the connections rather than the neurons, offering a potentially more efficient and interpretable path for AI in science and math.
