# Improvements: `SubagentRunner.py`

## Suggested improvements

- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting).
- Function `llm_chat_via_ollama` is missing type annotations.
- Function `llm_chat_via_vllm` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\backend\SubagentRunner.py`