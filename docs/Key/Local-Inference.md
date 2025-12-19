# Local Large Language Models (Local LLMs)

Running Large Language Models (LLMs) locally on consumer hardware (instead of relying on cloud APIs like OpenAI or Anthropic) offers significant benefits in privacy, cost, and control. This document details the technologies and techniques that make this possible.

## 1. Why Run Locally?
*   **Privacy**: Data never leaves your machine. Essential for healthcare, legal, or proprietary code.
*   **Cost**: No per-token fees. One-time hardware cost vs. recurring API bills.
*   **Latency**: No network lag. Speed is limited only by your hardware.
*   **Offline Access**: Works without an internet connection.
*   **Uncensored Models**: Access to models that haven't been "safety-tuned" to refuse certain requests (useful for creative writing or red-teaming).

## 2. Key Technologies

### A. Quantization
Standard models are trained in 16-bit floating point (FP16). A 70B parameter model in FP16 requires ~140GB of VRAM, which is out of reach for most consumers.
**Quantization** reduces the precision of the weights to 8-bit, 4-bit, or even 2-bit integers.
*   **4-bit Quantization (Q4_K_M)**: Often retains 95-99% of the model's intelligence while reducing VRAM usage by ~75%.
*   **Formats**:
    *   **GGUF** (GPT-Generated Unified Format): The standard for CPU+GPU inference (used by Llama.cpp).
    *   **EXL2** (ExLlamaV2): Optimized for extreme speed on NVIDIA GPUs.
    *   **AWQ / GPTQ**: Common GPU-only quantization formats.

### B. Inference Engines
*   **Llama.cpp**: The "universal" engine. Runs on almost anything (Apple Silicon, NVIDIA, AMD, pure CPU). It splits layers between CPU RAM and GPU VRAM ("offloading") to run models larger than your GPU.
*   **Ollama**: A user-friendly wrapper around Llama.cpp. Allows running models with a single command (`ollama run llama3`).
*   **vLLM**: High-throughput engine for production serving (mostly Linux/Server).
*   **LM Studio / GPT4All**: GUI applications that make downloading and chatting with models easy.

## 3. Hardware Requirements (Rule of Thumb)

To run a model, you generally need VRAM (Video RAM) or System RAM (for Apple Silicon/CPU) equal to the model size + 2GB overhead.

| Model Size | Quantization | VRAM Needed | Example GPU |
| :--- | :--- | :--- | :--- |
| **8B** (Llama 3) | Q4 | ~6 GB | RTX 3060 / 4060 |
| **8B** (Llama 3) | FP16 | ~16 GB | RTX 3090 / 4080 |
| **70B** (Llama 3) | Q4 | ~40 GB | 2x RTX 3090 / Mac Studio (64GB) |
| **70B** (Llama 3) | IQ2 (2-bit) | ~24 GB | RTX 3090 / 4090 |

## 4. Popular Open Weights Models

*   **Llama 3 (Meta)**: The current state-of-the-art for open weights. Available in 8B and 70B sizes.
*   **Mistral / Mixtral (Mistral AI)**: Highly efficient models. Mixtral 8x7B uses Mixture of Experts to be fast and smart.
*   **Gemma (Google)**: Open models based on Gemini research.
*   **Phi-3 (Microsoft)**: Extremely small (3.8B) but capable models, great for mobile/edge.
*   **Command R (Cohere)**: Specialized for RAG and tool use.

## 5. Summary

Local LLMs have shifted from a niche hobby to a viable alternative for production applications. With 4-bit quantization and efficient engines like Llama.cpp, a standard gaming PC or MacBook can now run models that rival GPT-3.5 in capability.
