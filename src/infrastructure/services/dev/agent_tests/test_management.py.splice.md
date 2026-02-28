# Splice: src/infrastructure/services/dev/agent_tests/test_management.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BaselineComparisonResult
- BaselineManager
- DIContainer
- TestPrioritizer
- FlakinessDetector
- QuarantineManager
- ImpactAnalyzer
- ContractValidator
- TestDocGenerator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
