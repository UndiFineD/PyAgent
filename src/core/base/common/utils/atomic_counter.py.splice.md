# Splice: src/core/base/common/utils/atomic_counter.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- Counter
- AtomicCounter
- AtomicFlag
- AtomicGauge

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
