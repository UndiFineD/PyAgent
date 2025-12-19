# Vector Search Algorithms

Vector Databases are the backbone of RAG, but how do they actually find the "nearest neighbor" among millions of vectors in milliseconds? They use Approximate Nearest Neighbor (ANN) algorithms.

## 1. HNSW (Hierarchical Navigable Small World)
The industry standard for in-memory vector search.
*   **Structure**: A multi-layered graph.
    *   **Top Layer**: Sparse connections (like an express highway). Allows long jumps across the graph.
    *   **Bottom Layer**: Dense connections (local roads). Allows fine-grained navigation.
*   **Search**: Start at the top layer, greedily move to the closest node, drop down a layer, repeat until the bottom layer is reached.
*   **Pros**: Extremely fast and accurate (Recall > 95%).
*   **Cons**: Memory hungry (stores the full graph structure).

## 2. IVF (Inverted File Index)
*   **Training**: Cluster the entire dataset into $K$ clusters (centroids) using K-Means.
*   **Indexing**: Assign every vector to its nearest centroid.
*   **Search**:
    1.  Find the nearest centroid(s) to the query vector.
    2.  Search *only* the vectors inside those clusters.
*   **Pros**: Reduces the search space drastically.
*   **Cons**: Lower recall if the correct vector is near the edge of a cluster that wasn't selected (Edge Problem).

## 3. Product Quantization (PQ)
A compression technique often combined with IVF (IVF-PQ).
*   **Method**:
    1.  Split a high-dimensional vector (e.g., 1024 dims) into $M$ sub-vectors (e.g., 8 sub-vectors of 128 dims).
    2.  Run K-Means on each sub-space to find 256 centroids.
    3.  Replace each sub-vector with the ID of its nearest centroid (1 byte).
*   **Result**: A 1024-float vector (4KB) is compressed to 8 bytes.
*   **Pros**: Massive memory reduction (100x).
*   **Cons**: Lossy compression reduces accuracy.

## 4. DiskANN (Vamana)
*   **Goal**: Run vector search on SSDs (Disk) instead of RAM, allowing billion-scale datasets on a single machine.
*   **Method**: A graph-based algorithm (like HNSW) optimized to minimize disk reads. It stores the graph on disk and caches the "entry points" in RAM.
