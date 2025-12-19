# Ring Attention

Ring Attention is the architectural breakthrough that enables **Infinite Context Windows** (e.g., Gemini 1.5's 1M+ tokens). It solves the memory bottleneck of standard Self-Attention.

## 1. The Bottleneck: Quadratic Memory

Standard Self-Attention requires calculating a score between every query and every key.
- For a sequence of length $N$, you need an $N \times N$ attention matrix.
- If $N=1,000,000$, the matrix has $10^{12}$ entries. This cannot fit in the memory (HBM) of any single GPU.

## 2. The Solution: Distributed Ring

Ring Attention distributes the sequence across multiple GPUs (devices) in a ring topology.

### Mechanism
1.  **Partitioning**: The long sequence is split into blocks. GPU 1 gets Block A, GPU 2 gets Block B, etc.
2.  **Local Attention**: Each GPU calculates attention for its own block (Query A vs. Key A).
3.  **Pass the Keys**: This is the magic step.
    - GPU 1 sends Key A to GPU 2.
    - GPU 2 sends Key B to GPU 3.
    - ...
    - GPU N sends Key N to GPU 1.
4.  **Compute & Accumulate**: GPU 1 now has Key N. It computes attention (Query A vs. Key N) and adds it to the running total.
5.  **Repeat**: Continue passing keys around the ring until every Query has seen every Key.

## 3. Why it Works

- **Zero Memory Overhead**: You never materialize the full $N \times N$ matrix. You only store the small blocks.
- **Communication Overlap**: The computation (matrix multiplication) takes a long time. While the GPU is computing, the network link is busy sending the next block of keys. This **overlap** means the communication cost is effectively zero.

## 4. Impact

- **Near-Infinite Context**: The context length is limited only by the number of GPUs you have.
- **Full Accuracy**: It is an *exact* calculation of attention, not an approximation (like Sparse Attention).

## Summary

Ring Attention turns the "Memory Wall" problem into a "Distributed Systems" problem, allowing us to process entire books, codebases, or movies in a single prompt.
