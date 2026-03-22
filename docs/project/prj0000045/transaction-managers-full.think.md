# transaction-managers-full — Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-22_

## Summary
Full analysis lives in `docs/agents/2think.memory.md` § 3.1 "Transaction Unification"
and §§ 4.1–4.7. This file is the canonical entry point for the think phase.

## Root Cause Analysis
Three of four transaction managers (Storage, Process, Context) are absent from the
codebase. `MemoryTransaction` exists but is a bare `threading.RLock` with no key/value
storage, no encryption, and no async support aligned with `BaseTransaction` contract.
`prj0000044` created minimal CI stubs that are non-functional for swarm use.

## Options
### Option A — Co-locate all four in a single file
Pack `MemoryTransaction`, `StorageTransaction`, `ProcessTransaction`,
`ContextTransaction` into one module.
**Pros:** Simple single import. **Cons:** SRP violation; hard to replace individually.

### Option B — `src/transactions/` package (**SELECTED**)
Dedicated package with `BaseTransaction` ABC and one PascalCase file per manager.
**Pros:** Clean interface; shared ABC enforces contracts; Rust FFI path is clear; single
import surface `from src.transactions import *`. **Cons:** New package to maintain.

### Option C — Domain-local files
Each manager lives in its domain package (`storage/`, `process/`, etc.).
**Pros:** Conceptually pure. **Cons:** Circular import risk; scattered.

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Interface consistency | Hard | **Easy** | Risky |
| Discoverability | Poor | **High** | Medium |
| Circular-import risk | Low | **Low** | High |
| PascalCase module rule | Awkward | **Clean** | Clean |
| Rust acceleration path | Difficult | **Easy** | Scattered |

## Recommendation
**Option B** — `src/transactions/` package. Rationale: canonical import surface,
shared `BaseTransaction` ABC enforces consistent `async with` contracts, no
circular-import risk, and clear path for Rust FFI acceleration. See
`docs/agents/2think.memory.md` §3.1 for full analysis.

## Open Questions
None remaining for this analysis. Design can proceed from the binding contracts
in §§ 4.1–4.7 of `2think.memory.md`.
