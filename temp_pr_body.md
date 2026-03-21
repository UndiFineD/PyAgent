## Problem

`maturin develop` fails in CI with:
```
Couldn't find a virtualenv or conda environment
```
`actions/setup-python` provides Python but no virtual environment. `maturin develop` requires `VIRTUAL_ENV` to be set.

## Fix

Add a "Create virtual environment" step that:
1. Creates `.venv` with `python -m venv .venv`
2. Appends `.venv/bin` to `$GITHUB_PATH` so subsequent steps use venv binaries
3. Sets `VIRTUAL_ENV` in `$GITHUB_ENV` so maturin can locate the environment

Unblocks PR #121 (Dependabot cargo bump) and all future PRs that trigger the Rust build step.
