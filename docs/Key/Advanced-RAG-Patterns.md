# Advanced RAG Patterns

Basic RAG (Retrieval-Augmented Generation) involves chunking text, embedding it, and retrieving the top-k chunks based on cosine similarity. While effective, it often fails on complex queries. Advanced patterns address these limitations.

## 1. HyDE (Hypothetical Document Embeddings)
*   **Problem**: User queries are short and lack keywords ("How to fix error 500?"), while documents are detailed. The semantic gap is large.
*   **Solution**:
    1.  Ask an LLM to generate a *hypothetical* answer to the query.
    2.  Embed that hypothetical answer.
    3.  Search for real documents that are similar to the hypothetical answer.
*   **Why it works**: The hypothetical answer may be factually wrong, but it will contain the right *keywords* and *structure* to match the real documents.

## 2. Sentence Window Retrieval
*   **Problem**: Embedding large chunks (500 tokens) dilutes the semantic meaning. Embedding small chunks (1 sentence) loses context.
*   **Solution**:
    1.  Embed and index individual sentences (or very small chunks).
    2.  When a sentence is retrieved, fetch the *window* of sentences around it (e.g., 3 before and 3 after) from the database.
    3.  Feed the full window to the LLM.
*   **Benefit**: High precision retrieval with full context generation.

## 3. Parent Document Retrieval (Auto-Merging)
*   **Problem**: Similar to Sentence Window.
*   **Solution**:
    1.  Split documents into "Parent" chunks (large) and "Child" chunks (small).
    2.  Embed and index the Child chunks.
    3.  When a Child chunk is retrieved, fetch its corresponding Parent chunk.
*   **Auto-Merging**: If multiple child chunks from the same parent are retrieved, replace them all with the single parent chunk to avoid redundancy.

## 4. Query Transformations
*   **Multi-Query**: Breaking a complex query into multiple sub-queries and retrieving documents for all of them.
*   **Step-Back Prompting**: Generating a more abstract, high-level question to retrieve background context, then answering the specific question.
