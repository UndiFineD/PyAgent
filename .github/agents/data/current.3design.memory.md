# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000106-idea000080-smart-prompt-routing-system
	state: DONE
	selected_design_path: Option B (hybrid guardrails + semantic classifier + bounded deterministic tie-break)
	assumptions:
		- Deterministic guardrails retain absolute precedence over classifier/tie-break outcomes.
		- Route decisions are promoted from shadow to active mode only after parity and latency gates pass.
		- Existing deterministic path remains available as operational fallback.
	interface_contract_notes:
		- IFACE-SPR-001 routing facade contract for total decision coverage.
		- IFACE-SPR-002 guardrail precedence invariant.
		- IFACE-SPR-003 classifier confidence + schema contract.
		- IFACE-SPR-004 deterministic tie-break + timeout contract.
		- IFACE-SPR-005 fail-closed fallback contract.
		- IFACE-SPR-006 redacted provenance telemetry contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md
	lesson:
		Pattern: Hybrid decision systems need explicit guardrail precedence and deterministic tie-break rules to stay testable.
		Root cause: Ambiguous prompt routing without staged control boundaries causes nondeterministic behavior and weak safety guarantees.
		Prevention: Enforce stage-order invariants, fixed tie-break determinism, and fail-closed fallback with provenance checks.
		First seen: 2026-03-30
		Seen in: prj0000106-idea000080-smart-prompt-routing-system
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000105-idea000016-mixin-architecture-base
	state: DONE
	selected_design_path: Option B (incremental migration with compatibility shims)
	assumptions:
		- Canonical base mixin namespace is introduced before broad host adoption.
		- Legacy shims are explicitly time-boxed to migration waves W1-W3.
		- @4plan will keep decomposition to roughly 10 code files and 10 test files as requested by workflow.
	interface_contract_notes:
		- IFACE-MX-001 canonical export determinism under src/core/base/mixins/.
		- IFACE-MX-002 host protocol requirements and validation hook contract.
		- IFACE-MX-003 legacy compatibility shim contract with deprecation signaling.
		- IFACE-MX-004 behavioral parity contract old vs canonical import paths.
		- IFACE-MX-005 shim expiry fail-closed governance gate.
		- IFACE-MX-006 migration observability event contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Explicit AC IDs plus interface-to-task traceability in design artifacts reduces @4plan ambiguity and rework.
		Root cause: Prior workflow stalls happen when architecture contracts exist without executable decomposition mapping.
		Prevention: Always include AC table and IFACE-to-task mapping block before @4plan handoff.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base
		Recurrence count: 2
		Promotion status: Promoted to hard rule

- task_id: prj0000104-idea000014-processing
	state: DONE
	selected_design_path: Option A (`pyproject.toml` canonical + deterministic generated `requirements.txt`)
	assumptions:
		- CI parity gate is authoritative and pre-commit is fast feedback.
		- Existing requirements-based install paths remain supported.
		- Heavy optional dependency extras migration is deferred.
	interface_contract_notes:
		- IFACE-C1 generation contract defined for deterministic output.
		- IFACE-C2 parity check contract defined for local/CI enforcement.
		- IFACE-C3 install compatibility contract preserves existing flows.
		- IFACE-C4 parity test contract covers drift/nondeterminism.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000104-idea000014-processing/idea000014-processing.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Design handoff quality improves when acceptance criteria and interface-to-task traceability are both explicit.
		Root cause: Prior handoffs can stall when interfaces are defined but not mapped to executable plan tasks.
		Prevention: Always include AC table with IDs and explicit IFACE-to-task mapping in the canonical design file.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing
		Recurrence count: 1
		Promotion status: Candidate

