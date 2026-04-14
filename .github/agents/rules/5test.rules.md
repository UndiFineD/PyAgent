---
agent: "5test"
description: "Fallback rules and operational constraints for the 5test agent."
---

# Base Rules: 5test

These rules act as a resilient fallback for the `@5test` agent. 
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
    Do not perform tasks outside the explicit capabilities of `@5test`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

**Pattern:** Coverage gate for a new module failed target (`src/core/audit` at 83.07% vs required >=90%).
**Pattern:** Plan validation commands referenced a non-existent test file (`tests/test_AuditExceptions.py`).
**Root cause:** Test artifact and plan command set diverged during implementation, but command list was not reconciled.
**Root cause:** Test suite emphasized contract path coverage but left multiple negative/error and no-core branches untested in `AuditTrailCore`, `AuditEvent`, and `AuditTrailMixin`.
- Pattern: Artifact-first completion can safely unblock implementation contracts when selector determinism and weak-test gates are explicit.
- Pattern: Chunk handoff quality degrades without a mandatory AC-to-test matrix and weak-test gate record.
- Pattern: Coverage-policy tests are stronger when they parse `pyproject.toml` and assert numeric thresholds instead of string presence.
- Pattern: Deterministic selector ordering and explicit failure-shape contracts are required to avoid weak red evidence in interface migration projects.
- Pattern: Deterministic selector ordering plus explicit forbidden red signatures prevents false red evidence and weak contract handoff.
- Pattern: Docs-only red contracts are strongest when each AC maps to one assertion-focused selector and one aggregate selector.
- Pattern: Frontend ACs (empty ideas state and local ideas filter behavior) were documented in plan/design but not represented in the final test file despite passing integration tests.
- Pattern: OpenAPI drift red contracts are strongest when one selector proves the committed artifact is missing or stale and another proves parity checks stay read-only.
- Pattern: RED docs-policy assertions should target implementation-facing workflow and execution artifacts, not only plan text that may already satisfy requirements.
- Pattern: RED tests that encode fail-closed gateway contracts reveal runtime exception propagation and policy bypass paths immediately.
- Pattern: RED-first gateway tests should encode orchestration invariants with dependency stubs and explicit contract-loader failures.
- Pattern: Red contracts for new route families are strongest when tests assert concrete status/payload behavior against real endpoints and fail on 404/contract mismatches.
- Pattern: Red-phase benchmark contracts are strongest when they validate Cargo wiring, Criterion macros, and CI command semantics as text-level structure checks.
- Pattern: Red-phase planning without immediate test file authoring requires explicit "not-ready" handoff semantics.
- Pattern: Red-phase suites are strongest when they assert behavior plus migration metadata in the same test path.
- Pattern: Red-phase tests can appear weak if they fail only on missing imports during collection.
- Pattern: Regression matrices that validate both dockerfile value and filesystem existence expose latent compose drift reliably.
- Pattern: Security workflow contracts are strongest when tests validate trigger shape, permissions, and CodeQL init arguments instead of only job existence.
- Pattern: Trigger contracts become weak when wildcard branch filters are too broad (`prj*`) to encode branch policy intent.
- Pattern: Workspace-migration red contracts are strongest when they combine TOML structure checks for workspace membership and patch ownership with lockfile singleton assertions.
- Root cause: AMD NPU guidance lacks canonical marker, command parity, fallback semantics, environment boundary, evidence schema, and defer/non-goals language.
- Root cause: Contract suites that import future modules directly trigger collection-time `ImportError` and mask expected behavior assertions.
- Root cause: Current Rust layout is mixed standalone crates with member lockfiles and crate-local patch governance, not root-workspace governance.
- Root cause: Early red drafts can drift toward symbol-existence checks if canonical modules are not yet present.
- Root cause: Existing CI trigger accepted ambiguous wildcard and lacked explicit required-check identity naming contract.
- Root cause: Fleet compose references deploy/Dockerfile.fleet, but that file is absent in repository.
- Root cause: GatewayCore.handle currently lacks budget-denied short-circuit, provider exception guard, and telemetry emit_result degradation guard.
- Root cause: Lifecycle handoffs can drift when AC mapping and failing signatures are implicit.
- Root cause: No scheduled security workflow file exists yet, so all contract selectors fail as intended in red phase.
- Root cause: Phase-one auth-session routes and persistence behavior are not implemented yet.
- Root cause: Plan/design documented strict and promotion contracts, but workflow and execution artifacts did not yet encode them.
- Root cause: Preparation task can be mistaken for completed red phase when selectors are listed but not executed.
- Root cause: Presence-only checks can stay green while enforcement remains ineffective (`fail_under` too low or unused in CI).
- Root cause: Red-phase work can be marked complete without clear failure-shape constraints, causing ambiguous @6code targets.
- Root cause: Repository has no Criterion dev-dependency, no stats benchmark harness file, and no CI smoke benchmark command yet.
- Root cause: Test artifacts often summarize failures but do not prove AC coverage or test-strength checks.
- Root cause: Test scope converged on happy-path render + failure-isolation assertions and did not re-check full AC matrix at final handoff.
- Root cause: The repository exposes backend.app.openapi() at runtime, but the phase-one generator and committed backend artifact do not exist yet.
- Root cause: Without explicit failure-shape constraints, red phase can pass with import/existence checks that do not verify CRDT semantics.
- Root cause: `src.core.gateway.gateway_core` contract module/class does not exist yet.
- avoid importing src.github_app or src.chat.api in the generator, test lane, or CI selector

### Learned Rules & Historical Patterns

**Pattern:** Coverage gate for a new module failed target (`src/core/audit` at 83.07% vs required >=90%).
**Pattern:** Plan validation commands referenced a non-existent test file (`tests/test_AuditExceptions.py`).
**Root cause:** Test artifact and plan command set diverged during implementation, but command list was not reconciled.
**Root cause:** Test suite emphasized contract path coverage but left multiple negative/error and no-core branches untested in `AuditTrailCore`, `AuditEvent`, and `AuditTrailMixin`.
- Pattern: Artifact-first completion can safely unblock implementation contracts when selector determinism and weak-test gates are explicit.
- Pattern: Chunk handoff quality degrades without a mandatory AC-to-test matrix and weak-test gate record.
- Pattern: Coverage-policy tests are stronger when they parse `pyproject.toml` and assert numeric thresholds instead of string presence.
- Pattern: Deterministic selector ordering and explicit failure-shape contracts are required to avoid weak red evidence in interface migration projects.
- Pattern: Deterministic selector ordering plus explicit forbidden red signatures prevents false red evidence and weak contract handoff.
- Pattern: Docs-only red contracts are strongest when each AC maps to one assertion-focused selector and one aggregate selector.
- Pattern: Frontend ACs (empty ideas state and local ideas filter behavior) were documented in plan/design but not represented in the final test file despite passing integration tests.
- Pattern: OpenAPI drift red contracts are strongest when one selector proves the committed artifact is missing or stale and another proves parity checks stay read-only.
- Pattern: RED docs-policy assertions should target implementation-facing workflow and execution artifacts, not only plan text that may already satisfy requirements.
- Pattern: RED tests that encode fail-closed gateway contracts reveal runtime exception propagation and policy bypass paths immediately.
- Pattern: RED-first gateway tests should encode orchestration invariants with dependency stubs and explicit contract-loader failures.
- Pattern: Red contracts for new route families are strongest when tests assert concrete status/payload behavior against real endpoints and fail on 404/contract mismatches.
- Pattern: Red-phase benchmark contracts are strongest when they validate Cargo wiring, Criterion macros, and CI command semantics as text-level structure checks.
- Pattern: Red-phase planning without immediate test file authoring requires explicit "not-ready" handoff semantics.
- Pattern: Red-phase suites are strongest when they assert behavior plus migration metadata in the same test path.
- Pattern: Red-phase tests can appear weak if they fail only on missing imports during collection.
- Pattern: Regression matrices that validate both dockerfile value and filesystem existence expose latent compose drift reliably.
- Pattern: Security workflow contracts are strongest when tests validate trigger shape, permissions, and CodeQL init arguments instead of only job existence.
- Pattern: Trigger contracts become weak when wildcard branch filters are too broad (`prj*`) to encode branch policy intent.
- Pattern: Workspace-migration red contracts are strongest when they combine TOML structure checks for workspace membership and patch ownership with lockfile singleton assertions.
- Root cause: AMD NPU guidance lacks canonical marker, command parity, fallback semantics, environment boundary, evidence schema, and defer/non-goals language.
- Root cause: Contract suites that import future modules directly trigger collection-time `ImportError` and mask expected behavior assertions.
- Root cause: Current Rust layout is mixed standalone crates with member lockfiles and crate-local patch governance, not root-workspace governance.
- Root cause: Early red drafts can drift toward symbol-existence checks if canonical modules are not yet present.
- Root cause: Existing CI trigger accepted ambiguous wildcard and lacked explicit required-check identity naming contract.
- Root cause: Fleet compose references deploy/Dockerfile.fleet, but that file is absent in repository.
- Root cause: GatewayCore.handle currently lacks budget-denied short-circuit, provider exception guard, and telemetry emit_result degradation guard.
- Root cause: Lifecycle handoffs can drift when AC mapping and failing signatures are implicit.
- Root cause: No scheduled security workflow file exists yet, so all contract selectors fail as intended in red phase.
- Root cause: Phase-one auth-session routes and persistence behavior are not implemented yet.
- Root cause: Plan/design documented strict and promotion contracts, but workflow and execution artifacts did not yet encode them.
- Root cause: Preparation task can be mistaken for completed red phase when selectors are listed but not executed.
- Root cause: Presence-only checks can stay green while enforcement remains ineffective (`fail_under` too low or unused in CI).
- Root cause: Red-phase work can be marked complete without clear failure-shape constraints, causing ambiguous @6code targets.
- Root cause: Repository has no Criterion dev-dependency, no stats benchmark harness file, and no CI smoke benchmark command yet.
- Root cause: Test artifacts often summarize failures but do not prove AC coverage or test-strength checks.
- Root cause: Test scope converged on happy-path render + failure-isolation assertions and did not re-check full AC matrix at final handoff.
- Root cause: The repository exposes backend.app.openapi() at runtime, but the phase-one generator and committed backend artifact do not exist yet.
- Root cause: Without explicit failure-shape constraints, red phase can pass with import/existence checks that do not verify CRDT semantics.
- Root cause: `src.core.gateway.gateway_core` contract module/class does not exist yet.
- avoid importing src.github_app or src.chat.api in the generator, test lane, or CI selector
