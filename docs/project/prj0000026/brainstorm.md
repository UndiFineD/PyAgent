# Design: 100% Test Coverage & Quality Tooling

**Date:** 2026-03-10

## Objective

Raise the repository Coverage


**Primary goal:** achieve 100% line coverage across all Python modules in `src/` and introduce a parallel static-analysis/linting regimen for both Python and Rust.

This effort will:

- eliminate blind spots in the codebase,
- surface hidden bugs through tests,
- enforce consistent style and type safety,
- make future contributions safer and easier to review.

## Scope & Metrics

1. **Coverage target:** 100% coverage per file.  Existing report shows gaps in:
   - `src/chat/api.py` 91%
   - `src/core/providers/FlmChatAdapter.py` 95%
   - various `tools/*.py` files at ~50%
   - many small modules with single-line misses.
2. **Static analysis:** ruff, mypy (`--strict`), flake8 for Python; `cargo clippy -D warnings` and `cargo fmt -- --check` for Rust.
3. **CI gating:** failing any test or linter stops merge; pre-commit hooks provide local feedback.

## Testing Strategy

Use an *incremental, file-by-file* expansion:

- Review coverage report to identify missing statements and branches.
- Add a corresponding pytest file under `tests/` per module. Mocks/stubs will satisfy dependencies (e.g. fake OpenAI client for `FlmChatAdapter`).
- Special cases: many `tools/*.py` modules share identical structure; after manual core tests, use helpers from `scripts-old` to auto-generate test skeletons and then fill assertion logic.
- Once a module reaches 100%, mark it in a maintenance checklist. CI ensures no regressions.

## Static Analysis & Linters

Configuration placed alongside existing project files:

- `pyproject.toml` to configure ruff and black rules.
- `mypy.ini` with `[mypy]` strict options and `src/` included.
- Optionally `setup.cfg` for flake8 if still needed.
- `pre-commit.yml` with ruff, mypy, black hooks.

Rust side:

- Add a `rust` job in CI running `cargo fmt -- --check` and `cargo clippy`.
- Keep the existing `rust_core/tests` but eventually consider coverage tooling like `cargo tarpaulin` if cross-language consistency becomes important.

## CI Integration

New GitHub Actions workflows:

```yaml
name: Quality
on: [push, pull_request]
jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: {python-version: '3.14'}
      - run: python -m pip install -r requirements-dev.txt
      - run: ruff .
      - run: mypy src/
      - run: pytest --maxfail=1 --disable-warnings --cov=src --cov-fail-under=100
  rust:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rs/toolchain@v1
        with: {profile: minimal, toolchain: stable, target: x86_64-unknown-linux-gnu}
      - run: cargo fmt -- --check
      - run: cargo clippy -- -D warnings
      - run: cargo test --release
```

- `push` or `PR` to any branch triggers checks; failures block merging.

## Workflow & Maintenance

1. Begin with the most critical modules (core providers, tools, workflow engine).
2. Add mocks and fixtures as needed; keep them minimal and reusable.
3. After each file is covered, move to the next until all 659 statements are tested.
4. Periodically run `ruff`/`mypy` locally or via pre-commit to prevent drift.
5. Document the process in `docs/` or contributing guide so reviewers know how to maintain quality.

## Rust Parallels

- Leverage existing `rust_core/` tests; add missing unit tests when new functionality appears.
- Require clippy/format checks in CI; these provide the "100%" analogue since coverage is not being measured yet.

## Approval & Next Steps

Once this design is approved, we will generate an implementation plan listing concrete tasks (write tests for each file, configure linters, create workflows) and work through them sequentially.

---

That completes the design draft. Please confirm whether it matches your expectations or suggest revisions before we proceed to planning.