# Splice: src/infrastructure/compute/cuda/cudagraph_dispatcher.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DispatchMode
- DispatchKey
- DispatchStats
- DispatchPolicy
- DefaultDispatchPolicy
- AdaptiveDispatchPolicy
- GraphEntry
- CudagraphDispatcher
- CompositeDispatcher
- StreamDispatcher

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
