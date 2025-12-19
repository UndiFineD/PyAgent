# Model Routing (LLM Cascades)

As the number of available LLMs grows (GPT-4, Claude 3, Llama 3, Mistral), a new architectural pattern has emerged: **Model Routing**. Instead of sending every query to the most expensive model (GPT-4), a "Router" dynamically selects the best model for the specific prompt.

## 1. The Motivation: Cost vs. Quality

- **The Problem**: Using GPT-4 for everything is expensive and slow. Using Llama-3-8B for everything is cheap but fails on complex reasoning.
- **The Solution**: Use Llama-3 for simple queries ("What is the capital of France?") and GPT-4 for complex ones ("Write a Python script to parse this complex PDF").

## 2. Router Architectures

### The Classifier Router
A small, fast model (e.g., BERT or a logistic regression) is trained to classify prompts into "Easy", "Medium", or "Hard".
- **Input**: User Prompt.
- **Output**: Model ID (e.g., `gpt-3.5-turbo` or `gpt-4`).

### The Embedding Router
1.  Embed the user prompt.
2.  Compare it to a database of "reference prompts" with known difficulty.
3.  Route based on the nearest neighbor.

### The Cascade (FrugalGPT)
Try models in sequence, from cheapest to most expensive.
1.  **Step 1**: Send prompt to Llama-3-8B.
2.  **Step 2**: A "Scorer" evaluates the answer. Is it good enough?
3.  **Step 3**: If yes, return it. If no, send the prompt to GPT-4.

## 3. Commercial Implementations

- **Martian**: A "Model Router" API that claims to route to the best model for every query.
- **Unify**: A platform that benchmarks all models and provides a unified API endpoint that routes based on user constraints (e.g., "Max latency 0.5s" or "Max cost $0.01").
- **RouteLLM**: An open-source framework for training routers.

## 4. Benefits

- **Cost Reduction**: Often saves 50-70% on API bills by offloading easy tasks to cheap models.
- **Latency Reduction**: Small models are faster. Routing easy queries to them improves average response time.
- **Reliability**: If one provider (e.g., OpenAI) goes down, the router can failover to another (e.g., Anthropic).

## Summary

Model Routing treats "Intelligence" as a utility grid. You don't care *which* power plant generated your electricity, and you shouldn't care *which* model answers your question, as long as it's correct and cheap.
