# Hybrid Search

Hybrid Search is a retrieval technique that combines the strengths of **Keyword Search (Sparse)** and **Semantic Search (Dense)** to improve the relevance of search results in RAG (Retrieval-Augmented Generation) systems and search engines.

## The Components

### 1. Sparse Retrieval (Keyword Search)
Matches exact keywords between the query and the document.
*   **Algorithm**: BM25 (Best Matching 25) is the industry standard. It improves upon TF-IDF by saturating term frequency (preventing "the the the" from scoring high) and normalizing for document length.
*   **Pros**: Excellent for exact matches (names, product codes, specific technical terms), interpretable.
*   **Cons**: Fails at synonyms ("car" vs "automobile") and semantic understanding.

### 2. Dense Retrieval (Semantic Search)
Encodes queries and documents into dense vectors (embeddings) and finds the nearest neighbors.
*   **Algorithm**: Cosine Similarity or Dot Product on embeddings from models like BERT, OpenAI `text-embedding-3`, or Cohere.
*   **Pros**: Captures meaning and intent, handles synonyms and multi-lingual queries.
*   **Cons**: Can miss exact keyword matches (the "out-of-domain" problem), computationally more expensive.

## The Hybrid Approach

Hybrid search runs both retrievers in parallel and combines their results.

### Reciprocal Rank Fusion (RRF)
A standard method for merging ranked lists from different sources without needing to normalize their scores.
$$ RRFscore(d) = \sum_{r \in R} \frac{1}{k + r(d)} $$
*   Where $r(d)$ is the rank of document $d$ in one of the lists, and $k$ is a constant (usually 60).
*   **Why it works**: It penalizes documents that are ranked low in any list, but highly rewards documents that appear near the top of multiple lists.

### Weighted Scoring
Normalizing the scores (e.g., Min-Max scaling) from both retrievers and taking a weighted average.
*   `Final_Score = alpha * Dense_Score + (1 - alpha) * Sparse_Score`
*   **Challenge**: Dense scores (0.7-0.9) and BM25 scores (0-infinite) have very different distributions, making normalization tricky.

## When to Use Hybrid Search
*   **RAG Applications**: Almost always superior to dense-only search.
*   **E-commerce**: Users search for specific product IDs (Sparse) but also "comfortable running shoes" (Dense).
*   **Legal/Medical**: Requires finding exact case law or drug names (Sparse) alongside conceptual precedents (Dense).
