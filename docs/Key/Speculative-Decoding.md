# Speculative Decoding

LLM inference is memory-bound, not compute-bound. Generating one token takes almost as much time as checking 5 tokens in parallel. Speculative Decoding exploits this to speed up inference by 2-3x without changing the output quality.

## The Problem
Running a massive model (e.g., Llama-70B) to generate "The cat sat on the..." is overkill. A smaller model (Llama-7B) could easily guess "mat".

## The Algorithm

1.  **Draft**: A small, fast "Draft Model" generates a short sequence of $K$ tokens (e.g., 5 tokens).
2.  **Verify**: The large "Target Model" processes all $K$ tokens in a single forward pass (parallel).
3.  **Accept/Reject**:
    *   If the Target Model agrees with the Draft Model's token $i$, it is accepted.
    *   If it disagrees at token $j$, all subsequent tokens are discarded, and the Target Model provides the correct token for $j$.
4.  **Repeat**: The process continues.

## Why it Works
*   **Memory Bandwidth**: Loading the weights of the 70B model is the bottleneck.
*   **Parallelism**: Checking 5 tokens takes 1 GPU call. Generating 5 tokens sequentially takes 5 GPU calls.
*   **Correctness**: The output is mathematically identical to running the Target Model alone (if using greedy decoding) or statistically identical (if using sampling with rejection sampling).

## Requirements
*   **Shared Vocabulary**: The Draft and Target models must use the same tokenizer.
*   **Model Compatibility**: Usually works best when the Draft model is a smaller version of the Target (e.g., Llama-68M drafting for Llama-7B).

## Medusa
A variant of speculative decoding where the model has multiple "heads" that predict not just the next token, but the next *several* tokens simultaneously. This removes the need for a separate draft model.
