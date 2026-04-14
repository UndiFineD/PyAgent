# amd-npu-feature-documentation - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-03_

## Selected Option
Option B from discovery: canonical docs plus maintainer verification checklist.

Rationale:
1. Keeps this lane documentation-only while still creating objective validation evidence.
2. Fits repository reality where `amd_npu` is feature-gated in `rust_core/Cargo.toml` and runtime paths in `rust_core/src/hardware.rs` can return unavailable status when the feature is off.
3. Reduces support ambiguity by defining prerequisite gates and expected unsupported outcomes, without introducing source or CI changes in this project.

## Problem Statement and Goals
The repository defines an `amd_npu` Cargo feature and Rust FFI entry points, but lacks a canonical documentation contract that tells maintainers exactly when to enable it, how to validate behavior, and what evidence is required for review.

Goals:
1. Define one canonical feature-documentation location and one project-governance trace location.
2. Define a deterministic maintainer validation checklist with mandatory evidence.
3. Define explicit non-goals so this project does not drift into implementation or CI expansion.

## Architecture
This design uses a two-layer documentation architecture.

### Layer A: Canonical Runtime Guidance
- Authoritative runtime-facing guidance remains in `docs/performance/HARDWARE_ACCELERATION.md` under an AMD NPU section.
- This location is where prerequisites, activation command examples, expected outcomes, and unsupported-path behavior are documented for maintainers.

### Layer B: Project Governance Trace
- `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.design.md` is the design governance source for scope boundaries, acceptance criteria, and interface contracts.
- Downstream artifacts must link implementation/documentation updates back to this design AC set.

### Data and Evidence Flow
1. Maintainer reads canonical AMD NPU guidance.
2. Maintainer executes documented validation commands (feature-off and feature-on paths).
3. Maintainer records evidence using the required evidence schema.
4. Reviewer checks evidence against AC table in this design and plan/test artifacts.

## Scope Boundaries
In scope:
1. Documentation architecture and contract definitions for AMD NPU feature guidance.
2. Validation checklist contract and evidence schema definition.
3. Explicit non-goal/defer statements for implementation and CI automation.

Out of scope:
1. Rust code edits in `rust_core/**`.
2. CI workflow edits in `.github/workflows/**`.
3. New runtime/platform support claims beyond repo-evidenced behavior.

## Interfaces and Contracts
### IFACE-AMD-001: Canonical Documentation Location Contract
- Canonical user-facing AMD NPU guidance must live in `docs/performance/HARDWARE_ACCELERATION.md`.
- Project artifacts may reference but must not become the sole runtime guidance source.

### IFACE-AMD-002: Feature Activation Contract
- Documentation must define feature activation through Cargo feature flag usage aligned with `rust_core/Cargo.toml` (`amd_npu = []`).
- Command examples must include an explicit feature-enabled invocation and a default/feature-off invocation.

### IFACE-AMD-003: Unsupported Fallback Contract
- Documentation must explicitly state safe unsupported behavior tied to `AMD_NPU_STATUS_UNAVAILABLE = -1` in `rust_core/src/hardware.rs`.
- Unsupported environment or disabled-feature outcomes must be documented as expected, not as defects.

### IFACE-AMD-004: Environment Gate Contract
- Documentation must define minimum supported validation environment as Windows x86_64 with AMD Ryzen AI SDK availability for feature-on validation.
- Non-Windows or missing-SDK paths must be classified as unsupported for feature-on validation in this project scope.

### IFACE-AMD-005: Validation Evidence Contract
- Checklist completion requires evidence with:
  - command text,
  - exit status/result code,
  - observed AMD NPU status outcome,
  - timestamp and runner context (OS + toolchain summary).
- Evidence may be captured as a status table plus short command-output excerpts.

### IFACE-AMD-006: Deferred Automation Contract
- This project does not add CI gates for AMD NPU.
- Documentation must include an explicit defer statement for CI automation to a follow-on project once repeated maintainer evidence exists.

## Acceptance Criteria
| AC ID | Requirement | Verification Evidence | Related Interfaces |
|---|---|---|---|
| AC-AMD-001 | Canonical runtime guidance location is explicitly defined and references AMD NPU feature behavior. | Updated canonical docs location and section references recorded in downstream plan/test artifacts. | IFACE-AMD-001 |
| AC-AMD-002 | Feature activation instructions include both feature-off and feature-on command forms aligned with `rust_core/Cargo.toml`. | Reviewer confirms command parity against Cargo feature declaration and documented command examples. | IFACE-AMD-002 |
| AC-AMD-003 | Unsupported/fallback behavior explicitly states expected `-1` unavailable outcome and safe interpretation. | Reviewer confirms fallback statement references runtime constant semantics from `rust_core/src/hardware.rs`. | IFACE-AMD-003 |
| AC-AMD-004 | Supported environment boundaries are explicit (Windows x86_64 + AMD SDK for feature-on) and non-supported paths are called out. | Environment matrix/checklist present with supported vs unsupported outcomes. | IFACE-AMD-004 |
| AC-AMD-005 | Validation checklist defines mandatory evidence schema (commands, status, outcomes, context). | Evidence template/table present and required fields non-optional. | IFACE-AMD-005 |
| AC-AMD-006 | Non-goals and CI defer contract are explicit and auditable. | Deferred automation statement and non-goals section present in canonical docs/project artifacts. | IFACE-AMD-006 |

## Interface-to-Task Traceability for @4plan
| Interface | Required @4plan Task IDs | Traceability Expectation |
|---|---|---|
| IFACE-AMD-001 | T2 | Task(s) that update canonical documentation location and cross-links. |
| IFACE-AMD-002 | T2, T3 | Task(s) that define/verify feature-off and feature-on command contracts. |
| IFACE-AMD-003 | T2, T3 | Task(s) that codify fallback semantics and validation interpretation guidance. |
| IFACE-AMD-004 | T1, T3 | Task(s) that define supported environment gate and unsupported-path outcomes. |
| IFACE-AMD-005 | T3 | Task(s) that create evidence template/checklist requirements. |
| IFACE-AMD-006 | T1 | Task(s) that capture explicit non-goal/defer statement and future-lane trigger. |

## Non-Functional Requirements
- Performance: Documentation changes must not alter runtime behavior or benchmark paths.
- Security: Guidance must avoid claims of support where SDK/hardware/runtime prerequisites are not satisfied; unsupported path must fail safe through documented unavailable status.
- Testability: Each AC must be verifiable from repository artifacts and captured maintainer evidence without requiring new CI in this lane.
- Maintainability: Canonical guidance location and evidence schema must be stable and easy to reuse by follow-on plan/test/code lanes.

## Open Questions Resolution
1. Canonical documentation location:
	- Resolved: Runtime guidance should live in `docs/performance/HARDWARE_ACCELERATION.md`, with project artifacts as governance trace only.
2. Minimum supported environment:
	- Resolved from repo evidence: Windows x86_64 + AMD SDK is required for feature-on validation; feature-off path remains valid on other environments with unavailable outcome.
3. Unsupported safe fallback statement:
	- Resolved: Mandatory and explicit; `-1` unavailable outcome is acceptance behavior for unsupported/disabled scenarios.
4. Evidence granularity:
	- Resolved: Both structured status table and short command output excerpts are required.
5. Follow-on automation filing:
	- Partially unresolved: this design defers CI automation and requires @4plan to include a follow-on trigger condition based on repeated maintainer evidence; actual project filing decision belongs to downstream governance lane.

## Risks and Mitigations
1. Risk: Docs drift from runtime behavior.
	- Mitigation: AC parity checks against `rust_core/Cargo.toml` and `rust_core/src/hardware.rs` are mandatory.
2. Risk: Over-claiming support across OS/SDK combinations.
	- Mitigation: Explicit supported/unsupported environment matrix required by AC-AMD-004.
3. Risk: Weak auditability of manual validation.
	- Mitigation: Evidence schema in IFACE-AMD-005 is mandatory for acceptance.

## Explicit Non-Goals
1. No Rust implementation changes.
2. No CI workflow additions for AMD NPU in this project.
3. No expansion into ROCm, NVIDIA, or unified acceleration redesign in this lane.

## Handoff Constraints for @4plan
1. Preserve docs-only boundary; do not create implementation tasks outside documentation/evidence artifacts.
2. Keep each planned task mapped to AC-AMD IDs and IFACE-AMD IDs.
3. Include a deterministic evidence collection task that satisfies IFACE-AMD-005.
4. Carry forward the CI defer statement and define clear trigger criteria for a separate follow-on project.