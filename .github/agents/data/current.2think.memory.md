# Current Memory - 2think

## Metadata
- agent: @2think
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-31
- rollover: At new project start, append this file's entries to history.2think.memory.md in chronological order, then clear Entries.

## Entries

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

