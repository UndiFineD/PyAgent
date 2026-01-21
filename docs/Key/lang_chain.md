# LangChain

## Overview
**LangChain** is an open-source framework designed to simplify the development of applications powered by Large Language Models (LLMs). It provides abstractions to chain together different components (Prompts, Models, Parsers) into complex workflows.

## Core Concepts

### 1. Chains
The fundamental building block. A sequence of calls to an LLM or other utilities.
*   **LLMChain**: Prompt Template + LLM.
*   **SequentialChain**: Output of one chain becomes the input of the next.
*   **RouterChain**: Dynamically selects which chain to use based on the input.

### 2. Agents
Agents use an LLM as a reasoning engine to determine which actions to take and in what order.
*   **Tools**: Functions the agent can call (Google Search, Calculator, Python REPL).
*   **ReAct**: The standard prompting strategy (Reason + Act) used by agents.

### 3. Memory
LLMs are stateless. LangChain provides memory components to persist state between calls.
*   **ConversationBufferMemory**: Stores the full history.
*   **ConversationSummaryMemory**: Uses an LLM to summarize the history as it grows.

### 4. Retrieval (RAG)
Components for connecting LLMs to private data.
*   **Document Loaders**: Read PDFs, HTML, CSVs.
*   **Text Splitters**: Chunk text into manageable pieces.
*   **Vector Stores**: Integrations with Pinecone, Chroma, Faiss.
*   **Retrievers**: Algorithms to fetch relevant chunks.

### 5. LangSmith
A platform for debugging, testing, and monitoring LangChain applications. Essential for tracing complex agent loops.

## LangChain Expression Language (LCEL)
A declarative way to compose chains using the pipe `|` operator.
```python
chain = prompt | model | output_parser
```

## Alternatives
*   **LlamaIndex**: More focused on data indexing and retrieval (RAG).
*   **Haystack**: End-to-end NLP framework.
*   **AutoGen**: Multi-agent framework by Microsoft.
