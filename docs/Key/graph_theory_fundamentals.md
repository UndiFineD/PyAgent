# Graph Theory Fundamentals for AI

**Graph Theory** is the mathematical study of graphs, which are structures used to model pairwise relations between objects. In Artificial Intelligence, graphs are ubiquitous, forming the backbone of Knowledge Graphs, Social Network Analysis, and Graph Neural Networks (GNNs).

## Core Components

### 1. Basic Definitions
*   **Graph ($G$)**: A pair $G = (V, E)$, where $V$ is a set of **Vertices** (Nodes) and $E$ is a set of **Edges** (Links) connecting them.
*   **Directed vs. Undirected**:
    *   **Undirected**: Edges have no direction (e.g., Facebook friends). $(u, v) = (v, u)$.
    *   **Directed (Digraph)**: Edges have a direction (e.g., Twitter follows). $(u, v) \neq (v, u)$.
*   **Weighted Graph**: Edges have a numerical value (weight) representing strength, distance, or cost.

### 2. Matrix Representations
To process graphs with computers (and Neural Networks), we convert them into matrices.
*   **Adjacency Matrix ($A$)**: A square matrix of size $N \times N$ (where $N$ is the number of nodes). $A_{ij} = 1$ if there is an edge from $i$ to $j$, else $0$.
*   **Degree Matrix ($D$)**: A diagonal matrix where $D_{ii}$ is the number of edges connected to node $i$.
*   **Laplacian Matrix ($L$)**: Defined as $L = D - A$. It captures the structure of the graph and is crucial for **Spectral Graph Theory**.

## Key Concepts in AI

### 1. Connectivity & Paths
*   **Path**: A sequence of edges connecting two nodes.
*   **Shortest Path**: The path with the minimum sum of edge weights (e.g., Dijkstra's algorithm, A* Search).
*   **Connected Component**: A subgraph where every node is reachable from every other node.

### 2. Centrality Measures
Identifying the most "important" nodes in a network.
*   **Degree Centrality**: Number of connections.
*   **PageRank**: A recursive measure where a node is important if other important nodes link to it (used by Google and in TextRank for summarization).

### 3. Spectral Graph Theory
The study of the properties of a graph in relationship to the characteristic polynomial, eigenvalues, and eigenvectors of matrices associated with the graph (like the Laplacian).
*   **Relevance**: This is the mathematical foundation for **Graph Convolutional Networks (GCNs)**, which perform convolution operations in the spectral domain (or approximations of it).

## Applications in AI
*   **Knowledge Graphs**: Modeling entities (Nodes) and relationships (Edges) for reasoning (e.g., "Paris" --is_capital_of--> "France").
*   **Graph Neural Networks**: Predicting node properties (e.g., is this user a bot?) or link prediction (e.g., will these two users become friends?).
*   **Causal Graphs**: Modeling cause-and-effect relationships (Directed Acyclic Graphs - DAGs).
