# KVzap: Fast, Adaptive, and Faithful KV Cache Pruning
**arXiv ID**: 2601.07891
**Date**: January 12, 2026
**Authors**: Simon Jégou, Maximilian Jeblick (NVIDIA)

## Summary
KVzap is a high-performance KV cache pruning method that achieves 2–4x compression with negligible accuracy loss. It approximates the expensive KVzip+ scoring policy (which involves multiple prefill passes) using a lightweight surrogate model (Linear or MLP) trained on the model's hidden states.

## Key Innovations
1.  **Surrogate Model Pruning**: Instead of re-calculating attention scores, KVzap uses a simple 1 or 2-layer MLP to predict the "importance" of a KV pair directly from the hidden state at that position.
2.  **KVzip+ Scoring**: An improved scoring mechanism that normalizes attention weights by the ratio of the output value norm to the residual stream norm, better reflecting the actual contribution to the next token.
3.  **Threshold-based Adaptive Pruning**: Unlike top-k methods that keep a fixed budget, KVzap uses a threshold $\tau$. This allows the model to retain more tokens for dense/complex prompts and prune heavily for redundant ones.
4.  **Phase-Agnostic**: Works for both prefilling and decoding.
5.  **Sliding Window Persistence**: Always retains the most recent $w=128$ tokens to preserve local context sensitivity.

## Performance
-   **2-4x compression** on Qwen3 (8B/32B) and Llama-3.1-8B.
-   **Negligible overhead**: $<1.1\%$ FLOPs for MLP, $<0.02\%$ for Linear.
-   **State-of-the-Art**: Ranks #1 on KVpress Leaderboard as of Jan 2026.

## Implementation Details for PyAgent
-   **Integration Point**: `src/infrastructure/engine/kv_cache/ARCOffloadManager.py` or a new `KVPruningEngine.py`.
-   **Mechanism**:
    -   Intercept hidden states before/after the attention layer.
    -   Pass hidden states through the KVzap surrogate model (pre-trained linear/MLP weights).
    -   Identify indices where `score < threshold`.
    -   Prune the KV cache tensors at those indices (excluding the sliding window).

## References
-   [arXiv:2601.07891](https://arxiv.org/abs/2601.07891)
-   [NVIDIA/kvpress](https://github.com/NVIDIA/kvpress)
