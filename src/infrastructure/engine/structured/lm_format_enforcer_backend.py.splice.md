# Splice: src/infrastructure/engine/structured/lm_format_enforcer_backend.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DFAStateType
- DFAState
- DFATransition
- CompiledDFA
- TokenVocabulary
- RegexMatchState
- CompiledEnforcer
- LMFormatEnforcerBackend
- AsyncLMFormatEnforcerBackend
- FormatEnforcerGrammar
- CompositeEnforcer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
