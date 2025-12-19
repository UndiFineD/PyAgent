# Observability for LLMs

Traditional software monitoring (CPU, RAM, Error Rate) is insufficient for LLM applications. You need to track *what* the model is saying, *how* it arrived at an answer, and *how much* it cost.

## Key Concepts

### 1. Tracing and Spans
*   **Trace**: The entire lifecycle of a user request (e.g., "Summarize this PDF").
*   **Span**: A single unit of work within a trace.
    *   *Span 1*: Retrieve documents from Vector DB.
    *   *Span 2*: Rerank documents.
    *   *Span 3*: Call LLM with context.
    *   *Span 4*: Parse JSON output.
*   **Why**: If a request fails or is slow, you can pinpoint exactly which step is the bottleneck.

### 2. Evaluation in Production
*   **User Feedback**: Thumbs up/down buttons.
*   **Model-Based Eval**: Running a "Judge" model on a sample of production logs to check for hallucinations or toxicity.
*   **Embedding Drift**: Checking if the user queries today are semantically different from the queries the system was designed for.

### 3. Cost and Latency Tracking
*   **Token Counting**: Tracking input/output tokens per user, per model, and per feature.
*   **Latency**: Measuring Time to First Token (TTFT) and total generation time.

## Tools

### LangSmith (LangChain)
*   **Features**: Visualizing traces, running datasets against chains, prompt versioning.
*   **Focus**: Developer experience and debugging.

### Arize Phoenix
*   **Features**: Embedding visualization (UMAP), drift detection, and retrieval evaluation.
*   **Focus**: ML Engineering and production monitoring.

### Weights & Biases (W&B) Prompts
*   **Features**: Tracking experiments, prompt engineering playground, and version control for prompts.
