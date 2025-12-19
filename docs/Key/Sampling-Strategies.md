# Sampling Strategies

When an LLM generates text, it predicts a probability distribution over the entire vocabulary for the next token. How we select the actual token from this distribution determines the creativity, coherence, and quality of the output.

## 1. Greedy Decoding
*   **Method**: Always pick the token with the highest probability.
*   **Pros**: Deterministic, coherent for short answers.
*   **Cons**: Can get stuck in repetitive loops. Often produces boring or generic text.

## 2. Temperature
A hyperparameter that scales the logits before applying Softmax.
*   **Formula**: $P_i = \frac{\exp(logit_i / T)}{\sum \exp(logit_j / T)}$
*   **Low Temperature (< 1.0)**: Sharpens the distribution. High probability tokens become even more likely. Makes the model more confident and deterministic.
*   **High Temperature (> 1.0)**: Flattens the distribution. Low probability tokens get a boost. Increases creativity but also the risk of nonsense.

## 3. Top-k Sampling
*   **Method**: Sort the vocabulary by probability and keep only the top $k$ tokens (e.g., $k=50$). Zero out the rest. Sample from the remaining pool.
*   **Effect**: Prevents the model from choosing extremely low-probability (garbage) tokens.
*   **Limitation**: $k$ is fixed. In some contexts, there are 100 valid next words; in others, only 1. Top-k is too rigid.

## 4. Top-p (Nucleus) Sampling
*   **Method**: Sort the vocabulary by probability. Keep the smallest set of top tokens whose cumulative probability exceeds $p$ (e.g., $p=0.9$).
*   **Effect**: Dynamic vocabulary size. If the model is unsure (flat distribution), the pool is large. If the model is sure (sharp distribution), the pool is small.
*   **Standard**: This is the default for most modern LLMs (GPT-4, Claude).

## 5. Min-p Sampling
A newer method that is often more robust than Top-p.
*   **Method**: Set a threshold relative to the *most likely* token. If the top token has probability 0.5, and `min_p` is 0.1, then any token with probability < 0.05 (0.5 * 0.1) is discarded.
*   **Benefit**: Scales naturally with the model's confidence.

## 6. Frequency and Presence Penalties
*   **Frequency Penalty**: Penalizes tokens based on how many times they have *already appeared* in the text. Reduces repetition.
*   **Presence Penalty**: Penalizes tokens if they have appeared *at least once*. Encourages introducing new topics.
