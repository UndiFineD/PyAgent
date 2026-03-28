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

## Retrospective Notes

- 2026-03-20 — Branch hygiene policy tightened after multiple project artifacts referenced unrelated `prj037-*` branches. Future agents must treat this pattern as a validation failure and trigger correction rather than continuing git work.
- 2026-03-20 — `@9git` now requires a post-staging `pre-commit` run before commit/push/PR actions so narrowed staging is validated before repository updates leave the workstation.
- 2026-03-20 — User requested blanket `add -A, commit, push, PR, pull` while working tree had 6,932 changes (120 outside `src-old/`) and missing `prj037` plan artifact; workflow was halted and handed back for scope/plan correction.
- 2026-03-26 — prj0000076: `run-precommit-checks` hook uses `pass_filenames: false`, making it a repo-wide Python check that always runs regardless of `--files` filter. This hook was already failing on the branch before @9git changes (confirmed by stash test). ruff+mypy both returned Skipped for JSON/MD tracking files. Pre-existing failure should be tracked as a separate remediation project assigned to @0master.
- 2026-03-27 — prj0000086: handoff staging scope was valid (`docs/project/prj0000086-universal-agent-shell/universal-agent-shell.git.md` only), but mandatory post-staging `pre-commit` failed on unrelated repository-wide violations, so commit/push/PR actions were blocked and returned to @0master.
- 2026-03-27 — prj0000088: scope validation passed (`docs/project/kanban.md` + `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.git.md`) and unrelated untracked CodeQL examples were excluded; handoff still blocked because `run-precommit-checks` failed on existing repo-wide Ruff docstring issues in `src/core/memory/AutoMemCore.py`, so no commit/push/PR was performed and task was returned to @0master.
- 2026-03-28 — prj0000091: branch and scope validation passed; staging was narrowed to approved project files while `docs/project/PROJECT_DASHBOARD.md` remained intentionally unstaged as out-of-scope. Mandatory post-staging `pre-commit` failed on existing repository-wide Ruff violations in `tests/` outside staged files, so commit/push/PR actions were blocked and disposition was recorded in project git artifact.

## Auto-handoff

Once git operations, PRs, and merges are complete, 
the next agent to run is **@0master**. 
Invoke it via `agent/runSubagent` to continue the cycle.
