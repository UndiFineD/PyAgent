# Improvements: src/observability/telemetry/usage_message.py

Potential improvements:
- Add comprehensive unit tests for `UsageMessage` serialization and opt-out behavior.
- Break module into smaller modules (`datamodels`, `runtime`, `detection`, `reporting`) to reduce cognitive complexity.
- Replace global mutable `_GLOBAL_RUNTIME_DATA` with an injectable runtime store or context object for testability.
- Avoid heavy optional imports at top-level; import lazily inside functions to speed up import time.
- Add type hints for all internal helper functions and document return shapes.
- Add retry/backoff and timeout behavior for any external calls and file I/O.
- Use dependency injection for filesystem paths and telemetry sinks to make testing easier.
- Improve privacy: reduce the amount of environment data collected by default, and add a clear opt-in flag.
- Consider making collection async to avoid blocking critical paths.
- Add clearer logging and metrics around telemetry dispatch and failures.
