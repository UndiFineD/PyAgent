# GraphRAG

Standard RAG treats documents as flat text chunks. It struggles with queries that require "connecting the dots" across many documents (e.g., "How does the relationship between Sam and Isabella evolve across the entire dataset?"). GraphRAG uses Knowledge Graphs to solve this.

## The Pipeline (Microsoft Research)

### 1. Indexing (Graph Construction)
*   **Extraction**: An LLM reads the raw text and extracts **Entities** (People, Places, Organizations) and **Relationships** (Works For, Located In, Friends With).
*   **Summarization**: The LLM generates summaries for each entity and relationship.
*   **Community Detection**: Algorithms like Leiden are used to cluster entities into hierarchical communities (e.g., "The Engineering Team", "The Company", "The Industry"). Summaries are generated for each community.

### 2. Retrieval (Global Search)
For broad queries ("What are the main themes in the data?"):
*   The system doesn't search for specific chunks.
*   It retrieves the pre-computed summaries of the high-level communities.
*   This allows the LLM to answer "global" questions that require reading the entire dataset.

### 3. Retrieval (Local Search)
For specific queries ("Who is Sam?"):
*   The system identifies the entity "Sam" in the graph.
*   It retrieves Sam's description, his direct relationships, and the community he belongs to.
*   It also retrieves the raw text chunks linked to these graph nodes (Hybrid RAG).

## Benefits
*   **Holistic Understanding**: Can answer "summary" questions that vector search fails at.
*   **Hallucination Reduction**: The graph provides a structured "fact-check" layer.
*   **Explainability**: You can trace the answer back to specific nodes and edges.
