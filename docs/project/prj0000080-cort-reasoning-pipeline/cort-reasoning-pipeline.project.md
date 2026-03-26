# cort-reasoning-pipeline — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-26_

## Project Identity
**Project ID:** prj0000080
**Short name:** cort-reasoning-pipeline
**Project folder:** `docs/project/prj0000080-cort-reasoning-pipeline/`

## Project Overview
Chain-of-Recursive-Thoughts (CoRT) is a multi-round recursive reasoning pipeline that
enables PyAgent's AI agents to perform structured self-improvement reasoning loops.
Instead of returning a single LLM response, CoRT generates N alternative reasoning
chains per round, evaluates them against a rubric (correctness, completeness,
reasoning-depth), and selects the best answer. The process repeats for a configurable
number of rounds, with each round using temperature-variant generation to explore the
solution space more broadly.

CoRT addresses a core limitation in PyAgent's current agents: they issue a single
prompt-response cycle with no self-critique or iterative refinement. By adding a CoRT
mixin, any existing agent (CoderAgent, SecurityAgent, etc.) can opt into structured
multi-round reasoning without changes to its core orchestration logic.

## Goal & Scope

**Goal:** Implement the Chain-of-Recursive-Thoughts reasoning pipeline as a reusable
async mixin for PyAgent agents, complete with a standalone evaluation engine and full
unit test coverage.

**In scope:**
- `src/core/reasoning/CortCore.py` — core recursive reasoning loop (N rounds, M alternatives)
- `src/core/reasoning/CortAgent.py` — agent wrapper / mixin that integrates CoRT
- `src/core/reasoning/EvaluationEngine.py` — scores alternative chains on rubric
- `src/core/reasoning/__init__.py` — module init and public API
- `tests/unit/test_CortCore.py` — unit tests for CortCore
- `tests/unit/test_EvaluationEngine.py` — unit tests for EvaluationEngine
- All project documentation stubs in this folder

**Out of scope:**
- Changes to existing agent classes other than opt-in mixin usage examples
- New LLM backends or provider integrations (CoRT uses existing registered backends)
- UI components or CLI changes
- Persistent storage of reasoning chains (in-memory only for now)
- Distributed / multi-agent CoRT orchestration

## Branch Plan
**Expected branch:** `prj0000080-cort-reasoning-pipeline`
**Scope boundary:** `docs/project/prj0000080-cort-reasoning-pipeline/`,
`src/core/reasoning/`, `tests/unit/test_CortCore.py`,
`tests/unit/test_EvaluationEngine.py`, plus `docs/project/kanban.md` and
`data/projects.json` for lifecycle updates.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch is `prj0000080-cort-reasoning-pipeline` and the changed files stay inside
the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Key Components

| File | Purpose |
|---|---|
| `src/core/reasoning/CortCore.py` | Core recursive reasoning loop — N rounds × M alternatives with temperature variation |
| `src/core/reasoning/CortAgent.py` | Agent wrapper / mixin exposing `async reason(prompt)` to any BaseAgent subclass |
| `src/core/reasoning/EvaluationEngine.py` | Scores each reasoning chain on rubric (correctness, completeness, reasoning-depth); returns ranked list |
| `src/core/reasoning/__init__.py` | Module init; exports `CortCore`, `CortAgent`, `EvaluationEngine` |
| `tests/unit/test_CortCore.py` | Unit tests for CortCore: round counts, alternative generation, temperature variation, selection logic |
| `tests/unit/test_EvaluationEngine.py` | Unit tests for EvaluationEngine: rubric scoring, ranking, edge cases (empty chains, ties) |

## Design Notes

### Recursion model
- `rounds` (default=3): number of recursive self-critique iterations
- `alternatives` (default=3): number of competing chains generated per round
- Each alternative uses a different temperature (`base_temp + i * temp_step`) to
  maximise diversity across the solution space

### EvaluationEngine rubric
Each chain is scored 0–10 on three axes:
1. **Correctness** — factual accuracy and logical consistency
2. **Completeness** — covers all aspects of the prompt
3. **Reasoning-depth** — shows step-by-step derivation rather than a bare answer

The final score is a weighted sum (weights configurable, default: 0.5 / 0.3 / 0.2).
The chain with the highest score is selected as the output of each round; the winning
chain from the final round becomes the agent's response.

### Architecture integration
- **Mixin-based**: `CortAgent` extends `BaseAgent` following the pattern used in
  `src/core/base/mixins/`. No deep inheritance changes needed.
- **Async-first**: all LLM calls, evaluation steps, and I/O use `asyncio`; no blocking
  calls anywhere in the pipeline.
- **Context lineage**: each CoRT invocation opens a `ContextTransaction` (from
  `ContextTransactionManager.py`) to prevent infinite recursion and ensure proper
  task attribution in the swarm.
- **LLM-backend agnostic**: `CortCore` accepts any callable matching the registered
  backend protocol; no hard dependency on a specific provider.
- **PascalCase modules**: all filenames follow project convention.

### Open questions for @2think
1. Should the EvaluationEngine use a lightweight local LLM call for scoring, or a
   heuristic parser? (Cost/latency tradeoff)
2. Is a configurable scoring weight API needed at agent-instantiation time, or is a
   global default sufficient for V1?
3. Should losing chains be logged (for future fine-tuning datasets)?

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Project setup | @1project | DONE |
| M2 | Options explored | @2think | |
| M3 | Design confirmed | @3design | |
| M4 | Plan finalized | @4plan | |
| M5 | Tests written | @5test | |
| M6 | Code implemented | @6code | |
| M7 | Integration validated | @7exec | |
| M8 | Security clean | @8ql | |
| M9 | Committed | @9git | |

## Acceptance Criteria
1. `src/core/reasoning/CortCore.py` implements `async reason(prompt, rounds, alternatives)` returning the best chain
2. `src/core/reasoning/EvaluationEngine.py` implements `score(chain) -> float` and `rank(chains) -> list[str]`
3. `src/core/reasoning/CortAgent.py` integrates `CortCore` as a mixin for `BaseAgent`
4. All unit tests in `tests/unit/test_CortCore.py` and `tests/unit/test_EvaluationEngine.py` pass
5. `pytest src/ tests/ -x -q` exits 0 with no new failures
6. flake8 reports 0 violations in `src/core/reasoning/`
7. Each new Python file carries the Apache 2.0 license header
8. `data/projects.json` shows `"lane": "Discovery"` for `prj0000080`
9. `docs/project/kanban.md` shows `prj0000080` in the Discovery lane

## Status
_Last updated: 2026-03-26_
Project folder created; all stubs initialised. Branch `prj0000080-cort-reasoning-pipeline`
is active. Ready for handoff to `@2think` for options exploration.
