---
agent: "7exec"
description: "Fallback rules and operational constraints for the 7exec agent."
---

# Base Rules: 7exec

These rules act as a resilient fallback for the `@7exec` agent. 
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
    Do not perform tasks outside the explicit capabilities of `@7exec`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

- Fix: add `validate()` call tests in per-module test files
- Fixes applied: None required
- Pattern: Clearing one pre-commit blocker can reveal a subsequent blocking gate in the same shared check pipeline.
- Pattern: Clearing prior failing selectors does not guarantee full-suite readiness; unrelated integration tests can still fail in shared infrastructure modules.
- Pattern: Compose build validation can terminate with context-canceled when the repository sends very large build context in constrained runtime sessions.
- Pattern: Dependency generation can pass parity check while still violating byte-stable no-op contract due case normalization drift.
- Pattern: Deploy-only implementation fixes can still require full runtime conclusive evidence to guard against unrelated integration regressions.
- Pattern: Deterministic @7exec evidence remains stable when branch gate and exact selector order are executed without expanding scope.
- Pattern: Deterministic closure evidence is strongest when suite-specific selectors and scope-diff selectors are captured in one ordered run.
- Pattern: Docs-only projects can achieve full contract closure with deterministic selector validation and documentation content verification.
- Pattern: Docs-policy legacy-file baseline can remain unchanged across project-scoped execution validations and must be recorded as a non-regression blocker.
- Pattern: Even with fully green runtime selectors, shared pre-commit gates can block handoff when test-format drift exists.
- Pattern: Executing the exact prior failing selector first provides deterministic closure evidence and avoids inconclusive full-suite reruns.
- Pattern: Fail-fast full suite can reveal structure-count drift even after targeted blocker tests pass.
- Pattern: Filtered pytest selection (`-k ideas`) can return only deselected tests while still exiting successfully.
- Pattern: Focused health-probe regression bundle remains stable when docs-policy selector is included.
- Pattern: For rerun requests focused on a known contract, targeted selectors plus scoped pre-commit provide deterministic closure when full-suite capture is unstable.
- Pattern: Full-suite async-loop governance gate can block specialized feature handoff even when project selectors are fully green.
- Pattern: Full-suite execution can be blocked by project artifact governance format drift even when backend runtime tests pass.
- Pattern: Full-suite quality gates frequently fail after introducing new core modules unless canonical test mapping and project registry counts are updated in lockstep.
- Pattern: Full-suite runtime commands can return empty terminal output in this environment, yielding inconclusive evidence even when deterministic command syntax is correct.
- Pattern: Full-suite validation can remain inconclusive when repeated KeyboardInterrupt events terminate pytest before normal completion.
- Pattern: Immediate focused rerun after governance artifact repair confirms closure without re-expanding test scope.
- Pattern: Including the exact previously failing conftest selector in the first selector gate provides direct closure evidence before full-suite runtime.
- Pattern: Mandatory pre-commit gate can fail on repository-shared checks even when scoped files appear clean; rerun must target the exact project task files from the remediation set.
- Pattern: New routing modules can satisfy AC selectors while still violating repository-wide async-loop governance tests.
- Pattern: OpenAPI artifact lanes stay stable when execution validation runs generator first and then drift/docs selectors in a fixed order.
- Pattern: Pre-commit shared checks can fail on core-quality contract tests even when target selectors and governance gates are green.
- Pattern: Project-scoped execution evidence can be complete while docs-policy selector remains blocked by legacy baseline gaps outside active project scope.
- Pattern: Project-scoped selector suites can pass while mandatory global placeholder policy still blocks downstream handoff.
- Pattern: Re-running exact prior failing selectors first gives deterministic evidence that blocker fixes are actually closed before broader gates.
- Pattern: Re-running the exact handoff command set with the full pre-commit file list confirms blocker clearance without scope drift.
- Pattern: Re-running the exact previously failing selector before broader gates confirms blocker remediation quickly and prevents false green handoff.
- Pattern: Re-running the exact previously failing selectors first provides fast, deterministic confirmation that blocker remediation actually closed the regression.
- Pattern: Repository-wide async-loop governance can fail on newly added core modules even when all project selectors are green.
- Pattern: Running a targeted deterministic slice immediately after full-suite validation provides fast confidence on the intended change surface.
- Pattern: Running the exact previously failing selector before broad gates gives deterministic blocker-closure evidence and faster triage.
- Pattern: Running the three backend selectors in fixed order provides deterministic phase-one execution confidence for JWT session refresh changes.
- Pattern: SARIF freshness gate can stay stale even when test rerun is executed with `CODEQL_REBUILD=1`.
- Pattern: Scoped `pre-commit run --files` still reports failures from unrelated repository test files.
- Pattern: Security module changes can pass feature tests while still failing global async-loop policy checks.
- Pattern: Validation-first closure can still fail at @7exec due to documentation policy gates in project `*.git.md` artifacts.
- Pattern: Warn-phase rollout gates stay deterministic when run in fixed command order with explicit config files.
- Pattern: `cargo test` for `rust_core` can fail with Windows host-runtime loader errors while Python import still succeeds.
- Pattern: `pip check` reports missing required transitive dependencies in the active env.
- Pattern: `pre-commit run --files <scoped project files>` can still fail due hook behavior that evaluates unrelated repository files.
- Prevention: Keep @7exec closure sequence fixed: branch gate -> targeted suites -> docs gate -> scope diff selectors -> artifact updates.
- Prevention: Keep mandatory order fixed: exact prior failing selectors -> aggregate mixins -> docs policy -> registry governance -> pre-commit on relevant changed files.
- Prevention: Keep mandatory rerun sequence fixed: exact prior failing selector -> dependency gate -> fail-fast full suite -> full non-fail-fast/docs/pre-commit gates.
- Prevention: Keep rerun order fixed: exact prior failing selector -> full fail-fast -> collect-only/full -> docs policy/pre-commit.
- Prevention: Keep the rerun order fixed: prior failing selectors -> aggregate project gate -> docs policy -> pre-commit evidence before security handoff.
- Root cause: Active project git summary omitted required modern `## Branch Plan` section.
- Root cause: Bare ellipsis placeholders exist in `src/` outside the active project scope.
- Root cause: Build context transfer size is large (~1.58 GB), causing cancellation before full image completion.
- Root cause: Clear AC-to-test mapping and explicit documentation content requirements enable rapid contract validation.
- Root cause: Earlier rerun omitted this selector and prior full-suite runs surfaced conftest-related integration breakage.
- Root cause: Earlier rerun was blocked by core-quality failures surfaced through mandatory pre-commit shared checks.
- Root cause: Environment drift left tooling packages partially installed without required deps.
- Root cause: External runtime/host dependency constraints (`0xc0000135`, occasional `0xc0000022`) outside repository source correctness.
- Root cause: Full-suite pass alone can hide uncertainty about whether the explicitly requested scope was exercised in isolation.
- Root cause: Generator output casing policy diverged from committed artifact canonical casing.
- Root cause: Historical artifact `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md` is absent while docs-policy selector still requires it.
- Root cause: Hook chain executes broad checks that are not effectively constrained to scoped file inputs.
- Root cause: Legacy summary file for prj0000005 is missing, and docs-policy selector hard-requires it.
- Root cause: Local/runtime execution path did not regenerate SARIF artifacts before freshness assertion, leaving file mtimes older than 24h.
- Root cause: N/A (no failure observed).
- Root cause: New canonical mixin modules and project row expectations drifted relative to `test_core_quality` mapping checks and kanban/projects governance counters.
- Root cause: New core mixin modules lacked required test-file mapping and top-level `validate()` contract expected by `tests/test_core_quality.py`.
- Root cause: No test names in the target file matched the requested selection expression.
- Root cause: None (all gates passed).
- Root cause: None (all required gates passed).
- Root cause: None (all targeted selectors passed).
- Root cause: None (no failure observed in this run).
- Root cause: Prior @7exec run for prj0000108 was blocked on `tests/test_async_loops.py::test_no_sync_loops`; rerun needed proof of closure before costly full-suite gates.
- Root cause: Prior blocker came from downstream shared checks in pre-commit and required exact command parity to verify remediation.
- Root cause: Prior blocker was an async-loop policy violation that can reappear unless explicitly revalidated before broader gates.
- Root cause: Prior docs-policy failure was isolated to project git artifact format drift.
- Root cause: Prior execution was blocked by inconclusive full-suite output capture and a transient shared-hook failure.
- Root cause: Prior full validation was blocked by governance and quality selectors plus pre-commit shared checks.
- Root cause: Prior run inherited an E501 violation in `tests/structure/test_kanban.py` detected by shared checks.
- Root cause: Prior run was blocked by deterministic casing drift in generated requirements output.
- Root cause: Project change set resolved a deploy artifact regression and needed full-suite confirmation for stable handoff.
- Root cause: Registry/count assertions in structure tests changed independently from focused rerun targets.
- Root cause: Repository hook configuration executes broad `ruff check src tests` logic during pre-commit, ignoring effective per-file isolation for this gate.
- Root cause: Runtime execution was interrupted externally before fail-fast suite reached a natural pass/fail stop.
- Root cause: Security closure requires both behavior proof (tests) and boundary proof (workflow/source immutability checks).
- Root cause: Sync loop construct in `src/security/secret_guardrail_policy.py` violates repository async policy gate.
- Root cause: `*.git.md` artifact for the active project did not include required modern Branch Plan section.
- Root cause: `classifier_schema.py` introduced a synchronous loop pattern detected by `tests/test_async_loops.py`.
- Root cause: `python -m pytest src/ tests/ -x --tb=short -q` produced no pass/fail stream output twice in tool capture.
- Root cause: `run-precommit-checks` executes `tests/test_core_quality.py`, which now fails on missing quality contracts for `src/core/gateway/gateway_core.py`.
- Root cause: `src/agents/specialization/specialization_telemetry_bridge.py` uses a synchronous loop at line 72, violating `tests/test_async_loops.py` policy.
- Root cause: `src/core/crdt_bridge.py` contains a synchronous loop at line 116 detected by `tests/test_async_loops.py::test_no_sync_loops`; shared pre-commit checks also fail due formatter drift on the same file.
- Root cause: `tests/core/gateway/test_gateway_core_orchestration.py` is not ruff-format clean under shared pre-commit checks.
- Root cause: `tests/test_conftest.py` fails on missing `SessionManager` attribute in `conftest` during full runtime gate.

### Learned Rules & Historical Patterns

- Fix: add `validate()` call tests in per-module test files
- Fixes applied: None required
- Pattern: Clearing one pre-commit blocker can reveal a subsequent blocking gate in the same shared check pipeline.
- Pattern: Clearing prior failing selectors does not guarantee full-suite readiness; unrelated integration tests can still fail in shared infrastructure modules.
- Pattern: Compose build validation can terminate with context-canceled when the repository sends very large build context in constrained runtime sessions.
- Pattern: Dependency generation can pass parity check while still violating byte-stable no-op contract due case normalization drift.
- Pattern: Deploy-only implementation fixes can still require full runtime conclusive evidence to guard against unrelated integration regressions.
- Pattern: Deterministic @7exec evidence remains stable when branch gate and exact selector order are executed without expanding scope.
- Pattern: Deterministic closure evidence is strongest when suite-specific selectors and scope-diff selectors are captured in one ordered run.
- Pattern: Docs-only projects can achieve full contract closure with deterministic selector validation and documentation content verification.
- Pattern: Docs-policy legacy-file baseline can remain unchanged across project-scoped execution validations and must be recorded as a non-regression blocker.
- Pattern: Even with fully green runtime selectors, shared pre-commit gates can block handoff when test-format drift exists.
- Pattern: Executing the exact prior failing selector first provides deterministic closure evidence and avoids inconclusive full-suite reruns.
- Pattern: Fail-fast full suite can reveal structure-count drift even after targeted blocker tests pass.
- Pattern: Filtered pytest selection (`-k ideas`) can return only deselected tests while still exiting successfully.
- Pattern: Focused health-probe regression bundle remains stable when docs-policy selector is included.
- Pattern: For rerun requests focused on a known contract, targeted selectors plus scoped pre-commit provide deterministic closure when full-suite capture is unstable.
- Pattern: Full-suite async-loop governance gate can block specialized feature handoff even when project selectors are fully green.
- Pattern: Full-suite execution can be blocked by project artifact governance format drift even when backend runtime tests pass.
- Pattern: Full-suite quality gates frequently fail after introducing new core modules unless canonical test mapping and project registry counts are updated in lockstep.
- Pattern: Full-suite runtime commands can return empty terminal output in this environment, yielding inconclusive evidence even when deterministic command syntax is correct.
- Pattern: Full-suite validation can remain inconclusive when repeated KeyboardInterrupt events terminate pytest before normal completion.
- Pattern: Immediate focused rerun after governance artifact repair confirms closure without re-expanding test scope.
- Pattern: Including the exact previously failing conftest selector in the first selector gate provides direct closure evidence before full-suite runtime.
- Pattern: Mandatory pre-commit gate can fail on repository-shared checks even when scoped files appear clean; rerun must target the exact project task files from the remediation set.
- Pattern: New routing modules can satisfy AC selectors while still violating repository-wide async-loop governance tests.
- Pattern: OpenAPI artifact lanes stay stable when execution validation runs generator first and then drift/docs selectors in a fixed order.
- Pattern: Pre-commit shared checks can fail on core-quality contract tests even when target selectors and governance gates are green.
- Pattern: Project-scoped execution evidence can be complete while docs-policy selector remains blocked by legacy baseline gaps outside active project scope.
- Pattern: Project-scoped selector suites can pass while mandatory global placeholder policy still blocks downstream handoff.
- Pattern: Re-running exact prior failing selectors first gives deterministic evidence that blocker fixes are actually closed before broader gates.
- Pattern: Re-running the exact handoff command set with the full pre-commit file list confirms blocker clearance without scope drift.
- Pattern: Re-running the exact previously failing selector before broader gates confirms blocker remediation quickly and prevents false green handoff.
- Pattern: Re-running the exact previously failing selectors first provides fast, deterministic confirmation that blocker remediation actually closed the regression.
- Pattern: Repository-wide async-loop governance can fail on newly added core modules even when all project selectors are green.
- Pattern: Running a targeted deterministic slice immediately after full-suite validation provides fast confidence on the intended change surface.
- Pattern: Running the exact previously failing selector before broad gates gives deterministic blocker-closure evidence and faster triage.
- Pattern: Running the three backend selectors in fixed order provides deterministic phase-one execution confidence for JWT session refresh changes.
- Pattern: SARIF freshness gate can stay stale even when test rerun is executed with `CODEQL_REBUILD=1`.
- Pattern: Scoped `pre-commit run --files` still reports failures from unrelated repository test files.
- Pattern: Security module changes can pass feature tests while still failing global async-loop policy checks.
- Pattern: Validation-first closure can still fail at @7exec due to documentation policy gates in project `*.git.md` artifacts.
- Pattern: Warn-phase rollout gates stay deterministic when run in fixed command order with explicit config files.
- Pattern: `cargo test` for `rust_core` can fail with Windows host-runtime loader errors while Python import still succeeds.
- Pattern: `pip check` reports missing required transitive dependencies in the active env.
- Pattern: `pre-commit run --files <scoped project files>` can still fail due hook behavior that evaluates unrelated repository files.
- Prevention: Keep @7exec closure sequence fixed: branch gate -> targeted suites -> docs gate -> scope diff selectors -> artifact updates.
- Prevention: Keep mandatory order fixed: exact prior failing selectors -> aggregate mixins -> docs policy -> registry governance -> pre-commit on relevant changed files.
- Prevention: Keep mandatory rerun sequence fixed: exact prior failing selector -> dependency gate -> fail-fast full suite -> full non-fail-fast/docs/pre-commit gates.
- Prevention: Keep rerun order fixed: exact prior failing selector -> full fail-fast -> collect-only/full -> docs policy/pre-commit.
- Prevention: Keep the rerun order fixed: prior failing selectors -> aggregate project gate -> docs policy -> pre-commit evidence before security handoff.
- Root cause: Active project git summary omitted required modern `## Branch Plan` section.
- Root cause: Bare ellipsis placeholders exist in `src/` outside the active project scope.
- Root cause: Build context transfer size is large (~1.58 GB), causing cancellation before full image completion.
- Root cause: Clear AC-to-test mapping and explicit documentation content requirements enable rapid contract validation.
- Root cause: Earlier rerun omitted this selector and prior full-suite runs surfaced conftest-related integration breakage.
- Root cause: Earlier rerun was blocked by core-quality failures surfaced through mandatory pre-commit shared checks.
- Root cause: Environment drift left tooling packages partially installed without required deps.
- Root cause: External runtime/host dependency constraints (`0xc0000135`, occasional `0xc0000022`) outside repository source correctness.
- Root cause: Full-suite pass alone can hide uncertainty about whether the explicitly requested scope was exercised in isolation.
- Root cause: Generator output casing policy diverged from committed artifact canonical casing.
- Root cause: Historical artifact `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md` is absent while docs-policy selector still requires it.
- Root cause: Hook chain executes broad checks that are not effectively constrained to scoped file inputs.
- Root cause: Legacy summary file for prj0000005 is missing, and docs-policy selector hard-requires it.
- Root cause: Local/runtime execution path did not regenerate SARIF artifacts before freshness assertion, leaving file mtimes older than 24h.
- Root cause: N/A (no failure observed).
- Root cause: New canonical mixin modules and project row expectations drifted relative to `test_core_quality` mapping checks and kanban/projects governance counters.
- Root cause: New core mixin modules lacked required test-file mapping and top-level `validate()` contract expected by `tests/test_core_quality.py`.
- Root cause: No test names in the target file matched the requested selection expression.
- Root cause: None (all gates passed).
- Root cause: None (all required gates passed).
- Root cause: None (all targeted selectors passed).
- Root cause: None (no failure observed in this run).
- Root cause: Prior @7exec run for prj0000108 was blocked on `tests/test_async_loops.py::test_no_sync_loops`; rerun needed proof of closure before costly full-suite gates.
- Root cause: Prior blocker came from downstream shared checks in pre-commit and required exact command parity to verify remediation.
- Root cause: Prior blocker was an async-loop policy violation that can reappear unless explicitly revalidated before broader gates.
- Root cause: Prior docs-policy failure was isolated to project git artifact format drift.
- Root cause: Prior execution was blocked by inconclusive full-suite output capture and a transient shared-hook failure.
- Root cause: Prior full validation was blocked by governance and quality selectors plus pre-commit shared checks.
- Root cause: Prior run inherited an E501 violation in `tests/structure/test_kanban.py` detected by shared checks.
- Root cause: Prior run was blocked by deterministic casing drift in generated requirements output.
- Root cause: Project change set resolved a deploy artifact regression and needed full-suite confirmation for stable handoff.
- Root cause: Registry/count assertions in structure tests changed independently from focused rerun targets.
- Root cause: Repository hook configuration executes broad `ruff check src tests` logic during pre-commit, ignoring effective per-file isolation for this gate.
- Root cause: Runtime execution was interrupted externally before fail-fast suite reached a natural pass/fail stop.
- Root cause: Security closure requires both behavior proof (tests) and boundary proof (workflow/source immutability checks).
- Root cause: Sync loop construct in `src/security/secret_guardrail_policy.py` violates repository async policy gate.
- Root cause: `*.git.md` artifact for the active project did not include required modern Branch Plan section.
- Root cause: `classifier_schema.py` introduced a synchronous loop pattern detected by `tests/test_async_loops.py`.
- Root cause: `python -m pytest src/ tests/ -x --tb=short -q` produced no pass/fail stream output twice in tool capture.
- Root cause: `run-precommit-checks` executes `tests/test_core_quality.py`, which now fails on missing quality contracts for `src/core/gateway/gateway_core.py`.
- Root cause: `src/agents/specialization/specialization_telemetry_bridge.py` uses a synchronous loop at line 72, violating `tests/test_async_loops.py` policy.
- Root cause: `src/core/crdt_bridge.py` contains a synchronous loop at line 116 detected by `tests/test_async_loops.py::test_no_sync_loops`; shared pre-commit checks also fail due formatter drift on the same file.
- Root cause: `tests/core/gateway/test_gateway_core_orchestration.py` is not ruff-format clean under shared pre-commit checks.
- Root cause: `tests/test_conftest.py` fails on missing `SessionManager` attribute in `conftest` during full runtime gate.
