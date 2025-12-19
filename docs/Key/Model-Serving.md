# Model Serving

## What is Model Serving?
Model Serving is the process of hosting a trained machine learning model (the artifact) on a server so that it can receive requests (inference) and return predictions via an API (usually REST or gRPC).

## Key Challenges
1.  **Latency**: Users expect instant responses. Loading a 70GB model into memory takes time, so it must be pre-loaded.
2.  **Throughput**: Handling thousands of concurrent requests.
3.  **Batching**: Grouping multiple user requests into a single GPU operation to maximize utilization.
4.  **KV Caching**: Managing the Key-Value cache for LLMs to speed up token generation.

## Serving Engines

### 1. vLLM
*   **Specialty**: High-throughput serving for LLMs.
*   **Key Tech**: **PagedAttention**. It manages GPU memory like an operating system manages RAM (paging), virtually eliminating memory fragmentation and allowing for much larger batch sizes.
*   **Use Case**: The gold standard for open-source LLM serving today.

### 2. NVIDIA Triton Inference Server
*   **Specialty**: Universal serving. Supports TensorFlow, PyTorch, ONNX, TensorRT, and custom backends.
*   **Key Tech**: Dynamic batching, concurrent model execution (running multiple models on one GPU).
*   **Use Case**: Enterprise environments with diverse model types (Vision, Audio, Tabular).

### 3. Text Generation Inference (TGI)
*   **Creator**: Hugging Face.
*   **Specialty**: Optimized for Hugging Face models. Includes tensor parallelism and quantization out of the box.

### 4. TorchServe
*   **Creator**: AWS and Meta.
*   **Specialty**: Native PyTorch serving. Easy to use if you are already in the PyTorch ecosystem.

## Deployment Patterns
*   **Real-time API**: Synchronous Request/Response (e.g., Chatbot).
*   **Async / Batch**: User submits a job, gets an ID, and checks back later (e.g., Video generation).
*   **Streaming**: Sending tokens one by one as they are generated (Server-Sent Events).
