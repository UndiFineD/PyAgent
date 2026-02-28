# Splice: src/infrastructure/engine/structured/params/constraints.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- OutputConstraint
- JsonSchemaConstraint
- RegexConstraint
- ChoiceConstraint
- GrammarConstraint
- TypeConstraint

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
