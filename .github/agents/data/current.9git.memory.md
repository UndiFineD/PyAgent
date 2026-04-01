# Current Memory - 9git

## Metadata
- agent: @9git
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
- rollover: At new project start, append this file's entries to history.9git.memory.md in chronological order, then clear Entries.

## Entries

## 2026-03-30 - prj0000104-idea000014-processing
- task_id: prj0000104-idea000014-processing
- status: DONE
- branch_expected: prj0000104-idea000014-processing
- branch_observed: prj0000104-idea000014-processing
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Mandatory placeholder scan found baseline placeholders in `src/` unrelated to this project scope.
	- Mandatory dashboard refresh gate executed; generated broad out-of-scope docs changes, excluded from staging.
	- Commit created: 08aa9e35899b7d57a847ea562e95bfbf7f8a9d45.
	- Branch pushed to origin and PR opened: https://github.com/UndiFineD/PyAgent/pull/256.

### Lesson
- Pattern: Project dashboard refresh can stage broad unrelated project docs and must be isolated from narrow handoff scope.
- Root cause: `scripts/generate_project_dashboard.py` updates multiple historical project artifacts as side-effects.
- Prevention: Run dashboard gate early, then explicitly unstage non-project files before pre-commit and commit.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-03-30 - prj0000105-idea000016-mixin-architecture-base
- task_id: prj0000105-idea000016-mixin-architecture-base
- status: DONE
- branch_expected: prj0000105-idea000016-mixin-architecture-base
- branch_observed: prj0000105-idea000016-mixin-architecture-base
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Mandatory dashboard refresh gate executed before staging (`python scripts/generate_project_dashboard.py`).
	- Narrow scope staging applied; out-of-scope dashboard side effects and unrelated idea artifact remained unstaged.
	- Placeholder gate scans for staged Python scope returned zero hits.
	- Mandatory pre-commit gate passed on exact staged manifest.
	- Primary project commit created: `5d8c531a7`.
	- Handoff evidence commit created: `d1de21933`.
	- Branch pushed: `prj0000105-idea000016-mixin-architecture-base` -> `origin/prj0000105-idea000016-mixin-architecture-base`.
	- PR confirmed: https://github.com/UndiFineD/PyAgent/pull/258.

### Lesson
- Pattern: Dashboard generation side effects must be treated as out-of-scope unless explicitly included by project boundary.
- Root cause: The dashboard script updates multiple historical project artifacts beyond the active project.
- Prevention: Run dashboard generation first, validate scope, and stage by explicit allowlist only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 2
- Promotion status: HARD

## 2026-03-30 - prj0000106-idea000080-smart-prompt-routing-system
- task_id: prj0000106-idea000080-smart-prompt-routing-system
- status: DONE
- branch_expected: prj0000106-idea000080-smart-prompt-routing-system
- branch_observed: prj0000106-idea000080-smart-prompt-routing-system
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Governance lane reconciliation executed with canonical tooling; prj0000106 moved to Review for PR handoff.
	- Baseline lane mismatch for prj0000104 was also reconciled to restore registry/kanban validation consistency.
	- Mandatory dashboard refresh gate executed and broad out-of-scope changes remained unstaged.
	- Placeholder gate for staged Python scope passed after targeted verification.
	- Mandatory pre-commit gate passed on exact staged manifest (40 files).
	- Commit created: 58cfd2e5c27bc551cf7f1a8266beedc9a98e71d7.
	- Branch pushed and tracking set on origin/prj0000106-idea000080-smart-prompt-routing-system.
	- PR created: https://github.com/UndiFineD/PyAgent/pull/259.

### Lesson
- Pattern: Mandatory dashboard generation frequently introduces unrelated documentation diffs during project-scoped git handoff.
- Root cause: scripts/generate_project_dashboard.py rewrites summary files for many projects outside current scope.
- Prevention: Run dashboard gate before staging and enforce explicit allowlist staging for project boundary files only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system
- Recurrence count: 3
- Promotion status: HARD

## 2026-03-31 - prj0000107-idea000015-specialized-agent-library
- task_id: prj0000107-idea000015-specialized-agent-library
- status: DONE
- branch_expected: prj0000107-idea000015-specialized-agent-library
- branch_observed: prj0000107-idea000015-specialized-agent-library
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Continued closure from @8ql commit `e54adfcc74435c3dbf9a73f14213a5a542124ba4`.
	- Verified requested scope inclusion from existing commit: `docs/project/kanban.json` plus agent/governance instruction updates.
	- Verified migration from `kanban.md` to `kanban.json` references in updated instruction files (`rg` no `kanban.md` matches; expected `kanban.json` matches present).
	- Mandatory dashboard gate executed; broad out-of-scope project doc side effects remained unstaged.
	- Docs policy gate passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
	- PR created for branch: https://github.com/UndiFineD/PyAgent/pull/260.

### Lesson
- Pattern: Mandatory dashboard generation introduces unrelated project-doc churn during scoped @9git closure work.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project overview files in a single run.
- Prevention: Run dashboard gate before staging, then enforce explicit file allowlist staging for active project artifacts only.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system; prj0000107-idea000015-specialized-agent-library
- Recurrence count: 4
- Promotion status: HARD

## 2026-03-31 - prj0000108-idea000019-crdt-python-ffi-bindings
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- status: DONE
- branch_expected: prj0000108-idea000019-crdt-python-ffi-bindings
- branch_observed: prj0000108-idea000019-crdt-python-ffi-bindings
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Received @8ql clear from `idea000019-crdt-python-ffi-bindings.ql.md` (`Status: DONE`, `CLEAR -> @9git`).
	- Mandatory dashboard refresh gate executed successfully: `python scripts/generate_project_dashboard.py` (`DASHBOARD_EXIT=0`).
	- Docs policy gate passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `12 passed`.
	- GH auth 401 override resolved via playbook by removing invalid `GITHUB_TOKEN` env override; `gh auth status` now active/pass.
	- Dashboard-generated out-of-scope docs changes detected and held unstaged for strict narrow-scope closure staging.
	- @9git closure evidence commit created and pushed: `121792c1bdfe4a5b96935d3a36b0b4498f8d7f4d`.
	- PR opened to `main`: https://github.com/UndiFineD/PyAgent/pull/261 (state: OPEN).

### Lesson
- Pattern: Invalid session-level `GITHUB_TOKEN` can silently flip gh auth active account state and block PR automation.
- Root cause: Shell environment override token was stale/invalid while keyring login remained valid.
- Prevention: Always run `gh auth status`; if 401 and env token exists, remove `GITHUB_TOKEN` and re-check before PR actions.
- First seen: 2026-03-31
- Seen in: prj0000108-idea000019-crdt-python-ffi-bindings
- Recurrence count: 1
- Promotion status: CANDIDATE

## 2026-03-31 - prj0000109-idea000002-missing-compose-dockerfile
- task_id: prj0000109-idea000002-missing-compose-dockerfile
- status: DONE
- branch_expected: prj0000109-idea000002-missing-compose-dockerfile
- branch_observed: prj0000109-idea000002-missing-compose-dockerfile
- branch_validation: PASS
- scope_validation: PASS
- notes:
	- Confirmed branch gate pass on expected project branch.
	- Mandatory dashboard refresh gate executed before staging; broad out-of-scope changes detected and excluded.
	- Explicitly excluded unrelated generated local file `.github/agents/data/pip_audit_current_8ql.json` from staging/commit.
	- Existing branch commits pushed to origin.
	- PR created targeting `main`: https://github.com/UndiFineD/PyAgent/pull/262.
	- Staged-file pre-commit gate passed for handoff artifacts (PRECOMMIT_RC=0).
	- @9git closure commit created and pushed: `7251daa69629e3100985f70301dfbfad008b6cbb`.
	- Post-push `gh` query hit `HTTP 401` due invalid `GITHUB_TOKEN`; resolved by clearing env override and re-running `gh auth status`.

### Lesson
- Pattern: Dashboard refresh consistently introduces broad out-of-scope churn during narrow project closure handoffs.
- Root cause: `scripts/generate_project_dashboard.py` rewrites many project artifacts globally by design.
- Prevention: Run dashboard gate before staging, then enforce explicit allowlist staging and verify excluded unrelated generated files stay untouched.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base; prj0000106-idea000080-smart-prompt-routing-system; prj0000107-idea000015-specialized-agent-library; prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 5
- Promotion status: HARD

## 2026-04-01 - prj0000110-idea000004-quality-workflow-branch-trigger
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- status: DONE
- branch_expected: prj0000110-idea000004-quality-workflow-branch-trigger
- branch_observed: prj0000110-idea000004-quality-workflow-branch-trigger
- branch_validation: PASS
- scope_validation: PASS_WITH_EXCLUSION
- notes:
	- Active working tree contains unrelated pre-existing modification in `scripts/project_registry_governance.py`; excluded from @9git scope and must remain unstaged.
	- Mandatory dashboard refresh gate executed before staging; generated broad out-of-scope docs updates and they were left unstaged.
	- Staged-file pre-commit gate passed on exact allowlist (PRECOMMIT_RC=0).
	- Docs policy validation passed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed`.
	- @9git commit pushed: `8ea6cfff85e448b23c253fc194ec71009cb51579`.
	- PR created targeting `main`: https://github.com/UndiFineD/PyAgent/pull/263.
	- gh auth override issue recurred and was resolved by removing invalid `GITHUB_TOKEN` env override before PR command.

### Lesson
- Pattern: Session-level `GITHUB_TOKEN` overrides can break gh auth and must be cleared to restore keyring-based authentication.
- Root cause: Invalid environment token shadowed valid keyring credentials during PR automation.
- Prevention: Always run `gh auth status`; if invalid token appears and env override exists, remove `GITHUB_TOKEN` and re-run auth check before PR operations.
- First seen: 2026-03-31
- Seen in: prj0000108-idea000019-crdt-python-ffi-bindings; prj0000110-idea000004-quality-workflow-branch-trigger
- Recurrence count: 2
- Promotion status: HARD

