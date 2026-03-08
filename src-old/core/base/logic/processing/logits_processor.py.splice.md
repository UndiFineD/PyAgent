# Splice: src/core/base/logic/processing/logits_processor.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LogitsProcessor
- LogitsProcessorList
- TemperatureProcessor
- TopKProcessor
- TopPProcessor
- RepetitionPenaltyProcessor
- NoBadWordsProcessor
- MinLengthProcessor
- MaxLengthProcessor
- PresencePenaltyProcessor
- FrequencyPenaltyProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
