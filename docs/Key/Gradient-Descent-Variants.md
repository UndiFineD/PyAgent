# Gradient Descent Variants

## Overview
**Gradient Descent** is the primary algorithm used to optimize neural networks. While standard Stochastic Gradient Descent (SGD) is powerful, it can be slow to converge and can get stuck in local minima or saddle points. Several variants have been developed to address these issues.

## Momentum
*   **Concept**: Momentum helps accelerate SGD in the relevant direction and dampens oscillations. It does this by adding a fraction $\gamma$ of the update vector of the past time step to the current update vector.
*   **Analogy**: A ball rolling down a hill accumulates momentum, becoming faster and faster (ignoring small bumps).
*   **Formula**:
    $$v_t = \gamma v_{t-1} + \eta \nabla_\theta J(\theta)$$
    $$\theta = \theta - v_t$$

## Adagrad (Adaptive Gradient Algorithm)
*   **Concept**: Adagrad adapts the learning rate to the parameters. It performs larger updates for infrequent parameters and smaller updates for frequent parameters.
*   **Use Case**: Great for sparse data (e.g., NLP word embeddings).
*   **Downside**: The accumulated squared gradients in the denominator keep growing, causing the learning rate to shrink to zero too early.

## RMSProp (Root Mean Square Propagation)
*   **Concept**: RMSProp fixes Adagrad's diminishing learning rate problem by using a moving average of squared gradients.
*   **Mechanism**: It divides the learning rate by an exponentially decaying average of squared gradients.

## Adam (Adaptive Moment Estimation)
*   **Concept**: Adam combines the best of both worlds: **Momentum** and **RMSProp**.
*   **Mechanism**: It keeps track of:
    1.  Exponential moving average of past gradients ($m_t$, like Momentum).
    2.  Exponential moving average of past squared gradients ($v_t$, like RMSProp).
*   **Status**: Adam is currently the default optimizer for most Deep Learning tasks.

## AdamW
*   **Concept**: A variant of Adam that decouples weight decay from the gradient update.
*   **Why**: In standard Adam, L2 regularization is not identical to weight decay (unlike in SGD). AdamW fixes this, leading to better generalization.
