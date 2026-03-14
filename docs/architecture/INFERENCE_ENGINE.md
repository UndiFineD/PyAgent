# Inference Engine Architecture

The inference layer (`src/infrastructure/engine/` and `src/inference/`) is a high-performance subsystem modeled after high-throughput runtimes like vLLM. It is designed to minimize latency and maximize token throughput across the distributed swarm.

## ⚡ Paged Attention & KV Cache
- **Block-Based Memory**: KV Cache is stored in non-contiguous memory blocks, eliminating memory fragmentation.
- **Online Softmax**: Implements partitioned softmax calculations to handle extremely long context windows.
- **Wait-for-Majority**: Convergence logic for consensus-based sampling.

## 🚀 Speculative Drafting
- **Draft & Verify**: Uses a fast "Drafter" model (e.g., Qwen-0.5B) to generate candidates, which the larger "Target" model (e.g., DeepSeek-V3) verifies in parallel.
- **Speculation Engine**: Manages the multi-candidate beam search to hide token generation latency.

## 📉 Quantization & bit-Scaling
- **Dynamic Bit-Width**: Automatically scales from FP16 to INT4 based on available VRAM and latency targets.
- **GGUF/FastFlowLM Support**: Native support for Ryzen AI NPUs (XDNA2) and local GGUF execution.

## 🔌 Model Converters & Backends
- **Unified Provider Interface**: Logic in `models_registry.py` provides a standard wrapper for 65+ providers (Ollama, Anthropic, OpenAI, etc.).
- **Backend Core**: Handle different protocol nuances (Chat vs Completion, Tool-calling schemas) to provide a unified "Thought-Step" API to agents.
- **Suffix Support (FIM)**: Native Fill-In-The-Middle support for code completion tasks.

## 🧠 Reasoning Engine
- **Think Tag Parsing**: Specialized logic for models with internal reasoning tokens (e.g., DeepSeek-R1), extracting thought chains for metadata and telemetry without polluting the final output.
- **Prompt Rendering**: High-performance Jinja2-based template rendering for complex multi-shot prompts.

---
*Throughput over Latency. Scaling to 100M+ tokens.*
