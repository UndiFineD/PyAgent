# Code LLMs

Large Language Models specialized for understanding, generating, and debugging code.

## 1. Unique Challenges

*   **Syntax Strictness**: Unlike natural language, one wrong character (`;` or `}`) breaks the code.
*   **Long Context**: Understanding a function requires knowing definitions from other files (Repository-level context).
*   **Execution**: Code is not just text; it has a functional output that can be tested.

## 2. Training Techniques

*   **Fill-in-the-Middle (FIM)**: Standard LLMs predict the *next* token. Code LLMs are trained to predict the *middle* token given the prefix and suffix.
    *   Essential for IDE auto-completion (where the cursor is in the middle of a file).
*   **Execution Feedback**: Generating code, running unit tests, and using the result (Pass/Fail) as a reward signal (RL).

## 3. Models & Tools

*   **Codex (OpenAI)**: The engine behind GitHub Copilot.
*   **StarCoder / BigCode**: Open-source models trained on "The Stack" (permissively licensed code).
*   **Code Llama**: A version of Llama 2 fine-tuned on 500B tokens of code with "Long Context" (100k tokens).
