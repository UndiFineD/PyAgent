# Splice: src/infrastructure/engine/structured/logit_processor.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LogitBias
- ProcessorStats
- LogitProcessor
- ConstrainedLogitProcessor
- BitmaskLogitProcessor
- BiasLogitProcessor
- CompositeLogitProcessor
- TemperatureProcessor
- TopKProcessor
- TopPProcessor
- RepetitionPenaltyProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
