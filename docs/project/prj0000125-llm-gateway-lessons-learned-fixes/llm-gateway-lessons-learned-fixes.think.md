# llm-gateway-lessons-learned-fixes - Cross-Project Lessons Synthesis

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-04_

## Branch Gate
- Expected branch from project overview: prj0000125-llm-gateway-lessons-learned-fixes
- Observed branch evidence: git branch --show-current -> prj0000125-llm-gateway-lessons-learned-fixes
- Result: PASS

## Research Coverage Used
1. Literature review
	- Reviewed requested project artifacts across legacy and modern project folders (project/think/git/plan where present).
2. Alternative enumeration
	- Compared lessons from runtime, CI/test, docs governance, and naming-policy categories to build remediation waves.
3. Prior-art search
	- Used cross-project patterns from prj0000101-prj0000124 plus legacy prj0000005-prj0000041.
4. Constraint mapping
	- Applied branch/scope constraints from prj0000125 overview and policy docs.
5. Stakeholder impact
	- Mapped owners to @3design, @5test, @6code, @7exec, @8ql, @9git.
6. Risk enumeration
	- Explicitly mapped each major lesson cluster to risk-if-deferred and validation signal.

## Source Inventory (Requested Paths)

### Requested path status
| Requested path | Status | Notes |
|---|---|---|
| docs/project/prj0000005 | FOUND | Contains 3 files; legacy/archived metadata |
| docs/project/prj0000005/llm-swarm-architecture.project.md | FOUND | Legacy dashboard-style summary |
| docs/project/prj0000005/prj005-llm-swarm-architecture.git.md | FOUND | Legacy branch exception artifact |
| docs/project/prj0000005/prj0000005-llm-swarm-architecture.project.md | FOUND | Archived legacy overview |
| docs/project/prj0000006 | FOUND | Legacy dashboard-style summary set |
| docs/project/prj0000007 | FOUND | Legacy dashboard-style summary set |
| docs/project/prj0000008 | FOUND | Legacy dashboard-style summary set |
| docs/project/prj0000011 | FOUND | Legacy project structure summaries |
| docs/project/prj0000041 | FOUND | Legacy benchmark summaries and risk block |
| docs/project/prj0000101-pending-definition | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000102-pyproject-requirements-sync | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000104-idea000014-processing | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000105-idea000016-mixin-architecture-base | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000106-idea000080-smart-prompt-routing-system | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000107-idea000015-specialized-agent-library | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000108-idea000019-crdt-python-ffi-bindings | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000109-idea000002-missing-compose-dockerfile | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000110-idea000004-quality-workflow-branch-trigger | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000114-ideatracker-batching-verbosity | FOUND | Mostly placeholder/TBD lifecycle content |
| docs/project/prj0000115-ci-security-quality-workflow-consolidation | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000116-rust-criterion-benchmarks | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000117-rust-sub-crate-unification | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000118-amd-npu-feature-documentation | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000119-pytest-stabilization | FOUND | Partial lifecycle + closure artifact |
| docs/project/prj0000120-openapi-spec-generation | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000121-ci-setup-python-stack-overflow | FOUND | Placeholder/TBD discovery artifacts |
| docs/project/prj0000122-jwt-refresh-token-support | FOUND | Full lifecycle artifacts present |
| docs/project/prj0000123-openapi-drift-post-merge-hotfix | FOUND | Mostly initialization/TBD discovery artifacts |
| docs/project/prj0000124-llm-gateway | FOUND | Full lifecycle artifacts present |

### Missing or renamed paths
- Missing from request list: none.
- Renamed/legacy state detected:
  - prj0000005 legacy branch exception recorded in prj005 artifact (shared branch history, not one-project-one-branch).
  - Multiple legacy folders (prj0000006/prj0000007/prj0000008/prj0000011/prj0000041) use dashboard-style summaries with missing design links rather than modern full lifecycle artifacts.

### High-signal source paths used for synthesis
- docs/project/prj0000124-llm-gateway/llm-gateway.think.md
- docs/project/prj0000124-llm-gateway/llm-gateway.git.md
- docs/project/prj0000123-openapi-drift-post-merge-hotfix/openapi-drift-post-merge-hotfix.project.md
- docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.think.md
- docs/project/prj0000121-ci-setup-python-stack-overflow/ci-setup-python-stack-overflow.think.md
- docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.think.md
- docs/project/prj0000119-pytest-stabilization/pytest-stabilization.git.md
- docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.think.md
- docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.git.md
- docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.think.md
- docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.git.md
- docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.think.md
- docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.git.md
- docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.think.md
- docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.git.md
- docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.think.md
- docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.think.md
- docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md
- docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.think.md
- docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.think.md
- docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.think.md
- docs/project/prj0000104-idea000014-processing/idea000014-processing.think.md
- docs/project/prj0000102-pyproject-requirements-sync/pyproject-requirements-sync.think.md
- docs/project/prj0000101-pending-definition/prj0000101-pending-definition.think.md
- docs/project/prj0000005/prj005-llm-swarm-architecture.git.md
- docs/project/naming_standards.md

## Conflicts and Duplicates Observed
1. Policy conflict: repository naming standard requires snake_case, while some attached Copilot guidance elsewhere mentions PascalCase module naming.
2. Lifecycle drift conflict: prj0000124 project overview still shows Discovery/NOT_STARTED while downstream think/git are DONE.
3. Legacy governance conflict: prj0000005 git summary documents one-project-one-branch exception.
4. Recurring process duplicate: many git summaries independently repeat dashboard side-effect and strict allowlist staging lessons.
5. Discovery completeness conflict: prj0000114, prj0000121, prj0000123 remain largely TBD, so they contribute limited direct technical lessons.

## Normalized Lessons by Remediation Wave

### Wave A - Runtime Correctness and Fail-Closed Behavior

#### Lesson A1
- Pattern: Fragmented control surfaces produce partial feature coverage (validation exists but lifecycle controls are missing).
- Root cause: Projects often ship thin phase-one slices (gateway/auth/openapi) without full failure-path closure.
- Prevention: Require explicit fail-closed contracts and error-path completion criteria before milestone closure.
- First seen / Seen in: First seen prj0000122; seen in prj0000124, prj0000120, prj0000123.
- Recurrence estimate: High (4 projects).
- Recommendation for prj0000125: Prioritize explicit budget-denied path, provider-exception commit-failure path, and degraded-telemetry fail-safe in gateway orchestration.

#### Lesson A2
- Pattern: Architecture intent is strong, but deterministic lifecycle contracts are missing at integration boundaries.
- Root cause: Reuse of prior primitives without one canonical orchestration contract.
- Prevention: Define one gateway request lifecycle contract with mandatory checkpoints (auth, policy, budget reserve, provider call, commit/rollback, telemetry).
- First seen / Seen in: First seen prj0000106; seen in prj0000107, prj0000124.
- Recurrence estimate: Medium-High (3 projects).
- Recommendation for prj0000125: Keep scope to contract-completion fixes, avoid broad redesign (cache/memory/fallback topology) in this wave.

### Wave B - Test Determinism and Quality Gates

#### Lesson B1
- Pattern: Lightweight CI is effective only when paired with targeted deterministic selectors for critical paths.
- Root cause: CI optimization toward speed left some drift and failure classes outside always-on checks.
- Prevention: Add narrow contract tests that fail loudly on drift and runtime-order ambiguity.
- First seen / Seen in: First seen prj0000110; seen in prj0000115, prj0000116, prj0000120, prj0000123.
- Recurrence estimate: High (5 projects).
- Recommendation for prj0000125: Add deterministic chronological assertion strategy for gateway orchestration and keep docs-policy selector mandatory.

#### Lesson B2
- Pattern: Post-merge closure lag causes registry and status drift even when implementation merged cleanly.
- Root cause: Release/kanban/nextproject updates executed after, not with, merge closure.
- Prevention: Immediate post-merge registry closure gate with explicit selector reruns.
- First seen / Seen in: First seen prj0000119; seen in prj0000118, prj0000123.
- Recurrence estimate: Medium (3 projects).
- Recommendation for prj0000125: Ensure project/state truth updates are part of closure checklist, not deferred cleanup.

### Wave C - Docs and Governance Consistency

#### Lesson C1
- Pattern: Source-of-truth documents drift from actual project state and confuse downstream agents.
- Root cause: Multiple artifacts updated unevenly across project lifecycle.
- Prevention: Enforce one truth-sync pass (project + think/design/plan/git consistency) before handoff/closure.
- First seen / Seen in: First seen prj0000101; seen in prj0000118, prj0000119, prj0000124.
- Recurrence estimate: High (4 projects).
- Recommendation for prj0000125: Update prj0000124 lifecycle/milestones/status to match merged state and keep prj0000125 rationale linked.

#### Lesson C2
- Pattern: Legacy baseline debt can block unrelated scoped work unless explicitly documented as baseline/non-regression.
- Root cause: Global policy tests include legacy files outside active project scope.
- Prevention: Record baseline debt explicitly and rerun exact failing selectors before declaring DONE.
- First seen / Seen in: First seen prj0000118; seen in prj0000116.
- Recurrence estimate: Medium (2 projects).
- Recommendation for prj0000125: Record any inherited docs-policy debt separately from prj0000125 regressions.

### Wave D - Naming and Convention Alignment

#### Lesson D1
- Pattern: Convention ambiguity (legacy guidance vs current standard) creates churn risk and unnecessary rename pressure.
- Root cause: Mixed policy sources persisted through migrations.
- Prevention: Explicit precedence rule in design: repository naming_standards governs implementation.
- First seen / Seen in: First seen prj0000105/prj0000107; seen in prj0000124/prj0000125.
- Recurrence estimate: Medium-High (4 projects).
- Recommendation for prj0000125: Default no-rename unless concrete runtime/import break requires rename.

#### Lesson D2
- Pattern: One-project-one-branch governance must override legacy exceptions.
- Root cause: Historical shared branch workflow (prj0000005) predates modern governance.
- Prevention: Treat legacy branch exceptions as audit-only, never as modern precedent.
- First seen / Seen in: First seen prj0000005; seen in prj0000101-prj0000124 governance artifacts.
- Recurrence estimate: Medium (policy-wide).
- Recommendation for prj0000125: Keep strict branch/scope gating and document any exception as BLOCKED escalation.

## Priority Matrix for prj0000125
| Lesson cluster | Severity | Effort | Risk if deferred | Proposed owner |
|---|---|---|---|---|
| Wave A fail-closed runtime completion (A1/A2) | Critical | M | Policy bypass, incorrect budget state, silent degraded telemetry | @6code with @3design constraints |
| Wave B deterministic orchestration tests (B1) | High | S-M | False green tests on wrong ordering; regression escapes | @5test |
| Wave C state truth sync for prj0000124/prj0000125 (C1) | High | S | Downstream planning on stale status; repeat hotfix loops | @3design then @9git |
| Wave B/C closure and selector discipline (B2/C2) | Medium-High | S | Registry/lane drift and repeated policy confusion | @7exec and @9git |
| Wave D naming precedence decision (D1) | Medium | S | Unnecessary refactor churn and import risk | @3design |
| Wave D legacy branch-exception handling (D2) | Medium | S | Governance backslide and scope leakage | @9git with @0master policy enforcement |

## Do Now vs Defer

### Do now
1. Wave A runtime correctness fixes for gateway fail-closed paths.
2. Wave B deterministic test corrections for orchestration chronology and failure-path assertions.
3. Wave C artifact truth-sync for prj0000124 and explicit linkage to prj0000125 remediation rationale.
4. Record Wave D naming precedence decision (no rename by default) in design docs now.

### Defer
1. Broad gateway redesign (cache architecture, fallback topology expansion, memory-system refactor).
2. Repo-wide markdown lint/legacy cleanup unrelated to prj0000124/prj0000125 truth sync.
3. Any filename/module rename campaign beyond proven import/runtime necessity.

## Recommended Implementation Order and Handoff

### Recommended implementation order
1. Wave A: implement fail-closed runtime completion in gateway core with explicit error-path behavior.
2. Wave B: lock deterministic test evidence for ordering and failure commits.
3. Wave C: synchronize project/status/docs truth between prj0000124 and prj0000125.
4. Wave D: finalize naming/convention decision record; only then evaluate whether any rename is justified.

### Risk-to-testability mapping for the recommended order
| Risk | Validation signal |
|---|---|
| Runtime path still allows partial success on failure | Targeted gateway selectors for deny/exception/degraded telemetry paths |
| Test suite still passes with non-chronological evidence | Shared chronological event-log assertions in orchestration tests |
| Docs/state drift remains after implementation | docs policy selector plus artifact cross-check before git handoff |
| Naming discussion expands into churn | Explicit no-rename gate in design unless import break evidence is produced |

### Handoff target
Handoff to @3design with this direction: execute sequenced waves A -> B -> C -> D, with strict scope control and default no-rename policy unless runtime evidence requires otherwise.