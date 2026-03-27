# prj0000082 — agent-execution-sandbox — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-26_

## Project Identity
**Project ID:** prj0000082
**Short name:** agent-execution-sandbox
**Project folder:** `docs/project/prj0000082-agent-execution-sandbox/`

## Project Overview
SandboxMixin: restrict each agent's file and network access to approved path sets; integrated with StateTransaction validation.

## Problem Statement
Agents currently have unrestricted access to the filesystem and network within the process. A compromised or
buggy agent could read/write outside its intended scope or make unauthorized network calls. The SandboxMixin
enforces access control at the Python layer before any I/O operation is dispatched.

## Goals
- [ ] Define `SandboxConfig` dataclass with `allowed_paths: list[Path]` and `allowed_hosts: list[str]`
- [ ] Implement `SandboxMixin` that reads config and validates every StorageTransaction path
- [ ] Raise `SandboxViolationError` on any unauthorized path or host access
- [ ] Integrate with existing `StateTransaction` validation hook
- [ ] Achieve ≥90% test coverage on sandbox module
- [ ] Zero regressions in existing 129+ structure tests

## Scope Boundary
**In scope:** `src/core/sandbox/` (new module), mixin integration in `src/core/base/mixins/`
**Out of scope:** network-level firewalling (OS-level), Rust FFI for this phase

## Branch Plan
**Expected branch:** `prj0000082-agent-execution-sandbox`
**Scope boundary:** `docs/project/prj0000082-agent-execution-sandbox/` and `src/core/sandbox/` and
`src/core/base/mixins/` and associated test files under `tests/`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch matches
this project and the changed files stay inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous,
return the task to `@0master` before downstream handoff.

## Acceptance Criteria
- `SandboxMixin` can be composed into any `BaseAgent` subclass
- Attempting to write outside `allowed_paths` raises `SandboxViolationError`
- All existing pytest structure tests still pass after integration
- Module has type annotations and passes mypy

## Dependencies
- `src/core/base/mixins/` — mixin architecture
- `src/core/base/agent_state_manager.py` — state/storage transaction hooks
- `tests/structure/` — must pass with zero regressions

## Priority & Budget
- **Priority:** P2
- **Budget:** S
- **Tags:** security, sandbox, core

## Milestones
| # | Milestone            | Agent    | Status      |
|---|----------------------|----------|-------------|
| M1 | Options explored    | @2think  |             |
| M2 | Design confirmed    | @3design |             |
| M3 | Plan finalized      | @4plan   |             |
| M4 | Tests written       | @5test   |             |
| M5 | Code implemented    | @6code   |             |
| M6 | Integration validated | @7exec |             |
| M7 | Security clean      | @8ql     |             |
| M8 | Committed           | @9git    |             |

## Artifact Links
| File | Purpose |
|------|---------|
| [prj0000082-agent-execution-sandbox.think.md](prj0000082-agent-execution-sandbox.think.md) | Options exploration |
| [prj0000082-agent-execution-sandbox.design.md](prj0000082-agent-execution-sandbox.design.md) | Architecture design |
| [prj0000082-agent-execution-sandbox.plan.md](prj0000082-agent-execution-sandbox.plan.md) | Implementation plan |
| [prj0000082-agent-execution-sandbox.test.md](prj0000082-agent-execution-sandbox.test.md) | Test artifacts |
| [prj0000082-agent-execution-sandbox.code.md](prj0000082-agent-execution-sandbox.code.md) | Code artifacts |
| [prj0000082-agent-execution-sandbox.exec.md](prj0000082-agent-execution-sandbox.exec.md) | Execution log |
| [prj0000082-agent-execution-sandbox.ql.md](prj0000082-agent-execution-sandbox.ql.md) | Security scan results |
| [prj0000082-agent-execution-sandbox.git.md](prj0000082-agent-execution-sandbox.git.md) | Git summary |

## Status
_Last updated: 2026-03-26_
Project folder created. All 9 artifact stubs initialized. Handing off to @2think for options exploration.


## Goal & Scope
**Goal:** Keep this historical project document template-compliant.
Goal: keep this historical project document template-compliant. Scope: documentation structure only.

