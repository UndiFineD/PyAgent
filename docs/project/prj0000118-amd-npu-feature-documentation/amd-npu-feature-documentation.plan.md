# amd-npu-feature-documentation - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-03_

## Overview
Deliver a docs-only implementation that makes AMD NPU feature usage auditable and testable without changing runtime code or CI workflows. This plan maps all work to AC-AMD-001..006 and IFACE-AMD-001..006, with deterministic validation commands and explicit evidence contracts for @5test, @6code, @7exec, and @8ql.

## Branch Gate
- Project ID: prj0000118
- Expected branch: prj0000118-amd-npu-feature-documentation
- Observed branch: prj0000118-amd-npu-feature-documentation
- Result: PASS

## Scope Guardrails
- In scope for this plan artifact update: this plan file, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/2026-04-03.4plan.log.md`.
- In scope for downstream implementation: documentation/test/governance artifacts only.
- Out of scope: `rust_core/**`, `.github/workflows/**`, and any runtime or CI behavior changes.

## AC and Interface Traceability
| Task ID | AC Coverage | Interface Coverage |
|---|---|---|
| T-AMD-001 | AC-AMD-004, AC-AMD-006 | IFACE-AMD-004, IFACE-AMD-006 |
| T-AMD-002 | AC-AMD-001, AC-AMD-002 | IFACE-AMD-001, IFACE-AMD-002 |
| T-AMD-003 | AC-AMD-003, AC-AMD-004, AC-AMD-005 | IFACE-AMD-003, IFACE-AMD-004, IFACE-AMD-005 |
| T-AMD-004 | AC-AMD-005 | IFACE-AMD-005 |
| T-AMD-005 | AC-AMD-001..006 (coverage closure) | IFACE-AMD-001..006 |
| T-AMD-006 | AC-AMD-001..006 (execution closure) | IFACE-AMD-001..006 |
| T-AMD-007 | AC-AMD-001..006 (quality closure) | IFACE-AMD-001..006 |

## Chunking Strategy
- Chunk C1 (documentation contract): T-AMD-001..T-AMD-004.
	- Estimated implementation files: 3 to 5 docs files.
	- Estimated test/validation files: 3 to 5 docs-policy or artifact verification files.
- Chunk C2 (closure and quality gates): T-AMD-005..T-AMD-007.
	- Estimated implementation files: 1 to 3 docs/governance files.
	- Estimated test/validation files: command evidence only.

## Task List
| Task ID | Parallel Class | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|---|
| T-AMD-001 | sequential-only | @6code | Add explicit supported environment gate and CI defer/non-goal contract to canonical AMD NPU guidance. | `docs/performance/HARDWARE_ACCELERATION.md` | Supported path explicitly states Windows x86_64 + AMD SDK; unsupported paths and defer statement are explicit and auditable (AC-AMD-004, AC-AMD-006). | `rg -n "Windows x86_64|AMD Ryzen AI SDK|unsupported|defer|CI" docs/performance/HARDWARE_ACCELERATION.md` |
| T-AMD-002 | sequential-only | @6code | Add canonical location marker and feature activation commands for feature-off and feature-on paths. | `docs/performance/HARDWARE_ACCELERATION.md` | Canonical section exists and includes both command forms aligned with Cargo feature declaration (AC-AMD-001, AC-AMD-002). | `rg -n "amd_npu|--features amd_npu|cargo" docs/performance/HARDWARE_ACCELERATION.md` |
| T-AMD-003 | parallel-safe | @6code | Add fallback semantics and evidence schema requirements in documentation. | `docs/performance/HARDWARE_ACCELERATION.md` | Fallback explicitly documents unavailable status `-1` and safe interpretation; evidence fields are all mandatory (AC-AMD-003, AC-AMD-005). | `rg -n "-1|AMD_NPU_STATUS_UNAVAILABLE|evidence|exit status|runner context" docs/performance/HARDWARE_ACCELERATION.md` |
| T-AMD-004 | parallel-safe | @5test | Author docs-focused verification matrix and failing-first selectors for AC coverage. | `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.test.md`, `tests/docs/test_agent_workflow_policy_docs.py` | Test artifact maps selectors to AC-AMD-001..006 and identifies fail/pass expectations for docs-only changes (AC-AMD-005). | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-AMD-005 | sequential-only (convergence) | @7exec | Execute convergence validation for C1 outputs and collect evidence pack. | `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.exec.md` | Evidence pack includes selector outputs, command transcripts, and AC pass/fail table for all completed tasks. | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-AMD-006 | sequential-only | @8ql | Perform quality/security/governance closure review for docs claims vs repository evidence. | `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.ql.md` | No over-claims beyond repo evidence; unsupported-path and defer language remains intact (AC-AMD-003, AC-AMD-004, AC-AMD-006). | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-AMD-007 | sequential-only | @9git | Stage scoped artifacts, commit, push, and open PR with AC traceability references. | `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.git.md` | Commit/PR evidence includes branch validation, scoped staging proof, and AC/interface traceability links. | `git status --short` |

## Parallelization and Sequencing
- Sequential hard constraints:
	- T-AMD-001 must complete before T-AMD-002 (environment/defer context must exist before activation details).
	- T-AMD-002 must complete before T-AMD-003 (fallback semantics must reference finalized activation contract).
	- T-AMD-005 waits for T-AMD-003 and T-AMD-004 convergence.
	- T-AMD-006 waits for T-AMD-005 evidence package.
	- T-AMD-007 waits for T-AMD-006 closure.
- Parallel-safe boundary:
	- T-AMD-003 and T-AMD-004 are parallel-safe with disjoint file ownership.
	- T-AMD-003 owner: `docs/performance/HARDWARE_ACCELERATION.md`.
	- T-AMD-004 owner: `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.test.md`, `tests/docs/test_agent_workflow_policy_docs.py`.

## Agent Validation Contracts and Evidence Expectations
### @5test Contract
- Deliverables:
	- AC-indexed verification matrix in `amd-npu-feature-documentation.test.md`.
	- Deterministic selector list tied to docs-only behavior.
- Required evidence:
	- Failing-first or baseline selector output for docs-policy checks.
	- Explicit mapping from selector to AC IDs.

### @6code Contract (docs-only)
- Deliverables:
	- Canonical AMD NPU documentation updates with commands, environment matrix, fallback semantics, and defer statement.
- Required evidence:
	- `rg` outputs proving required strings/sections exist.
	- Diff snippets showing no runtime/CI code touched.

### @7exec Contract
- Deliverables:
	- Execution log in `amd-npu-feature-documentation.exec.md`.
- Required evidence:
	- Command invocation outputs, exit codes, and AC pass/fail table.
	- Explicit note when docs-policy failure is unchanged known baseline.

### @8ql Contract
- Deliverables:
	- Quality/security closure report in `amd-npu-feature-documentation.ql.md`.
- Required evidence:
	- Claim-to-source checks against `rust_core/Cargo.toml`, `rust_core/src/hardware.rs`, `.github/workflows/ci.yml`.
	- Confirmation no unsupported environment was documented as supported.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Contract foundations complete | T-AMD-001, T-AMD-002 | PLANNED |
| M2 | Parallel docs/test contract complete | T-AMD-003, T-AMD-004 | PLANNED |
| M3 | Convergence execution complete | T-AMD-005 | PLANNED |
| M4 | Quality and release closure ready | T-AMD-006, T-AMD-007 | PLANNED |

## Validation Commands
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python scripts/project_registry_governance.py validate
rg -n "amd_npu|AMD_NPU_STATUS_UNAVAILABLE|Windows x86_64|AMD Ryzen AI SDK|defer|unsupported" docs/performance/HARDWARE_ACCELERATION.md
git status --short
```

## Validation Evidence (Planning Update)
- Executed: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
- Result: `1 failed, 16 passed`
- Failure identity: legacy baseline `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md` missing.
- Disposition: unchanged known baseline outside prj0000118 scope; planning artifact remains valid for downstream handoff.