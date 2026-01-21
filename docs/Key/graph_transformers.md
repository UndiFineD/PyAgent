# Graph Transformers

Standard Graph Neural Networks (GNNs) like GCNs and GATs rely on **Message Passing**: nodes only talk to their immediate neighbors.
This leads to issues:
1.  **Oversmoothing**: After many layers, all node representations become identical.
2.  **Long-Range Dependencies**: Information takes $K$ steps to travel $K$ hops.

**Graph Transformers** apply the global Self-Attention mechanism to graphs, allowing every node to talk to every other node directly.

## 1. The Challenge: Structure

In NLP, position is a 1D sequence (1, 2, 3...). In Graphs, "position" is complex.
If we just treat nodes as a set, we lose the graph structure.
We need **Graph Positional Encodings**.

## 2. Positional Encodings

- **Laplacian PEs**: Using the eigenvectors of the Graph Laplacian matrix (similar to Fourier modes).
- **Random Walk PEs**: Using the probability of landing on a node after $k$ steps of a random walk.
- **Shortest Path Distance**: Encoding the distance between nodes $i$ and $j$ as a bias in the attention matrix.

## 3. Architecture

- **Global Attention**: $Attention(Q, K, V)$. Allows capturing long-range interactions (e.g., in a molecule, two distant atoms might interact).
- **Edge Features**: Edges are not just connectivity; they have features (bond type). These are injected into the attention score calculation.

## Summary

Graph Transformers (like Graphormer) are now the state-of-the-art for molecular property prediction (e.g., OGB-LSC), replacing MPNNs for complex tasks.
