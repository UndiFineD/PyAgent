# Cognitive Architectures

**Cognitive Architectures** are blueprints for intelligent agents. They attempt to model the fixed structures and processes of the mind that remain constant across different domains and tasks. While modern AI is dominated by Deep Learning, the field of Cognitive Architectures (which dates back decades) provides the structural inspiration for today's autonomous agents.

## Classical Architectures

### 1. Soar (State, Operator, And Result)
Developed by John Laird, Allen Newell, and Paul Rosenbloom (1983).
*   **Core Concept**: Problem solving is a search through a problem space.
*   **Mechanism**: It uses a production system (If-Then rules) to select operators that move the state forward. If it gets stuck (impasse), it uses sub-goaling and learning (chunking) to resolve it.
*   **Relevance today**: The idea of "sub-goaling" is central to modern Chain-of-Thought prompting.

### 2. ACT-R (Adaptive Control of Thought-Rational)
Developed by John Anderson (CMU).
*   **Core Concept**: Models human cognition as a set of modules (Visual, Motor, Goal, Declarative Memory) communicating through a central production system.
*   **Mechanism**: It distinguishes strictly between **Declarative Knowledge** (facts, "knowing that") and **Procedural Knowledge** (rules, "knowing how").
*   **Relevance today**: Modern agents often separate "Knowledge Bases" (RAG) from "Tools/Skills" (Functions), mirroring this distinction.

## Modern LLM-based Architectures

We are seeing a convergence where LLMs serve as the "Reasoning Engine" or "CPU" within a larger cognitive architecture.

### 1. Coala (Cognitive Architectures for Language Agents)
A framework that maps LLM agent components to classical cognitive modules:
*   **Memory**: Long-term storage (Vector DB).
*   **Action Space**: Tools and APIs.
*   **Decision Making**: The LLM itself.

### 2. BabyAGI / AutoGPT
Early experimental architectures focused on autonomous loops:
*   **Loop**: Task Creation -> Task Prioritization -> Execution -> Result Storage.
*   **Goal**: To execute a high-level objective by recursively breaking it down without human intervention.

### 3. The "System 1" vs. "System 2" Paradigm
Inspired by Daniel Kahneman's *Thinking, Fast and Slow*.
*   **System 1 (Fast)**: The raw LLM output. Intuitive, fast, but prone to hallucination.
*   **System 2 (Slow)**: An architectural layer that forces the model to "think", verify, plan, and critique its own output before showing it to the user (e.g., Tree of Thoughts, Reflextion).

## Why This Matters
Deep Learning gave us powerful *components* (the LLM), but Cognitive Architectures give us the *system design* needed to turn that component into a reliable, autonomous agent that can work over long periods.
