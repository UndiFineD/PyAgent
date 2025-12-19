# Calculus for Machine Learning

## Overview
**Calculus** provides the tools to optimize neural networks. While Linear Algebra defines the architecture, Calculus defines how we train it (minimize error).

## Key Concepts

### 1. The Derivative
The rate of change of a function at a specific point.
$$ f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} $$
*   **Significance**: Tells us which way to nudge a weight to decrease the loss.

### 2. Partial Derivatives
When a function has multiple inputs (like a neural network with millions of weights), we calculate the derivative with respect to *one* variable while holding others constant.
$$ \frac{\partial f}{\partial x} $$

### 3. The Gradient ($\nabla$)
A vector containing all the partial derivatives of a function.
$$ \nabla f = \left[ \frac{\partial f}{\partial w_1}, \frac{\partial f}{\partial w_2}, \dots \right] $$
*   **Significance**: The gradient points in the direction of steepest ascent. To minimize loss, we move in the opposite direction (Gradient Descent).

### 4. The Chain Rule
The formula for computing the derivative of a composite function $f(g(x))$.
$$ \frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx} $$
*   **Significance**: This is the mathematical engine of **Backpropagation**. It allows us to calculate how a change in the first layer affects the loss in the final layer by multiplying gradients layer-by-layer.

### 5. Jacobian and Hessian Matrices
*   **Jacobian**: A matrix of all first-order partial derivatives of a vector-valued function. Used in robotics and advanced optimization.
*   **Hessian**: A matrix of second-order partial derivatives (curvature). Used in Newton's Method optimization (though rarely in Deep Learning due to computational cost).

## Automatic Differentiation (Autograd)
Modern frameworks (PyTorch, JAX) do not require you to calculate derivatives by hand. They build a computational graph and apply the Chain Rule automatically.
*   **Forward Mode**: Efficient for functions with few inputs and many outputs.
*   **Reverse Mode (Backprop)**: Efficient for functions with many inputs and few outputs (like a scalar Loss), which is the case for Neural Networks.
