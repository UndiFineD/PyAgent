# Splice: src/infrastructure/engine/logprobs/processor/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LogprobFormat
- TopLogprob
- LogprobEntry
- PromptLogprobs
- SampleLogprobs
- LogprobsResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
