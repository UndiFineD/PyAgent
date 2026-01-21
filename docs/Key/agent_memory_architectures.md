# Agent Memory Architectures

One of the primary limitations of standard Large Language Models (LLMs) is that they are stateless; they reset after every interaction. To build truly autonomous and useful agents, we must implement **Memory Architectures** that allow them to retain information over time, learn from past experiences, and maintain context across long sessions.

## Types of Memory

Inspired by human cognitive psychology, agent memory is often categorized into:

### 1. Short-Term Memory (Working Memory)
This is the information currently available in the model's **Context Window**.
*   **Mechanism**: The prompt history (chat logs) passed to the model in the API call.
*   **Limitation**: Finite size (e.g., 8k, 128k tokens). As conversation grows, older information falls off (FIFO) or must be summarized.

### 2. Long-Term Memory
Storage of information that persists beyond the current session and exceeds the context window limit.
*   **Episodic Memory**: Recalling specific past events or interactions. "What did the user tell me to do last Tuesday?"
*   **Semantic Memory**: General knowledge about the world or the user's domain. "The user prefers Python over Java."
*   **Procedural Memory**: Knowing *how* to do things. Stored sequences of actions or tool usage patterns that were successful in the past.

## Implementation Strategies

### Vector Databases (RAG for Memory)
The most common way to implement long-term memory.
1.  **Storage**: Every interaction or fact is embedded into a vector and stored in a database (e.g., Pinecone, Chroma).
2.  **Retrieval**: When a new query comes in, the system searches the database for the most *semantically similar* past memories.
3.  **Injection**: These retrieved memories are inserted into the context window before the model generates a response.

### Memory Stream (Generative Agents)
Proposed in the "Generative Agents" paper (Park et al., 2023).
*   **Observation**: The agent records everything it sees in a raw stream.
*   **Reflection**: Periodically, the agent pauses to analyze the stream and synthesize higher-level thoughts or insights.
*   **Planning**: The agent uses these insights to plan future actions.

### Entity-Based Memory
Instead of storing raw text chunks, the agent maintains a structured profile for specific entities (Users, Projects, Companies).
*   **Structure**: A JSON object or Knowledge Graph that is updated.
    *   `User: { "name": "Alice", "role": "Admin", "preferences": ["dark mode", "concise answers"] }`
*   **Update Mechanism**: An extraction step runs after every turn to see if any new attributes should be updated in the profile.

## Challenges

*   **Retrieval Accuracy**: Finding the *right* memory is hard. Simple similarity search might return irrelevant facts.
*   **Memory Consolidation**: How to merge conflicting information? (e.g., User liked Blue yesterday, but likes Red today).
*   **Forgetting**: Infinite memory is not always good. Old, irrelevant data acts as noise. Agents need a mechanism to "forget" or decay the importance of old memories.
