# prj030 — Agent Document Frequency

**Status:** IN_PROGRESS  
**Created:** 2026-03-18  
**Owner:** @1project  

---

## Goal

Extend the PyAgent agent workflow system so every agent writes incremental progress
to its own artifacts **after every major finding** (not just at completion).

Currently agents only update `docs/agents/Nagent.memory.md` and the four canonical
project docs (`project.md`, `think.md`, `design.md`, `plan.md`) when their entire
subagent call ends.  The user wants live, per-agent artifact files inside the project
folder that show in-progress state so the human (and other agents) can track work
without waiting for a subagent to exit.

---

## Scope

| In scope | Out of scope |
|---|---|
| Extend per-project file schema with `test.md`, `code.md`, `exec.md`, `ql.md`, `git.md` | Changing the underlying `runSubagent` invocation model |
| Update agent mode instructions to write incremental checkpoints | Real-time filesystem watchers / inotify integrations |
| Define a checkpoint cadence policy (every finding / every sub-task) | GUI dashboard auto-refresh |
| Update `docs/agents/Nagent.memory.md` write contract | Adding new agents |

---

## Milestones

| # | Milestone | Target |
|---|---|---|
| M1 | Options explored, Option selected | @2think ✅ |
| M2 | Design confirmed, file schema defined | @3design |
| M3 | Implementation plan with task list | @4plan |
| M4 | Tests written for checkpoint logic | @5test |
| M5 | Agent instruction patches implemented | @6code |
| M6 | Integration validation green | @7exec |
| M7 | Security / static analysis clean | @8ql |
| M8 | Committed to branch | @9git |

---

## Stakeholders

| Role | Name |
|---|---|
| Requester | User (UndiFineD) |
| Workflow owner | @1project |
| Primary impacted | @2think … @9git (all agents) |

---

## Key Constraints

- Must not break existing `docs/agents/Nagent.memory.md` structure.
- File writes must be **atomic** (use `StorageTransaction` or equivalent).
- New artifact file names follow existing `<project-slug>.<doc-type>.md` convention.
- Agent instructions must work inside the `runSubagent` + VS Code Copilot model  
  (no persistent background threads; checkpoints are synchronous file writes at defined  
  step boundaries).

---

## Artifact Links

| File | Purpose |
|---|---|
| [agent-doc-frequency.think.md](agent-doc-frequency.think.md) | Options exploration |
| [agent-doc-frequency.design.md](agent-doc-frequency.design.md) | Selected design |
| [agent-doc-frequency.plan.md](agent-doc-frequency.plan.md) | Implementation task list |
| [agent-doc-frequency.test.md](agent-doc-frequency.test.md) | Test artefacts (@5test) |
| [agent-doc-frequency.code.md](agent-doc-frequency.code.md) | Code artefacts (@6code) |
| [agent-doc-frequency.exec.md](agent-doc-frequency.exec.md) | Execution log (@7exec) |
| [agent-doc-frequency.ql.md](agent-doc-frequency.ql.md) | Security scan results (@8ql) |
| [agent-doc-frequency.git.md](agent-doc-frequency.git.md) | Git commit summary (@9git) |
