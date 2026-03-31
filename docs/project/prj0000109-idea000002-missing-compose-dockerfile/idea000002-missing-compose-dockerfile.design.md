# idea000002-missing-compose-dockerfile - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-31_

## Selected Option
Option B - Incremental hardening around the existing compose Dockerfile path fix.

Rationale:
1. The original defect is already remediated in deployment assets, so this lane should lock durability and governance rather than re-implement path edits.
2. This option preserves the known-good runtime contract while reducing documentation and ownership ambiguity.
3. It stays within project scope and cleanly defers compose topology consolidation to the dedicated consolidation idea lane.

Design lock:
- This project explicitly avoids deploy asset edits unless contradictory evidence appears.
- This project defines behavioral and documentation contracts for sustained reliability.
- Full compose-topology consolidation remains out of scope for this lane.

## Architecture
### High-level architecture
1. `deploy/compose.yaml` remains the canonical compose file for this defect lane's contract checks.
2. Docker build contract remains deploy-local: compose references `deploy/Dockerfile.pyagent` using path semantics valid on clean checkout.
3. Contract verification is enforced via targeted deploy tests and workflow policy tests.
4. Project artifacts in this folder become the authoritative governance source for acceptance and handoff boundaries.

### Components and responsibilities
| Component | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `ComposeDockerfileContract` | Defines required Dockerfile path relationship for compose build | `deploy/compose.yaml`, repository tree | Pass/fail contract state |
| `ComposePathValidationTests` | Detects Dockerfile path regressions | Contract fixtures and compose content | Deterministic test outcomes |
| `ProjectDesignContract` | Captures selected option, non-goals, and acceptance hooks | @2think recommendation and policy constraints | Actionable design for @4plan/@5test |
| `WorkflowPolicyDocsGate` | Ensures agent workflow docs policy remains valid after artifact edits | `docs/project/**` updates | Pass/fail workflow policy signal |

### Architecture constraints
1. Branch must remain `prj0000109-idea000002-missing-compose-dockerfile` for all lane actions.
2. Scope is limited to this project documentation and required @3design memory/log records.
3. No deploy compose or Dockerfile runtime content changes are permitted in this lane unless branch-gated reclassification is approved.
4. Acceptance criteria must include explicit regression signals tied to existing deploy path tests.
5. Design output must be directly decomposable by @4plan without expanding into implementation details owned by later agents.

## Interfaces & Contracts
### Interface contracts
| Interface ID | Interface | Contract summary | Test hook |
|---|---|---|---|
| IFACE-DC-001 | Compose file to Dockerfile path contract | `deploy/compose.yaml` must reference an existing Dockerfile path resolvable from compose context on clean checkout | AC-DC-001 |
| IFACE-DC-002 | Defect-lane scope guard contract | This lane modifies only project docs and required @3design memory/log files | AC-DC-002 |
| IFACE-DC-003 | Regression signal contract | Compose path regression must fail fast via deterministic deploy tests | AC-DC-003 |
| IFACE-DC-004 | Handoff contract for @4plan | Every interface and AC is mapped to planned tasks for implementation planning | AC-DC-004 |
| IFACE-DC-005 | Testability contract for @5test | Each risk has a concrete verification path and failure signal | AC-DC-005 |
| IFACE-DC-006 | Non-goal boundary contract | Compose topology consolidation is explicitly deferred to the consolidation lane | AC-DC-006 |

### Behavioral changes (design-level)
1. Behavior is locked from implicit fix-lane implementation to explicit governance-hardening mode.
2. Any future compose path change in this lane must be treated as a policy exception and escalated before execution.
3. @4plan must produce tasks that preserve current deploy behavior while strengthening validation and ownership evidence.

### Data/decision contracts
| Contract artifact | Required fields | Notes |
|---|---|---|
| Design acceptance record | AC ID, requirement, verification hook | IDs must be unique and stable for downstream tracing |
| Risk register entry | risk id, likelihood, impact, mitigation, verification | Used by @5test to derive test assertions |
| Interface trace row | planned task id, interface id, delivery expectation | Mandatory for @4plan decomposition quality |

## Non-Functional Requirements
- Performance:
	- Design/test gate overhead stays minimal by reusing existing deterministic checks rather than adding broad compose matrix runs in this lane.
	- Validation commands must remain CI-friendly and bounded.
- Security:
	- No credential/path secret exposure in documentation examples or logs.
	- Scope controls prevent accidental broad changes to deploy infrastructure files.
- Reliability:
	- Existing compose path behavior must remain unchanged and continuously verifiable.
	- Regression detection remains deterministic with explicit failing selectors.
- Testability:
	- Every acceptance criterion is paired with an executable validation hook.
	- Risk-driven checks are mapped for both policy docs and deploy path contracts.

## Acceptance Criteria
| AC ID | Requirement | Verification hook |
|---|---|---|
| AC-DC-001 | Compose Dockerfile reference remains valid on clean checkout semantics | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py` |
| AC-DC-002 | Project execution remains on expected branch with scope-bounded artifacts only | Branch check evidence plus changed-files review |
| AC-DC-003 | Regression in compose Dockerfile contract is surfaced by deterministic tests | Targeted deploy test failure/success evidence |
| AC-DC-004 | Design artifact contains explicit interfaces and task traceability for @4plan | Review of traceability table completeness |
| AC-DC-005 | Risks and mitigations are test-linked for @5test planning | Risk table mapped to verification hooks |
| AC-DC-006 | Non-goal boundary (no compose topology consolidation) is explicit and enforceable | Non-goals section review and scope diff evidence |

## Interface-to-Task Traceability
| Planned Task ID (@4plan) | Interface/Contract | Delivery expectation |
|---|---|---|
| T-DC-01 | IFACE-DC-001 | Keep compose Dockerfile contract explicit in plan assumptions and constraints |
| T-DC-02 | IFACE-DC-002 | Add branch/scope verification task before any planned edits |
| T-DC-03 | IFACE-DC-003 | Include deterministic deploy path validation task in execution sequence |
| T-DC-04 | IFACE-DC-004 | Translate all interface contracts into concrete implementation-planning tasks |
| T-DC-05 | IFACE-DC-005 | Derive risk-based test tasks with clear pass/fail criteria for @5test |
| T-DC-06 | IFACE-DC-006 | Add explicit non-goal guard task to prevent consolidation scope creep |
| T-DC-07 | AC-DC-001, AC-DC-003 | Define regression test command ownership and rerun policy |
| T-DC-08 | AC-DC-002 | Define evidence capture format for branch and scope checks |
| T-DC-09 | AC-DC-004 | Define artifact quality checks ensuring complete traceability blocks |
| T-DC-10 | AC-DC-005, AC-DC-006 | Define risk closure checklist and non-goal enforcement in handoff |

## Risks and Mitigations
| Risk ID | Risk | Likelihood | Impact | Mitigation | Verification |
|---|---|---|---|---|---|
| R-DC-001 | Hidden compose path drift reintroduces missing Dockerfile behavior | Medium | High | Preserve explicit contract and run targeted deploy tests | AC-DC-001, AC-DC-003 hooks |
| R-DC-002 | Scope creep into compose consolidation causes unplanned blast radius | Medium | Medium | Enforce non-goal boundary and scope validation | AC-DC-002, AC-DC-006 hooks |
| R-DC-003 | Handoff ambiguity leads to weak @4plan decomposition | Medium | Medium | Maintain complete interface-to-task traceability table | AC-DC-004 hook |
| R-DC-004 | Test strategy under-specification weakens @5test coverage | Low | Medium | Require risk-to-verification mapping per criterion | AC-DC-005 hook |

## Testability Points for @5test
1. Preserve a deterministic selector for compose Dockerfile contract checks.
2. Capture branch and scope validation evidence as explicit preconditions for any execution workflow.
3. Verify non-goal compliance by asserting no consolidation-specific deploy topology changes in this lane.
4. Tie each risk row to at least one executable or reviewable verification artifact.

## ADR Impact
- No new ADR is required for this lane because no architecture topology or runtime implementation decision is introduced.
- Existing prior-art ADRs and project artifacts remain the governing architectural record for the already-implemented fix.

## Open Questions
Resolved for @4plan handoff readiness:
1. Should this lane edit deploy runtime files? No, unless contradictory evidence is discovered under branch-gated escalation.
2. Does this lane include compose topology consolidation? No, deferred by explicit non-goal.
3. Are regression hooks sufficient for @5test planning? Yes, targeted deploy path tests plus workflow policy validation are required hooks.

No blocking open design questions remain.
