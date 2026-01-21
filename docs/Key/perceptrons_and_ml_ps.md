# Perceptrons and Multi-Layer Perceptrons (MLPs)

## The Perceptron (1958)
The simplest form of a neural network, invented by Frank Rosenblatt. It models a single biological neuron.
*   **Inputs**: $x_1, x_2, ...$
*   **Weights**: $w_1, w_2, ...$ (Importance of each input)
*   **Bias**: $b$ (Threshold)
*   **Operation**: Weighted Sum $z = \sum (x_i \cdot w_i) + b$
*   **Activation**: Step function (Output 1 if $z > 0$, else 0).
*   **Limitation**: Can only solve linearly separable problems (e.g., AND, OR). It famously cannot solve **XOR**.

## Multi-Layer Perceptron (MLP)
To solve complex problems, we stack neurons in layers.
1.  **Input Layer**: Receives raw data.
2.  **Hidden Layers**: One or more layers in between.
3.  **Output Layer**: Final prediction.

This architecture is a **Universal Function Approximator**. With enough neurons and layers, it can theoretically approximate any continuous function.

## Key Components

### 1. Activation Functions
Non-linear functions applied to the output of each neuron. Without them, a deep network is mathematically equivalent to a single linear layer.
*   **Sigmoid / Tanh**: S-shaped curves. Prone to vanishing gradients.
*   **ReLU (Rectified Linear Unit)**: $f(x) = max(0, x)$. The standard for modern deep learning. Solves vanishing gradients but can suffer from "dying ReLU."
*   **GELU / Swish**: Smoother variants of ReLU used in Transformers.

### 2. Forward Propagation
Passing data from input to output to get a prediction.

### 3. Loss Function
Calculating the error between the prediction and the actual target (e.g., Mean Squared Error).

### 4. Backpropagation
The algorithm used to train the network. It calculates the gradient of the loss function with respect to each weight by applying the Chain Rule of calculus backwards from the output layer to the input.

### 5. Optimizer (SGD)
Updating the weights in the opposite direction of the gradient to minimize the loss.
