# GPU Programming for AI

Deep Learning's success is largely due to the massive parallelism provided by Graphics Processing Units (GPUs). While frameworks like PyTorch abstract away the details, understanding the lower levels is crucial for optimization.

## CUDA (Compute Unified Device Architecture)
NVIDIA's parallel computing platform and programming model.
*   **Kernels**: Functions that run on the GPU. You write a kernel in C/C++ and launch it with thousands of threads.
*   **Thread Hierarchy**:
    *   **Grid**: The collection of all threads launched for a kernel.
    *   **Block**: A group of threads that can share memory (Shared Memory) and synchronize.
    *   **Thread**: The smallest unit of execution.
*   **Memory Hierarchy**:
    *   **Global Memory**: Large but slow (HBM/GDDR). Accessible by all threads.
    *   **Shared Memory**: Small but extremely fast (L1 cache speed). User-managed cache shared by threads in a block.
    *   **Registers**: Fastest memory, private to a thread.

## Triton
An open-source language and compiler for writing highly efficient GPU code, developed by OpenAI.
*   **Goal**: To make writing high-performance kernels easier than CUDA (which is verbose and complex).
*   **How it works**: You write Python-like code that operates on blocks of data. The Triton compiler automatically handles memory coalescing, shared memory management, and thread scheduling.
*   **Adoption**: Used heavily in PyTorch 2.0 (`torch.compile`) to generate optimized kernels on the fly.

## Optimization Techniques

### 1. Kernel Fusion
Combining multiple operations (e.g., `Add` -> `Relu` -> `Multiply`) into a single kernel launch.
*   **Benefit**: Reduces the overhead of launching kernels and reading/writing to global memory (memory bandwidth is often the bottleneck).

### 2. Mixed Precision Training (FP16 / BF16)
Using 16-bit floating-point numbers instead of 32-bit.
*   **Benefit**: Reduces memory usage by half and speeds up math operations (using Tensor Cores).
*   **BF16 (Bfloat16)**: Has the same range as FP32 but less precision. Preferred over FP16 for training stability.

### 3. FlashAttention
An IO-aware exact attention algorithm.
*   **Innovation**: Reorders the attention computation to minimize reads/writes to slow global memory (HBM) and maximize usage of fast SRAM (Shared Memory).
*   **Result**: 2-4x faster training and lower memory footprint for Transformers.

## Hardware Concepts
*   **Tensor Cores**: Specialized hardware units on NVIDIA GPUs designed specifically for matrix multiplication (GEMM), the core operation of Deep Learning.
*   **HBM (High Bandwidth Memory)**: The specialized RAM on GPUs (e.g., 80GB on an A100) that provides massive throughput.
