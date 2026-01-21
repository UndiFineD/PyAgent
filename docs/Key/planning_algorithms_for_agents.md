# Planning Algorithms for Agents

Standard LLM generation is linear: it produces token after token from left to right. However, complex problems often require non-linear thinking, backtracking, and exploring multiple possibilities. Planning algorithms structure the LLM's reasoning process.

## 1. Chain of Thought (CoT)
The baseline for planning.
*   **Method**: Prompting the model to "Think step by step".
*   **Limitation**: It's a single linear path. If one step is wrong, the whole solution fails.

## 2. Tree of Thoughts (ToT)
Generalizes CoT by exploring multiple reasoning paths simultaneously.
*   **Structure**: A tree where each node is a partial solution or a "thought".
*   **Process**:
    1.  **Decomposition**: Break the problem into steps.
    2.  **Generation**: Generate multiple candidates for the next step.
    3.  **Evaluation**: Critique each candidate (Vote/Score).
    4.  **Search**: Use BFS (Breadth-First Search) or DFS (Depth-First Search) to navigate the tree.
*   **Use Case**: Creative writing, Crosswords, Game of 24.

## 3. Graph of Thoughts (GoT)
Generalizes ToT by allowing thoughts to be combined (aggregated).
*   **Structure**: A Directed Acyclic Graph (DAG).
*   **Innovation**: Information can flow from multiple previous thoughts into a new one.
*   **Operations**:
    *   **Generate**: Create a new thought.
    *   **Aggregate**: Combine multiple thoughts into a summary or a better solution.
    *   **Refine**: Improve a single thought.
*   **Use Case**: Sorting, Keyword counting, Document merging.

## 4. Algorithm of Thoughts (AoT)
Attempting to teach the LLM to run the search algorithm *inside* its context window, rather than using an external Python script to manage the tree.
*   **Method**: Few-shot prompting with examples of the search process (e.g., "I tried path A, it failed. Now backtracking to B...").

## 5. Classical Search Integration
Using LLMs as the heuristic function for classical search algorithms.
*   **LLM + A* Search**: The LLM estimates the "cost to goal" (heuristic) for each state, guiding the A* algorithm to the solution efficiently.
*   **LLM + MCTS (Monte Carlo Tree Search)**: Used in AlphaGo, now applied to reasoning. The LLM simulates "rollouts" to see if a partial solution leads to a correct answer.
