---
agent: "8ql"
description: "Fallback rules and operational constraints for the 8ql agent."
---

# Base Rules: 8ql

These rules act as a resilient fallback for the `@8ql` agent. 
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
    Do not perform tasks outside the explicit capabilities of `@8ql`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

**Pattern:** `SandboxViolationError.reason` exposes allowlist contents
**Root cause:** `_validate_path()` includes `self._sandbox.allowed_paths` in the reason string for debugging convenience. In a multi-agent environment this gives an untrusted agent knowledge of all allowed directories upon triggering a violation.
- Lesson: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Lesson: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` must be prevented with paired updates and immediate validation.
- Lessons written: 0
- Lessons written: 0 (existing lesson retained as CANDIDATE)
- Lessons written: 0 (no new recurring pattern beyond existing entries)
- Lessons written: 0 (no new recurring pattern)
- Lessons written: 0 (no new recurring patterns)
- Lessons written: 1
- Lessons written: 1 (`8ql.memory.md`)
- Lessons written: 1 (allowlist exposure in error reason field — new, recurrence 1)
- Lessons written: 1 (get_event_loop pattern → 6code.memory.md)
- Lessons written: 1 (rerun evidence capture pattern)
- Lessons written: 2 (`6code.memory.md`, `5test.memory.md`)
- Lessons written: 2 (`6code.memory.md`, `7exec.memory.md`)
- Lessons written: 2 (`8ql.memory.md`)
- Lessons written: 2 (coverage gate miss, missing test-file reference -> `5test.memory.md`)
- Pattern: Assert-based contract guards in deterministic generator lanes are acceptable as informational security findings when execution context is controlled, but should remain visible.
- Pattern: Blocker-remediation reruns are safest when they include direct single-test proof for the exact failing policy test before full handoff.
- Pattern: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Pattern: Chunked implementation scopes create closure ambiguity when undelivered plan tasks are not listed in `## Deferred Items`.
- Pattern: Design acceptance tables can diverge from plan/test/code artifacts when contract-level requirements are added in design but not propagated.
- Pattern: Final rust quality gates fail when requested package selector is not resolvable from current workspace.
- Pattern: Gateway closure is stable when branch gate, scoped selector rerun, docs policy, ADR governance, and py_compile are all executed in one deterministic pass.
- Pattern: Hotfix workflow rollbacks can be safely released even when unrelated baseline placeholder debt persists, provided exact blocker rerun is documented and full pre-commit is green.
- Pattern: In bounded backend auth slices, combine focused Ruff-S + exact selector rerun + line-level token/persistence grep evidence to avoid false blockers from unrelated modules.
- Pattern: Including `.rs` files in Python Ruff checks creates parser noise and false quality blockers.
- Pattern: New project `*.git.md` artifacts can be created without modern Branch Plan sections, causing policy-gate failures in execution and quality stages.
- Pattern: Project initialization scope boundary text can drift from downstream implementation scope, creating governance ambiguity at handoff.
- Pattern: Registry lane drift between `docs/project/kanban.json` and `docs/project/kanban.md` can survive until governance validation is run at @8ql.
- Pattern: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` can recur even after prior remediation if lane updates are not validated at project close.
- Pattern: Reopened gates can be unblocked by aligning Rust validation to project-scope workspace integrity checks instead of package-targeted strict lint commands when scope objective is contract verification.
- Pattern: Ruff S101 findings in pytest-only contract tests should be dispositioned as informational when execution selectors and governance gates are green.
- Pattern: Wave allowlist expansion can expose transitive strict-lane typing errors outside directly edited files.
- Pattern: Workflow syntax checks must use YAML-aware parsing/linting rather than Python compilation when the artifact is `.yml`.
- Pattern: `pip-audit --output json` is not reliable across environments; explicit `-f json` is required for machine-readable comparison.
- Root cause: A requested command attempted `py_compile` against YAML, which is syntactically invalid for Python by design.
- Root cause: AC updates in design (`/readyz` degraded 503 path) were not reflected in plan tasks, tests, or implementation evidence.
- Root cause: Command used `-p pyagent-crdt --all-features` against a package/workspace configuration that does not accept that selector.
- Root cause: Downstream artifact updates did not migrate the git summary template to the required modern branch-plan format.
- Root cause: Earlier gate used strict `clippy -p` package selectors that were not aligned with project-scope integrity objective.
- Root cause: Lifecycle lane transition was not synchronized across both registry sources before @8ql gate.
- Root cause: Lint command mixed Rust and Python sources.
- Root cause: Newly allowlisted core modules pull in `src/transactions/*` dependencies with pre-existing typing debt.
- Root cause: None (all required checks passed).
- Root cause: Output-format flag mismatch produced table output and broke JSON baseline parsing.
- Root cause: Prior @7exec blocker depended on repository-wide placeholder policy findings outside project boundary.
- Root cause: Prior blocker confidence relied on downstream notes before direct rerun in @8ql.
- Root cause: Registry updates in one representation were not mirrored in the other.
- Root cause: Repository files can contain unrelated lint findings (e.g., simulation randomness) in the same modified file.
- Root cause: Ruff S101 flags assert usage even in deterministic artifact/test lanes.
- Root cause: Security lint rule set includes assertion checks that are expected in pytest test lanes.
- Root cause: `code.md` reported DONE for Chunk A but did not explicitly defer T007-T011.
- Root cause: `project.md` retained @1project-only scope boundary while later phases correctly modified production and test files for planned slice delivery.
- Root cause: committed baseline lagged current environment audit state.

### Learned Rules & Historical Patterns

**Pattern:** `SandboxViolationError.reason` exposes allowlist contents
**Root cause:** `_validate_path()` includes `self._sandbox.allowed_paths` in the reason string for debugging convenience. In a multi-agent environment this gives an untrusted agent knowledge of all allowed directories upon triggering a violation.
- Lesson: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Lesson: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` must be prevented with paired updates and immediate validation.
- Lessons written: 0
- Lessons written: 0 (existing lesson retained as CANDIDATE)
- Lessons written: 0 (no new recurring pattern beyond existing entries)
- Lessons written: 0 (no new recurring pattern)
- Lessons written: 0 (no new recurring patterns)
- Lessons written: 1
- Lessons written: 1 (`8ql.memory.md`)
- Lessons written: 1 (allowlist exposure in error reason field — new, recurrence 1)
- Lessons written: 1 (get_event_loop pattern → 6code.memory.md)
- Lessons written: 1 (rerun evidence capture pattern)
- Lessons written: 2 (`6code.memory.md`, `5test.memory.md`)
- Lessons written: 2 (`6code.memory.md`, `7exec.memory.md`)
- Lessons written: 2 (`8ql.memory.md`)
- Lessons written: 2 (coverage gate miss, missing test-file reference -> `5test.memory.md`)
- Pattern: Assert-based contract guards in deterministic generator lanes are acceptable as informational security findings when execution context is controlled, but should remain visible.
- Pattern: Blocker-remediation reruns are safest when they include direct single-test proof for the exact failing policy test before full handoff.
- Pattern: CVE baseline drift can emerge as non-project-specific debt and still requires explicit owner and closure criteria.
- Pattern: Chunked implementation scopes create closure ambiguity when undelivered plan tasks are not listed in `## Deferred Items`.
- Pattern: Design acceptance tables can diverge from plan/test/code artifacts when contract-level requirements are added in design but not propagated.
- Pattern: Final rust quality gates fail when requested package selector is not resolvable from current workspace.
- Pattern: Gateway closure is stable when branch gate, scoped selector rerun, docs policy, ADR governance, and py_compile are all executed in one deterministic pass.
- Pattern: Hotfix workflow rollbacks can be safely released even when unrelated baseline placeholder debt persists, provided exact blocker rerun is documented and full pre-commit is green.
- Pattern: In bounded backend auth slices, combine focused Ruff-S + exact selector rerun + line-level token/persistence grep evidence to avoid false blockers from unrelated modules.
- Pattern: Including `.rs` files in Python Ruff checks creates parser noise and false quality blockers.
- Pattern: New project `*.git.md` artifacts can be created without modern Branch Plan sections, causing policy-gate failures in execution and quality stages.
- Pattern: Project initialization scope boundary text can drift from downstream implementation scope, creating governance ambiguity at handoff.
- Pattern: Registry lane drift between `docs/project/kanban.json` and `docs/project/kanban.md` can survive until governance validation is run at @8ql.
- Pattern: Registry lane mismatch between `data/projects.json` and `docs/project/kanban.md` can recur even after prior remediation if lane updates are not validated at project close.
- Pattern: Reopened gates can be unblocked by aligning Rust validation to project-scope workspace integrity checks instead of package-targeted strict lint commands when scope objective is contract verification.
- Pattern: Ruff S101 findings in pytest-only contract tests should be dispositioned as informational when execution selectors and governance gates are green.
- Pattern: Wave allowlist expansion can expose transitive strict-lane typing errors outside directly edited files.
- Pattern: Workflow syntax checks must use YAML-aware parsing/linting rather than Python compilation when the artifact is `.yml`.
- Pattern: `pip-audit --output json` is not reliable across environments; explicit `-f json` is required for machine-readable comparison.
- Root cause: A requested command attempted `py_compile` against YAML, which is syntactically invalid for Python by design.
- Root cause: AC updates in design (`/readyz` degraded 503 path) were not reflected in plan tasks, tests, or implementation evidence.
- Root cause: Command used `-p pyagent-crdt --all-features` against a package/workspace configuration that does not accept that selector.
- Root cause: Downstream artifact updates did not migrate the git summary template to the required modern branch-plan format.
- Root cause: Earlier gate used strict `clippy -p` package selectors that were not aligned with project-scope integrity objective.
- Root cause: Lifecycle lane transition was not synchronized across both registry sources before @8ql gate.
- Root cause: Lint command mixed Rust and Python sources.
- Root cause: Newly allowlisted core modules pull in `src/transactions/*` dependencies with pre-existing typing debt.
- Root cause: None (all required checks passed).
- Root cause: Output-format flag mismatch produced table output and broke JSON baseline parsing.
- Root cause: Prior @7exec blocker depended on repository-wide placeholder policy findings outside project boundary.
- Root cause: Prior blocker confidence relied on downstream notes before direct rerun in @8ql.
- Root cause: Registry updates in one representation were not mirrored in the other.
- Root cause: Repository files can contain unrelated lint findings (e.g., simulation randomness) in the same modified file.
- Root cause: Ruff S101 flags assert usage even in deterministic artifact/test lanes.
- Root cause: Security lint rule set includes assertion checks that are expected in pytest test lanes.
- Root cause: `code.md` reported DONE for Chunk A but did not explicitly defer T007-T011.
- Root cause: `project.md` retained @1project-only scope boundary while later phases correctly modified production and test files for planned slice delivery.
- Root cause: committed baseline lagged current environment audit state.
