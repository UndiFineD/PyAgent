# Developer Onboarding

Welcome to the PyAgent codebase!  This document will help you get up to
speed quickly.

1. **Read the README** (`README.md`) to understand the project's purpose and
   high‑level architecture.
2. **Follow the setup guide** (`docs/setup.md`) to install prerequisites and
   run the initial test suite.
3. **Explore the directory layout**:
   * `src/` contains Python packages; `rust_core/` holds the Rust FFI crate.
   * `tests/` includes unit and integration tests; `tests/docs/` contains
     documentation validation tests.
   * `scripts/` holds helper utilities for scaffolding and tooling.
   * `.github/superpower/brainstorm/` stores design documents used by the
     Copilot agent.
4. **Writing code**:
   * Follow the coding standards in existing modules (type hints, logging,
     license header).
   * Add new functionality under `src/` and write corresponding tests under
     `tests/`.
   * If you create a new tool, add an entry to `docs/tools.md` and include a
     sentence in the README or guide where appropriate.
5. **Documentation**:
   * Docstrings are used to generate API docs with MkDocs; run
     `mkdocs build` to verify.
   * Architecture diagrams live in `docs/architecture` and are compiled by
     `scripts/compile_diagrams.py`.
6. **Submitting changes**:
   * Use a feature branch (`feature/…`) and push it to your fork.
   * Open a pull request against `main` using conventional commit messages.
   * The CI pipeline will run tests and build docs; address any failures.

Enjoy working on PyAgent!  If you have questions, the design documents in
`.github/superpower/brainstorm` are a great resource, and you can search the
codebase or ask in the project chat.