# Normalization Methods

Techniques to stabilize training by ensuring the inputs to each layer have a consistent distribution (mean ~0, variance ~1). Without normalization, Deep Networks suffer from "Internal Covariate Shift" and are impossible to train.

## 1. Batch Normalization (BatchNorm)

*   **How**: Normalizes across the **Batch** dimension.
*   **Pros**: Allows much higher learning rates; acts as a regularizer.
*   **Cons**: Depends on batch size (fails with small batches); hard to use in RNNs/Transformers.
*   **Usage**: Standard in CNNs (ResNet).

## 2. Layer Normalization (LayerNorm)

*   **How**: Normalizes across the **Feature** dimension (for a single sample).
*   **Pros**: Independent of batch size. Works perfectly for sequences (RNNs, Transformers).
*   **Usage**: Standard in NLP (BERT, GPT-2).

## 3. RMSNorm (Root Mean Square Normalization)

*   **How**: A simplified LayerNorm that only re-scales the inputs (ignoring the mean centering).
*   **Pros**: Computationally cheaper and often more stable for Large Language Models.
*   **Usage**: Standard in modern LLMs (Llama, Gopher, PaLM).
