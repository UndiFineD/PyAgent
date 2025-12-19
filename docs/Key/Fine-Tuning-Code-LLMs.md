# Fine-Tuning Code LLMs

## Overview
**Fine-Tuning Code LLMs** involves taking a pre-trained base model (like CodeLlama, StarCoder, or DeepSeek-Coder) and training it further on a specific codebase or programming language to improve its performance on proprietary or domain-specific tasks.

## Why Fine-Tune?
*   **Proprietary APIs**: Base models don't know your internal libraries or private SDKs.
*   **Coding Style**: Enforcing company-specific linting rules and variable naming conventions.
*   **Legacy Languages**: Improving performance on niche languages (e.g., proprietary DSLs, older COBOL dialects).

## The Process

### 1. Data Preparation
*   **Deduplication**: Removing near-duplicate files to prevent overfitting (MinHash LSH).
*   **PII Redaction**: Scrubbing secrets, API keys, and personal emails from the training data.
*   **Formatting**: Structuring data as "Fill-in-the-Middle" (FIM) or Instruction-Response pairs.

### 2. Base Models
*   **StarCoder2**: Optimized for code, trained on The Stack v2.
*   **CodeLlama**: Meta's code-specialized version of Llama 2/3.
*   **DeepSeek-Coder**: High-performance open weights model.

### 3. Training Techniques
*   **Full Fine-Tuning**: Updating all weights (expensive).
*   **LoRA/QLoRA**: Low-Rank Adaptation. Fine-tuning only a small subset of parameters (efficient).
*   **Instruction Tuning**: Training on "Task -> Code" pairs (e.g., "Write a function to calculate tax" -> `def calculate_tax...`).

## Evaluation
*   **HumanEval**: Standard benchmark for Python coding tasks.
*   **MBPP**: Mostly Basic Python Problems.
*   **Internal Benchmarks**: Creating a test set of internal coding tasks to measure improvement on proprietary logic.

## Risks
*   **Catastrophic Forgetting**: The model might lose its general coding ability while learning the specific codebase.
*   **Data Leakage**: If not careful, the model might memorize and regurgitate secrets found in the training data.
