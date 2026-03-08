# Splice: src/core/base/common/utils/lazy_loader.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LazyModule
- LazyImport
- DeferredImport

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
