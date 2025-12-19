# Agentic Workflows

An **AI Agent** is an LLM that can *act* on the world, not just talk about it. It uses tools, plans, and memory to achieve goals.

## 1. The Core Loop: ReAct

**ReAct (Reasoning + Acting)** is the fundamental pattern for agents.
1.  **Thought**: The model analyzes the user request. "The user wants the weather in Tokyo."
2.  **Action**: The model decides to call a tool. `get_weather("Tokyo")`.
3.  **Observation**: The tool returns the result. "15°C, Cloudy."
4.  **Thought**: "I have the answer."
5.  **Response**: "It is currently 15°C and cloudy in Tokyo."

## 2. Tool Use (Function Calling)

Modern models (GPT-4, Llama-3) are fine-tuned to output structured data (JSON) representing function calls.
*   The developer defines a schema: `{"name": "get_weather", "parameters": {"city": "string"}}`.
*   The model outputs: `{"name": "get_weather", "parameters": {"city": "Tokyo"}}`.
*   The code executes the function and feeds the result back to the model.

## 3. Planning Patterns

*   **Plan-and-Solve**: The agent generates a full checklist of steps *before* executing the first one. Good for complex tasks.
*   **Reflection / Self-Correction**: The agent checks its own output. "Did the code I wrote actually run? No, it failed. I need to fix the syntax error."
*   **Multi-Agent Systems**: Different agents with different personas (e.g., "Coder", "Reviewer", "Manager") collaborate.

## 4. Memory

*   **Short-term Memory**: The context window (limited size).
*   **Long-term Memory**: Vector Databases (RAG). The agent stores past experiences/documents and retrieves them when relevant.

## 5. Challenges

*   **Infinite Loops**: Agents can get stuck repeating the same failed action.
*   **Hallucinated Tool Calls**: Calling functions that don't exist or with wrong arguments.
*   **Cost & Latency**: Agent loops can require dozens of LLM calls for a single user request.
