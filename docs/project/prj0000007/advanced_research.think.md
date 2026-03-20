# advanced_research - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-20_

## Root Cause Analysis
- PyAgent needs a modular home for speculative/research-phase subsystems.
- Research areas (transport, memory, multimodal, RL, speculation) all share a pattern:
  they need to be importable and testable before real implementation begins.
- Without dedicated packages, research code ends up scattered or blocking core modules.

## Options

### Option A — Skeleton top-level packages under `src/`
Create minimal `__init__.py` modules under `src/transport/`, `src/memory/`, etc.
Pros: Follows existing monorepo layout, immediately importable, zero runtime cost.
Cons: Placeholder nature must be documented carefully to avoid confusion.

### Option B — Single `src/research/` meta-package with sub-modules
Nest all research packages under one `src/research/` namespace.
Pros: Clear grouping, single entry point.
Cons: Breaks expected import paths (`import transport` vs `from research import transport`).

### Option C — Separate top-level repo per research package
Each research package lives in its own repo and is pulled in as a git submodule.
Pros: Maximum isolation.
Cons: Massive overhead for placeholder-stage work; premature.

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Delivery speed | Fast | Medium | Slow |
| Import simplicity | High | Medium | Low |
| Structural consistency | High | Medium | Low |
| Future migration cost | Low | Medium | High |

## Selected Option
**Option A** — Skeleton top-level packages under `src/`. Chosen for consistency
with existing monorepo layout and minimal friction to promote packages to full
implementations later.
