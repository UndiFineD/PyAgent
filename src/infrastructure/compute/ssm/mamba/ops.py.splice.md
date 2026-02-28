# Splice: src/infrastructure/compute/ssm/mamba/ops.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CausalConv1d
- SelectiveScan

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
