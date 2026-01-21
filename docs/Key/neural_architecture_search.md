# Neural Architecture Search (NAS)

Designing neural networks is an art. How many layers? How wide? What kernel size? **Neural Architecture Search (NAS)** automates this process, using AI to design AI.

## 1. The Search Space

What are we allowed to change?
*   **Macro Search**: Designing the entire network topology (e.g., how layers connect).
*   **Micro Search (Cell-Based)**: Designing a small "Cell" (a block of operations) and then stacking it repeatedly (like ResNet blocks). This is more efficient.

## 2. Search Strategies

### A. Reinforcement Learning (RL)
Used in the original NASNet paper.
*   **Controller (RNN)**: Generates a string describing a child network architecture.
*   **Reward**: Train the child network for a few epochs and get its accuracy.
*   **Update**: Use PPO/REINFORCE to update the Controller to generate better architectures.
*   **Cost**: Extremely expensive (thousands of GPU hours).

### B. Evolutionary Algorithms
Treat architectures as DNA.
*   **Mutation**: Change a layer size, add a skip connection.
*   **Crossover**: Combine parts of two good networks.
*   **Selection**: Keep the fittest networks.

### C. Differentiable NAS (DARTS)
The modern, fast approach.
*   Instead of making discrete choices (Layer A vs. Layer B), relax the search space to be continuous.
*   Compute a weighted sum of *all possible operations* (Conv3x3, Conv5x5, MaxPool).
*   Train the weights of the operations and the weights of the architecture selection simultaneously using gradient descent.
*   **Cost**: Can run on a single GPU in a day.

## 3. EfficientNet

A famous result of NAS. Google used NAS to find a baseline network (EfficientNet-B0) and then discovered a compound scaling law to scale it up (B1-B7) balancing depth, width, and resolution.

## 4. Hardware-Aware NAS

Designing networks for specific devices (e.g., MobileNet for phones).
*   The loss function includes not just Accuracy, but also **Latency** and **Power Consumption** on the target hardware.
