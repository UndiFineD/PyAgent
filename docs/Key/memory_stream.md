# Memory Stream

The "Memory Stream" is the core architectural component introduced in the famous paper **"Generative Agents: Interactive Simulacra of Human Behavior"** (Park et al., 2023). It allows agents to maintain a coherent identity and long-term memory over extended periods.

## The Structure

The memory stream is a comprehensive list of *everything* the agent has perceived or done, stored as natural language objects.
*   *Example*: "Isabella saw Sam enter the store.", "Isabella is hungry.", "Isabella bought milk."

## Retrieval Function

Since the stream is too long to fit in the context window, the agent must retrieve only the most relevant memories when making a decision. The retrieval score is a weighted sum of three components:

### 1. Recency
*   **Concept**: Recent events are more likely to be relevant than distant ones.
*   **Implementation**: Exponential decay function based on the time since the memory was last accessed.

### 2. Importance
*   **Concept**: Some memories are trivial ("I ate breakfast"), others are core ("I broke up with my boyfriend").
*   **Implementation**: The LLM itself is asked to score the "poignancy" of a memory on a scale of 1-10.

### 3. Relevance
*   **Concept**: Memories related to the current situation are needed.
*   **Implementation**: Cosine similarity between the embedding of the current query (context) and the embedding of the memory.

$$ Score = \alpha \cdot Recency + \beta \cdot Importance + \gamma \cdot Relevance $$

## Reflection

To prevent the agent from just reacting to raw observations, the architecture includes a **Reflection** step.
1.  **Periodically**, the agent looks at recent memories.
2.  **Synthesizes** high-level thoughts or insights.
    *   *Raw*: "Sam is buying flowers", "Sam is checking his watch", "Sam looks nervous".
    *   *Reflection*: "Sam is likely going on a date."
3.  **Storage**: These reflections are stored back into the memory stream as new memories, allowing the agent to retrieve them later.

## Planning

The agent creates high-level plans (e.g., "Write a book") and recursively breaks them down into hourly schedules. These plans are also stored in the memory stream and can be modified if new events occur.
