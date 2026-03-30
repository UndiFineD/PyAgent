# Current Memory - 2think

## Metadata
- agent: @2think
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
- rollover: At new project start, append this file's entries to history.2think.memory.md in chronological order, then clear Entries.

## Entries

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

