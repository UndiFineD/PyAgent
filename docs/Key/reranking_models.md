# Reranking Models

In a standard RAG pipeline, the retrieval step uses **Bi-Encoders** (Vector Search) to find the top-k documents. However, Bi-Encoders trade accuracy for speed. Reranking adds a second stage to improve precision.

## Bi-Encoders vs. Cross-Encoders

### Bi-Encoders (Retrieval)
*   **Mechanism**: The Query and the Document are passed through the model *separately* to produce two vectors. Similarity is the dot product of these vectors.
*   **Pros**: Extremely fast. You can pre-compute document vectors and index them (FAISS, Pinecone).
*   **Cons**: The model doesn't see the interaction between the query and document words. It misses subtle nuances.

### Cross-Encoders (Reranking)
*   **Mechanism**: The Query and the Document are concatenated (`[CLS] Query [SEP] Document`) and passed through the model *together*. The output is a single score (0-1) indicating relevance.
*   **Pros**: Much higher accuracy. The self-attention mechanism can compare every word in the query to every word in the document.
*   **Cons**: Very slow. Cannot be pre-computed.

## The Two-Stage Pipeline
1.  **Retrieval**: Use a Bi-Encoder (or BM25) to fetch the top 100 candidates from millions of documents.
2.  **Reranking**: Use a Cross-Encoder to score those 100 candidates and sort them.
3.  **Selection**: Take the top 5 from the reranked list for the LLM context.

## Popular Rerankers
*   **Cohere Rerank**: A managed API that is currently the industry standard for performance.
*   **BGE-Reranker (BAAI)**: Open-source models that top the MTEB benchmarks.
*   **ColBERT**: A "late interaction" model that tries to get the best of both worlds (speed of bi-encoders, accuracy of cross-encoders) by keeping token-level embeddings.
