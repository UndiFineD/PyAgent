# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
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

