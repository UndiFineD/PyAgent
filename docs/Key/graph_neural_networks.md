# Graph Neural Networks (GNNs)

While Transformers process sequences (Text) and CNNs process grids (Images), **Graph Neural Networks (GNNs)** process graphs (Nodes and Edges). They are essential for data that has complex, non-Euclidean relationships.

## 1. Where are Graphs used?

*   **Social Networks**: Users are nodes, friendships are edges.
*   **Molecules**: Atoms are nodes, chemical bonds are edges. (Drug Discovery).
*   **Knowledge Graphs**: Entities ("Obama", "Hawaii") are nodes, relationships ("Born In") are edges.
*   **Recommender Systems**: Users and Products are nodes in a bipartite graph.

## 2. Message Passing

The core algorithm of GNNs.
1.  **Aggregate**: Every node looks at its neighbors. It gathers their feature vectors.
2.  **Update**: The node updates its own feature vector based on the aggregated information from its neighbors.
3.  **Repeat**: Do this for $K$ layers. After 1 layer, a node knows about its immediate neighbors. After 2 layers, it knows about neighbors-of-neighbors.

## 3. Key Architectures

### A. GCN (Graph Convolutional Network)
The "CNN for Graphs." It averages the features of neighbors. Simple and effective for node classification (e.g., "Is this user a bot?").

### B. GAT (Graph Attention Network)
Applies the **Attention Mechanism** to graphs.
*   Instead of treating all neighbors equally (like GCN), GAT learns *weights* for each neighbor.
*   "My relationship with neighbor A is more important than with neighbor B."

### C. GraphSAGE
Designed for massive graphs (like Pinterest). Instead of training on the whole graph at once, it samples a neighborhood for each node. This allows it to scale to billions of nodes.

## 4. GNNs + LLMs (GraphRAG)

A cutting-edge field is combining GNNs with LLMs.
*   **GraphRAG**: Instead of retrieving just "text chunks" (standard RAG), we retrieve a subgraph of related concepts from a Knowledge Graph.
*   This allows the LLM to answer multi-hop reasoning questions ("How is the CEO of Company A connected to the scandal in Company B?") that standard vector search misses.
