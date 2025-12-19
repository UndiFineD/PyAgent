# Quantization Formats (GGUF, AWQ, GPTQ)

Running Large Language Models (LLMs) on consumer hardware requires reducing their size. While the concept is "Quantization" (reducing precision from FP16 to INT4), the *file formats* and *algorithms* used to achieve this determine performance and compatibility.

## 1. GGUF (GPT-Generated Unified Format)

The standard for **CPU + Apple Silicon** inference.
- **Origin**: Created by Georgi Gerganov for `llama.cpp`. Replaced the older GGML format.
- **Mechanism**: Stores tensors in a binary format optimized for `mmap` (memory mapping). This allows the model to be loaded instantly and offloaded layer-by-layer to the GPU if VRAM is limited.
- **Quantization**: Uses "k-quants" (e.g., `Q4_K_M`), a smart block-wise quantization method that mixes different precisions (some weights are 6-bit, some 4-bit) to preserve accuracy.
- **Best For**: MacBooks, CPUs, and scenarios with limited VRAM.

## 2. GPTQ (Post-Training Quantization for GPT)

The standard for **NVIDIA GPUs**.
- **Mechanism**: A "One-Shot" quantization method. It quantizes weights row-by-row, adjusting the remaining unquantized weights to compensate for the error introduced by the quantization.
- **Performance**: Extremely fast inference on CUDA cores.
- **Format**: Usually stored as `.safetensors`.
- **Best For**: Dedicated GPU servers where the model fits entirely in VRAM.

## 3. AWQ (Activation-aware Weight Quantization)

A newer, often superior alternative to GPTQ.
- **Insight**: Not all weights are equally important. Weights that multiply with large *activations* are more critical to the output.
- **Mechanism**: AWQ identifies these critical weights (about 1%) and keeps them in higher precision (or scales them up) to protect them from quantization noise.
- **Benefit**: Better perplexity (accuracy) than GPTQ at the same bit-width.
- **Best For**: High-performance GPU inference (vLLM supports it natively).

## 4. EXL2 (ExLlamaV2)

The speed king for consumer GPUs.
- **Mechanism**: A format designed specifically for the ExLlamaV2 loader. It allows for **mixed precision** at a very granular level (e.g., 4.65 bits per weight).
- **Benefit**: You can tune the model size exactly to fill your VRAM (e.g., a 24GB card can fit a 70B model at 2.4 bits).
- **Best For**: Enthusiasts maximizing the utility of their RTX 3090/4090s.

## Summary

| Format | Primary Engine | Hardware Target | Key Feature |
| :--- | :--- | :--- | :--- |
| **GGUF** | llama.cpp | CPU / Apple / Low VRAM | Partial GPU offloading |
| **GPTQ** | AutoGPTQ | NVIDIA GPU | Fast, standard |
| **AWQ** | vLLM / AutoAWQ | NVIDIA GPU | Better accuracy than GPTQ |
| **EXL2** | ExLlamaV2 | NVIDIA GPU | Fastest, flexible bitrate |
