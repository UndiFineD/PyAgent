# Splice: src/infrastructure/engine/outputs/logprobs_processor.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TokenLogprob
- TopLogprobs
- LogprobsLists
- LogprobsTensors
- AsyncCPUTransfer
- SamplerOutput
- ModelRunnerOutput
- StreamingLogprobsCollector

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
