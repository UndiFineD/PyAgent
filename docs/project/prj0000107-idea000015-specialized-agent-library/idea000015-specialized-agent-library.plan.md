# idea000015-specialized-agent-library - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-31_

## Overview
Implement the Option B hybrid specialized-agent adapter runtime defined by @3design and ADR-0005.
This plan maps AC-SAL-001..AC-SAL-008 to executable, owner-sequenced tasks for @5test, @6code, @7exec, @8ql, and @9git.

## Branch and Scope Gate
- Expected branch: `prj0000107-idea000015-specialized-agent-library`
- Observed branch: `prj0000107-idea000015-specialized-agent-library`
- Branch gate result: PASS
- Scope boundary for this phase: `docs/project/prj0000107-idea000015-specialized-agent-library/` plus `@4plan` memory/log files.
- Explicit constraint: do not modify `docs/project/kanban.json` due to existing local drift.

## Requirements and Constraints
- REQ-SAL-001: Deliver a versioned specialization registry + adapter runtime aligned to Option B design.
- REQ-SAL-002: Keep agent orchestration thin; place domain behavior behind `*Core` contracts.
- SEC-SAL-001: Enforce deny-by-default capability policy with immutable policy evidence fields.
- REL-SAL-001: Fail closed on schema/version/policy faults with deterministic fallback.
- OBS-SAL-001: Emit redacted provenance telemetry with correlation continuity.
- GOV-SAL-001: Each task must include objective, target files, acceptance criteria, and at least one validation command.
- CON-SAL-001: Naming must follow snake_case for files/folders and PascalCase for classes per policy.
- CON-SAL-002: No placeholder deliverables; all planned tasks must produce testable working logic.

## Acceptance Criteria to Task Mapping
| AC | Planned tasks |
|---|---|
| AC-SAL-001 | T-SAL-001, T-SAL-011 |
| AC-SAL-002 | T-SAL-003, T-SAL-012 |
| AC-SAL-003 | T-SAL-004, T-SAL-013 |
| AC-SAL-004 | T-SAL-005, T-SAL-014 |
| AC-SAL-005 | T-SAL-006, T-SAL-015 |
| AC-SAL-006 | T-SAL-007, T-SAL-016 |
| AC-SAL-007 | T-SAL-002, T-SAL-011 |
| AC-SAL-008 | T-SAL-003, T-SAL-012 |

## Chunk Plan

### Chunk A - Registry, Contracts, Adapter, and Policy Core (about 10 code + 10 test files)

- [ ] T-SAL-001 - Implement descriptor schema + registry resolution pipeline (@5test -> @6code)
	- Objective: implement schema-validated specialization descriptor resolution with typed failure taxonomy.
	- Target files: `src/agents/specialization/descriptor_schema.py`, `src/agents/specialization/specialization_registry.py`, `src/agents/specialization/manifest_loader.py`, `tests/agents/specialization/test_descriptor_schema.py`, `tests/agents/specialization/test_specialization_registry.py`
	- Acceptance criteria: schema-valid descriptors resolve; invalid schema returns typed failure reason.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_registry.py -k "resolve or schema"`

- [ ] T-SAL-002 - Add adapter contract version gate (@5test -> @6code)
	- Objective: reject unsupported major `adapter_contract_version` before runtime execution.
	- Target files: `src/agents/specialization/contract_versioning.py`, `src/agents/specialization/specialization_registry.py`, `tests/agents/specialization/test_contract_versioning.py`
	- Acceptance criteria: supported version accepted; incompatible major versions fail with deterministic reason code.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_contract_versioning.py`

- [ ] T-SAL-003 - Build deterministic request mapping adapter (@5test -> @6code)
	- Objective: implement pure deterministic descriptor/context to shell-request mapping.
	- Target files: `src/agents/specialization/adapter_contracts.py`, `src/agents/specialization/specialized_agent_adapter.py`, `tests/agents/specialization/test_specialized_agent_adapter.py`, `tests/agents/specialization/test_manifest_request_parity.py`
	- Acceptance criteria: identical inputs yield byte-equivalent canonical request payload.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialized_agent_adapter.py -k "deterministic or replay"`

- [ ] T-SAL-004 - Implement deny-by-default capability authorization (@5test -> @6code)
	- Objective: enforce allowlist capability matrix and immutable policy evidence fields.
	- Target files: `src/agents/specialization/capability_policy_enforcer.py`, `src/agents/specialization/policy_matrix.py`, `tests/agents/specialization/test_capability_policy_enforcer.py`
	- Acceptance criteria: unauthorized capability is denied with non-empty `deny_reason` and policy version evidence.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_capability_policy_enforcer.py`

- [ ] T-SAL-005 - Implement specialization-to-core binding planner (@5test -> @6code)
	- Objective: bind shell request to explicit `*Core` contract and reject unresolved core targets.
	- Target files: `src/agents/specialization/specialized_core_binding.py`, `src/core/universal/UniversalCoreRegistry.py`, `tests/agents/specialization/test_specialized_core_binding.py`
	- Acceptance criteria: valid target emits invocation plan; unresolved target fails closed with typed reason.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialized_core_binding.py`

- [ ] T-SAL-006 - Implement deterministic fail-closed fallback policy (@5test -> @6code)
	- Objective: provide policy/schema/timeout fault fallback with deterministic outcome taxonomy.
	- Target files: `src/agents/specialization/adapter_fallback_policy.py`, `tests/agents/specialization/test_adapter_fallback_policy.py`, `tests/agents/specialization/test_fault_injection_fallback.py`
	- Acceptance criteria: all modeled failures route to fail-closed fallback without side-effectful capability execution.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_fault_injection_fallback.py`

- [ ] T-SAL-007 - Implement specialization telemetry bridge with redaction (@5test -> @6code)
	- Objective: emit required provenance fields while excluding prompt/tool secret content.
	- Target files: `src/agents/specialization/specialization_telemetry_bridge.py`, `src/observability/structured_logger.py`, `tests/agents/specialization/test_specialization_telemetry_bridge.py`, `tests/agents/specialization/test_telemetry_redaction.py`
	- Acceptance criteria: telemetry payload contains required fields and passes redaction assertions.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_telemetry_redaction.py`

- [ ] T-SAL-008 - Wire feature flag and runtime path into universal shell (@5test -> @6code)
	- Objective: integrate adapter path via feature flag without regressing baseline universal route.
	- Target files: `src/agents/specialization/runtime_feature_flags.py`, `src/core/universal/UniversalAgentShell.py`, `tests/core/universal/test_universal_agent_shell_specialization_flag.py`
	- Acceptance criteria: adapter path enabled only when feature flag and policy preconditions are satisfied.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/core/universal/test_universal_agent_shell_specialization_flag.py`

- [ ] T-SAL-009 - Add typed error taxonomy for specialization runtime (@5test -> @6code)
	- Objective: standardize typed runtime errors for schema, version, policy, and binding failures.
	- Target files: `src/agents/specialization/errors.py`, `src/agents/specialization/specialized_agent_adapter.py`, `tests/agents/specialization/test_specialization_error_taxonomy.py`
	- Acceptance criteria: all modeled failure modes raise/return expected typed codes consumed by fallback and telemetry.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_error_taxonomy.py`

- [ ] T-SAL-010 - Publish specialization package exports and contract docs (@5test -> @6code)
	- Objective: provide import-stable module exports for the specialization runtime package.
	- Target files: `src/agents/specialization/__init__.py`, `src/agents/specialization/README.md`, `tests/agents/specialization/test_package_imports.py`
	- Acceptance criteria: package imports expose expected public contracts and import tests pass.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_package_imports.py`

### Chunk B - Parity, NFR, Integration, and Release Gates

- [ ] T-SAL-011 - AC schema/version regression suite hardening (@5test)
	- Objective: add regression fixtures for schema and major-version gates.
	- Target files: `tests/agents/specialization/fixtures/descriptor_valid.json`, `tests/agents/specialization/fixtures/descriptor_invalid_schema.json`, `tests/agents/specialization/fixtures/descriptor_unsupported_major.json`, `tests/agents/specialization/test_specialization_registry.py`
	- Acceptance criteria: regressions fail deterministically on schema/version drift.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_registry.py -k "version or schema"`

- [ ] T-SAL-012 - Determinism and manifest parity suite (@5test)
	- Objective: verify parity of manifest intent vs built shell request across fixture corpus.
	- Target files: `tests/agents/specialization/test_manifest_request_parity.py`, `tests/agents/specialization/fixtures/parity_cases.json`
	- Acceptance criteria: parity suite passes across baseline and edge-case fixtures.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_manifest_request_parity.py`

- [ ] T-SAL-013 - Authorization matrix deny/allow suite (@5test)
	- Objective: verify actor/policy/capability matrix behavior including deny-by-default fallback.
	- Target files: `tests/agents/specialization/test_capability_policy_enforcer.py`, `tests/agents/specialization/fixtures/policy_matrix_cases.json`
	- Acceptance criteria: explicit allow paths pass and all unspecified capabilities are denied.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_capability_policy_enforcer.py -k "allow or deny"`

- [ ] T-SAL-014 - Core binding contract integration suite (@5test -> @6code)
	- Objective: validate binding interoperability with `UniversalCoreRegistry` and specialized `*Core` contracts.
	- Target files: `tests/agents/specialization/test_specialized_core_binding.py`, `tests/core/universal/test_core_registry_specialization_binding.py`
	- Acceptance criteria: unresolved core references fail closed; valid bindings execute expected plan path.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/core/universal/test_core_registry_specialization_binding.py`

- [ ] T-SAL-015 - Fault-injection fallback reliability suite (@5test -> @7exec)
	- Objective: inject schema/policy/timeout faults and verify deterministic fallback behavior.
	- Target files: `tests/agents/specialization/test_fault_injection_fallback.py`, `tests/agents/specialization/test_adapter_fallback_policy.py`
	- Acceptance criteria: no unauthorized side effects under induced failures.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_fault_injection_fallback.py -k "timeout or policy or schema"`

- [ ] T-SAL-016 - Telemetry schema/redaction integration suite (@5test -> @8ql)
	- Objective: verify correlation continuity, required fields, and redaction invariants.
	- Target files: `tests/agents/specialization/test_specialization_telemetry_bridge.py`, `tests/agents/specialization/test_telemetry_redaction.py`
	- Acceptance criteria: required provenance fields present and secret-bearing fields absent.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_telemetry_bridge.py`

- [ ] T-SAL-017 - Performance instrumentation and thresholds (@6code -> @7exec)
	- Objective: add adapter/registry/fallback latency metrics and threshold checks per NFR.
	- Target files: `src/agents/specialization/perf_metrics.py`, `tests/agents/specialization/test_perf_thresholds.py`, `performance/metrics_bench.py`
	- Acceptance criteria: p95 adapter <= 25 ms, registry <= 10 ms (warmed), fallback overhead <= 5 ms.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_perf_thresholds.py`

- [ ] T-SAL-018 - Runtime integration smoke path (@7exec)
	- Objective: verify feature-flagged specialization path in a representative end-to-end shell execution.
	- Target files: `tests/integration/test_specialization_adapter_runtime_path.py`, `tests/integration/test_specialization_adapter_rollback_path.py`
	- Acceptance criteria: specialization-enabled flow succeeds and rollback path uses baseline universal route.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/integration/test_specialization_adapter_runtime_path.py`

- [ ] T-SAL-019 - Security and quality closure checks (@8ql)
	- Objective: run narrow quality/security checks for changed specialization/runtime surfaces.
	- Target files: `src/agents/specialization/*.py`, `tests/agents/specialization/*.py`
	- Acceptance criteria: no high-severity blocker remains in scoped checks.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

- [ ] T-SAL-020 - Git handoff and narrow staging gate (@9git)
	- Objective: stage only project-scoped and implementation-scoped files after validation closure.
	- Target files: `docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.plan.md`, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/2026-03-31.4plan.log.md`
	- Acceptance criteria: branch validation pass, narrow staged file list, commit + push succeed.
	- Validation command: `git status --short`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Chunk A planning baseline completed | T-SAL-001..T-SAL-010 | PLANNED |
| M2 | Chunk B verification and rollout planning completed | T-SAL-011..T-SAL-020 | PLANNED |
| M3 | Handoff package to @5test prepared | T-SAL-011..T-SAL-016 | PLANNED |

## Dependency Order
1. @5test authors failing/contract tests for T-SAL-001..T-SAL-016.
2. @6code implements runtime modules to satisfy tests and NFR targets.
3. @7exec validates integration and runtime rollback behavior.
4. @8ql verifies security/quality closure and policy gates.
5. @9git performs narrow staging/commit/push on validated branch.

## Rollback and Failure Gates
- If descriptor schema or version tests fail, block adapter runtime enablement and keep baseline universal route active.
- If policy deny-by-default assertions fail, block all specialization capability execution.
- If fallback determinism fails, block rollout and route exclusively through universal baseline.
- If telemetry redaction tests fail, block release until provenance payload is compliant.
- If performance thresholds are exceeded, keep feature flag off and defer rollout.

## Validation Commands
```powershell
# Required docs policy gate for project artifacts
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# Representative task-level selectors for downstream execution
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialization_registry.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_specialized_agent_adapter.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_capability_policy_enforcer.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/agents/specialization/test_fault_injection_fallback.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/integration/test_specialization_adapter_runtime_path.py
```

## Handoff to @5test
First handoff scope: T-SAL-001..T-SAL-008 and T-SAL-011..T-SAL-016.
Handoff expectation: create deterministic failing tests first, grouped by AC and interface contract ID, with fixture-driven parity evidence.

## Validation Evidence
- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed in 5.98s`