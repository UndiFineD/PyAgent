---
agent: "9git"
description: "Fallback rules and operational constraints for the 9git agent."
---

# Base Rules: 9git

These rules act as a resilient fallback for the `@9git` agent. 
They may be dynamically updated by `@agentwriter`, 
or superseded by PostgreSQL database records during workflow orchestration.

## Core Constraints
1. **Preserve State**: Always log intermediate work to `.github/agents/data/`.
2. **Acknowledge Overrides**: 
    If the PostgreSQL schema provides a newer rule for a given context, 
    obey the database rule over this file.
3. **Continuous Learning**: 
    If a task fails, analyze the failure signature and propose updates 
    to this file via `@agentwriter` or using your own file editing tools.
4. **Scope Strictness**: 
    Do not perform tasks outside the explicit capabilities of `@9git`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

- Pattern: Ad-hoc PR command variants increase failure rate and duplicate/failed PR attempts under partial auth states.
- Pattern: Dashboard generation side effects must be treated as out-of-scope unless explicitly included by project boundary.
- Pattern: Dashboard refresh consistently introduces broad out-of-scope churn during narrow project closure handoffs.
- Pattern: GH CLI subcommand flags differ across versions (`gh pr view --head` unavailable in this environment).
- Pattern: GitHub CLI authentication can fail when an invalid `GITHUB_TOKEN` environment override is present even with a valid keyring login.
- Pattern: Invalid session-level `GITHUB_TOKEN` can silently flip gh auth active account state and block PR automation.
- Pattern: Mandatory dashboard generation frequently introduces unrelated documentation diffs during project-scoped git handoff.
- Pattern: Mandatory dashboard generation introduces unrelated project-doc churn during scoped @9git closure work.
- Pattern: PR operations blocked by expired or missing GitHub CLI authentication after successful push.
- Pattern: Pre-commit blocked by Python dependency mismatch outside narrowed staging scope.
- Pattern: Project dashboard refresh can stage broad unrelated project docs and must be isolated from narrow handoff scope.
- Pattern: Project handoff quality improves when timeline evidence is captured from the exact stage-labeled commit chain before final @9git commit.
- Pattern: Project-scoped handoff blocked by repository-wide hook baseline debt.
- Pattern: Recording the exact `origin/main..HEAD` timeline before final handoff prevents ambiguity when multiple quality-stage commits exist in close succession.
- Pattern: Session-level `GITHUB_TOKEN` overrides can break gh auth and must be cleared to restore keyring-based authentication.
- Pattern: `rust_core/Cargo.lock` updated silently when `cargo bench` or `cargo clippy --bench` runs; must check `git diff --name-only` before finalizing scope manifest and always include Cargo.lock alongside Cargo.toml changes.
- Root cause: Cargo deterministically regenerates Cargo.lock on any bench/clippy invocation that resolves new deps.
- Root cause: Interpreter environment used by hook resolved `pydantic` with incompatible `pydantic-core` (`2.43.0` vs required `2.41.5`).
- Root cause: Invalid environment token shadowed valid keyring credentials during PR automation.
- Root cause: Local gh version does not support `--head` on `gh pr view`.
- Root cause: Missing deterministic command order and missing preflight auth gate in prior runs.
- Root cause: Parallel stage cadence can produce similar commit subjects (`quality/security gate evidence`) that are hard to disambiguate without timeline capture.
- Root cause: Shell environment override token was stale/invalid while keyring login remained valid.
- Root cause: The dashboard script updates multiple historical project artifacts beyond the active project.
- Root cause: Without explicit stage-to-commit mapping, PR reviewers must reconstruct provenance manually.
- Root cause: `gh` preferred the invalid environment token and returned `HTTP 401` until the override was cleared.
- Root cause: `gh` token/session was invalid for GraphQL API calls (`gh pr view`, `gh pr create`).
- Root cause: `run-precommit-checks` executes `ruff check src tests` without staged-file scoping.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project artifacts globally by design.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project overview files in a single run.
- Root cause: `scripts/generate_project_dashboard.py` updates multiple historical project artifacts as side-effects.
- Root cause: scripts/generate_project_dashboard.py rewrites summary files for many projects outside current scope.

### Learned Rules & Historical Patterns

- Pattern: Ad-hoc PR command variants increase failure rate and duplicate/failed PR attempts under partial auth states.
- Pattern: Dashboard generation side effects must be treated as out-of-scope unless explicitly included by project boundary.
- Pattern: Dashboard refresh consistently introduces broad out-of-scope churn during narrow project closure handoffs.
- Pattern: GH CLI subcommand flags differ across versions (`gh pr view --head` unavailable in this environment).
- Pattern: GitHub CLI authentication can fail when an invalid `GITHUB_TOKEN` environment override is present even with a valid keyring login.
- Pattern: Invalid session-level `GITHUB_TOKEN` can silently flip gh auth active account state and block PR automation.
- Pattern: Mandatory dashboard generation frequently introduces unrelated documentation diffs during project-scoped git handoff.
- Pattern: Mandatory dashboard generation introduces unrelated project-doc churn during scoped @9git closure work.
- Pattern: PR operations blocked by expired or missing GitHub CLI authentication after successful push.
- Pattern: Pre-commit blocked by Python dependency mismatch outside narrowed staging scope.
- Pattern: Project dashboard refresh can stage broad unrelated project docs and must be isolated from narrow handoff scope.
- Pattern: Project handoff quality improves when timeline evidence is captured from the exact stage-labeled commit chain before final @9git commit.
- Pattern: Project-scoped handoff blocked by repository-wide hook baseline debt.
- Pattern: Recording the exact `origin/main..HEAD` timeline before final handoff prevents ambiguity when multiple quality-stage commits exist in close succession.
- Pattern: Session-level `GITHUB_TOKEN` overrides can break gh auth and must be cleared to restore keyring-based authentication.
- Pattern: `rust_core/Cargo.lock` updated silently when `cargo bench` or `cargo clippy --bench` runs; must check `git diff --name-only` before finalizing scope manifest and always include Cargo.lock alongside Cargo.toml changes.
- Root cause: Cargo deterministically regenerates Cargo.lock on any bench/clippy invocation that resolves new deps.
- Root cause: Interpreter environment used by hook resolved `pydantic` with incompatible `pydantic-core` (`2.43.0` vs required `2.41.5`).
- Root cause: Invalid environment token shadowed valid keyring credentials during PR automation.
- Root cause: Local gh version does not support `--head` on `gh pr view`.
- Root cause: Missing deterministic command order and missing preflight auth gate in prior runs.
- Root cause: Parallel stage cadence can produce similar commit subjects (`quality/security gate evidence`) that are hard to disambiguate without timeline capture.
- Root cause: Shell environment override token was stale/invalid while keyring login remained valid.
- Root cause: The dashboard script updates multiple historical project artifacts beyond the active project.
- Root cause: Without explicit stage-to-commit mapping, PR reviewers must reconstruct provenance manually.
- Root cause: `gh` preferred the invalid environment token and returned `HTTP 401` until the override was cleared.
- Root cause: `gh` token/session was invalid for GraphQL API calls (`gh pr view`, `gh pr create`).
- Root cause: `run-precommit-checks` executes `ruff check src tests` without staged-file scoping.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project artifacts globally by design.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project overview files in a single run.
- Root cause: `scripts/generate_project_dashboard.py` updates multiple historical project artifacts as side-effects.
- Root cause: scripts/generate_project_dashboard.py rewrites summary files for many projects outside current scope.
