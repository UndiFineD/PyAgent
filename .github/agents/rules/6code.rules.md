---
agent: "6code"
description: "Fallback rules and operational constraints for the 6code agent."
---

# Base Rules: 6code

These rules act as a resilient fallback for the `@6code` agent. 
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
    Do not perform tasks outside the explicit capabilities of `@6code`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

**Pattern:** Conflicting docstring rules D203/D211 and D212/D213 generate `warning: ... are incompatible` on every ruff run when both members of each pair are active.
**Pattern:** Deprecated ruff config keys — `select` and `ignore` placed directly under `[tool.ruff]` instead of `[tool.ruff.lint]`, producing deprecation warnings on every ruff invocation.
**Pattern:** Import block unsorted (I001) in new Python files — `from pathlib import Path` and `import yaml` placed without a blank line separator between stdlib and third-party groups.
**Pattern:** `asyncio.get_event_loop()` used in an `async` method instead of `asyncio.get_running_loop()`.
**Root cause:** Inconsistent copy-paste between `initialize()` and `_rpc_call()`; `_rpc_call()` was written correctly but `initialize()` retained the deprecated form.
**Root cause:** Rule pairs were not explicitly resolved in the `ignore` list; ruff auto-resolves but still warns.
**Root cause:** `ruff check --select D` was run (docstrings only) but `ruff check --fix` covering all rules was not run before handoff to @7exec.
**Root cause:** pyproject.toml was not re-checked after ruff version upgrade; old key location silently continued to work but emitted warnings.
- Fixed Criterion API contract usage in `rust_core/benches/stats_baseline.rs` by providing the required second argument to `BenchmarkId::new`.
- Fixed lane mismatch using governance command `set-lane --id prj0000105 --lane Review` so kanban markdown matches canonical json lane.
- Pattern: @7exec gate failures can mix policy/doc structure issues with environment-runtime failures that are not code defects.
- Pattern: AC-driven routing work is fastest and safest when a small standalone package is added with deterministic defaults and explicit fallback taxonomy.
- Pattern: Backend OpenAPI contract lanes stay stable when one explicit script owns artifact generation and tests/CI remain read-only drift verifiers.
- Pattern: CI action major-version regressions can break workflow startup before tests, and a narrow rollback to the previous stable major restores execution quickly.
- Pattern: CI coverage governance is stabilized fastest when threshold and gate-path presence/blocking checks are enforced together.
- Pattern: CI threshold values hardcoded in workflow commands drift from canonical config policy values.
- Pattern: Contract tests for CI command text are strict substring checks and require command/path tokens to appear verbatim.
- Pattern: Core-quality gates rely on static filename mapping and top-level `validate()` presence, independent of behavioral test coverage.
- Pattern: Core-quality mapping gates require explicit root-level filename alignment (`tests/test_core_<module_path>.py`) even when deeper behavior tests already exist.
- Pattern: Criterion constructor contracts may tighten by requiring both benchmark name and parameter in `BenchmarkId::new`.
- Pattern: Dependency parity tests are satisfied fastest by a small deterministic CLI pair (generate/check) with explicit remediation output.
- Pattern: Design/plan endpoint-query contract drifted from shipped backend/frontend behavior (`q` and `sort=priority` missing; frontend fetch omitted explicit documented query parameters).
- Pattern: Fail-closed orchestration remains robust when each external boundary (budget, provider, telemetry) has explicit non-raising fallback envelope behavior.
- Pattern: FastAPI route return annotations that union dict payload with `JSONResponse` can fail response-model generation during import-time route registration.
- Pattern: For backend OpenAPI drift selectors, first remediate by re-running the canonical generator before modifying canonicalization logic.
- Pattern: For first-slice orchestration work, constructor-compatible dependency injection plus deterministic fail-closed sequencing enables green tests without overbuilding.
- Pattern: Full-repo validation can fail on project governance doc-policy checks unrelated to the current backend code slice.
- Pattern: Incremental artifact pipelines become rerun-safe when persisted rows are keyed by stable entities (`idea_id`, `(idea_id, reference)`, pair keys) instead of only by batch ID.
- Pattern: Introducing canonical modules plus legacy shims in packages with eager `__init__` exports can create import cycles during test collection.
- Pattern: Missing planned module/test trees can be delivered quickly by creating an isolated package with contract-first deterministic tests mapped directly to AC selectors.
- Pattern: Mixed package+workspace Cargo manifests can satisfy Python install/bench contracts and Rust workspace governance simultaneously when root package metadata is left intact.
- Pattern: New `src/core/**` module sets repeatedly fail shared core-quality gates unless root-level mapped test filenames and top-level `validate()` helpers are added immediately.
- Pattern: Pre-existing formatting drift in legacy test files can block mandatory pre-commit in otherwise clean implementation branches.
- Pattern: Progressive typing rollouts are stable when strict and broad lanes use explicit config authority and distinct CI steps.
- Pattern: Quality blockers on partial chunk delivery are closed fastest by implementing the missing AC selector files directly instead of broad refactors.
- Pattern: Registry parity failures can originate from missing ID placeholders even when current project rows exist in one registry view.
- Pattern: Repository-wide async-loop governance can be violated by introducing explicit `for` loops in synchronous helper functions, even for small deterministic utilities.
- Pattern: Route-level auth session bootstrapping can stay bounded when persistence, rotation, and revocation are encapsulated in a dedicated store module.
- Pattern: Sync `for`/`while` constructs inside synchronous helper methods trigger repository async-loop policy tests even when business behavior is correct.
- Pattern: Sync-loop policy checks also flag explicit loop syntax in helper methods, even when semantics are simple metadata filtering.
- Pattern: Sync-loop policy checks flag explicit `for`/`while` statements inside synchronous functions even when logic is deterministic merge behavior.
- Pattern: Tests that need repository-root `conftest.py` become order-sensitive when they use plain `import conftest` in suites that also load nested `tests/**/conftest.py`.
- Pattern: Validation-first closure can complete implementation phase without touching source when acceptance checks are already satisfied.
- Pattern: When @7exec reports pre-commit formatting drift, run scoped `ruff format` on the exact file and then re-run both selector and `--check` gate.
- Pattern: When selector files are missing, add selector-aligned tests first and keep implementation minimal to those contracts.
- Pattern: YAML workflow contract tests are most reliable when workflow keys are explicit and use stable scalar values for action `with` fields.
- Root cause: @5test artifact defined selectors but physical selector files were absent in workspace.
- Root cause: @5test artifacts provided selector contracts but no physical SAL test/code files existed in this branch.
- Root cause: Backend previously validated JWT/API key only and lacked session lifecycle routes/state.
- Root cause: Behavior tests under `tests/core/base/mixins/` did not satisfy the static filename mapping rule in `tests/test_core_quality.py`.
- Root cause: Canonical mixins imported package-level modules that re-imported legacy shims before canonical module initialization finished.
- Root cause: Chunk A was marked complete while Chunk B artifacts and AC evidence were absent, leaving governance and quality gates red.
- Root cause: Coverage gate step used `--cov-fail-under=40` directly instead of reading policy from `[tool.coverage.report].fail_under` in `pyproject.toml`.
- Root cause: Existing threshold in config was not sufficient because CI had no explicit coverage-gate path.
- Root cause: Formatter drift in `tests/core/gateway/test_gateway_core_orchestration.py` caused pre-commit failure despite passing tests.
- Root cause: Implementation optimized for minimal working path and relied on defaults without re-validating full IFC/plan contract matrix.
- Root cause: Initial Slice 1 implementation used straightforward explicit loops instead of loop-free expression patterns accepted by `tests/test_async_loops.py`.
- Root cause: Initial implementation considerations (`--manifest-path` or directory-local artifact checks) can miss exact string contracts even when behavior is equivalent.
- Root cause: Missing `.github/workflows/security-scheduled.yml` caused contract-test failures across all required assertions.
- Root cause: Module-name collision on `conftest` in `sys.modules` allowed a nested fixture module to shadow root `conftest.py`, so `SessionManager` was missing.
- Root cause: Planned file paths did not exist, so extending unrelated modules would have increased blast radius and slowed validation.
- Root cause: Policy evaluation helper `_evaluate` used an explicit `for` statement instead of an expression-oriented projection/filter.
- Root cause: Prior slices already removed stub behavior and exposed non-empty package APIs.
- Root cause: Pure batch-key replacement leaves room for duplicates when the same ideas are reprocessed with different batch boundaries or rerun configurations.
- Root cause: RED contracts failed because CI lacked explicit strict command/config authority and exec artifacts lacked N=5 promotion markers.
- Root cause: Red contracts failed because workspace membership/patch ownership and lockfile authority were distributed across member crates.
- Root cause: Required command contracts were absent (`scripts/deps` scripts and install/parity text contracts).
- Root cause: Routing package introduced modules with behavior tests under `tests/core/routing/` but without root-level mapped test filenames expected by static gate.
- Root cause: Runtime path lacked budget-denied check, provider exception guard, and telemetry-emission degradation handling.
- Root cause: Runtime-generated OpenAPI output can diverge transiently from the committed artifact due to environment/module state.
- Root cause: Test files diverged from enforced `ruff-format` style prior to this task.
- Root cause: The repository exposed `backend.app.openapi()` at runtime, but no committed backend schema artifact or explicit generator command existed.
- Root cause: Top-level architecture doc sprawl exceeded enforced count policy, while rust_core tests depended on Windows runtime behavior outside repository control.
- Root cause: `BenchmarkId::new` was called with one argument in `stats_baseline.rs`.
- Root cause: `GatewayCore` contract module/class did not exist and orchestration sequence guarantees were absent.
- Root cause: `_deep_merge` used an explicit sorted key iteration loop in a sync helper.
- Root cause: `_redact` used explicit `for` iteration plus a generator predicate within a synchronous function.
- Root cause: `actions/setup-python@v5` fails in the runner with `Maximum call stack size exceeded` during CI / Lightweight setup.
- Root cause: `dict[str, Any] | JSONResponse` annotation is not a valid Pydantic response model type in this app setup.
- Root cause: `docs/project/kanban.json` and `docs/project/kanban.md` drifted from `data/nextproject.md` allocation count (missing `prj0000103` and json-only gap for `prj0000104`).
- Root cause: `src/core/gateway/gateway_core.py` lacked a module-level `validate()` function and no gateway-core test filename matched the expected mapping prefixes.
- Root cause: prj0000098 git artifact template is not yet migrated to required modern Branch Plan sections.

### Learned Rules & Historical Patterns

**Pattern:** Conflicting docstring rules D203/D211 and D212/D213 generate `warning: ... are incompatible` on every ruff run when both members of each pair are active.
**Pattern:** Deprecated ruff config keys — `select` and `ignore` placed directly under `[tool.ruff]` instead of `[tool.ruff.lint]`, producing deprecation warnings on every ruff invocation.
**Pattern:** Import block unsorted (I001) in new Python files — `from pathlib import Path` and `import yaml` placed without a blank line separator between stdlib and third-party groups.
**Pattern:** `asyncio.get_event_loop()` used in an `async` method instead of `asyncio.get_running_loop()`.
**Root cause:** Inconsistent copy-paste between `initialize()` and `_rpc_call()`; `_rpc_call()` was written correctly but `initialize()` retained the deprecated form.
**Root cause:** Rule pairs were not explicitly resolved in the `ignore` list; ruff auto-resolves but still warns.
**Root cause:** `ruff check --select D` was run (docstrings only) but `ruff check --fix` covering all rules was not run before handoff to @7exec.
**Root cause:** pyproject.toml was not re-checked after ruff version upgrade; old key location silently continued to work but emitted warnings.
- Fixed Criterion API contract usage in `rust_core/benches/stats_baseline.rs` by providing the required second argument to `BenchmarkId::new`.
- Fixed lane mismatch using governance command `set-lane --id prj0000105 --lane Review` so kanban markdown matches canonical json lane.
- Pattern: @7exec gate failures can mix policy/doc structure issues with environment-runtime failures that are not code defects.
- Pattern: AC-driven routing work is fastest and safest when a small standalone package is added with deterministic defaults and explicit fallback taxonomy.
- Pattern: Backend OpenAPI contract lanes stay stable when one explicit script owns artifact generation and tests/CI remain read-only drift verifiers.
- Pattern: CI action major-version regressions can break workflow startup before tests, and a narrow rollback to the previous stable major restores execution quickly.
- Pattern: CI coverage governance is stabilized fastest when threshold and gate-path presence/blocking checks are enforced together.
- Pattern: CI threshold values hardcoded in workflow commands drift from canonical config policy values.
- Pattern: Contract tests for CI command text are strict substring checks and require command/path tokens to appear verbatim.
- Pattern: Core-quality gates rely on static filename mapping and top-level `validate()` presence, independent of behavioral test coverage.
- Pattern: Core-quality mapping gates require explicit root-level filename alignment (`tests/test_core_<module_path>.py`) even when deeper behavior tests already exist.
- Pattern: Criterion constructor contracts may tighten by requiring both benchmark name and parameter in `BenchmarkId::new`.
- Pattern: Dependency parity tests are satisfied fastest by a small deterministic CLI pair (generate/check) with explicit remediation output.
- Pattern: Design/plan endpoint-query contract drifted from shipped backend/frontend behavior (`q` and `sort=priority` missing; frontend fetch omitted explicit documented query parameters).
- Pattern: Fail-closed orchestration remains robust when each external boundary (budget, provider, telemetry) has explicit non-raising fallback envelope behavior.
- Pattern: FastAPI route return annotations that union dict payload with `JSONResponse` can fail response-model generation during import-time route registration.
- Pattern: For backend OpenAPI drift selectors, first remediate by re-running the canonical generator before modifying canonicalization logic.
- Pattern: For first-slice orchestration work, constructor-compatible dependency injection plus deterministic fail-closed sequencing enables green tests without overbuilding.
- Pattern: Full-repo validation can fail on project governance doc-policy checks unrelated to the current backend code slice.
- Pattern: Incremental artifact pipelines become rerun-safe when persisted rows are keyed by stable entities (`idea_id`, `(idea_id, reference)`, pair keys) instead of only by batch ID.
- Pattern: Introducing canonical modules plus legacy shims in packages with eager `__init__` exports can create import cycles during test collection.
- Pattern: Missing planned module/test trees can be delivered quickly by creating an isolated package with contract-first deterministic tests mapped directly to AC selectors.
- Pattern: Mixed package+workspace Cargo manifests can satisfy Python install/bench contracts and Rust workspace governance simultaneously when root package metadata is left intact.
- Pattern: New `src/core/**` module sets repeatedly fail shared core-quality gates unless root-level mapped test filenames and top-level `validate()` helpers are added immediately.
- Pattern: Pre-existing formatting drift in legacy test files can block mandatory pre-commit in otherwise clean implementation branches.
- Pattern: Progressive typing rollouts are stable when strict and broad lanes use explicit config authority and distinct CI steps.
- Pattern: Quality blockers on partial chunk delivery are closed fastest by implementing the missing AC selector files directly instead of broad refactors.
- Pattern: Registry parity failures can originate from missing ID placeholders even when current project rows exist in one registry view.
- Pattern: Repository-wide async-loop governance can be violated by introducing explicit `for` loops in synchronous helper functions, even for small deterministic utilities.
- Pattern: Route-level auth session bootstrapping can stay bounded when persistence, rotation, and revocation are encapsulated in a dedicated store module.
- Pattern: Sync `for`/`while` constructs inside synchronous helper methods trigger repository async-loop policy tests even when business behavior is correct.
- Pattern: Sync-loop policy checks also flag explicit loop syntax in helper methods, even when semantics are simple metadata filtering.
- Pattern: Sync-loop policy checks flag explicit `for`/`while` statements inside synchronous functions even when logic is deterministic merge behavior.
- Pattern: Tests that need repository-root `conftest.py` become order-sensitive when they use plain `import conftest` in suites that also load nested `tests/**/conftest.py`.
- Pattern: Validation-first closure can complete implementation phase without touching source when acceptance checks are already satisfied.
- Pattern: When @7exec reports pre-commit formatting drift, run scoped `ruff format` on the exact file and then re-run both selector and `--check` gate.
- Pattern: When selector files are missing, add selector-aligned tests first and keep implementation minimal to those contracts.
- Pattern: YAML workflow contract tests are most reliable when workflow keys are explicit and use stable scalar values for action `with` fields.
- Root cause: @5test artifact defined selectors but physical selector files were absent in workspace.
- Root cause: @5test artifacts provided selector contracts but no physical SAL test/code files existed in this branch.
- Root cause: Backend previously validated JWT/API key only and lacked session lifecycle routes/state.
- Root cause: Behavior tests under `tests/core/base/mixins/` did not satisfy the static filename mapping rule in `tests/test_core_quality.py`.
- Root cause: Canonical mixins imported package-level modules that re-imported legacy shims before canonical module initialization finished.
- Root cause: Chunk A was marked complete while Chunk B artifacts and AC evidence were absent, leaving governance and quality gates red.
- Root cause: Coverage gate step used `--cov-fail-under=40` directly instead of reading policy from `[tool.coverage.report].fail_under` in `pyproject.toml`.
- Root cause: Existing threshold in config was not sufficient because CI had no explicit coverage-gate path.
- Root cause: Formatter drift in `tests/core/gateway/test_gateway_core_orchestration.py` caused pre-commit failure despite passing tests.
- Root cause: Implementation optimized for minimal working path and relied on defaults without re-validating full IFC/plan contract matrix.
- Root cause: Initial Slice 1 implementation used straightforward explicit loops instead of loop-free expression patterns accepted by `tests/test_async_loops.py`.
- Root cause: Initial implementation considerations (`--manifest-path` or directory-local artifact checks) can miss exact string contracts even when behavior is equivalent.
- Root cause: Missing `.github/workflows/security-scheduled.yml` caused contract-test failures across all required assertions.
- Root cause: Module-name collision on `conftest` in `sys.modules` allowed a nested fixture module to shadow root `conftest.py`, so `SessionManager` was missing.
- Root cause: Planned file paths did not exist, so extending unrelated modules would have increased blast radius and slowed validation.
- Root cause: Policy evaluation helper `_evaluate` used an explicit `for` statement instead of an expression-oriented projection/filter.
- Root cause: Prior slices already removed stub behavior and exposed non-empty package APIs.
- Root cause: Pure batch-key replacement leaves room for duplicates when the same ideas are reprocessed with different batch boundaries or rerun configurations.
- Root cause: RED contracts failed because CI lacked explicit strict command/config authority and exec artifacts lacked N=5 promotion markers.
- Root cause: Red contracts failed because workspace membership/patch ownership and lockfile authority were distributed across member crates.
- Root cause: Required command contracts were absent (`scripts/deps` scripts and install/parity text contracts).
- Root cause: Routing package introduced modules with behavior tests under `tests/core/routing/` but without root-level mapped test filenames expected by static gate.
- Root cause: Runtime path lacked budget-denied check, provider exception guard, and telemetry-emission degradation handling.
- Root cause: Runtime-generated OpenAPI output can diverge transiently from the committed artifact due to environment/module state.
- Root cause: Test files diverged from enforced `ruff-format` style prior to this task.
- Root cause: The repository exposed `backend.app.openapi()` at runtime, but no committed backend schema artifact or explicit generator command existed.
- Root cause: Top-level architecture doc sprawl exceeded enforced count policy, while rust_core tests depended on Windows runtime behavior outside repository control.
- Root cause: `BenchmarkId::new` was called with one argument in `stats_baseline.rs`.
- Root cause: `GatewayCore` contract module/class did not exist and orchestration sequence guarantees were absent.
- Root cause: `_deep_merge` used an explicit sorted key iteration loop in a sync helper.
- Root cause: `_redact` used explicit `for` iteration plus a generator predicate within a synchronous function.
- Root cause: `actions/setup-python@v5` fails in the runner with `Maximum call stack size exceeded` during CI / Lightweight setup.
- Root cause: `dict[str, Any] | JSONResponse` annotation is not a valid Pydantic response model type in this app setup.
- Root cause: `docs/project/kanban.json` and `docs/project/kanban.md` drifted from `data/nextproject.md` allocation count (missing `prj0000103` and json-only gap for `prj0000104`).
- Root cause: `src/core/gateway/gateway_core.py` lacked a module-level `validate()` function and no gateway-core test filename matched the expected mapping prefixes.
- Root cause: prj0000098 git artifact template is not yet migrated to required modern Branch Plan sections.
