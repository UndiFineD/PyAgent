# unified-transaction-manager - Implementation Plan

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-03-20_

## Overview
Implement a unified transaction orchestration layer that standardizes lifecycle semantics across file, memory, process, and context operations while reusing existing managers.

## Task List
- [ ] T1 - Inventory transaction entry points | Files: src/core, src/MemoryTransactionManager.py | Acceptance: All current transaction APIs mapped
- [ ] T2 - Define shared transaction models | Files: src/core/base/models | Acceptance: Envelope/result contracts added
- [ ] T3 - Add domain adapters | Files: src/core/*transaction* | Acceptance: file/memory/process/context adapters implemented
- [ ] T4 - Implement orchestrator lifecycle | Files: src/core | Acceptance: begin/commit/rollback path tested
- [ ] T5 - Add regression and integration tests | Files: tests/ | Acceptance: tests fail before code and pass after

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Discovery complete | T1 | IN_PROGRESS |
| M2 | Interface ready | T2 | NOT_STARTED |
| M3 | Adapters done | T3 | NOT_STARTED |
| M4 | Lifecycle complete | T4 | NOT_STARTED |
| M5 | Test validation complete | T5 | NOT_STARTED |

## Validation Commands
```powershell
python -m pytest -q
```
