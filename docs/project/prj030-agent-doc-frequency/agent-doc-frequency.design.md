# agent-doc-frequency — Design

_Status: DONE — Ready for @4plan_
_Designer: @3design | Date: 2026-03-18_

---

## 1. Selected Option

**Option A — Step-Gated Full Overwrite** (from agent-doc-frequency.think.md).

Every agent rewrites its entire artifact file after completing each numbered step in its Operating Procedure. This matches the existing write pattern (agents already fully-overwrite `.think.md` / `.design.md` at the end of a session), applied at higher frequency. Zero Python code changes required; the entire implementation is instruction text in `*.agent.md` files.

**Design decisions confirmed by project owner:**
- Templates inline per agent (each `*.agent.md` contains its own artifact template).
- Both `@1project` pre-creates all 9 stubs AND each agent defensively creates its file at Step 1 if missing.
- Checkpoint rule backported to all 9 artifact types, including the existing `.project.md`, `.think.md`, `.design.md`, `.plan.md`.
- Documents updated **before** `runSubagent` is called for the next agent.

---

## 2. Checkpoint Rule — Exact Instruction Text

The following block is inserted into each agent's "Operating procedure" section, parameterized only by `<doctype>`:

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

## 3. Nine Artifact Templates

Each template is embedded inline in the respective agent's `*.agent.md` file.

### `.project.md` — owned by @1project
```
# <project-name> — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: <date>_

## Project Overview
<one paragraph description>

## Goal & Scope
**Goal:** <goal>
**In scope:** <items>
**Out of scope:** <items>

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think |  |
| M2 | Design confirmed | @3design |  |
| M3 | Plan finalized | @4plan |  |
| M4 | Tests written | @5test |  |
| M5 | Code implemented | @6code |  |
| M6 | Integration validated | @7exec |  |
| M7 | Security clean | @8ql |  |
| M8 | Committed | @9git |  |

## Status
_Last updated: <date>_
<current status narrative>
```

### `.think.md` — owned by @2think
```
# <project-name> — Options

_Status: IN_PROGRESS_
_Analyst: @2think | Updated: <date>_

## Root Cause Analysis
<root causes>

## Options
### Option A — <name>
<description, pros, cons>

### Option B — <name>
<description, pros, cons>

### Option C — <name>
<description, pros, cons>

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| <criterion 1> | | | |

## Recommendation
**Option <X>** — <rationale>

## Open Questions
1. <question for @3design>
```

### `.design.md` — owned by @3design
```
# <project-name> — Design

_Status: IN_PROGRESS_
_Designer: @3design | Updated: <date>_

## Selected Option
<option name and rationale>

## Architecture
<high-level architecture prose or diagram>

## Interfaces & Contracts
<key classes, methods, endpoints, data shapes>

## Non-Functional Requirements
- Performance: <requirement>
- Security: <requirement>
- Testability: <requirement>

## Open Questions
<any unresolved questions for @4plan>
```

### `.plan.md` — owned by @4plan
```
# <project-name> — Implementation Plan

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: <date>_

## Overview
<summary of what is being built and why>

## Task List
- [ ] T1 — <task description> | Files: <files> | Acceptance: <criteria>
- [ ] T2 — <task description> | Files: <files> | Acceptance: <criteria>

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | <milestone> | T1, T2 | |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q
python -m mypy <module>
python -m ruff check <module>
```
```

### `.test.md` — owned by @5test
```
# <project-name> — Test Artifacts

_Status: IN_PROGRESS_
_Tester: @5test | Updated: <date>_

## Test Plan
<scope, approach, frameworks used>

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC1 | <description> | tests/<file>.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC1 | | |

## Unresolved Failures
<any failing tests with diagnostics>
```

### `.code.md` — owned by @6code
```
# <project-name> — Code Artifacts

_Status: IN_PROGRESS_
_Coder: @6code | Updated: <date>_

## Implementation Summary
<what was implemented and key decisions made>

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| <module> | <change type> | +N/-N |

## Test Run Results
```
<paste of pytest -q output>
```

## Deferred Items
<any items not implemented, with reason>
```

### `.exec.md` — owned by @7exec
```
# <project-name> — Execution Log

_Status: IN_PROGRESS_
_Executor: @7exec | Updated: <date>_

## Execution Plan
<which commands will be run and why>

## Run Log
```
<timestamped command output>
```

## Pass/Fail Summary
| Check | Status | Notes |
|---|---|---|
| pytest -q | | |
| mypy | | |
| ruff | | |
| import check | | |
| smoke test | | |

## Blockers
<anything preventing handoff to @8ql>
```

### `.ql.md` — owned by @8ql
```
# <project-name> — Security Scan Results

_Status: IN_PROGRESS_
_Scanner: @8ql | Updated: <date>_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| <file> | Python security | CodeQL |

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|

## False Positives
| ID | Reason |
|---|---|

## Cleared
All HIGH/CRITICAL findings must be cleared before @9git proceeds.
Current status: <CLEAR or BLOCKED>
```

### `.git.md` — owned by @9git
```
# <project-name> — Git Summary

_Status: IN_PROGRESS_
_Git: @9git | Updated: <date>_

## Branch
`<branch-name>`

## Commit Hash
`<sha>`

## Files Changed
| File | Change |
|---|---|
| <file> | added/modified/deleted |

## PR Link
<URL or "N/A — direct merge">
```

---

## 4. @1project Step 1 Additions

Add to **Step 1 — Create or validate project folder** in `1project.agent.md`:

```
- Ensure ALL 9 artifact stub files exist in the project folder:
  - `<project>.project.md`  (see inline template below)
  - `<project>.think.md`    (see inline template below)
  - `<project>.design.md`   (see inline template below)
  - `<project>.plan.md`     (see inline template below)
  - `<project>.test.md`     (see inline template below)
  - `<project>.code.md`     (see inline template below)
  - `<project>.exec.md`     (see inline template below)
  - `<project>.ql.md`       (see inline template below)
  - `<project>.git.md`      (see inline template below)
- If any stub is missing, create it using the inline template for that type with `_Status: IN_PROGRESS_`.
- Stubs for downstream agents (@5test through @9git) are pre-created with the header only and `_Status: NOT_STARTED_`.
```

---

## 5. Impact Table

| Agent file | Change type | Summary |
|---|---|---|
| `1project.agent.md` | Add to Step 1 | List all 9 stubs; create missing stubs; add checkpoint rule for `.project.md` |
| `2think.agent.md` | Add checkpoint rule | Rewrite `.think.md` after each of Steps 1–4; final write before @3design call |
| `3design.agent.md` | Add checkpoint rule | Rewrite `.design.md` after each of Steps 1–4; final write before @4plan call |
| `4plan.agent.md` | Add checkpoint rule | Rewrite `.plan.md` after each of Steps 1–5; final write before @5test call |
| `5test.agent.md` | Add template + checkpoint rule | Add `.test.md` template; rewrite after each phase step |
| `6code.agent.md` | Add template + checkpoint rule | Add `.code.md` template; rewrite after each of Steps 1–6 |
| `7exec.agent.md` | Add template + checkpoint rule | Add `.exec.md` template; rewrite after each of Steps 1–7 |
| `8ql.agent.md` | Add template + checkpoint rule | Add `.ql.md` template; rewrite after each of Steps 1–5 |
| `9git.agent.md` | Add template + checkpoint rule | Add `.git.md` template; rewrite after each operational section |

---

## 6. Non-Functional Requirements

- **Atomicity:** Direct file writes via VS Code `createFile`/`editFiles` tool calls. Single write per checkpoint. No `StorageTransaction` dependency (not yet implemented). Acceptable for single-machine, single-agent-at-a-time execution.
- **Backwards compatibility:** Existing project folders without the new stubs are handled by each agent's defensive Step 1 create-if-missing logic. No migration script required.
- **Token cost:** Full overwrite per step is acceptable; artifact files are expected to be < 200 lines each.
- **Failure recovery:** If a `runSubagent` call is interrupted, the last checkpoint write provides a partial artifact. The downstream agent reads the partial file and continues where the status section indicates.
