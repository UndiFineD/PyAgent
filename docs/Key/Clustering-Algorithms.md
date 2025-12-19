# Clustering Algorithms

Unsupervised learning techniques to group similar data points together without any labels.

## 1. K-Means

*   **Algorithm**:
    1.  Pick $K$ random centroids.
    2.  Assign every point to the nearest centroid.
    3.  Move the centroid to the average position of its points.
    4.  Repeat until convergence.
*   **Pros**: Fast and simple.
*   **Cons**: You must specify $K$ (number of clusters); assumes clusters are spherical.

## 2. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

*   **Concept**: Clusters are dense regions separated by sparse regions.
*   **Pros**:
    *   Does not require specifying $K$.
    *   Can find arbitrarily shaped clusters (e.g., a ring surrounding a ball).
    *   Identifies **Noise** (outliers) automatically.
*   **Cons**: Struggles with varying densities.

## 3. Hierarchical Clustering

*   **Agglomerative**: Start with every point as its own cluster. Merge the two closest clusters. Repeat until only one cluster remains.
*   **Dendrogram**: A tree diagram showing the hierarchy of merges. You can "cut" the tree at any level to get $N$ clusters.
*   **Use Case**: Taxonomies (grouping animals into species/families).
