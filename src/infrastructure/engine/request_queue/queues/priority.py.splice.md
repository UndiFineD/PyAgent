# Splice: src/infrastructure/engine/request_queue/queues/priority.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PriorityQueue
- DeadlineQueue

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
