# Multi-GPU Optimization & Distributed Training

Training modern Large Language Models (LLMs) is impossible on a single device. It requires distributing the workload across dozens, hundreds, or thousands of GPUs. This document outlines the key strategies for Multi-GPU optimization.

## 1. Data Parallelism (DDP)

**Distributed Data Parallel (DDP)** is the simplest form of scaling.
*   **Concept**: Replicate the *entire* model on every GPU.
*   **Process**:
    1.  Split the dataset into chunks (batches).
    2.  Each GPU processes a different batch of data.
    3.  Gradients are calculated locally.
    4.  **All-Reduce**: Gradients are averaged across all GPUs.
    5.  Weights are updated simultaneously.
*   **Limitation**: The model must fit entirely within the VRAM of a single GPU.

## 2. Model Parallelism

When the model is too big to fit on one GPU (e.g., a 70B parameter model requires ~140GB VRAM, but an A100 only has 80GB), we must split the model itself.

### A. Pipeline Parallelism (PP)
*   **Concept**: Split the model vertically (by layers).
*   **Setup**: GPU 1 holds Layers 1-10, GPU 2 holds Layers 11-20, etc.
*   **Flow**: Data flows from GPU 1 $\rightarrow$ GPU 2 $\rightarrow$ ...
*   **Issue**: "Bubble" inefficiency. GPU 2 sits idle waiting for GPU 1 to finish.

### B. Tensor Parallelism (TP)
*   **Concept**: Split the model horizontally (within layers).
*   **Setup**: A single large Matrix Multiplication ($W \cdot x$) is split across multiple GPUs. Each GPU computes a part of the result, and they communicate to combine them.
*   **Requirement**: Extremely fast interconnects (NVLink) because communication happens *per layer*.

## 3. Fully Sharded Data Parallel (FSDP)

**FSDP** (popularized by Meta/PyTorch) is the modern standard for training large models. It combines the best of Data Parallelism and Model Parallelism.
*   **Concept**: Instead of replicating the model (DDP), **shard** (split) the model parameters, gradients, and optimizer states across all GPUs.
*   **Process**:
    1.  When GPU 1 needs a specific layer for computation, it temporarily fetches the missing shards from other GPUs.
    2.  It computes the forward/backward pass.
    3.  It immediately discards the shards to free up memory.
*   **Result**: You can train massive models on standard clusters without complex Tensor Parallelism code.

## 4. ZeRO (Zero Redundancy Optimizer)

Developed by Microsoft (DeepSpeed), ZeRO is the algorithm behind FSDP. It defines three stages of optimization:
*   **Stage 1**: Shard Optimizer States (4x memory reduction).
*   **Stage 2**: Shard Gradients (8x memory reduction).
*   **Stage 3**: Shard Model Parameters (Linear memory reduction with N GPUs).

## 5. Summary

*   **Small Model / Single Node**: Use **DDP**.
*   **Large Model / Standard Cluster**: Use **FSDP / ZeRO-3**.
*   **Massive Model / Supercomputer**: Use **3D Parallelism** (TP + PP + DP).
