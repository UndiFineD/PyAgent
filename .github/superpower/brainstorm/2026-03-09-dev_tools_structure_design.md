# Development Tools Structure Design

All checklist items open; this document defines where tools live and classification.

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

## Implementation Status

The file structure described above is already in place in the repository:

* Helper modules appear under `src/tools/` (e.g. `pm`, `roadmap`, `cort`) and
  are importable by tests and scripts.
* Root‑level configuration files for pytest, flake8, and mypy are present
  (`pytest.ini`, `.flake8`, `pyproject.toml`), and no special linting
  utilities are required yet.
* Automation scripts such as `scripts/setup_tests.py`,
  `scripts/generate_test_data.py`, and `scripts/generate_governance_templates.py`
  reside in `scripts/` and import from `src/tools` where necessary.

Given this layout has already been exercised and committed, the structural
principles are validated; future tools should follow these conventions.
