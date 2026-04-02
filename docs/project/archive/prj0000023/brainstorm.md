# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Testing Infrastructure Design

All items remain unchecked.  This design document outlines the structure and where tests live relative to source code.

## Tasks

- Implement hierarchical test suite structure reflecting `src/`
  modules (e.g. `tests/core/`, `tests/agents/`, `tests/transport/`).
- Create and maintain configuration files (`pytest.ini`, `conftest.py`)
  with common fixtures and markers.
- Establish a reproducible test environment via pyproject/venv, pinning
  dependencies and including utilities like `pytest-asyncio`, coverage,
  and linters.
- Develop test data generation and mocking scripts (under `scripts/`)
  producing fixtures used by integration and unit tests.
- Configure coverage thresholds and automated reporting (Codecov or
  GitHub Actions badge).
- Implement CI/CD workflows that run tests on every PR, enforce
  coverage, and optionally perform security/dependency scans.
- Add specialized test categories:
  - **Workflow tests** exercising `context_manager`, `cort`, and the
    newly built workflow engine.
  - **Performance benchmarks** under `tests/benchmarks/` using the
    benchmarking scaffold from the roadmap plan.
  - **Concurrency & resilience tests** simulating multiple agents
    operating concurrently, verifying the task queue and CORT behaviours.
  - **Tool/skill hot‑reload tests** that create temporary `.agents/skills`
    directories and assert dynamic registration.

## Motivation

Robust automated testing is the foundation for safe incremental
development.  Given the project’s ambition—multi‑agent workflows, recursive
reasoning, and dynamic tool ecosystems—tests must cover not just
algorithms but long‑running stateful interactions, context windowing, and
integration with external components.  A clear infrastructure lowers the
barrier for contributors and is a prerequisite for high‑confidence CI/CD.

## Approaches

1. **Layered directory layout.**  Mirror source packages in `tests/` so
   naming is predictable and code ownership is obvious.  Shared fixtures
   live at top level; domain‑specific fixtures within each test package.
2. **Config templating.**  Generate `pytest.ini` and `conftest.py` via
   a helper script (`scripts/setup_tests.py`) to ensure consistency across
   branches and new repos.
3. **Fixture generators.**  Use data factories (e.g., `pytest-factoryboy`)
   and the `scripts` directory to create realistic payloads for agents and
   workflows.  Generated files are cached under `tests/data/` and cleaned up
   by CI post‑run.
4. **CI matrix.**  Set up GitHub Actions workflows that run tests under
   multiple Python versions, with coverage and linting stages.  Include
   long‑running integration jobs triggered manually for load/performance
   tests.
5. **Context/agent focus.**  Add dedicated subtests for the context manager
   and CORT functionality described in the roadmap; reuse the same
   packages created earlier to avoid duplication.
6. **Tool/skill lifecycle tests.**  Dynamically create, modify, and delete
   skill files during a test run to verify the registry updates as
   specified in the workflow design.

## Success criteria

* `pytest` command run from repository root returns exit code 0
  with >95 % coverage on all core modules.
* CI pipeline fails pull requests that introduce new code without
  accompanying tests or that drop overall coverage.
* New contributors can add a test by following documented patterns and see
  it executed in CI within minutes.
* Automated benchmark tests catch any performance regression relative to
  stored baselines.
* Skill hot‑reload behaviour is exercised regularly in a nightly test
  job, ensuring any refactor to the registry remains functional.

## Dependencies

- `pytest` plus plugins (`pytest-asyncio`, `pytest-cov`, `pytest-mock`).
- `GitHub Actions` or equivalent CI service with matrix support.
- `scripts/` utilities for test setup and data generation.
- Existing packages: `context_manager`, `skills_registry`, `cort`,
  `workflow` modules from earlier plans.
- A lightweight in‑repo vector store (Rust or Python) for context windowing
  tests, if the design chooses persistent indexing.

## Risks & Questions

* Writing high‑quality integration tests is time‑consuming; plan to
  dedicate some sprint capacity for test development.
* Test data may become stale; consider regenerating fixtures on schedule.
* Performance tests in CI may be flaky; keep them separate from the
  fast unit test suite to avoid blocking PRs.
* Security of CI credentials and coverage reports must be managed.  

## Classification in `src`

- `tests/` mirrors `src/` structure; new `tests/benchmarks/` and
  `tests/integration/` subfolders are introduced.
- `tests/conftest.py` will contain global fixtures (e.g. temporary
  `.agents/skills` directories, `ContextManager` instances).
- Helper scripts under `scripts/` produce test fixtures and configure

## Implementation Status

Most of the infrastructure outlined above has now been implemented.  A `scripts/setup_tests.py` helper, comprehensive structure tests, and the context/skills/CORT packages exist.  CI is configured to run the suite and enforce coverage.
  environment variables used by tests (e.g. `TEST_LOG_LEVEL`).

## Notes

This document should evolve alongside the codebase; every major
refactor should include a review of corresponding tests.  Once the
implementation plan is generated and executed, this design will serve as
an anchor for future testing efforts.
## Classification in `src`

- Tests mirror the package layout inside `src/` using the `tests/` directory at repo root.
  For example, `tests/core/`, `tests/agents/`, etc.
- Fixtures and helpers live in `tests/conftest.py` and will import from `src/`.
- Data generation scripts may be placed under `scripts/` but will output fixtures consumed by tests.

## Notes

Testing is vital for all modules in `src`.  The CI configuration will invoke `pytest` against the `tests/` tree and enforce coverage thresholds.

No actual tests exist yet; this document records the intended layout so implementation can track against it.