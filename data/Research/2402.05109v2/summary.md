# Hydra: Sequentially-Dependent Draft Heads
**arXiv ID**: 2402.05109
**Date**: February 2024
**GitHub**: [zankner/Hydra](https://github.com/zankner/Hydra)

## Summary
Hydra is a "Medusa-style" speculative decoding framework that improves draft token accuracy by introducing **sequentially-dependent** draft heads. In standard Medusa, multiple heads predict multiple future tokens in parallel ($x_{t+1}, x_{t+2}, \dots$) based solely on the current hidden state $h_t$. Hydra instead allows each head $i$ to "see" the embeddings of the tokens speculated by heads $1, \dots, i-1$.

## Key Innovations
1.  **Sequentially-Dependent Heads**: Each head $i$ takes the base hidden state $h_t$ and the embeddings of all previously speculated draft tokens as input. This significantly improves the acceptance rate compared to independent heads.
2.  **Hydra++ Architecture**:
    -   Uses **Deep Heads** (4-layer MLPs) for better representative power.
    -   Uses **Distillation** from the base model to train the heads (KL-divergence loss).
    -   **Prefix Attention**: A small shared transformer layer improves the hidden states transferred to the heads.
3.  **Static Tree Search**: Pre-calculates the optimal draft tree topology for specific hardware/workload constraints.

## Performance Benchmarks
- **Throughput**: **2.70x** speedup over autoregressive decoding.
- **Accuracy**: Increases token acceptance length by **+0.46 tokens/step** over Medusa.

## Implementation Details for PyAgent
- **Integration Point**: `src/infrastructure/speculative_v2/`
- **Key Components**:
    - `HydraDraftHeads`: MLP heads with sequential skip-links for token embeddings.
    - `HydraTrainer`: Logic to distill knowledge from a large teacher model (e.g., Llama-3-70B) into the heads.

## Mathematical Formulation
Instead of $f_i(h_t)$, Hydra computes:
$$f_{Hydra, i}(h_t, \text{embed}(\hat{x}_{t+1}), \dots, \text{embed}(\hat{x}_{t+i-1}))$$

## References
- [arXiv:2402.05109](https://arxiv.org/abs/2402.05109)
