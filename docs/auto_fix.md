# Auto-Fix Library

This document describes the new `auto_fix` Python package which provides a
modular framework for automatically correcting code/style issues detected by
rule definitions.

## Components

* `RuleEngine` – evaluates rules against file contents and returns `Fix`
  objects.
* `TransactionManager` – applies edits inside a transactional context; commits
  each batch to Git and supports rollback.
* `AutoFixLogger` – records planned changes and formats a dry-run report.
* `cli` – simple command-line interface (`auto-fix`) exposing dry-run and
  apply modes.

## Usage

Install the package as part of the `pyagent` project. Then run:

```sh
python -m auto_fix.cli --rules rules/ --dry-run
```

or to apply fixes:

```sh
python -m auto_fix.cli --rules rules/ --apply
```

The `--dry-run` flag prints a summary of proposed modifications without
mutating any files.

## Rule Format

Rules live in the `rules/` directory and must implement the `Rule` protocol
(copying the interface from `auto_fix.rule_engine`). At minimum a Python file
returning objects with a `check` method is acceptable. Future versions may
support JSON/YAML rule definitions.

## Safety

The library uses a hybrid rollback strategy: file edits are wrapped in a
`StateTransaction` (which can undo file system changes) and every commit is
also staged to Git, allowing `git reset` to revert if needed. Always run
`git status` before invoking the CLI to ensure a clean working tree.

## Extending

To add a new rule, create a module under `rules/` implementing `Rule.check`
and returning one or more `Fix` objects. See `tests/` for examples of how
rules are exercised.
