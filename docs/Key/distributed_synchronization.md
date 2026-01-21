# Synchronization in Distributed AI

When training large models across multiple GPUs or nodes, **Synchronization** is the critical bottleneck. It refers to the process of ensuring all devices agree on the model state (weights, gradients, optimizer states) at specific points in time.

## 1. Collective Communications (NCCL)

NVIDIA Collective Communications Library (NCCL) is the standard primitive for GPU communication. Understanding these primitives is key to debugging distributed training.

*   **All-Reduce**: The most common operation. Every GPU starts with a buffer (e.g., gradients). At the end, every GPU has the *sum* (or average) of all buffers. Used to synchronize gradients in DDP.
*   **All-Gather**: Every GPU starts with a piece of data. At the end, every GPU has *all* pieces concatenated. Used in FSDP to gather full weights for the forward pass.
*   **Reduce-Scatter**: Every GPU starts with a full buffer. At the end, each GPU has a *different chunk* of the reduced sum. Used in FSDP to shard gradients after the backward pass.
*   **Broadcast**: One GPU (Rank 0) sends its data to all other GPUs. Used to initialize weights identically at the start of training.

## 2. Gradient Synchronization

In **Data Parallelism (DDP)**:
1.  **Forward Pass**: Each GPU computes loss on its local batch.
2.  **Backward Pass**: Each GPU computes local gradients.
3.  **Sync (All-Reduce)**: Gradients are averaged across all GPUs. This is the synchronization point.
4.  **Optimizer Step**: Each GPU updates its local copy of the model. Since gradients were identical (averaged), the model remains identical.

**Bucketization**: To hide latency, gradients are not synced one by one. They are grouped into "buckets" (e.g., 25MB). As soon as a bucket is ready (computed in backward pass), it is asynchronously All-Reduced while the GPU computes the next layer's gradients.

## 3. Asynchronous vs. Synchronous

*   **Synchronous SGD**: All workers wait for each other. Mathematically equivalent to a large batch size. Safe, stable, but slow if one worker is a "straggler" (slow hardware/network).
*   **Asynchronous SGD**: Workers update the global model whenever they are ready, without waiting. Faster, but mathematically unstable (stale gradients). Rarely used in modern LLM training due to instability.

## 4. Barrier Synchronization

A **Barrier** is a checkpoint where all processes must arrive before any can proceed.
*   Implicit barriers exist in collective operations (All-Reduce).
*   Explicit barriers (`dist.barrier()`) are used for coordination (e.g., ensuring all workers have finished saving a checkpoint before loading it).

## 5. Challenges

*   **Stragglers**: If one GPU is slow (thermal throttling, bad cable), *all* GPUs wait.
*   **Network Bandwidth**: All-Reduce requires moving gigabytes of data per second. NVLink and InfiniBand are essential for large clusters.
*   **Deadlocks**: If Rank 0 waits for Rank 1, but Rank 1 waits for Rank 0 (e.g., different code paths), the training hangs forever.
