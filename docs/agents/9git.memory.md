# 9git Memory

This file records git operations, branch status, 
and pull request coordination notes.

## Standing Rules

- One project, one branch. A `prjNNN` task must use its own project-specific branch.
- Do not treat another project's active branch as valid just because it already contains related repository changes.
- Validate branch/project match before any staging, commit, push, or PR action.
- Validate changed-file scope against the project overview scope boundary before any staging.
- Do not use blanket staging for project work (`git add .`, `git add -A`, or equivalent).
- On validation failure, stop git work, update the project git artifact, record a short retrospective note here, and hand the task back to `@0master`.

## Retrospective Notes

- 2026-03-20 — Branch hygiene policy tightened after multiple project artifacts referenced unrelated `prj037-*` branches. Future agents must treat this pattern as a validation failure and trigger correction rather than continuing git work.

## Auto-handoff

Once git operations, PRs, and merges are complete, 
the next agent to run is **@0master**. 
Invoke it via `agent/runSubagent` to continue the cycle.
