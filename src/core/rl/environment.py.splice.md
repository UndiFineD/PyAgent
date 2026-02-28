# Splice: src/core/rl/environment.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EpisodeStats
- RLEnvironment
- CodeImprovementEnvironment

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
