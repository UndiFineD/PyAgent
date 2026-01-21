# Mixture of Experts (MoE)

Scaling laws tell us that bigger models are smarter. But bigger models are also slower and more expensive to run. **Mixture of Experts (MoE)** is the architecture that solves this dilemma by decoupling **Parameter Count** (Capacity) from **Compute Cost** (Inference Latency).

## 1. The Core Concept

In a standard "Dense" Transformer, every token passes through every single neuron in the Feed-Forward Network (FFN) layers.
In an **MoE** Transformer:
*   The FFN layer is replaced by a set of $N$ distinct "Expert" networks (e.g., 8 experts).
*   A **Router** (Gating Network) decides which experts are best suited for the current token.
*   **Sparse Activation**: Only the top-k experts (usually $k=2$) are activated for any given token.

## 2. Benefits

*   **Massive Scale, Low Latency**: A model can have 47B parameters (like Mixtral 8x7B) but only use 13B parameters per token during inference. It runs as fast as a small model but knows as much as a large model.
*   **Specialization**: Theoretically, different experts can specialize in different topics (e.g., one for code, one for math, one for history), though in practice, the specialization is often more abstract.

## 3. Challenges

*   **Training Instability**: MoEs are harder to train. The router might collapse and send all tokens to just one expert (Load Balancing issue).
*   **VRAM Usage**: Even though inference is fast (FLOPs are low), the *entire* model must be loaded into VRAM. You need a lot of GPU memory, even if the compute requirement is low.

## 4. Famous MoE Models

*   **GPT-4**: Widely rumored to be a massive MoE (e.g., 8x220B).
*   **Mixtral 8x7B**: The first high-quality open-source MoE. It outperforms Llama-2 70B while being 6x faster.
*   **DeepSeek-MoE**: Introduces "Fine-Grained" experts (splitting experts into smaller pieces) for better specialization.
