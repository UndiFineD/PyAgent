# prj0000100-repo-cleanup-docs-code - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-29_

## Overview
Concrete phased roadmap for governance-first repository cleanup, covering docs cleanup, code cleanup, code structure index maintenance protocol, and search policy enforcement.

## Inputs and Constraints
- Design source: `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.design.md`.
- Project policy source: `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.
- Mandatory policy references: `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Scope boundary: project folder, tracking files, `codestructure.md`, `allowed_websites.md`, and focused guidance updates only.

## Phase Chunks
| Chunk | Phase Goal | Code Files (target) | Test Files (target) | Exit Gate |
|---|---|---|---|---|
| C1 | Lock governance protocol and contracts | 4-8 | 2-4 | Protocol checks pass; no malformed policy artifacts |
| C2 | Execute docs cleanup wave | 8-12 | 4-6 | Docs consistency checks pass; project tracking synchronized |
| C3 | Execute bounded code cleanup wave | 8-12 | 6-10 | Focused lint/tests pass for touched files |
| C4 | Close lifecycle and handoff packet | 2-4 | 1-2 | Milestones, memory, and traceability artifacts finalized |

## Task List
- [ ] T1 - Governance baseline lock
	- Objective: confirm governance artifacts and contract-bearing docs are canonical before cleanup waves.
	- Target files: `.github/agents/data/codestructure.md`, `.github/agents/data/allowed_websites.md`, `.github/copilot-instructions.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.design.md`.
	- Acceptance criteria: AC-03, AC-04, AC-05.
	- Validation command: `rg -n "^# Code Structure Index$|^\| file \| line \| code \|$|^# Allowed Websites Policy$|^## Allowed Domains$|allowed_websites\.md" .github/agents/data/codestructure.md .github/agents/data/allowed_websites.md .github/copilot-instructions.md`.

- [ ] T2 - Code structure index maintenance protocol implementation plan
	- Objective: define deterministic protocol steps for add/update/remove anchor rows and stale row cleanup in touched files.
	- Target files: `.github/agents/data/codestructure.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.code.md` (future), `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.exec.md` (future).
	- Acceptance criteria: AC-03.
	- Validation command: `python -c "from pathlib import Path; import re; p=Path('.github/agents/data/codestructure.md'); t=p.read_text(encoding='utf-8'); rows=[ln for ln in t.splitlines() if ln.startswith('| ') and ln.count('|')>=4 and not ln.startswith('| file |') and not ln.startswith('|---')]; key=[tuple(part.strip() for part in ln.strip('|').split('|')[:3]) for ln in rows]; print('PASS' if len(key)==len(set(key)) else 'FAIL:duplicate-rows'); raise SystemExit(0 if len(key)==len(set(key)) else 1)"`.

- [ ] T3 - Search policy enforcement plan
	- Objective: define fail-closed search policy flow requiring local search evidence first, then allowlist-gated external lookup.
	- Target files: `.github/agents/data/allowed_websites.md`, `.github/copilot-instructions.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.exec.md` (future).
	- Acceptance criteria: AC-04, AC-05.
	- Validation command: `rg -n "local code search first|search_subagent|rg|allowed websites|allowed_websites\.md|fail closed|allowlist" .github/agents/data/allowed_websites.md .github/copilot-instructions.md`.

- [ ] T4 - Docs cleanup wave scope and normalization
	- Objective: execute a bounded docs cleanup batch for formatting, stale references, and consistency across target docs.
	- Target files: `README.md`, `MIGRATION.md`, `docs/setup.md`, `docs/tools.md`, `docs/PROGRESS_DASHBOARD.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.
	- Acceptance criteria: AC-01, AC-02.
	- Validation command: `rg -n "TODO|TBD|FIXME" README.md MIGRATION.md docs/setup.md docs/tools.md docs/PROGRESS_DASHBOARD.md docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.

- [ ] T5 - Project tracking and lifecycle synchronization
	- Objective: keep project tracking artifacts aligned with current lifecycle state and scope.
	- Target files: `docs/project/kanban.md`, `data/projects.json`, `data/nextproject.md`, `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.
	- Acceptance criteria: AC-01, AC-02.
	- Validation command: `rg -n "prj0000100|repo-cleanup-docs-code|Discovery|Review|Released|M3|Plan finalized" docs/project/kanban.md data/projects.json data/nextproject.md docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`.

- [ ] T6 - Code cleanup wave planning (bounded file list)
	- Objective: define and execute a bounded non-destructive cleanup list for high-noise files (lint, style, unused code).
	- Target files: `src-old/tools/run_full_pipeline.py`, `src-old/tools/security/fuzzing.py`, `src-old/observability/structured_logger.py`, `src-old/observability/stats/metrics_engine.py`, `src-old/observability/stats/observability_core.py`, `src-old/observability/tracing/OpenTelemetryTracer.py`, `src-old/observability/telemetry/UsageMessage.py`.
	- Acceptance criteria: AC-01.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m flake8 src-old/tools/run_full_pipeline.py src-old/tools/security/fuzzing.py src-old/observability/structured_logger.py src-old/observability/stats/metrics_engine.py src-old/observability/stats/observability_core.py src-old/observability/tracing/OpenTelemetryTracer.py src-old/observability/telemetry/UsageMessage.py`.

- [ ] T7 - Cleanup regression guard tests planning
	- Objective: maintain/extend focused tests validating policy and cleanup gates to avoid regressions after wave execution.
	- Target files: `tests/test_zzc_flake8_config.py`, `tests/` (focused cleanup-policy tests added in downstream phases).
	- Acceptance criteria: AC-01, AC-05.
	- Validation command: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -v tests/test_zzc_flake8_config.py`.

- [ ] T8 - Closure, evidence, and handoff packet
	- Objective: finalize plan/code/test/exec/ql/git artifact linkage, AC evidence matrix, and downstream handoff readiness.
	- Target files: `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.plan.md`, `.github/agents/data/4plan.memory.md`.
	- Acceptance criteria: AC-01, AC-02, AC-03, AC-04, AC-05.
	- Validation command: `rg -n "_Status:|AC Traceability|Task List|Validation Commands|handoff|@5test" docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.plan.md .github/agents/data/4plan.memory.md`.

## Acceptance Criteria Traceability
| Task | AC Coverage | Trace Intent |
|---|---|---|
| T1 | AC-03, AC-04, AC-05 | Establish protocol-bearing governance baseline |
| T2 | AC-03 | Enforce code index schema/protocol behavior |
| T3 | AC-04, AC-05 | Enforce local-first and allowlist-gated search policy |
| T4 | AC-01, AC-02 | Cleanup and normalize docs in scoped files |
| T5 | AC-01, AC-02 | Sync project tracking and milestone data |
| T6 | AC-01 | Execute bounded code cleanup with deterministic validation |
| T7 | AC-01, AC-05 | Preserve policy and cleanup quality gates via tests |
| T8 | AC-01, AC-02, AC-03, AC-04, AC-05 | Produce complete closure evidence and handoff package |

## Dependencies and Order
1. T1 -> T2 -> T3 are required before any broad cleanup wave execution.
2. T4 and T5 can run in parallel after T1-T3 pass.
3. T6 depends on T1-T3 and should be executed in bounded batches.
4. T7 runs after each cleanup batch and before closure.
5. T8 is final and depends on T4-T7 completion.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M3.1 | Governance protocol locked | T1-T3 | PLANNED |
| M3.2 | Docs and tracking cleanup ready | T4-T5 | PLANNED |
| M3.3 | Code cleanup and tests scoped | T6-T7 | PLANNED |
| M3.4 | Closure package ready for @5test | T8 | PLANNED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
rg -n "^# Code Structure Index$|^\| file \| line \| code \|$" .github/agents/data/codestructure.md
rg -n "^# Allowed Websites Policy$|^## Allowed Domains$|^- wikipedia\.org$|^- github\.com$" .github/agents/data/allowed_websites.md
c:/Dev/PyAgent/.venv/Scripts/python.exe -m flake8 src-old/tools/run_full_pipeline.py src-old/tools/security/fuzzing.py src-old/observability/structured_logger.py src-old/observability/stats/metrics_engine.py src-old/observability/stats/observability_core.py src-old/observability/tracing/OpenTelemetryTracer.py src-old/observability/telemetry/UsageMessage.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -v tests/test_zzc_flake8_config.py
```
