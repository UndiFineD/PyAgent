# Retrieval-Enhanced Transformer (RETRO)

Standard Large Language Models (LLMs) store all their knowledge in their weights (parametric memory). This is inefficient:
1. **Hallucination**: If the model forgets a fact, it makes one up.
2. **Staleness**: To update knowledge, you must retrain the model.
3. **Size**: You need massive parameters to memorize the internet.

RETRO (DeepMind) decouples **compute** from **memory** by retrieving text chunks from a massive external database during generation.

## 1. The Architecture

RETRO is an encoder-decoder (or decoder-only) architecture that is augmented with a retrieval mechanism.

### The Database
- The training corpus (e.g., 2 Trillion tokens) is split into chunks (e.g., 64 tokens).
- These chunks are embedded using a frozen BERT model and stored in a Key-Value index (FAISS).

### Retrieval
- During generation, the input is also split into chunks.
- For each input chunk, the model retrieves the top-k most similar chunks from the database (Nearest Neighbor Search).

## 2. Chunked Cross-Attention

How do we fuse the retrieved text with the current context?
RETRO introduces a **Chunked Cross-Attention** layer:
1. The retrieved chunks are encoded.
2. The current generation stream attends to these retrieved encodings via Cross-Attention.
3. This happens every few layers (e.g., every 9th layer), keeping inference cost low.

## 3. Benefits

- **Smaller Models, Better Performance**: A 7B parameter RETRO model can outperform a 175B parameter GPT-3 model on perplexity tasks because it can "look up" the answers.
- **Updatability**: You can update the database (add new documents) without retraining the model.
- **Interpretability**: You can see exactly which source document the model used to generate an answer.

## 4. RAG vs. RETRO

- **RAG (Retrieval-Augmented Generation)**: Usually refers to a prompt-engineering technique where retrieved text is stuffed into the context window.
- **RETRO**: Is an *architecture* modification. The retrieval is integrated into the middle of the network layers, not just the input.

## Summary

RETRO represents the future of "Semi-Parametric" models, where the neural net focuses on reasoning and syntax, while the external database handles factual knowledge storage.
