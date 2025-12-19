# Dimensionality Reduction

Techniques to reduce the number of input variables (features) in a dataset while preserving the most important information. Essential for visualization and removing noise.

## 1. PCA (Principal Component Analysis)

*   **Linear**: Finds the "Principal Components" (directions of maximum variance) in the data.
*   **Projection**: Rotates and projects the data onto these new axes.
*   **Use Case**: Compressing data, removing correlated features.

## 2. t-SNE (t-Distributed Stochastic Neighbor Embedding)

*   **Non-Linear**: Focuses on keeping similar data points close together in the lower dimension.
*   **Probabilistic**: Converts distances into probabilities.
*   **Use Case**: Visualizing high-dimensional clusters (e.g., visualizing MNIST digits or Word Embeddings in 2D).
*   **Drawback**: Slow; does not preserve global structure well (distances between far-away clusters are meaningless).

## 3. UMAP (Uniform Manifold Approximation and Projection)

*   **The Modern Standard**: Faster than t-SNE and preserves both local and global structure better.
*   **Manifold Learning**: Assumes the data lies on a curved surface (manifold) within the high-dimensional space.
*   **Use Case**: Visualizing single-cell genomics data, document embeddings.
