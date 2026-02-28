# Splice: src/infrastructure/services/dev/agent_tests/testing_utils.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- VisualRegressionTester
- ContractTestRunner
- ResultAggregator
- TestMetricsCollector

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
