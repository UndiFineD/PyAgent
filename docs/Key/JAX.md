# JAX

## Overview
**JAX** is a high-performance numerical computing library developed by Google. It is often described as "NumPy on steroids" (GPU/TPU support) combined with automatic differentiation. It is gaining popularity in research for its speed and functional purity.

## Key Features

### 1. Functional Programming
Unlike PyTorch (Object-Oriented), JAX is **Functional**.
*   **Pure Functions**: Functions should have no side effects (no global state).
*   **Stateless**: Model parameters are passed explicitly into the function, rather than being stored inside a class.

### 2. The Four Transformations
JAX provides function transformations (decorators) that give it superpowers:
*   **`grad()`**: Automatically computes the gradient of a function (Autodiff).
*   **`jit()`**: **Just-In-Time Compilation**. Compiles Python code into XLA (Accelerated Linear Algebra) kernels for massive speedups.
*   **`vmap()`**: **Vectorization**. Automatically batches a function. Write code for a single example, and `vmap` makes it work for a batch.
*   **`pmap()`**: **Parallelization**. Automatically distributes computation across multiple devices (GPUs/TPUs).

### 3. XLA (Accelerated Linear Algebra)
A domain-specific compiler for linear algebra. It fuses operations (e.g., Add + Multiply + Activation) into a single GPU kernel, reducing memory bandwidth usage.

## Ecosystem
Since JAX is a low-level library (like NumPy), several high-level neural network libraries are built on top of it:
*   **Flax**: The most popular neural network library for JAX (developed by Google Brain). Flexible and powerful.
*   **Equinox**: A library that brings PyTorch-like syntax (classes) to JAX.
*   **Optax**: Optimization library (Adam, SGD).

## JAX vs. PyTorch
*   **Speed**: JAX (with JIT) is often faster than PyTorch, especially on TPUs.
*   **Complexity**: JAX has a steeper learning curve due to the functional paradigm and immutable data structures.
*   **Debugging**: Harder in JAX because of JIT compilation (you can't just print inside a compiled function).
