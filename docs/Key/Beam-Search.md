# Beam Search

Greedy decoding picks the best token *right now*, but that might lead to a dead end later. Beam Search explores multiple potential futures simultaneously to find the sequence with the highest *total* probability.

## The Algorithm

1.  **Initialization**: Start with the initial prompt.
2.  **Expansion**: Generate the top $k$ (beam width) most likely next tokens.
3.  **Selection**: For each of the $k$ paths, generate the top $k$ next tokens (total $k^2$ candidates).
4.  **Pruning**: Calculate the cumulative probability for all $k^2$ paths. Keep only the top $k$ best paths.
5.  **Repeat**: Continue until the `<EOS>` token is generated or max length is reached.

## Parameters

### 1. Beam Width ($k$)
*   **Small $k$ (1)**: Equivalent to Greedy Decoding. Fast but suboptimal.
*   **Large $k$ (5-10)**: Better quality, finds more optimal sequences. Slower and uses more memory.
*   **Too Large $k$**: Diminishing returns. Can sometimes lead to shorter, generic translations (in NMT).

### 2. Length Penalty
Beam search tends to favor shorter sentences because the probability of a sequence is the product of probabilities (which are < 1). Adding more tokens always lowers the total probability.
*   **Solution**: Normalize the score by the sequence length.
    $$ Score = \frac{\log P(Y|X)}{Length(Y)^\alpha} $$
    Where $\alpha$ (usually 0.6 - 1.0) controls the penalty.

## Use Cases
*   **Machine Translation**: Almost always uses Beam Search (width 4-5) because grammatical correctness is paramount.
*   **Summarization**: Often uses Beam Search to ensure the summary is concise and coherent.
*   **Creative Writing**: **Avoid** Beam Search. It tends to produce very "safe", repetitive, and boring text. Use Sampling (Top-p) instead.
