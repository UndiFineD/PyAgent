# Semantic Code Search

## Overview
**Semantic Code Search** allows developers to search codebases using natural language queries describing *intent* or *functionality*, rather than just matching exact keywords or variable names (like `grep` or `Ctrl+F`).

## How It Works
1.  **Embedding**: Code snippets (functions, classes) are converted into high-dimensional vectors using code-specific embedding models (e.g., OpenAI `text-embedding-3-small`, `jina-embeddings-v2-base-code`).
2.  **Indexing**: These vectors are stored in a Vector Database (Pinecone, Milvus, Weaviate).
3.  **Querying**: The user's natural language query ("Find the authentication logic") is embedded into the same vector space.
4.  **Retrieval**: The system finds code snippets with vectors closest to the query vector (Cosine Similarity).

## Comparison
| Feature | Keyword Search (Grep/Regex) | Semantic Search |
| :--- | :--- | :--- |
| **Query** | Exact strings (`def login`) | Concepts ("How do users log in?") |
| **Understanding** | None (Literal match) | Contextual (Synonyms, Logic) |
| **False Positives** | High (Matches comments, strings) | Low (Matches intent) |
| **Language Agnostic** | No (Must know syntax) | Yes (Can describe logic in English) |

## Advanced Techniques
*   **Hybrid Search**: Combining keyword search (BM25) with semantic search to get the best of both worlds (exact matches + conceptual matches).
*   **Code-Aware Embedding**: Models trained specifically to understand code structure (AST) and data flow, not just text.
*   **Reranking**: Using a cross-encoder model to re-score the top results for higher accuracy.

## Use Cases
*   **Discovery**: "Is there already a function to validate email addresses?"
*   **Impact Analysis**: "Find all code that handles credit card processing."
*   **Cross-Language Search**: Searching for "QuickSort implementation" and finding it in Python, Java, and C++.

## Tools
*   **Sourcegraph Cody**: Enterprise code search and intelligence.
*   **GitHub Copilot Chat**: Search within the IDE context.
*   **Bloop**: Natural language search for local repositories.
