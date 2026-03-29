# 9git Memory

This file records git operations, branch status, 
and pull request coordination notes.

## Standing Rules

- One project, one branch. A `prjNNN` task must use its own project-specific branch.
- Do not treat another project's active branch as valid just because it already contains related repository changes.
- Validate branch/project match before any staging, commit, push, or PR action.
- Validate changed-file scope against the project overview scope boundary before any staging.
- After `git add` of the validated project files, run `pre-commit` before commit, push, or PR actions.
- Treat that `pre-commit` run as a local workstation gate; do not mirror it as a GitHub-side requirement unless explicitly requested.
- Do not bypass the post-staging `pre-commit` run with `--no-verify` or skipped hooks for normal project work.
- Do not use blanket staging for project work (`git add .`, `git add -A`, or equivalent).
- On validation failure, stop git work, update the project git artifact, record a short retrospective note here, and hand the task back to `@0master`.
- Before any `gh pr view/create/edit`, run `gh auth status` and record the result in git handoff evidence.
- If `gh` returns 401 and `GITHUB_TOKEN` is present, clear the session override (`Remove-Item Env:GITHUB_TOKEN`) and retry `gh auth status` before declaring BLOCKED.
- Prefer branch-scoped PR commands: `gh pr view --head <branch>` then `gh pr create --base main --head <branch>` when missing, otherwise `gh pr edit`.

## Retrospective Notes

- 2026-03-20 — Branch hygiene policy tightened after multiple project artifacts referenced unrelated `prj037-*` branches. Future agents must treat this pattern as a validation failure and trigger correction rather than continuing git work.
- 2026-03-20 — `@9git` now requires a post-staging `pre-commit` run before commit/push/PR actions so narrowed staging is validated before repository updates leave the workstation.
- 2026-03-20 — User requested blanket `add -A, commit, push, PR, pull` while working tree had 6,932 changes (120 outside `src-old/`) and missing `prj037` plan artifact; workflow was halted and handed back for scope/plan correction.
- 2026-03-26 — prj0000076: `run-precommit-checks` hook uses `pass_filenames: false`, making it a repo-wide Python check that always runs regardless of `--files` filter. This hook was already failing on the branch before @9git changes (confirmed by stash test). ruff+mypy both returned Skipped for JSON/MD tracking files. Pre-existing failure should be tracked as a separate remediation project assigned to @0master.
- 2026-03-27 — prj0000086: handoff staging scope was valid (`docs/project/prj0000086-universal-agent-shell/universal-agent-shell.git.md` only), but mandatory post-staging `pre-commit` failed on unrelated repository-wide violations, so commit/push/PR actions were blocked and returned to @0master.
- 2026-03-27 — prj0000088: scope validation passed (`docs/project/kanban.md` + `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.git.md`) and unrelated untracked CodeQL examples were excluded; handoff still blocked because `run-precommit-checks` failed on existing repo-wide Ruff docstring issues in `src/core/memory/AutoMemCore.py`, so no commit/push/PR was performed and task was returned to @0master.
- 2026-03-28 — prj0000091: branch and scope validation passed; staging was narrowed to approved project files while `docs/project/PROJECT_DASHBOARD.md` remained intentionally unstaged as out-of-scope. Mandatory post-staging `pre-commit` failed on existing repository-wide Ruff violations in `tests/` outside staged files, so commit/push/PR actions were blocked and disposition was recorded in project git artifact.
- 2026-03-28 — prj0000092: branch and scope validation passed on `prj0000092-mypy-strict-enforcement`; narrow staging included project artifacts, strict-lane config/CI/tests, src/core compatibility fix, registry/kanban/nextproject updates, and agent-memory files, while `pip_audit_results.json` and `docs/project/PROJECT_DASHBOARD.md` were explicitly excluded as out-of-scope.
- 2026-03-28 — prj0000092 follow-up: local commit and push succeeded, but `gh` PR creation was blocked by `HTTP 401: Bad credentials`; preserve pushed-branch PR URL in project git artifact and hand off for authenticated PR creation.
- 2026-03-29 — prj0000098: branch/scope validation passed, narrow staging + post-staging pre-commit passed, and push to origin succeeded; GitHub CLI PR view/create both blocked by `HTTP 401: Bad credentials`.
	Pattern: PR operations blocked by expired or missing GitHub CLI authentication after successful push.
	Root cause: `gh` token/session was invalid for GraphQL API calls (`gh pr view`, `gh pr create`).
	Prevention: Run `gh auth status` and refresh credentials (`gh auth login`) before invoking @9git PR steps.
	First seen: 2026-03-28.
	Seen in: `prj0000092-mypy-strict-enforcement`, `prj0000098-backend-health-check-endpoint`.
	Recurrence count: 2.
	Promotion status: Promoted to hard rule (require `gh` auth check before PR operations).
- 2026-03-28 — prj0000093: branch/scope validation passed and narrow staging correctly excluded `docs/project/PROJECT_DASHBOARD.md` and `pip_audit_results.json`, but mandatory post-staging `pre-commit` failed on repository-wide `ruff check src tests` baseline debt (141 violations outside staged scope); commit/push/PR was blocked and returned to @0master.
- 2026-03-28 — prj0000095: branch validation passed and straightforward Ruff auto-fixes were applied to changed files, but mandatory `run-precommit-checks` remained blocked by environment-level dependency drift during pytest collection.
	Pattern: Pre-commit blocked by Python dependency mismatch outside narrowed staging scope.
	Root cause: Interpreter environment used by hook resolved `pydantic` with incompatible `pydantic-core` (`2.43.0` vs required `2.41.5`).
	Prevention: Pin and repair Python dependency pair in the environment used by hooks before invoking `@9git` handoff.
	First seen: 2026-03-28.
	Seen in: `prj0000095-source-stub-remediation`.
	Recurrence count: 1.
	Promotion status: Candidate (not promoted; threshold is >=2).
- 2026-03-29 — prj0000099: branch/scope validation passed and narrow staging was prepared for project closure, but mandatory post-staging `pre-commit` failed in `run-precommit-checks` due repository-wide Ruff findings in `tests/` outside staged scope; commit/push/PR were blocked and handoff returned to `@0master`.
	Pattern: Project-scoped handoff blocked by repository-wide hook baseline debt.
	Root cause: `run-precommit-checks` executes `ruff check src tests` without staged-file scoping.
	Prevention: Reduce baseline Ruff debt or split hook policy so project-scoped docs handoffs are not blocked by unrelated violations.
	First seen: 2026-03-28.
	Seen in: `prj0000093-projectmanager-ideas-autosync`, `prj0000099-stub-module-elimination`.
	Recurrence count: 2.
	Promotion status: Promoted to hard rule (run/verify repo-wide hook health before starting @9git handoff for docs-only closures).
- 2026-03-29 — prj0000099 completion: branch validation, scoped staging, post-staging pre-commit, commit, push, and PR creation all completed successfully.
	Pattern: GitHub CLI authentication can fail when an invalid `GITHUB_TOKEN` environment override is present even with a valid keyring login.
	Root cause: `gh` preferred the invalid environment token and returned `HTTP 401` until the override was cleared.
	Prevention: Run `gh auth status`, clear invalid `GITHUB_TOKEN` for the session, then retry `gh pr view/create` on the active account.
	First seen: 2026-03-29.
	Seen in: `prj0000099-stub-module-elimination`.
	Recurrence count: 1.
	Promotion status: Candidate (not promoted; threshold is >=2).
- 2026-03-29 — PR command hardening: standardized @9git PR flow to `gh auth status` -> branch-scoped `gh pr view --head <branch>` -> `gh pr create --base main --head <branch>` or `gh pr edit`.
	Pattern: Ad-hoc PR command variants increase failure rate and duplicate/failed PR attempts under partial auth states.
	Root cause: Missing deterministic command order and missing preflight auth gate in prior runs.
	Prevention: Enforce the command playbook in @9git operating procedure and record auth evidence in git artifacts.
	First seen: 2026-03-29.
	Seen in: `prj0000092-mypy-strict-enforcement`, `prj0000098-backend-health-check-endpoint`, `prj0000099-stub-module-elimination`.
	Recurrence count: 3.
	Promotion status: Promoted to hard rule.

## Auto-handoff

Once git operations, PRs, and merges are complete, 
the next agent to run is **@0master**. 
Invoke it via `agent/runSubagent` to continue the cycle.
