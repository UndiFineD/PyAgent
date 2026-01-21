# Recommendation Architectures

Modern recommender systems have evolved from simple matrix factorization to complex deep learning architectures capable of handling massive scale and rich features.

## 1. Two-Tower Models (Dual Encoders)

The standard architecture for retrieval at scale.

### Architecture
- **User Tower**: A neural network that processes user features (demographics, history) into a dense embedding vector $u$.
- **Item Tower**: A separate neural network that processes item features (content, metadata) into a dense embedding vector $v$.
- **Scoring**: The dot product $u \cdot v$ (or cosine similarity) represents the affinity score.

### Advantages
- **Scalability**: Item embeddings can be pre-computed and indexed in a Vector Database (ANN). At inference time, only the user embedding is computed, followed by a fast nearest neighbor search.
- **Flexibility**: Each tower can use different architectures (e.g., RNN for user history, CNN for item images).

### Limitations
- **Late Interaction**: User and item features only interact at the very end (dot product), missing complex cross-feature interactions (e.g., "users under 25 like sci-fi movies released after 2010").

## 2. Deep Learning Recommendation Model (DLRM)

Open-sourced by Meta, DLRM is designed to handle both categorical and dense features effectively, specifically for the ranking stage.

### Key Components
- **Sparse Features**: Handled by massive embedding tables (e.g., User ID, Item ID).
- **Dense Features**: Processed by a Multi-Layer Perceptron (MLP) (e.g., age, time of day).
- **Feature Interaction**: Explicitly models interactions between embeddings using dot products of all pairs of embedding vectors.
- **Top MLP**: Combines the interaction signals to output a probability (click/no-click).

### Why it Matters
- **Personalization**: Captures high-order interactions that Two-Tower models miss.
- **Efficiency**: Optimized for training on GPU clusters with model parallelism (due to large embedding tables).

## 3. Session-Based Recommendation (RNNs/Transformers)

Focuses on the sequence of user actions within a short session, rather than long-term history.

### Architectures
- **GRU4Rec**: Uses Gated Recurrent Units to model the sequence of item clicks.
- **SASRec (Self-Attentive Sequential Recommendation)**: Uses Transformer encoders to weigh the importance of previous items in the sequence to predict the next one.

### Use Cases
- **Anonymous Users**: When no long-term profile exists (e.g., e-commerce guest checkout).
- **Dynamic Intent**: When user intent shifts rapidly (e.g., browsing for gifts vs. personal items).

## 4. Graph Neural Networks (GNNs) for RecSys

- **PinSage / GraphSAGE**: Models users and items as nodes in a bipartite graph.
- **Mechanism**: Aggregates information from neighbors (e.g., "items bought by similar users") to generate embeddings.
- **Benefit**: Naturally captures high-order connectivity (A is similar to B because they share neighbors C and D).

## Summary Comparison

| Architecture | Stage | Strength | Weakness |
| :--- | :--- | :--- | :--- |
| **Two-Tower** | Retrieval | Extremely fast inference; scalable | Misses complex feature interactions |
| **DLRM** | Ranking | High accuracy; captures interactions | Computationally expensive for retrieval |
| **SASRec** | Retrieval/Ranking | Captures sequential context | Requires sequence history |
| **GNNs** | Retrieval | Leverages structural data | Hard to scale to billion-node graphs |
