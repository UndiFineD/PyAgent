# Current Memory - 2think

## Metadata
- agent: @2think
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-03
- rollover: At new project start, append this file's entries to history.2think.memory.md in chronological order, then clear Entries.

## Entries

### 2026-04-03 - prj0000117-rust-sub-crate-unification
- task_id: prj0000117-rust-sub-crate-unification
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.think.md
- recommendation_summary: Select Option B (root-workspace unification anchored at rust_core/Cargo.toml) to achieve dependency/lockfile convergence while preserving maturin and existing CI command contracts.
- prior_art_refs:
	- docs/project/archive/prj0000005/prj005-llm-swarm-architecture.project.md
	- docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md
	- docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md
	- docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000117-rust-sub-crate-unification`
- rationale_for_handoff: Completed 3-option analysis with repository and approved external Cargo guidance, SWOT/security risk-to-testability mapping, decision matrix, design open questions, and minimal-first implementation slice.
- required_validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> unchanged known baseline failure in `test_legacy_git_summaries_document_branch_exception_and_corrective_ownership` due missing legacy file `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`.

#### Lesson
- Pattern: Rust multi-crate governance decisions should preserve existing root build contracts while centralizing dependency and patch ownership.
- Root cause: Separate standalone lockfiles and crate-local patch declarations increase drift and security-governance ambiguity.
- Prevention: Prefer root workspace topology that keeps existing primary manifest path stable and enforces root-level patch/dependency checks with package-scoped command validation.
- First seen: 2026-04-03
- Seen in: prj0000117-rust-sub-crate-unification
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-04-03 - prj0000116-rust-criterion-benchmarks
- task_id: prj0000116-rust-criterion-benchmarks
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.think.md
- recommendation_summary: Leading option is Option B (minimal Rust Criterion harness plus lightweight CI smoke benchmark) for strongest balance of governance-compliant first slice and anti-drift enforcement.
- prior_art_refs:
	- docs/architecture/1agents.md
	- docs/architecture/archive/9operations-observability.md
	- docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md
	- docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000116-rust-criterion-benchmarks`; `git pull --ff-only` -> `Already up to date.`
- rationale_for_handoff: Branch gate and policy references validated; three options documented with SWOT, security risks, risk-to-testability mapping, decision matrix, and concrete downstream file targets. Required docs-policy test run completed with known baseline failure in `test_legacy_git_summaries_document_branch_exception_and_corrective_ownership` due missing legacy file `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`.

#### Lesson
- Pattern: Docs-policy selector can fail for known historical missing legacy files outside active project scope.
- Root cause: Repository-wide historical artifact gap (`prj0000005` legacy git summary) remains unresolved.
- Prevention: Always run required selector, report exact known baseline failure, and avoid scope-creep fixes in unrelated legacy projects during active project delivery.
- First seen: 2026-04-03
- Seen in: prj0000116-rust-criterion-benchmarks
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-04-02 - prj0000115-ci-security-quality-workflow-consolidation
- task_id: prj0000115-ci-security-quality-workflow-consolidation
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.think.md
- recommendation_summary: Select Option C (hybrid: fast pre-commit baseline + lightweight CI verifier + scheduled heavyweight security scans) with phased rollout discipline from Option A.
- prior_art_refs:
	- docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md
	- docs/project/ideas/archive/idea000006-codeql-ci-integration.md
	- docs/project/ideas/archive/idea000007-security-scanning-ci.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000115-ci-security-quality-workflow-consolidation`
- rationale_for_handoff: Completed 3-option analysis with current-state evidence, decision matrix, per-option SWOT, security risk-to-testability mapping, and explicit @3design open questions.

#### Lesson
- Pattern: When repository CI is already lightweight and pre-commit-first, the highest-value discovery move is to close heavyweight scheduled security gaps instead of re-litigating fast-path checks.
- Root cause: Backlog context reflected older CI assumptions (multiple workflows and missing pre-commit-central verification), while current repo already converged on a single lightweight workflow.
- Prevention: Require mandatory current-state workflow inventory before option scoring and tie recommendation to observed files, not historical assumptions.
- First seen: 2026-04-02
- Seen in: prj0000115-ci-security-quality-workflow-consolidation
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-04-01 - prj0000110-idea000004-quality-workflow-branch-trigger
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.think.md
- recommendation_summary: Select Option B (targeted branch-governance quality gate with narrow full-suite triggers) to satisfy branch-trigger quality intent while avoiding reintroduction of redundant workflow sprawl.
- prior_art_refs:
	- docs/project/prj0000075/prj0000075.think.md
	- docs/project/prj0000096-coverage-minimum-enforcement/coverage-minimum-enforcement.think.md
	- docs/project/prj0000026/prj0000026.git.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000110-idea000004-quality-workflow-branch-trigger`
- rationale_for_handoff: Completed 3-option analysis with repository and approved external evidence, per-option SWOT, security risk analysis, risk-to-testability mapping, and acceptance-criteria-linked recommendation.

#### Lesson
- Pattern: When an idea references a removed legacy workflow, quality-trigger discovery should map intent to current active workflows and governance scripts instead of recreating deprecated topology.
- Root cause: Backlog idea metadata drifted from repository state after CI simplification removed `quality.yml`.
- Prevention: Add mandatory current-state workflow inventory step before optioning, with explicit prior-art references from workflow-retirement projects.
- First seen: 2026-04-01
- Seen in: prj0000110-idea000004-quality-workflow-branch-trigger
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-03-31 - prj0000108-idea000019-crdt-python-ffi-bindings
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md
- recommendation_summary: Select Option B (integrate CRDT APIs into existing `rust_core` PyO3 module) to deliver true Python FFI with best reuse of maturin/PyO3 pipeline and lower long-term operational risk than subprocess bridging.
- prior_art_refs:
	- docs/project/prj0000056/rust-async-transport-activation.think.md
	- docs/project/prj0000067/rust-file-watcher.think.md
	- docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000108-idea000019-crdt-python-ffi-bindings`
- rationale_for_handoff: Completed 3-option exploration with repository and approved external evidence, SWOT and security risk-to-testability mapping per option, decision matrix, and explicit @3design open questions.

#### Lesson
- Pattern: When a Rust capability already has a proven repository PyO3+maturin delivery path, extending that path is usually lower risk than introducing parallel packaging or retaining subprocess bridges.
- Root cause: CRDT functionality exists as a standalone CLI crate while Python integration expectations require in-process FFI contracts.
- Prevention: Require early decision on extension topology (existing module vs separate package) with parity tests against current subprocess behavior.
- First seen: 2026-03-31
- Seen in: prj0000108-idea000019-crdt-python-ffi-bindings
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-03-30 - prj0000105-idea000016-mixin-architecture-base
- task_id: prj0000105-idea000016-mixin-architecture-base
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.think.md
- recommendation_summary: Select Option B (incremental migration to `src/core/base/mixins/` with compatibility shims) to close architecture gap with controlled rollout risk.
- prior_art_refs:
	- docs/project/prj0000086-universal-agent-shell/universal-agent-shell.think.md
	- docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md
	- docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000105-idea000016-mixin-architecture-base`
- rationale_for_handoff: Discovery complete with 3 options, full tradeoff matrix, security/testability mapping, and explicit @3design open questions.

#### Lesson
- Pattern: Architecture-gap projects are safest when they combine immediate structural correction with temporary compatibility shims and explicit parity tests.
- Root cause: Contract required a canonical base mixin namespace, but implementation drift distributed mixins across unrelated domains without a base anchor.
- Prevention: Require first-wave migration plan with shim expiry deadlines, behavior parity tests, and import smoke checks.
- First seen: 2026-03-30
- Seen in: prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-03-30 - prj0000104-idea000014-processing
- task_id: prj0000104-idea000014-processing
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000104-idea000014-processing/idea000014-processing.think.md
- recommendation_summary: Select Option A (`pyproject.toml` canonical with generated `requirements.txt`) for strongest drift elimination and testability.
- prior_art_refs:
	- docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md
	- docs/project/prj0000076/prj0000076.think.md
	- docs/architecture/archive/8testing-quality.md
- branch_gate_evidence: `git rev-parse --abbrev-ref HEAD` -> `prj0000104-idea000014-processing`
- rationale_for_handoff: Option space complete (3 options), decision matrix and reject reasons documented, open design questions listed.

#### Lesson
- Pattern: Dependency-governance projects benefit from explicit single-source authority with deterministic parity checks.
- Root cause: Dual manifest ownership causes drift and inconsistent local/CI environments.
- Prevention: Require canonical source declaration, parity gate, and policy-level tests in design.
- First seen: 2026-03-29
- Seen in: prj0000102, prj0000104
- Recurrence count: 2
- Promotion status: PROMOTED_TO_HARD_RULE

### 2026-03-30 - prj0000106-idea000080-smart-prompt-routing-system
- task_id: prj0000106-idea000080-smart-prompt-routing-system
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.think.md
- recommendation_summary: Select Option B (hybrid routing with deterministic guardrails, semantic classifier, and bounded LLM tie-break) for best accuracy/safety balance within project boundaries.
- prior_art_refs:
	- docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md
	- docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md
	- docs/project/prj0000080-cort-reasoning-pipeline/prj0000080.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000106-idea000080-smart-prompt-routing-system`
- rationale_for_handoff: Completed 3-option analysis with SWOT, security/risk-to-testability mapping, constraints tie-in, decision matrix, and explicit @3design questions.

#### Lesson
- Pattern: Smart-routing designs should combine deterministic guardrails with selective adaptive classification instead of pure static rules or full decoupled mediator architecture at v1.
- Root cause: Rule-only systems under-handle ambiguity; fully decoupled mediator systems add excessive operational risk early.
- Prevention: Require guardrail precedence contracts, confidence-threshold governance, and shadow-mode route validation before activation.
- First seen: 2026-03-30
- Seen in: prj0000106-idea000080-smart-prompt-routing-system
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-03-30 - prj0000107-idea000015-specialized-agent-library
- task_id: prj0000107-idea000015-specialized-agent-library
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.think.md
- recommendation_summary: Select Option B (hybrid adapter layer over universal shell primitives) to close specialization-runtime gap with lower migration risk and stronger governance/testability.
- prior_art_refs:
	- docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md
	- docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.project.md
	- docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.project.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000107-idea000015-specialized-agent-library`
- rationale_for_handoff: Completed 3-option exploration with repository/external evidence, per-option SWOT, security risk-to-testability mapping, explicit decision matrix, and @3design open questions.

#### Lesson
- Pattern: Specialization-library decisions are most stable when introducing typed adapters between declarative capability metadata and shared runtime orchestration.
- Root cause: Repository contains specialization definitions and universal shell primitives, but lacks a formal runtime contract layer connecting them.
- Prevention: Require adapter contract schemas, allowlisted capability routing, and declared-vs-runtime parity tests before broad implementation.
- First seen: 2026-03-30
- Seen in: prj0000107-idea000015-specialized-agent-library
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-03-31 - prj0000109-idea000002-missing-compose-dockerfile
- task_id: prj0000109-idea000002-missing-compose-dockerfile
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.think.md
- recommendation_summary: Select Option B (incremental hardening around the existing deploy-local Dockerfile fix) to preserve reliability while keeping scope bounded and deferring compose-topology consolidation to idea000010.
- prior_art_refs:
	- docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md
	- docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md
	- docs/project/ideas/idea000010-docker-compose-consolidation.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000109-idea000002-missing-compose-dockerfile`
- rationale_for_handoff: Completed 3-option analysis with repository + approved external evidence, per-option SWOT, risk-to-testability mapping, decision matrix, acceptance criteria mapping, and bounded recommendation.

#### Lesson
- Pattern: When a backlog defect is already fixed by prior work, the next-phase option should prefer governance hardening and explicit non-goal boundaries over re-implementing the same technical change.
- Root cause: Idea registry signal lagged behind repository state, creating risk of duplicate or scope-creep remediation.
- Prevention: Require early current-state verification against deploy and test contracts before proposing implementation-heavy options.
- First seen: 2026-03-28
- Seen in: prj0000091-missing-compose-dockerfile; prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 2
- Promotion status: PROMOTED_TO_HARD_RULE

