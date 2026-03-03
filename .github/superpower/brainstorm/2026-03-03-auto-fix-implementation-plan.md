# Implementation Plan: Modular Auto-Fix Library

This document captures the actionable steps derived from the approved design:
refactor the existing auto-fix script into a modular Python library with hybrid
rollback safety and a dry-run preview mode.

## 1. Repository Structure

1. Create package `src/auto_fix/` with the following stub modules:
   - `__init__.py`
   - `rule_engine.py`
   - `transaction.py`
   - `logger.py`
   - `cli.py` (command‑line entrypoints)

2. Update `pyproject.toml`/`setup.cfg` as necessary to expose the new package.

## 2. Core Components

### RuleEngine

* Define `Rule` dataclass/interface with `apply`/`check` methods.
* Implement loader that reads JSON/YAML/py rule definitions from `rules/`.
* Evaluation pipeline returning `Fix` objects containing file path and edit.

### TransactionManager

* Wrap edits with `StateTransaction` (existing utility).
* On commit, stage affected files and create a descriptive git commit.
* Provide methods `begin()`, `commit()`, `rollback()` and context manager API.

### Logger / Preview

* Implement `AutoFixLogger` recording planned changes.
* Support formatting previews as console tables or JSON structures.
* Respect `--dry-run` flag: engine runs but transaction commits are skipped.

## 3. Hybrid Rollback Strategy

* TransactionManager integrates with Git: after each `commit()` create a
  temporary branch or commit that can be reset.
* Ensure clean working tree before running; abort if uncommitted changes exist.

## 4. Script Refactor

* Rewrite `scripts/auto_fix_pytest_issues.py` to call library components.
* Provide CLI parameters: `--dry-run`, `--apply`, `--rules=<path>`,
  `--verbose`.
* Add entry point in `setup.py` or `pyproject.toml` for `auto-fix` command.

## 5. Testing

* Unit tests:
  - `tests/test_rule_engine.py`
  - `tests/test_transaction.py`
  - `tests/test_logger.py`
  - `tests/test_cli.py` (dry-run vs apply modes)
* Integration tests using `tempfile` repo fixtures to simulate git rollback.
* Add rollback and error scenarios to CI.

## 6. Documentation

* Update main README with library overview and CLI usage examples.
* Add `docs/auto_fix.md` describing rule format, how to author rules, and
  safety precautions.
* Include dry-run sample output and explanation of git commits.

## 7. Continuous Integration

* Add new test files to existing `run_all_tests.py` and CI workflow.
* Ensure linting and type checking run on new modules.
* Optionally include a nightly job that runs the auto-fixer in dry-run mode
  against the repo and reports proposed changes.

## 8. Iteration and Rollout

1. Prototype library and migrate a subset of current rules.
2. Exercise tool on a branch; inspect commit history and dry-run reports.
3. Adjust logging verbosity and rule loader flexibility based on feedback.
4. Gradually convert remaining scripts (e.g. lint auto-fixes) to use the
   new library.

---

This plan aligns with the design and establishes a clear path to
implementation. Tasks may be broken into individual GitHub issues as needed.