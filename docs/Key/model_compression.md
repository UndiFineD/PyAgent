# Model Compression

## Why Compress Models?
Modern AI models (especially LLMs) are massive, often containing billions of parameters. This makes them:
1.  **Slow**: High latency during inference.
2.  **Expensive**: Requiring expensive GPUs with lots of VRAM.
3.  **Power-Hungry**: Consuming significant energy.
4.  **Hard to Deploy**: Difficult to run on edge devices (phones, laptops).

Model compression techniques aim to reduce the size and computational cost of models while maintaining as much accuracy as possible.

## Key Techniques

### 1. Quantization
Reducing the precision of the numbers used to represent the model's weights and activations.
*   **FP32 (32-bit Float)**: Standard training precision.
*   **FP16 / BF16 (16-bit)**: Standard inference precision.
*   **INT8 (8-bit Integer)**: Common for deployment; 4x smaller than FP32.
*   **4-bit / 3-bit / 2-bit**: Aggressive quantization used for running large LLMs on consumer hardware (e.g., GPTQ, AWQ, GGUF).
*   **Post-Training Quantization (PTQ)**: Quantizing a model after it has been trained.
*   **Quantization-Aware Training (QAT)**: Simulating quantization errors *during* training so the model learns to be robust to lower precision.

### 2. Pruning
Removing unnecessary connections (weights) or entire neurons/layers from the network.
*   **Unstructured Pruning**: Setting individual weights to zero. Creates "sparse" matrices which are hard to accelerate on standard hardware.
*   **Structured Pruning**: Removing entire channels, filters, or attention heads. Easier to accelerate as it shrinks the matrix dimensions.
*   **Lottery Ticket Hypothesis**: The idea that dense networks contain smaller "winning ticket" subnetworks that, if trained in isolation, would match the full model's performance.

### 3. Knowledge Distillation
Training a small "Student" model to mimic the behavior of a large "Teacher" model.
*   The student learns not just from the hard labels (Ground Truth) but from the teacher's "soft targets" (probability distributions), which contain richer information about the relationships between classes.

### 4. Low-Rank Factorization
Decomposing large weight matrices into products of smaller matrices (similar to LoRA, but applied for compression rather than just fine-tuning).

## Impact
*   **Memory**: A 70B parameter model in FP16 takes ~140GB VRAM. In 4-bit, it takes ~40GB, making it runnable on dual consumer GPUs.
*   **Speed**: Integer operations are often faster than floating-point operations on modern hardware.
