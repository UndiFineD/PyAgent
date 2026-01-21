# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is a technique that enhances the accuracy and reliability of Large Language Models (LLMs) by fetching relevant data from external sources before generating a response. It bridges the gap between the model's frozen training data and dynamic, real-world information.

## 1. The Problem with Standard LLMs

Standard LLMs (like GPT-4 out of the box) have two major limitations:
1.  **Knowledge Cutoff**: They only know what they were trained on. If trained in 2023, they don't know about events in 2024.
2.  **Hallucinations**: When they don't know an answer, they may confidently invent one. They lack access to private or proprietary data (e.g., your company's internal emails).

## 2. How RAG Works: The Pipeline

RAG introduces an intermediate step between the user's question and the LLM's answer.

### Step 1: Retrieval (The "Open Book" Exam)

Instead of asking the LLM to answer from memory, the system first searches a trusted knowledge base.
*   **Input**: "What is our company's vacation policy?"
*   **Search**: The system queries a database (often a Vector Database) to find documents related to "vacation policy".
*   **Result**: It retrieves specific paragraphs from the Employee Handbook.

### Step 2: Augmentation (Context Injection)

The system combines the user's question with the retrieved data into a single prompt.
*   **Prompt**:
    > "You are a helpful HR assistant. Answer the user's question using ONLY the context provided below.
    >
    > **Context**: 'Employees are entitled to 20 days of PTO per year...'
    >
    > **Question**: 'What is our company's vacation policy?'"

### Step 3: Generation

The LLM receives this augmented prompt. Since the answer is right there in the context, the model doesn't need to rely on its training memory. It simply summarizes or formats the information provided.

## 3. Key Components

### A. Embeddings Model

To find relevant documents, text is converted into **Vectors** (lists of numbers) using an Embedding Model (e.g., OpenAI `text-embedding-3`, HuggingFace `all-MiniLM`).
*   "Dog" and "Puppy" will have vectors that are mathematically close.
*   "Dog" and "Car" will be far apart.

### B. Vector Database

A specialized database (like Pinecone, Milvus, Weaviate, or Chroma) stores these vectors. It allows for **Semantic Search**: finding documents that match the *meaning* of the query, not just keywords.

### C. The LLM

The generator (e.g., GPT-4, Llama 3) acts as the reasoning engine. It reads the retrieved context and formulates a coherent answer.

## 4. Evolution of RAG

### Naive RAG

The basic "Retrieve-Read-Generate" loop described above.

### Advanced RAG

*   **Hybrid Search**: Combining Vector Search (semantic) with Keyword Search (BM25) for better precision.
*   **Re-ranking**: Retrieving 50 documents, then using a specialized "Re-ranker" model to sort them and keep only the top 5 most relevant ones before sending to the LLM.
*   **Query Transformation**: Rewriting the user's vague question into a better search query (e.g., turning "How do I fix it?" into "Troubleshooting steps for Error 503").

### Agentic RAG

Instead of a linear pipeline, an AI Agent decides *when* to retrieve information, *what* to search for, and can perform multiple searches to answer complex multi-step questions.

## 5. Summary

RAG is currently the industry standard for building enterprise AI applications. It solves the "hallucination" problem by grounding the AI in facts, and solves the "freshness" problem by allowing the AI to access up-to-the-minute data without retraining.
