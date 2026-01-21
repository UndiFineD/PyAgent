# Efficient Fine-Tuning (PEFT)

Fine-tuning a massive model (e.g., 70B parameters) is expensive. Updating every single weight ("Full Fine-Tuning") requires hundreds of gigabytes of VRAM for optimizer states. **PEFT (Parameter-Efficient Fine-Tuning)** solves this by updating only a tiny fraction of parameters.

## 1. LoRA (Low-Rank Adaptation)

The most popular PEFT method.
*   **Hypothesis**: The change in weights ($\Delta W$) during fine-tuning has a "low intrinsic rank." We don't need to change the full matrix.
*   **Method**: Instead of updating the dense matrix $W$ ($d \times d$), we train two small matrices $A$ ($d \times r$) and $B$ ($r \times d$), where $r$ is very small (e.g., 16 or 64).
*   **Update**: $W_{new} = W_{frozen} + (B \times A)$.
*   **Savings**: Reduces trainable parameters by 10,000x. A 70B model can be fine-tuned on a single GPU.

## 2. QLoRA (Quantized LoRA)

Combining LoRA with 4-bit Quantization.
*   **Base Model**: Loaded in 4-bit (NF4 format) to save memory.
*   **LoRA Adapters**: Trained in 16-bit (BF16) to maintain precision.
*   **Double Quantization**: Even the quantization constants are quantized.
*   **Impact**: Allows fine-tuning a 65B parameter model on a single 48GB GPU (A6000), democratizing access to large models.

## 3. Adapters (Houlsby)

An older method. Inserts small "Adapter Layers" (Feed-Forward Networks) *between* the Transformer layers.
*   **Cons**: Adds inference latency (extra layers to run).
*   **LoRA vs. Adapters**: LoRA merges into the main weights at inference time, so there is **zero latency penalty**.

## 4. Prompt Tuning / Prefix Tuning

Instead of changing weights, we learn "Soft Prompts."
*   **Method**: Prepend a sequence of trainable vectors to the input embeddings.
*   **Analogy**: Like finding the perfect "System Prompt," but using gradient descent to find the optimal continuous vectors instead of discrete words.
