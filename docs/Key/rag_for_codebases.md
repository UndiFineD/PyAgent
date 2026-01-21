# Retrieval-Augmented Generation (RAG) for Codebases

## Overview
**RAG for Codebases** involves specialized techniques to index, retrieve, and generate code by grounding Large Language Models (LLMs) in the specific context of a software repository. Unlike standard text RAG, code RAG must understand syntax, structure, and dependencies.

## Challenges of Code RAG
*   **Non-Linearity**: Code execution jumps around (function calls, imports). Reading a file from top to bottom doesn't capture the full logic.
*   **Context Window Limits**: Large repositories cannot fit entirely into an LLM's context window.
*   **Stale Documentation**: Comments and docs may not match the actual code implementation.

## Key Techniques

### 1. Abstract Syntax Tree (AST) Parsing
Instead of chunking code by lines or paragraphs, use ASTs to chunk by logical units:
*   **Functions/Methods**: Treat each function as a chunk.
*   **Classes**: Group methods within a class.
*   **Imports**: Identify dependencies explicitly.

### 2. Dependency Graph Indexing
*   **Call Graphs**: Map which functions call which other functions.
*   **Import Graphs**: Map file-to-file dependencies.
*   **Usage**: When retrieving a function, also retrieve its callees and callers to provide full context.

### 3. GraphRAG for Code
Combining Knowledge Graphs with Vector Search:
*   **Nodes**: Functions, Classes, Files, Variables.
*   **Edges**: "Calls", "Imports", "Inherits From", "Instantiates".
*   **Query**: "How is the `User` class authenticated?" -> Traverses the graph to find the `AuthService` and `LoginController`.

### 4. Repository Map
Creating a compressed representation of the entire repo structure (file tree + key signatures) to fit in the system prompt, giving the LLM a "map" of where to look.

## Tools & Libraries
*   **LlamaIndex**: Has specific splitters for code (Python, JS, etc.).
*   **LangChain**: CodeTextSplitter.
*   **Continue.dev**: Open-source IDE extension using RAG.
*   **Greptile**: API for querying codebases.
*   **Bloop**: Semantic code search engine.

## Use Cases
*   **Onboarding**: "Explain how the payment processing flow works in this repo."
*   **Bug Localization**: "Where is the `InvalidTokenError` likely originating?"
*   **Feature Implementation**: "What files do I need to touch to add a new API endpoint?"
