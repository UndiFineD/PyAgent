# Splice: src/core/rl/reward_functions.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RewardType
- RewardSignal
- RewardFunctions
- CompositeRewardFunction
- RewardShaper

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
