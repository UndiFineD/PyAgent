# Development Tools & Utilities Design

All checklist items open; this document centralizes them and comments on their placement relative to `src`.

## Tasks

- Create project-specific development tools
- Implement code formatting and linting rules
- Develop code quality analysis scripts
- Create project-specific shell scripts
- Implement version control configuration
- Develop project-specific automation scripts

## Classification in `src`

- Utility modules that aid development can reside under `src/tools/` or `src/utils/` to keep them importable by other code.
- Configuration files for linters/formatters (`.prettierrc`, `pyproject.toml` sections, `.flake8`) live at repo root but may be referenced by a `src/tools/lint.py` script.
- Automation scripts (build assistants, analysis) are often kept in `scripts/` but may import helper functions from `src/` when they need to programmatically inspect the codebase.

## Notes

This design ensures that developer-facing tooling is maintained alongside production code so it can be versioned and tested.