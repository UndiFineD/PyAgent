# amd-npu-feature-documentation - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-03_

## Root Cause Analysis
1. The feature exists in `rust_core/Cargo.toml` as `amd_npu = []`, but there is no canonical project doc that defines activation prerequisites, supported environments, and maintainer validation commands.
2. Runtime behavior is partially implemented in `rust_core/src/hardware.rs` with `#[cfg(feature = "amd_npu")]` and `#[link(name = "amd_npu")]`, but documentation does not define expected link/runtime outcomes when SDK or hardware is missing.
3. Existing CI (`.github/workflows/ci.yml`) validates benchmark smoke only; no documented policy states if amd_npu validation is in-scope now or explicitly deferred.
4. Historical project artifacts classify this as idea000020 and previously describe amd_npu as a stub capability, indicating documentation/governance drift over time.

## Discovery Evidence
### 1. Literature Review (Repository)
- `rust_core/Cargo.toml`
- `rust_core/src/hardware.rs`
- `docs/performance/HARDWARE_ACCELERATION.md`
- `docs/project/ideas/idea000020-amd-npu-feature-documentation.md`
- `.github/workflows/ci.yml`
- `tests/ci/test_ci_workflow.py`

### 2. Alternative Enumeration
- Option A: Canonical docs-only guidance in the project artifact.
- Option B: Canonical docs + maintainer validation checklist (manual verification contract).
- Option C: Canonical docs + explicit deferred CI/test roadmap contract for follow-on project.

### 3. Prior-Art Search
- `docs/project/archive/prj0000051/readme-update.think.md`
- `docs/project/archive/prj0000056/rust-async-transport-activation.think.md`
- `docs/project/archive/prj0000076/prj0000076.think.md`
- `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.think.md`
- `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md`

### 4. Constraint Mapping
- Must stay on branch `prj0000118-amd-npu-feature-documentation`.
- Allowed scope for this task is documentation and 2think memory/log artifacts only.
- No source, CI workflow, or test implementation changes in this phase.
- Must comply with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Must produce recommendation with explicit risk-to-testability mapping and prior-art citations.

### 5. Stakeholder Impact
- @2think: provide merge-ready option analysis only.
- @3design: consumes recommended option and resolves unresolved acceptance boundaries.
- @5test/@7exec: impacted by how validation expectations are documented (manual-only vs follow-on automated).
- Maintainers/users enabling amd_npu: need trustworthy prerequisites and failure-mode expectations.

### 6. Risk Enumeration (Cross-option)
- False confidence from documentation that lacks verifiable validation signals.
- Scope creep into CI/source changes inside discovery wave.
- Underspecified prerequisites leading to non-reproducible setup and support burden.

### Approved External Research
- Cargo feature documentation and dependency reference on GitHub (allowed domain) confirm:
	- features should be clearly documented for discovery/usability;
	- optional/feature-driven behavior should be explicit, and feature combinations require deliberate validation strategy.
- Source references:
	- `https://github.com/rust-lang/cargo/blob/master/src/doc/src/reference/features.md`
	- `https://github.com/rust-lang/cargo/blob/master/src/doc/src/reference/specifying-dependencies.md`

## Options
### Option A - Canonical docs-only clarification
Approach:
- Produce a single canonical documentation narrative in project artifacts describing feature purpose, prerequisites, activation command examples, expected return codes, and non-goals.
- No validation checklist beyond prose-level guidance.

Trade-offs:
- Pros: smallest scope and fastest to complete; lowest immediate change risk.
- Cons: weaker operational trust because guidance is not tied to explicit validation evidence.

SWOT:
- Strengths: minimal blast radius; zero runtime impact.
- Weaknesses: can become stale quickly without explicit validation contract.
- Opportunities: establishes baseline language for later automation.
- Threats: maintainers may interpret prose inconsistently.

Security Risk Analysis and Testability Mapping:
- Risk A1: undocumented SDK/source provenance expectations could permit unsafe local linkage (Likelihood M, Impact M).
	- Testability signal: documentation lint/checklist asserts prerequisite section explicitly names trusted SDK source boundaries.
- Risk A2: unclear fallback behavior can hide runtime misuse in production paths (Likelihood M, Impact H).
	- Testability signal: documentation contract includes deterministic fallback status semantics (`-1` unavailable).
- Risk A3: command examples may drift from actual build contract (Likelihood M, Impact M).
	- Testability signal: doc review checklist requires command parity check with `rust_core/Cargo.toml` and existing workflow commands.

Research coverage by task type: literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

### Option B - Canonical docs plus maintainer verification checklist
Approach:
- Produce canonical feature documentation and include a concrete manual verification checklist for local maintainers (preflight, build invocation with feature flag, expected outcomes with/without hardware/SDK, log or status capture requirements).
- Keep checks documentation-only (no new CI or code).

Trade-offs:
- Pros: highest practical usability inside current scope; creates deterministic acceptance evidence without implementation changes.
- Cons: requires disciplined maintenance and explicit ownership to keep checklist current.

SWOT:
- Strengths: balanced scope vs reliability; better reproducibility.
- Weaknesses: still manual verification; cannot guarantee continuous enforcement.
- Opportunities: clean handoff path for @3design to codify future automated checks.
- Threats: checklist can degrade if ownership is unclear.

Security Risk Analysis and Testability Mapping:
- Risk B1: checklist omits secure handling of model path input/context assumptions (Likelihood M, Impact H).
	- Testability signal: checklist includes negative-case verification for invalid/unsafe model path handling expectations.
- Risk B2: maintainers may enable feature in unsupported environments and misinterpret failures (Likelihood H, Impact M).
	- Testability signal: checklist includes explicit environment gate section (OS/toolchain/SDK/hardware expectations) and required "unsupported" outcome criteria.
- Risk B3: manual validation evidence not archived, reducing auditability (Likelihood M, Impact M).
	- Testability signal: checklist defines minimum evidence artifact (command output snippets/status notes) for review.

Research coverage by task type: literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

### Option C - Canonical docs plus explicit deferred automation contract
Approach:
- Produce canonical documentation and an explicit deferred follow-on contract for CI/test automation (scope, entry criteria, and acceptance for a next project).
- Current project remains docs-only but includes formal defer decision and boundaries.

Trade-offs:
- Pros: strongest governance clarity for future enforcement; reduces ambiguity about what is deferred.
- Cons: larger discovery artifact complexity; may overfit future path before @3design resolves details.

SWOT:
- Strengths: clear governance lineage and roadmap.
- Weaknesses: higher documentation complexity for a P3/S project.
- Opportunities: improved planning quality for follow-on automation project.
- Threats: pre-committing to future scope may constrain better later design choices.

Security Risk Analysis and Testability Mapping:
- Risk C1: deferred automation scope may be too vague and never executed (Likelihood M, Impact M).
	- Testability signal: follow-on contract includes measurable entry criteria and owner lane target.
- Risk C2: roadmap assumptions may conflict with actual CI/runtime constraints (Likelihood M, Impact M).
	- Testability signal: follow-on contract requires compatibility check against existing CI smoke and rust workspace constraints.
- Risk C3: governance debt if deferred boundaries are not explicit (Likelihood M, Impact H).
	- Testability signal: explicit in-scope/out-of-scope matrix and handoff questions logged for @3design.

Research coverage by task type: literature review, alternative enumeration, prior-art search, constraint mapping, stakeholder impact, risk enumeration.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Scope fit for this project boundary | High | High | Medium |
| Validation feasibility without code changes | Low | High | Medium |
| Operational clarity for maintainers | Medium | High | High |
| Governance/audit readiness | Medium | High | High |
| Risk of over-scoping discovery wave | Low | Medium | High |
| Effort complexity | Low | Medium | Medium-High |

## Recommendation
**Recommend Option B (canonical docs plus maintainer verification checklist).**

Rationale:
1. Option B best satisfies current scope boundaries by remaining documentation-only while still creating objective, reviewable validation signals.
2. It reduces operational ambiguity more effectively than Option A and avoids the upfront complexity/commitment overhead of Option C.
3. Validation feasibility is strongest in this wave because manual checklist evidence can be reviewed immediately without CI/source modifications.
4. This aligns with prior-art patterns where capability governance is introduced first with explicit contract tests/checklists before implementation expansion:
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md`
	 - `docs/project/archive/prj0000056/rust-async-transport-activation.think.md`
	 - `docs/project/archive/prj0000051/readme-update.think.md`

## Recommendation-to-Risk/Testability Map
- Primary risk: documentation drift from runtime reality.
	- Validation strategy: require checklist parity checks against `rust_core/Cargo.toml`, `rust_core/src/hardware.rs`, and `.github/workflows/ci.yml`.
- Primary risk: unsupported environment confusion.
	- Validation strategy: require explicit unsupported-path expected result criteria in checklist.
- Primary risk: missing audit trail.
	- Validation strategy: require capture format for maintainer verification evidence in project artifacts.

## Open Questions
1. What minimum supported environment should @3design define (Windows-only vs broader OS matrix) for this feature's documented activation path?
2. Should @3design require a strict "unsupported but safe fallback" acceptance statement tied to `AMD_NPU_STATUS_UNAVAILABLE` behavior?
3. What evidence granularity should be mandatory for checklist completion (command output excerpt, status table, or both)?
4. Should follow-on CI automation be explicitly filed as a separate project artifact now, or deferred until checklist evidence shows repeated maintainer usage?