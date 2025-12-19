# Evaluation Metrics

Measuring the "intelligence" of an LLM is notoriously difficult. Unlike classification (Accuracy = 95%), text generation is open-ended.

## 1. Traditional NLP Metrics

These compare the model's output to a "Gold Reference" text.
*   **BLEU (Bilingual Evaluation Understudy)**: Measures n-gram overlap. Common in translation. Flawed because "The cat sat on the mat" and "On the mat sat the cat" might get low scores despite same meaning.
*   **ROUGE**: Recall-oriented. Common in summarization.
*   **Perplexity (PPL)**: A measure of how "surprised" the model is by real text. Lower is better. $PPL = e^{Loss}$. Good for checking if a base model is well-trained, but doesn't correlate perfectly with chat quality.

## 2. Standard Benchmarks

Sets of multiple-choice or short-answer questions.
*   **MMLU (Massive Multitask Language Understanding)**: 57 subjects (STEM, humanities, etc.). The de facto standard for general knowledge.
*   **GSM8K**: Grade School Math. Measures reasoning.
*   **HumanEval / MBPP**: Python coding problems.
*   **HellaSwag**: Common sense reasoning.

## 3. LLM-as-a-Judge

Using a stronger model (e.g., GPT-4) to grade the outputs of a weaker model.
*   **MT-Bench**: A set of multi-turn conversation questions. GPT-4 scores the response from 1-10.
*   **AlpacaEval**: Head-to-head comparison. GPT-4 decides which model won.
*   **Pros**: Fast, cheap, correlates well with human preference.
*   **Cons**: "Self-preference bias" (GPT-4 likes outputs that sound like GPT-4).

## 4. The Evaluation Crisis

*   **Data Contamination**: Many benchmarks are leaked into the training data. A model might score 90% on GSM8K because it memorized the answers, not because it can do math.
*   **Goodhart's Law**: "When a measure becomes a target, it ceases to be a good measure." Models are now being optimized specifically to game the leaderboards.
