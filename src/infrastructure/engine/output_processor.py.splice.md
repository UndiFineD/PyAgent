# Splice: src/infrastructure/engine/output_processor.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EventType
- RequestEvent
- LoRARequest
- ParentRequest
- SamplingParams
- EngineCoreRequest
- EngineCoreOutput
- EngineCoreOutputs
- RequestOutput
- OutputProcessorOutput
- RequestOutputCollector
- RequestState
- LoRARequestStates
- OutputProcessor
- IterationStats

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
