# Llama (Large Language Model Meta AI)

## Overview
**Llama** is a family of open-weights Large Language Models released by Meta.
*   **Llama 1 (Feb 2023)**: Proved that smaller, better-trained models could outperform larger ones (Chinchilla Scaling Laws).
*   **Llama 2 (July 2023)**: Released with a commercially permissive license and RLHF fine-tuning (Llama-2-Chat).
*   **Llama 3 (April 2024)**: State-of-the-art performance for open models, rivaling GPT-4 in some benchmarks.

## Architectural Improvements
Llama is based on the standard Transformer architecture but includes several modern tweaks:
1.  **RMSNorm (Root Mean Square Normalization)**: Used instead of LayerNorm for better stability.
2.  **SwiGLU Activation**: A variant of GLU (Gated Linear Unit) that improves performance.
3.  **RoPE (Rotary Positional Embeddings)**: A relative position encoding scheme that generalizes better to longer sequence lengths than absolute embeddings.
4.  **GQA (Grouped-Query Attention)**: Used in larger Llama models to speed up inference and reduce memory usage (KV cache) compared to standard Multi-Head Attention.

## The "Llama Moment"
The release of Llama 1's weights (initially leaked, then embraced) triggered the "Cambrian Explosion" of open-source AI.
*   It enabled the community to run LLMs locally (llama.cpp).
*   It allowed for fine-tuning on consumer hardware (Alpaca, Vicuna).
*   It shifted the power dynamic from closed APIs (OpenAI, Anthropic) to open ecosystems.
