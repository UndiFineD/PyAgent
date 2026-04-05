# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-05
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000128-coverage-minimum-enforcement
	state: DONE
	branch: prj0000128-coverage-minimum-enforcement
	selected_design_path: Option B (dedicated blocking coverage job in existing ci.yml at the current 40 baseline)
	assumptions:
		- `[tool.coverage.report].fail_under = 40` in `pyproject.toml` remains the single threshold authority for this slice.
		- The first implementation slice adds one blocking `coverage` job without changing the semantics of `jobs.quick`.
		- No new workflow files or per-package coverage floors are introduced.
	interface_contract_notes:
		- IFACE-COV-001 CI coverage job contract.
		- IFACE-COV-002 canonical coverage command contract.
		- IFACE-COV-003 threshold authority contract.
		- IFACE-COV-004 blocking semantics contract.
		- IFACE-COV-005 CI structure guard contract.
		- IFACE-COV-006 config guard contract.
		- IFACE-COV-007 rollback contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000128-coverage-minimum-enforcement/coverage-minimum-enforcement.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Coverage-gate projects stay low-risk when they restore one blocking CI path before attempting any threshold ratchet increase.
		Root cause: Repository policy drift let the configured coverage floor survive in `pyproject.toml` while the blocking CI workflow stopped exercising it.
		Prevention: Keep one threshold authority, one blocking coverage job, and one structure-test contract that fails on removal, duplication, or softening of the gate.
		First seen: 2026-04-05
		Seen in: prj0000128-coverage-minimum-enforcement
		Recurrence count: 1
		Promotion status: Candidate

