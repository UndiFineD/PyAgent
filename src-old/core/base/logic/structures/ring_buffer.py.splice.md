# Splice: src/core/base/logic/structures/ring_buffer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RingBuffer
- ThreadSafeRingBuffer
- TimestampedValue
- TimeSeriesBuffer
- SlidingWindowAggregator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
