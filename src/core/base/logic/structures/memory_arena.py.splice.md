# Splice: src/core/base/logic/structures/memory_arena.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ArenaStats
- MemoryArena
- TypedArena
- StackArena
- SlabAllocator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
