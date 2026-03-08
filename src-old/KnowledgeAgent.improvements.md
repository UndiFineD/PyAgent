# Improvements: `KnowledgeAgent.py`

## Suggested improvements

- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Contains bare `except:` clause (catches SystemExit / KeyboardInterrupt).
- Function `_init_chroma` is missing type annotations.
- Function `build_index` is missing type annotations.
- Function `build_vector_index` is missing type annotations.
- Function `record_tier_memory` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\context\KnowledgeAgent.py`