# Vector Databases

Vector Databases are the memory systems of modern AI. They store high-dimensional vectors (embeddings) and allow for efficient "Nearest Neighbor" search. This is the core technology behind **RAG (Retrieval Augmented Generation)**.

## 1. What is a Vector DB?

Standard databases (SQL) search for exact matches (`WHERE id = 5`).
Vector databases search for *semantic similarity*.
*   **Input**: A query vector (e.g., embedding of "How do I reset my password?").
*   **Operation**: Find the top K vectors in the database that are closest (Euclidean distance or Cosine Similarity) to the query.
*   **Output**: The documents associated with those vectors (e.g., the "Password Reset" manual page).

## 2. Indexing Algorithms

Searching a billion vectors one by one (Brute Force / KNN) is too slow ($O(N)$). We need Approximate Nearest Neighbor (ANN) algorithms ($O(\log N)$).

### A. HNSW (Hierarchical Navigable Small World)
The industry standard (used in Chroma, Weaviate, Pinecone).
*   **Structure**: A multi-layered graph.
*   **Top Layer**: Sparse connections (like a highway) to quickly jump across the vector space.
*   **Bottom Layer**: Dense connections for fine-grained search.
*   **Analogy**: Like zooming in on a map. Start at the continent level, then city, then street.

### B. IVF (Inverted File Index)
Used in Faiss.
*   **Clustering**: Divide the vector space into Voronoi cells (clusters) using K-Means.
*   **Search**: Only search the vectors inside the closest cluster(s) to the query.

## 3. Popular Libraries & Databases

*   **Faiss (Facebook AI Similarity Search)**: A library (C++/Python) for efficient similarity search. Not a full database, but the engine inside many.
*   **Chroma / LanceDB**: Open-source, embedded databases. Run locally within your Python process. Great for development.
*   **Pinecone / Weaviate / Milvus**: Server-based, scalable databases for production.

## 4. Challenges

*   **Curse of Dimensionality**: As dimensions increase (e.g., 1536 for OpenAI, 4096 for Llama), distance metrics become less meaningful.
*   **Filtering**: "Find documents about 'Cats' (semantic) that were published yesterday (metadata)." Combining vector search with SQL-like filtering is complex (Pre-filtering vs. Post-filtering).
