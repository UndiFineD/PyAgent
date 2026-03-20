# agent-doc-frequency — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-18_

---

## Overview

Backport a **Step-Gated Full Overwrite** checkpoint rule to all 9 `*.agent.md` files in
`.github/agents/`. Each agent receives:

1. A verbatim **Checkpoint rule (MANDATORY)** block inserted into its Operating Procedure.
2. An **inline artifact template** for its owned document type.
3. For `@1project` only: Step 1 is extended to pre-create all 9 stubs.

No Python code changes are involved. `@5test` is skipped; handoff goes directly to `@6code`.

---

## Task List

- [ ] T0 — Survey: read every target file before editing
  - Files: `.github/agents/1project.agent.md` through `9git.agent.md`
  - Acceptance: Full content of all 9 files confirmed; no existing checkpoint rule found.

- [ ] T1 — Edit `1project.agent.md`
  - (a) Extend Step 1 to require all 9 stub files and create any that are missing.
  - (b) Add inline templates for all 9 artifact types at the bottom of the file.
  - (c) Insert checkpoint rule (doctype = `project`) after Step 1.
  - Acceptance: Checkpoint rule present, all 9 stub names listed, template present.

- [ ] T2 — Edit `2think.agent.md`
  - (a) Insert checkpoint rule (doctype = `think`) in Operating Procedure, triggers at Steps 1–4.
  - (b) Add inline `.think.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T3 — Edit `3design.agent.md`
  - (a) Insert checkpoint rule (doctype = `design`) in Operating Procedure, triggers at Steps 1–4.
  - (b) Add inline `.design.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T4 — Edit `4plan.agent.md`
  - (a) Insert checkpoint rule (doctype = `plan`) in Operating Procedure, triggers at Steps 1–5.
  - (b) Add inline `.plan.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T5 — Edit `5test.agent.md`
  - (a) Insert checkpoint rule (doctype = `test`) in Operating Procedure.
  - (b) Add inline `.test.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T6 — Edit `6code.agent.md`
  - (a) Insert checkpoint rule (doctype = `code`) in Operating Procedure, one trigger per step.
  - (b) Add inline `.code.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T7 — Edit `7exec.agent.md`
  - (a) Insert checkpoint rule (doctype = `exec`) in Operating Procedure, one trigger per step.
  - (b) Add inline `.exec.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T8 — Edit `8ql.agent.md`
  - (a) Insert checkpoint rule (doctype = `ql`) in Operating Procedure.
  - (b) Add inline `.ql.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

- [ ] T9 — Edit `9git.agent.md`
  - (a) Insert checkpoint rule (doctype = `git`) in Operating Procedure.
  - (b) Add inline `.git.md` template at the bottom of the file.
  - Acceptance: Checkpoint rule present, template present.

---

## Checkpoint rule text (verbatim — insert into every agent)

```
**Checkpoint rule (MANDATORY):**
1. At the start of Step 1 — ensure `docs/project/<project>/<project>.<doctype>.md` exists.
   If missing, create it from the inline template below with `_Status: IN_PROGRESS_`.
   If present, overwrite the status line to `_Status: IN_PROGRESS_`.
2. After completing each subsequent numbered step — overwrite `docs/project/<project>/<project>.<doctype>.md`
   with the full current content of all template sections. Never omit a section.
3. Before calling `runSubagent` for the next agent — do a final overwrite and set `_Status: DONE_`.
   If work is handed off mid-task, use `_Status: HANDED_OFF_` instead.
```

---

## Validation Commands

```powershell
# All 9 agent files must contain the checkpoint rule string
rg "Checkpoint rule" .github/agents/ -l
```

Expected: exactly 9 filenames returned, one per agent file.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Survey complete | T0 | |
| M2 | Upstream agents updated | T1–T4 | |
| M3 | Downstream agents updated | T5–T9 | |
| M4 | Validation passes | — | |
