# LLM Benchmarks and Evaluation

Evaluating Large Language Models (LLMs) is notoriously difficult because "quality" is subjective. However, a standard suite of benchmarks has emerged to measure performance across different capabilities.

## General Knowledge & Reasoning

### 1. MMLU (Massive Multitask Language Understanding)
*   **What**: 57 subjects across STEM, the humanities, and social sciences (e.g., elementary math, US history, computer science, law).
*   **Format**: Multiple-choice questions.
*   **Significance**: The de facto standard for measuring general "intelligence" and world knowledge.

### 2. ARC (AI2 Reasoning Challenge)
*   **What**: Grade-school science questions.
*   **Focus**: Tests reasoning and common sense, specifically designed to be hard for simple retrieval systems.

### 3. HellaSwag
*   **What**: Sentence completion tasks requiring common sense inference.
*   **Example**: "A woman is putting makeup on. She..." (Model must choose the logical continuation).

## Coding and Math

### 1. HumanEval
*   **What**: 164 hand-written Python programming problems created by OpenAI.
*   **Metric**: `pass@k` (probability that at least one of the top `k` generated solutions passes the unit tests).
*   **Significance**: The gold standard for coding capability.

### 2. MBPP (Mostly Basic Python Problems)
*   **What**: Similar to HumanEval but focuses on basic programming concepts.

### 3. GSM8K (Grade School Math 8K)
*   **What**: 8.5k high quality grade school math word problems.
*   **Focus**: Multi-step mathematical reasoning.

### 4. MATH
*   **What**: Harder mathematics problems (algebra, calculus, geometry) from high school competitions.

## Chat and Instruction Following

### 1. Chatbot Arena (LMSYS)
*   **What**: A crowdsourced platform where users chat with two anonymous models side-by-side and vote on which one is better.
*   **Metric**: Elo rating (like in Chess).
*   **Significance**: Currently considered the most reliable measure of "real-world" helpfulness and conversational ability, as it captures nuances that static benchmarks miss.

### 2. MT-Bench
*   **What**: A set of challenging multi-turn questions graded by GPT-4.
*   **Focus**: Conversation flow, instruction following, and reasoning.

## Issues with Benchmarks
*   **Contamination**: Models may have been trained on the test data (since they scrape the internet), inflating scores.
*   **Goodhart's Law**: "When a measure becomes a target, it ceases to be a good measure." Model builders now optimize specifically for these benchmarks.
