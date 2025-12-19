# LLM-as-a-Judge

Evaluating open-ended text generation (summarization, creative writing, chat) is hard. Metrics like BLEU or ROUGE only measure word overlap, not quality. Human evaluation is expensive and slow. The solution is to use a strong LLM (like GPT-4) to evaluate weaker LLMs.

## Methodology

### 1. Pairwise Comparison (Chatbot Arena Style)
*   **Input**: A prompt and two responses (Model A vs Model B).
*   **Judge**: GPT-4 is asked: "Which response is better? A, B, or Tie? Explain why."
*   **Result**: A win-rate is calculated.
*   **Benchmarks**: **AlpacaEval** uses this method to rank models against a baseline (Davinci-003).

### 2. Single Score Grading (MT-Bench)
*   **Input**: A prompt and one response.
*   **Judge**: GPT-4 is asked to rate the response on a scale of 1-10 based on helpfulness, relevance, accuracy, and detail.
*   **Benchmarks**: **MT-Bench** uses this for multi-turn conversations.

## Biases and Limitations

### 1. Position Bias
The judge often prefers the first response presented (or the second).
*   **Fix**: Swap the order (A vs B, then B vs A) and only count it if the judge is consistent.

### 2. Verbosity Bias
The judge tends to prefer longer answers, even if they are repetitive or less accurate.
*   **Fix**: Hard to fix completely, but instructing the judge to value conciseness helps.

### 3. Self-Preference Bias
GPT-4 tends to prefer outputs that sound like GPT-4.

## Cost vs. Accuracy
*   **GPT-4**: The gold standard, correlates highly with human preference. Expensive.
*   **Llama-3-70B**: A cheaper alternative that is "good enough" for preliminary evaluation.
*   **Prometheus**: An open-source model fine-tuned specifically to be a judge.
