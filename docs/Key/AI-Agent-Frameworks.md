# AI Agent Frameworks

While "Agents" are a concept (LLMs using tools), **Agent Frameworks** provide the scaffolding to build, orchestrate, and deploy them reliably.

## 1. The Landscape

### AutoGen (Microsoft)
- **Philosophy**: Multi-Agent Conversation.
- **Core Concept**: Agents are "conversable" entities that send messages to each other.
- **Key Feature**: **Group Chat Manager**. You can define a "User Proxy", a "Coder", and a "Reviewer", and AutoGen manages the turn-taking and message passing between them to solve a task.
- **Best For**: Code generation, complex problem solving requiring multiple perspectives.

### CrewAI
- **Philosophy**: Role-Playing Teams.
- **Core Concept**: Structured teams with specific "Roles", "Goals", and "Backstories".
- **Key Feature**: **Process Management**. You can define tasks as "Sequential" (waterfall) or "Hierarchical" (manager delegates to workers).
- **Best For**: Business process automation, content creation pipelines.

### LangGraph (LangChain)
- **Philosophy**: State Machines (Cyclic Graphs).
- **Core Concept**: Unlike standard LangChain (DAGs), LangGraph allows **cycles** (loops), which are essential for agents (Plan -> Act -> Observe -> Refine Plan).
- **Key Feature**: **State**. The graph maintains a global state object that is passed between nodes (agents/tools), allowing for complex, long-running workflows with persistence.
- **Best For**: Production-grade agents requiring fine-grained control over control flow and state.

## 2. Key Patterns Supported

### ReAct (Reason + Act)
The fundamental loop:
1.  **Thought**: LLM reasons about what to do.
2.  **Action**: LLM selects a tool.
3.  **Observation**: Tool output is fed back to LLM.
4.  **Repeat**.

### Plan-and-Solve
1.  **Planner**: One agent breaks the user request into a step-by-step plan.
2.  **Executor**: Another agent executes the steps one by one.

### Reflection / Critique
1.  **Worker**: Generates an output (e.g., writes code).
2.  **Critic**: Reviews the output and provides feedback (e.g., "This code has a bug").
3.  **Worker**: Revises based on feedback.

## 3. Comparison

| Framework | Abstraction Level | Control Flow | Best Use Case |
| :--- | :--- | :--- | :--- |
| **AutoGen** | High (Conversational) | Automatic (Conversation) | Multi-agent collaboration |
| **CrewAI** | High (Role-based) | Structured (Process) | Defined business workflows |
| **LangGraph** | Low (Graph/State) | Explicit (Edges/Conditions) | Custom, complex agent logic |
