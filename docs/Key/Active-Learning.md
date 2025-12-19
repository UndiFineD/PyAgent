# Active Learning

Data labeling is expensive. If you have 1 million unlabeled images, you can't afford to label them all. **Active Learning** is a strategy to select the *most informative* 1% of data points to label, such that the model learns as much as possible.

## 1. The Loop

1.  **Unlabeled Pool**: A massive dataset of raw data.
2.  **Selection Strategy**: The model (or a heuristic) picks a few samples.
3.  **Oracle (Human)**: A human annotator labels these samples.
4.  **Training**: The model is retrained (or updated) on the new labeled data.
5.  **Repeat**.

## 2. Selection Strategies

### A. Uncertainty Sampling
Pick the examples the model is most confused about.
*   **Least Confidence**: $1 - P(\hat{y}|x)$. (Pick the one with the lowest probability for the predicted class).
*   **Entropy**: Pick the one where the probability distribution is flattest (e.g., [0.33, 0.33, 0.34] is high entropy; [0.99, 0.01, 0.00] is low entropy).

### B. Diversity Sampling
Don't just pick hard examples; pick *different* examples.
*   If the model is confused about "Black Cats," don't just label 100 black cats. Label one black cat, one white dog, one red car.
*   **Core-Set**: Select a subset of points that cover the geometry of the entire dataset.

### C. Expected Model Change
Pick the examples that would cause the biggest change in the model's weights (gradients) if we knew their labels.

## 3. Human-in-the-Loop

Active Learning is the core of modern "Data Engines" (like Tesla's Autopilot team).
*   The car drives.
*   The model detects an edge case (e.g., a construction cone flying in the air).
*   It sends that clip to the server.
*   Humans label it.
*   The model is retrained.
