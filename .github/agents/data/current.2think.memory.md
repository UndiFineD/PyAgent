# Current Memory - 2think

## Metadata
- agent: @2think
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.2think.memory.md in chronological order, then clear Entries.

## Entries

### 2026-04-04 - prj0000127-mypy-strict-enforcement
- task_id: prj0000127-mypy-strict-enforcement
- status: DONE
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.think.md
- recommendation_summary: Choose progressive blocking allowlist strictness (Option B) for `src/core` with phased expansion, deterministic guardrails, and explicit config-precedence governance.
- prior_art_refs:
	- docs/project/archive/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md
	- docs/project/prj0000124-llm-gateway/llm-gateway.plan.md
	- docs/project/kanban.json
- branch_gate_evidence: `git branch --show-current` -> `prj0000127-mypy-strict-enforcement`
- rationale_for_handoff: Repository evidence shows conflicting mypy baselines across `mypy.ini` and `pyproject.toml`; progressive scoped blocking achieves enforceable quality gains without immediate broad refactor risk.
- required_validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

#### Lesson
- Pattern: Dual linter/type-check config surfaces with opposite defaults can silently dilute intended governance.
- Root cause: Incremental migration introduced stricter `pyproject.toml` settings while permissive `mypy.ini` remained active.
- Prevention: Require explicit canonical-config declaration plus deterministic tests that assert effective strict-lane behavior.
- First seen: 2026-04-04
- Seen in: prj0000127-mypy-strict-enforcement
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-04-04 - prj0000125-llm-gateway-lessons-learned-fixes
- task_id: prj0000125-llm-gateway-lessons-learned-fixes
- status: DONE
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.think.md
- recommendation_summary: Synthesize cross-project lessons into sequenced remediation waves for prj0000125 (A runtime fail-closed, B deterministic tests, C docs/governance truth sync, D naming alignment) with explicit do-now/defer decisions and owner matrix.
- prior_art_refs:
	- docs/project/prj0000124-llm-gateway/llm-gateway.think.md
	- docs/project/prj0000124-llm-gateway/llm-gateway.git.md
	- docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.think.md
	- docs/project/prj0000119-pytest-stabilization/pytest-stabilization.git.md
	- docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.git.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000125-llm-gateway-lessons-learned-fixes`
- rationale_for_handoff: Cross-project evidence from prj0000101-prj0000124 shows recurring failures around fail-closed completeness, deterministic test signal, and post-merge artifact drift. Sequenced waves reduce blast radius while preserving one-project accountability.
- required_validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

#### Lesson
- Pattern: Recurring cross-project drift appears as the trio of partial fail-closed behavior, non-deterministic/insufficient validation signals, and stale lifecycle artifacts.
- Root cause: Projects close phase slices before all failure paths and closure/governance synchronization are bound to mandatory selectors.
- Prevention: Enforce wave-based closure (runtime -> deterministic tests -> truth sync -> naming decision) with explicit do-now/defer gates.
- First seen: 2026-04-04
- Seen in: prj0000118-amd-npu-feature-documentation, prj0000119-pytest-stabilization, prj0000123-openapi-drift-post-merge-hotfix, prj0000124-llm-gateway, prj0000125-llm-gateway-lessons-learned-fixes
- Recurrence count: 5
- Promotion status: HARD_RULE

#### Lesson
- Pattern: Dashboard/registry side effects repeatedly cause out-of-scope diffs and closure noise.
- Root cause: Required dashboard refresh and registry updates touch broad shared docs while projects are scoped narrowly.
- Prevention: Keep strict explicit allowlist staging and always separate baseline debt from project regression evidence.
- First seen: 2026-03-31
- Seen in: prj0000106, prj0000107, prj0000108, prj0000109, prj0000110, prj0000121, prj0000122
- Recurrence count: 7
- Promotion status: HARD_RULE

### 2026-04-04 - prj0000124-llm-gateway
- task_id: prj0000124-llm-gateway
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000124-llm-gateway/llm-gateway.think.md
- recommendation_summary: Select Option C (hybrid split-plane gateway) to combine fail-closed control-plane governance with a data-plane hot path that can start in Python and graduate selective operations to Rust after parity gates.
- prior_art_refs:
	- docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md
	- docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md
	- docs/project/archive/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md
	- docs/architecture/archive/TASK_COMPLETION_REPORT.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000124-llm-gateway`
- rationale_for_handoff: Repository discovery confirmed reusable routing, guardrail, provider, resilience, auth, memory, and tracing primitives already exist but are fragmented. Option C gives full requirement coverage with bounded phase-one complexity and clear contracts for @3design.
- required_validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

#### Lesson
- Pattern: For new gateway surfaces, prefer split-plane contracts when both governance controls and hot-path performance are first-class requirements.
- Root cause: Existing capabilities were present but scattered, creating policy sequencing and ownership ambiguity.
- Prevention: Define one canonical request lifecycle contract with mandatory guardrail and telemetry checkpoints before expanding provider breadth.
- First seen: 2026-04-04
- Seen in: prj0000124-llm-gateway
- Recurrence count: 1
- Promotion status: MONITOR

### 2026-04-04 - prj0000122-jwt-refresh-token-support
- task_id: prj0000122-jwt-refresh-token-support
- status: DONE
- target_agent: @3design
- canonical_artifact: docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.think.md
- recommendation_summary: Select Option A (backend-owned refresh-session store with opaque rotating refresh tokens and short-lived access JWTs) because it is the only phase-one option that materially improves security posture while still delivering backend JWT refresh support.
- prior_art_refs:
	- docs/project/archive/prj0000054/backend-authentication.design.md
	- docs/project/archive/prj0000054/backend-authentication.think.md
	- docs/project/archive/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md
	- docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md
- branch_gate_evidence: `git branch --show-current` -> `prj0000122-jwt-refresh-token-support`
- rationale_for_handoff: Completed 3-option discovery with repository evidence from `backend/auth.py`, `backend/app.py`, `backend/session_manager.py`, `backend/memory_store.py`, auth/worker tests, and approved external evidence from Python `secrets` docs plus PyJWT documentation. Discovery confirmed refresh support is absent rather than framework-blocked, with the key phase-one decisions being bootstrap credential flow and session-store durability.
- required_validation: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`

#### Lesson
- Pattern: Refresh-token projects in validator-only JWT backends should first separate token validation, session persistence, and transport/session binding concerns before scoring options.
- Root cause: Existing auth surfaces often appear “JWT-capable” while still lacking issuance, revocation, and replay-resistant refresh semantics.
- Prevention: Make bootstrap contract, store durability, and WebSocket/session boundaries explicit in discovery before design starts.
- First seen: 2026-04-04
- Seen in: prj0000122-jwt-refresh-token-support
- Recurrence count: 1
- Promotion status: MONITOR

