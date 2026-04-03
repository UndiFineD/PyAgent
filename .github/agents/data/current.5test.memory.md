# Current Memory - 5test

## Metadata
- agent: @5test
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-03
- rollover: At new project start, append this file's entries to history.5test.memory.md in chronological order, then clear Entries.

## Entries

### Entry 2026-04-03 - prj0000120 openapi spec generation red contracts
- task_id: prj0000120-openapi-spec-generation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000120-openapi-spec-generation
  - observed: prj0000120-openapi-spec-generation
  - result: PASS
- scope:
  - tests/docs/test_backend_openapi_drift.py
  - docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/docs/test_backend_openapi_drift.py
  - PASS: .venv\Scripts\ruff.exe check tests/docs/test_backend_openapi_drift.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/docs/test_backend_openapi_drift.py
  - RED(expected): python -m pytest -q tests/docs/test_backend_openapi_drift.py (2 failed, 1 passed in 4.92s)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed in 5.61s)
- red_failure_signatures:
  - AssertionError: Missing committed backend OpenAPI artifact at C:\Dev\PyAgent\docs\api\openapi\backend_openapi.json. @6code must add the generator and commit the backend-only schema before drift checks can pass.
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add scripts/generate_backend_openapi.py with backend.app as the only phase-one import target
    - commit docs/api/openapi/backend_openapi.json generated from backend.app.openapi()
    - preserve read-only drift verification semantics in tests/docs/test_backend_openapi_drift.py
    - avoid importing src.github_app or src.chat.api in the generator, test lane, or CI selector

#### Lesson
- Pattern: OpenAPI drift red contracts are strongest when one selector proves the committed artifact is missing or stale and another proves parity checks stay read-only.
- Root cause: The repository exposes backend.app.openapi() at runtime, but the phase-one generator and committed backend artifact do not exist yet.
- Prevention: Keep generation, committed artifact ownership, and drift verification separate so missing freshness fails via assertion-level contract checks instead of import-level failures.
- First seen: 2026-04-03
- Seen in: prj0000120-openapi-spec-generation
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000118 amd npu feature documentation red contracts
- task_id: prj0000118-amd-npu-feature-documentation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000118-amd-npu-feature-documentation
  - observed: prj0000118-amd-npu-feature-documentation
  - result: PASS
- scope:
  - tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - PASS: .venv\Scripts\ruff.exe check tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - RED(expected): python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py (6 failed in 6.68s)
- red_failure_signatures:
  - AssertionError: missing canonical runtime guidance marker section for amd_npu
  - AssertionError: missing feature-off and feature-on command examples
  - AssertionError: missing AMD_NPU_STATUS_UNAVAILABLE and -1 fallback semantics
  - AssertionError: missing Windows x86_64 + AMD Ryzen AI SDK boundary and unsupported path phrase
  - AssertionError: missing mandatory evidence schema fields
  - AssertionError: missing non-goals and CI defer contract text
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - update docs/performance/HARDWARE_ACCELERATION.md to satisfy AC-AMD-001..006 selectors

#### Lesson
- Pattern: Docs-only red contracts are strongest when each AC maps to one assertion-focused selector and one aggregate selector.
- Root cause: AMD NPU guidance lacks canonical marker, command parity, fallback semantics, environment boundary, evidence schema, and defer/non-goals language.
- Prevention: Keep phrase-level selectors aligned to AC text and fail on missing contract language, not file existence.
- First seen: 2026-04-03
- Seen in: prj0000118-amd-npu-feature-documentation
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000117 rust sub-crate workspace unification red contracts
- task_id: prj0000117-rust-sub-crate-unification
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000117-rust-sub-crate-unification
  - observed: prj0000117-rust-sub-crate-unification
  - result: PASS
- scope:
  - tests/rust/test_workspace_unification_contracts.py
  - tests/ci/test_ci_workspace_unification_contracts.py
  - docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - PASS: .venv\Scripts\ruff.exe check tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - RED(expected): python -m pytest -q tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py (3 failed, 4 passed)
  - BASELINE_FAIL(known): python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (1 failed, 16 passed)
- red_failure_signatures:
  - AssertionError: rust_core/Cargo.toml [workspace].members must include 'crdt', 'p2p', and 'security'
  - AssertionError: Workspace lockfile contract violation due to existing member Cargo.lock files
  - AssertionError: rust_core/Cargo.toml must own [patch.crates-io] for workspace-wide dependency overrides
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add [workspace] members (crdt, p2p, security) to rust_core/Cargo.toml
    - remove member Cargo.lock files and keep rust_core/Cargo.lock as singleton
    - move [patch.crates-io] ownership to rust_core/Cargo.toml from member manifests

#### Lesson
- Pattern: Workspace-migration red contracts are strongest when they combine TOML structure checks for workspace membership and patch ownership with lockfile singleton assertions.
- Root cause: Current Rust layout is mixed standalone crates with member lockfiles and crate-local patch governance, not root-workspace governance.
- Prevention: Keep three independent selectors for workspace membership, lockfile singleton, and root patch ownership so implementation deltas are explicit.
- First seen: 2026-04-03
- Seen in: prj0000117-rust-sub-crate-unification
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000116 rust criterion benchmark baseline red contracts
- task_id: prj0000116-rust-criterion-benchmarks
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000116-rust-criterion-benchmarks
  - observed: prj0000116-rust-criterion-benchmarks
  - result: PASS
- scope:
  - tests/rust/test_rust_criterion_baseline.py
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - PASS: .venv\Scripts\ruff.exe check tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate (4 failed in 4.74s)
  - BASELINE_FAIL(known): python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (1 failed, 16 passed)
- red_failure_signatures:
  - AssertionError: rust_core/Cargo.toml must add criterion under [dev-dependencies] for stats baseline bench
  - AssertionError: rust_core/benches/stats_baseline.rs must exist
  - AssertionError: ci.yml must contain exactly one benchmark smoke command: 'cargo bench --bench stats_baseline -- --noplot'
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add criterion under rust_core/Cargo.toml [dev-dependencies]
    - add [[bench]] target name=stats_baseline with harness=false
    - add rust_core/benches/stats_baseline.rs with Criterion harness + naming contract
    - add single CI smoke benchmark command and artifact check in .github/workflows/ci.yml

#### Lesson
- Pattern: Red-phase benchmark contracts are strongest when they validate Cargo wiring, Criterion macros, and CI command semantics as text-level structure checks.
- Root cause: Repository has no Criterion dev-dependency, no stats benchmark harness file, and no CI smoke benchmark command yet.
- Prevention: Keep three independent contract selectors for Cargo, bench source, and CI smoke so @6code receives precise implementation deltas.
- First seen: 2026-04-03
- Seen in: prj0000116-rust-criterion-benchmarks
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-02 - prj0000115 ci-security-quality workflow consolidation wave A
- task_id: prj0000115-ci-security-quality-workflow-consolidation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000115-ci-security-quality-workflow-consolidation
  - observed: prj0000115-ci-security-quality-workflow-consolidation
  - result: PASS
- scope:
  - tests/ci/test_security_workflow.py
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-02.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/ci/test_security_workflow.py (7 failed in 4.56s)
  - PASS: python -m pytest -q tests/ci/test_ci_workflow.py (7 passed in 3.68s)
- red_failure_signatures:
  - AssertionError: security workflow file does not exist yet (.github/workflows/security-scheduled.yml)
  - FileNotFoundError: no such file or directory .github/workflows/security-scheduled.yml
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add .github/workflows/security-scheduled.yml meeting AC-SEC-001..003

#### Lesson
- Pattern: Security workflow contracts are strongest when tests validate trigger shape, permissions, and CodeQL init arguments instead of only job existence.
- Root cause: No scheduled security workflow file exists yet, so all contract selectors fail as intended in red phase.
- Prevention: Keep one explicit existence test plus behavior assertions that fail on missing/incorrect YAML content.
- First seen: 2026-04-02
- Seen in: prj0000115-ci-security-quality-workflow-consolidation
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-01 - prj0000110 quality workflow branch trigger red contracts
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000110-idea000004-quality-workflow-branch-trigger
  - observed: prj0000110-idea000004-quality-workflow-branch-trigger
  - result: PASS
- scope:
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-01.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/ci/test_ci_workflow.py tests/test_enforce_branch.py (2 failed, 25 passed)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed)
- red_failure_signatures:
  - AssertionError: explicit project branch glob missing from pull_request.branches
  - AssertionError: workflow name mismatch for required-check identity
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - update ci trigger branch pattern from `prj*` to explicit prjNNNNNNN-style glob
    - update workflow name to the required-check identity contract

#### Lesson
- Pattern: Trigger contracts become weak when wildcard branch filters are too broad (`prj*`) to encode branch policy intent.
- Root cause: Existing CI trigger accepted ambiguous wildcard and lacked explicit required-check identity naming contract.
- Prevention: Add contract tests that assert explicit branch glob shape and exact required-check workflow identity.
- First seen: 2026-04-01
- Seen in: prj0000110-idea000004-quality-workflow-branch-trigger
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-03-31 - prj0000109 missing compose dockerfile red-phase tests
- task_id: prj0000109-idea000002-missing-compose-dockerfile
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000109-idea000002-missing-compose-dockerfile
  - observed: prj0000109-idea000002-missing-compose-dockerfile
  - result: PASS
- scope:
  - docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md
  - tests/deploy/test_compose_context_contract.py
  - tests/deploy/test_compose_dockerfile_regression_matrix.py
  - tests/deploy/test_compose_file_selection.py
  - tests/deploy/test_compose_non_goal_guardrails.py
  - tests/deploy/test_compose_scope_boundary_markers.py
  - tests/docs/test_agent_workflow_policy_docs.py
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-03-31.5test.log.md
- evidence:
  - authored deterministic red-phase selectors for T-DC-001, T-DC-003, T-DC-005, T-DC-007, T-DC-011
  - docs artifact includes branch/scope preconditions, AC-to-test matrix, weak-test gate, and selector order
  - selector S3 produced assertion-level RED evidence for missing deploy/Dockerfile.fleet
- failing_test_evidence:
  - python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py
  - result: 3 failed, 8 passed
  - failure signatures: AssertionError for missing C:/Dev/PyAgent/deploy/Dockerfile.fleet
  - invalid signatures absent: ImportError, AttributeError
- pass_fail_summary:
  - PASS: python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py (2 passed)
  - PASS: python -m pytest -q tests/deploy/test_compose_context_contract.py (2 passed)
  - FAIL(RED): python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py (3 failed, 8 passed)
  - PASS: python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py (4 passed)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (15 passed)
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION_CONTRACTS
  - blocker_for_green: provide deploy/Dockerfile.fleet or align fleet compose dockerfile references to existing files

#### Lesson
- Pattern: Regression matrices that validate both dockerfile value and filesystem existence expose latent compose drift reliably.
- Root cause: Fleet compose references deploy/Dockerfile.fleet, but that file is absent in repository.
- Prevention: Keep matrix tests coupling compose dockerfile references with real file existence checks for all service entries.
- First seen: 2026-03-31
- Seen in: prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 1
- Promotion status: Candidate
