# AI Accelerators

## What are AI Accelerators?
AI Accelerators are specialized hardware designed to speed up Artificial Intelligence applications, specifically neural network training and inference. Unlike general-purpose CPUs, they are optimized for the massive parallel matrix multiplication operations that dominate deep learning.

## Types of Accelerators

### 1. GPU (Graphics Processing Unit)
*   **Dominant Player**: NVIDIA (H100, A100, RTX 4090).
*   **Architecture**: Thousands of small cores designed for parallel processing. Originally for graphics, but perfect for matrix math.
*   **Key Tech**: CUDA (Compute Unified Device Architecture) - the software layer that makes NVIDIA GPUs the standard for AI development.
*   **Use Case**: General-purpose AI training and inference across all model types.

### 2. TPU (Tensor Processing Unit)
*   **Creator**: Google.
*   **Architecture**: ASIC (Application-Specific Integrated Circuit) designed specifically for TensorFlow and JAX. Uses "Systolic Arrays" to pass data through the chip efficiently, minimizing memory access.
*   **Availability**: Only available via Google Cloud (GCP).
*   **Use Case**: Massive scale training of Transformer models (e.g., Gemini, PaLM).

### 3. LPU (Language Processing Unit)
*   **Creator**: Groq.
*   **Architecture**: Deterministic, single-core architecture with massive on-chip memory (SRAM). Eliminates the "memory wall" bottleneck (HBM) found in GPUs.
*   **Use Case**: Extremely low-latency **Inference** for LLMs. Not used for training.

### 4. NPU (Neural Processing Unit)
*   **Context**: Often found in consumer devices (Apple Neural Engine, Intel NPU, Qualcomm Hexagon).
*   **Use Case**: Running small AI models locally on laptops and phones (FaceID, background blur, local chatbots) to save battery and protect privacy.

### 5. FPGA (Field-Programmable Gate Array)
*   **Concept**: "Rewritable" hardware chips.
*   **Use Case**: Niche applications requiring ultra-low latency where the model architecture might change frequently (e.g., High-Frequency Trading).

## The "Memory Wall"
The speed of AI chips has increased faster than the speed of memory.
*   **HBM (High Bandwidth Memory)**: Essential for feeding data to powerful GPUs. HBM3e is the current standard.
*   **Bottleneck**: Often, the chip spends time waiting for data to arrive from memory rather than computing.
