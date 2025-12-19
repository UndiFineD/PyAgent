# Hyperparameter Optimization (HPO)

Parameters are learned by the model (weights). **Hyperparameters** are set by the human *before* training (Learning Rate, Batch Size, Number of Layers). HPO is the process of finding the best ones.

## 1. Basic Methods

*   **Grid Search**: Try every combination.
    *   `LR = [0.1, 0.01]`, `Batch = [32, 64]`.
    *   Tries: (0.1, 32), (0.1, 64), (0.01, 32), (0.01, 64).
    *   **Cons**: Extremely expensive ($O(N^k)$).
*   **Random Search**: Pick random combinations.
    *   **Pros**: Surprisingly effective. Often beats Grid Search because some hyperparameters matter much more than others.

## 2. Bayesian Optimization

*   **Concept**: Build a probabilistic model (surrogate) of the function `Accuracy = f(Hyperparameters)`.
*   **Workflow**:
    1.  Try a few random points.
    2.  Update the model: "High Learning Rate seems bad."
    3.  Use an **Acquisition Function** to pick the next point to try (balancing Exploration vs. Exploitation).
*   **Tools**: **Optuna**, Hyperopt.

## 3. Neural Architecture Search (NAS)

*   Taking HPO to the extreme: Optimizing the architecture itself (e.g., "How many layers? How wide? Should I use a skip connection here?").
*   Used to discover EfficientNet and MobileNet.
