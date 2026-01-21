# Math & Reasoning

Enhancing the logical problem-solving capabilities of LLMs. Standard LLMs are good at pattern matching but struggle with multi-step arithmetic and logic.

## 1. Chain of Thought (CoT)

*   **Concept**: Prompting the model to "Think step by step" before giving the final answer.
*   **Why it works**: It allows the model to dump intermediate computation into the context window, effectively giving it "scratchpad" memory.
*   **Zero-Shot CoT**: Just adding "Let's think step by step" to the prompt.

## 2. Tree of Thoughts (ToT)

*   **Concept**: Instead of a single linear chain, the model explores multiple possible branches of reasoning.
*   **Search**: It uses algorithms like BFS (Breadth-First Search) or DFS to explore the tree, evaluating the promise of each branch.
*   **Self-Correction**: The model can backtrack if a branch leads to a dead end.

## 3. Process Supervision

*   **Outcome Supervision**: Rewarding the model only if the *final answer* is correct.
*   **Process Supervision**: Rewarding the model for *each correct step* of reasoning.
*   **Impact**: Drastically improves performance on hard math benchmarks (like GSM8K and MATH).
