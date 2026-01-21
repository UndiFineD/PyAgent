# Mixture of Depths (MoD)

Mixture of Depths is an efficiency technique (proposed by Google DeepMind) that dynamically allocates compute resources to different tokens in a sequence.

## 1. The Problem: Uniform Compute

In a standard Transformer, every token (e.g., "the", "quantum", ".") goes through every single layer.
- **Inefficiency**: The word "the" is easy to process; it doesn't need 32 layers of deep reasoning. The word "quantum" might need all 32 layers.
- **Waste**: We waste massive amounts of FLOPs processing simple tokens.

## 2. The Solution: Dynamic Routing

MoD allows the model to decide, at each layer, which tokens to process and which to skip.

### Mechanism
1.  **Router**: A small network predicts a scalar "importance score" for each token.
2.  **Top-k Selection**: Only the top $k$ tokens (e.g., top 12.5%) are selected to participate in the Self-Attention and MLP blocks of that layer.
3.  **The Rest**: The remaining tokens simply copy their state from the previous layer (Residual Connection) and skip the computation.

## 3. IsoFLOP Analysis

MoD is designed to be "IsoFLOP optimal."
- If you have a fixed compute budget (FLOPs), you can either:
    - Train a small model where every token sees every layer.
    - Train a **larger** model (more parameters) but only process a fraction of tokens per layer.
- MoD shows that the second approach yields better performance for the same inference cost.

## 4. Comparison with Mixture of Experts (MoE)

| Feature | Mixture of Experts (MoE) | Mixture of Depths (MoD) |
| :--- | :--- | :--- |
| **What is Dynamic?** | *Which* parameters are used. | *Whether* parameters are used. |
| **Routing** | Token goes to Expert A or Expert B. | Token goes to Layer or Skips Layer. |
| **Goal** | Increase model capacity (parameters). | Decrease compute cost (FLOPs). |

## Summary

Mixture of Depths moves us away from "static compute" graphs to "dynamic compute" graphs, where the model spends its "thinking time" only on the parts of the input that actually require it.
