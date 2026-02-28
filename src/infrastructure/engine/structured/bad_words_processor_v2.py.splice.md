# Splice: src/infrastructure/engine/structured/bad_words_processor_v2.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BadWordsPenaltyMode
- TrieNode
- BadWordsProcessorV2
- BadPhrasesProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
