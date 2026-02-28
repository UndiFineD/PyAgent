# Splice: src/infrastructure/services/dev/agent_tests/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TestCase
- TestRun
- CoverageGap
- TestFactory
- VisualRegressionConfig
- ContractTest
- TestEnvironment
- ExecutionTrace
- TestDependency
- CrossBrowserConfig
- AggregatedResult
- Mutation
- GeneratedTest
- TestProfile
- ScheduleSlot
- ProvisionedEnvironment
- ValidationResult
- Recording
- ReplayResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
