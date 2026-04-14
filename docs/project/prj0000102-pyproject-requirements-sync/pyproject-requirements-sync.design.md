# pyproject-requirements-sync - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-29_

## Selected Option
Option A is selected: pyproject.toml is the canonical dependency authority and requirements.txt is a generated derivative artifact.

### Rationale
1. Eliminates the root cause (dual manual authorities) identified in think phase.
2. Aligns with modern Python packaging where project metadata in pyproject.toml is first-class.
3. Provides the cleanest governance model for deterministic parity checks in CI.

## Architecture
### Architecture Overview
The synchronization design uses a single-source flow:

1. Source of truth:
	- pyproject.toml section [project.dependencies]
2. Derivation:
	- A deterministic synchronization mechanism materializes requirements.txt from canonical dependencies.
3. Verification:
	- Parity checks validate that committed requirements.txt matches deterministic output.
4. Governance:
	- CI gate blocks merges on drift and structural violations.

### Logical Components
1. Dependency Source Reader
	- Responsibility: read canonical dependencies from pyproject.toml.
2. Requirements Materializer
	- Responsibility: emit normalized requirements.txt content from canonical model.
3. Parity Validator
	- Responsibility: compare generated output and committed artifact.
4. Policy Gate
	- Responsibility: enforce parity and package-spec policy in CI.

### Data Flow
1. Parse pyproject.toml dependencies.
2. Normalize dependency specifiers (ordering, formatting, duplicate handling).
3. Emit requirements.txt.
4. Run parity validation in CI and local checks.
5. Fail fast on mismatches.

## Interfaces and Contracts
The following contracts are implementation-agnostic interfaces for @4plan and later agents.

| Interface ID | Name | Inputs | Outputs | Contract Rules |
|---|---|---|---|---|
| IF-001 | CanonicalDependencyProvider | pyproject.toml path | Canonical dependency set | Must read only canonical runtime dependencies from [project.dependencies]. |
| IF-002 | RequirementsEmitter | Canonical dependency set | requirements.txt content | Must be deterministic (same input -> byte-equivalent output). |
| IF-003 | DriftChecker | generated requirements + committed requirements | pass/fail + diff summary | Must fail on any semantic mismatch and surface actionable diff. |
| IF-004 | PolicyEnforcer | dependency set | pass/fail + policy violations | Must enforce duplicate prevention and critical package spec policy. |

### Contract Invariants
1. INV-001: pyproject.toml is the only writable dependency authority for runtime requirements.
2. INV-002: requirements.txt must be reproducible from canonical dependencies with no manual edits required.
3. INV-003: CI must fail when parity or policy checks fail.
4. INV-004: Tooling output must be stable across supported developer environments.

## Acceptance Criteria
| AC ID | Acceptance Criterion | Verification Signal | Owner Stage |
|---|---|---|---|
| AC-001 | A single canonical runtime dependency authority is documented as pyproject.toml [project.dependencies]. | Design and plan artifacts explicitly encode source-of-truth rule. | @3design -> @4plan |
| AC-002 | requirements.txt is defined as deterministic derived output, not a manually authoritative file. | Planned generation workflow and parity checks are present. | @4plan |
| AC-003 | Drift between generated and committed requirements artifacts blocks CI. | Failing parity check when mismatch is introduced. | @5test/@7exec |
| AC-004 | Duplicate and malformed dependency line protections are specified. | Policy validator test coverage for duplicates/format invariants. | @5test |
| AC-005 | Security-sensitive package spec policy is explicitly defined and enforced. | Policy check for selected critical package constraints. | @4plan/@5test |
| AC-006 | Scope remains bounded to dependency-sync governance and does not change unrelated runtime features. | Plan boundaries and code diffs constrained to dependency tooling and docs/tests. | @4plan/@9git |

## Implementation Boundaries
### In Scope
1. Dependency synchronization contracts and governance.
2. Deterministic generation/parity validation behavior definition.
3. CI gate expectations for drift/policy failures.

### Out of Scope
1. Functional feature changes unrelated to dependency governance.
2. Non-dependency refactors across application runtime modules.
3. Broad packaging ecosystem migrations beyond this project boundary.

## Interface-to-Task Traceability
This table is mandatory handoff material for @4plan task decomposition.

| Interface/Contract | Planned Task ID (for @4plan) | Task Intent | Related AC IDs |
|---|---|---|---|
| IF-001 + INV-001 | PLN-001 | Define canonical dependency extraction behavior from pyproject.toml. | AC-001 |
| IF-002 + INV-002 | PLN-002 | Define deterministic requirements materialization and normalization rules. | AC-002 |
| IF-003 + INV-003 | PLN-003 | Define parity check command and CI integration contract. | AC-003 |
| IF-004 + INV-004 | PLN-004 | Define policy checks for duplicates/specifiers/critical packages. | AC-004, AC-005 |
| Scope boundary constraints | PLN-005 | Define change boundary checks and review gates. | AC-006 |

## Risks and Consequences
### Security Consequences
1. Positive: a single authority improves auditability of dependency intent and reduces hidden drift.
2. Positive: explicit policy checks enable earlier detection of unsafe or noncompliant package specifiers.
3. Negative: if critical package policy is too permissive, vulnerable version ranges may still pass.

### Operability Consequences
1. Positive: deterministic generation reduces onboarding ambiguity and local-vs-CI variance.
2. Positive: parity gates create fast-fail behavior for manifest drift.
3. Negative: synchronization tooling instability can create noisy failures and developer friction.

### Mitigation Direction
1. Keep generator output deterministic and formatter-stable.
2. Emit actionable, minimal diffs on drift failures.
3. Define a documented exception process for urgent security pin updates.

## Non-Functional Requirements
- Performance: parity and policy checks should complete quickly enough to run in standard CI validation stages without material pipeline slowdown.
- Security: dependency policy must allow enforcement of stricter constraints for designated critical packages.
- Testability: every contract above must map to at least one deterministic automated check.
- Maintainability: synchronization behavior must be explicit and centrally documented, not tribal knowledge.

## ADR Impact
No repository-wide architecture ADR is created in this step. This design introduces project-scoped dependency-governance decisions; @4plan should confirm whether implementation details warrant a formal ADR update under docs/architecture/adr.

## Open Questions For @4plan
1. Which concrete generation mechanism should be adopted (pip-compile, uv export, or repository script), and what is the fallback path?
2. Which packages are classified as critical for stricter spec policy enforcement in this repository?
3. Should requirements-ci.txt be fully derived, partially derived, or separately governed with explicit rationale?
4. What is the exact CI command surface and failure messaging standard for parity and policy checks?
5. Should developer workflow include a mandatory pre-commit/parity command, or CI-only enforcement?
