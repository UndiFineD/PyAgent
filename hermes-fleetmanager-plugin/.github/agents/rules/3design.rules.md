---
agent: "3design"
description: "Fallback rules and operational constraints for the 3design agent."
---

# Base Rules: 3design

These rules act as a resilient fallback for the `@3design` agent. 
They may be dynamically updated by `@agentwriter`, 
or superseded by PostgreSQL database records during workflow orchestration.

## Core Constraints
1. **Preserve State**: Always log intermediate work to `.github/agents/data/`.
2. **Acknowledge Overrides**: 
    If the PostgreSQL schema provides a newer rule for a given context, 
    obey the database rule over this file.
3. **Continuous Learning**: 
    If a task fails, analyze the failure signature and propose updates 
    to this file via `@agentwriter` or using your own file editing tools.
4. **Scope Strictness**: 
    Do not perform tasks outside the explicit capabilities of `@3design`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

- Pattern: API contract publication lanes stay implementable when generation ownership, verification ownership, and docs publication ownership are assigned to separate surfaces.
- Pattern: Backend auth upgrades stay implementation-ready when bootstrap identity and persistence durability are resolved explicitly before planning.
- Pattern: Benchmark governance lands cleanly when CI introduces harness-health smoke checks before any threshold enforcement.
- Pattern: Defect-lane design artifacts stay actionable when they explicitly lock non-goals and map interfaces to planned task IDs.
- Pattern: Design handoff quality improves when acceptance criteria and interface-to-task traceability are both explicit.
- Pattern: Docs-only hardware feature projects stay actionable when unsupported behavior semantics and evidence schema are both mandatory acceptance gates.
- Pattern: Explicit AC IDs plus interface-to-task traceability in design artifacts reduces @4plan ambiguity and rework.
- Pattern: FFI migration designs stay implementable when boundary contracts and parity rollback gates are defined before planning.
- Pattern: Governance-trigger designs stay executable when they separate lightweight branch-policy gates from full quality suites and encode required-check identity as an explicit contract.
- Pattern: Hybrid decision systems need explicit guardrail precedence and deterministic tie-break rules to stay testable.
- Pattern: Hybrid specialization designs stay actionable when adapter contracts, policy gates, and parity hooks are defined together.
- Pattern: Post-merge remediation projects require explicit fail-closed path audits before any implementation handoff.
- Pattern: Progressive type-enforcement efforts stay executable when warn/required lane contracts, rollback rules, and allowlist drift checks are designed together.
- Pattern: Rust workspace migrations stay actionable when lockfile policy, command continuity, and patch-ownership contracts are specified together.
- Pattern: Split-plane gateway projects move faster when contracts are pinned to existing integration points and tied to explicit @4plan task IDs.
- Root cause: Ambiguous prompt routing without staged control boundaries causes nondeterministic behavior and weak safety guarantees.
- Root cause: Branch-trigger requests can drift into noisy CI expansion when gate scope and required-check semantics are not specified.
- Root cause: CRDT subprocess integrations accumulate latency and reliability risk when boundary contracts are implicit.
- Root cause: Feature documentation efforts often stop at activation prose and omit fallback interpretation plus auditable validation proof requirements.
- Root cause: Immediate threshold gating in early benchmark adoption creates flakiness and slows rollout.
- Root cause: OpenAPI efforts become brittle when scripts, tests, CI, and docs builds all try to own generation at once.
- Root cause: Phase-one gateway slices ship happy-path contracts but leave budget-denied, exception, and telemetry-failure paths as implicit.
- Root cause: Planning drift appears when interface contracts are defined without concrete ownership mapping to integration modules.
- Root cause: Prior handoffs can stall when interfaces are defined but not mapped to executable plan tasks.
- Root cause: Prior workflow stalls happen when architecture contracts exist without executable decomposition mapping.
- Root cause: Refresh-token projects stall when teams leave initial session creation or storage durability as follow-up questions.
- Root cause: Specialized-agent intent can stall when manifests and runtime orchestration are not connected by explicit interface contracts.
- Root cause: Stale or already-fixed defect lanes can drift into unnecessary implementation scope without explicit boundary contracts.
- Root cause: Teams often define strictness goals without deterministic promotion and rollback mechanics, causing gate flapping and ad-hoc bypasses.
- Root cause: Unification tasks fail when teams migrate manifests without explicit command and lockfile contracts.
- lesson:

### Learned Rules & Historical Patterns

- Pattern: API contract publication lanes stay implementable when generation ownership, verification ownership, and docs publication ownership are assigned to separate surfaces.
- Pattern: Backend auth upgrades stay implementation-ready when bootstrap identity and persistence durability are resolved explicitly before planning.
- Pattern: Benchmark governance lands cleanly when CI introduces harness-health smoke checks before any threshold enforcement.
- Pattern: Defect-lane design artifacts stay actionable when they explicitly lock non-goals and map interfaces to planned task IDs.
- Pattern: Design handoff quality improves when acceptance criteria and interface-to-task traceability are both explicit.
- Pattern: Docs-only hardware feature projects stay actionable when unsupported behavior semantics and evidence schema are both mandatory acceptance gates.
- Pattern: Explicit AC IDs plus interface-to-task traceability in design artifacts reduces @4plan ambiguity and rework.
- Pattern: FFI migration designs stay implementable when boundary contracts and parity rollback gates are defined before planning.
- Pattern: Governance-trigger designs stay executable when they separate lightweight branch-policy gates from full quality suites and encode required-check identity as an explicit contract.
- Pattern: Hybrid decision systems need explicit guardrail precedence and deterministic tie-break rules to stay testable.
- Pattern: Hybrid specialization designs stay actionable when adapter contracts, policy gates, and parity hooks are defined together.
- Pattern: Post-merge remediation projects require explicit fail-closed path audits before any implementation handoff.
- Pattern: Progressive type-enforcement efforts stay executable when warn/required lane contracts, rollback rules, and allowlist drift checks are designed together.
- Pattern: Rust workspace migrations stay actionable when lockfile policy, command continuity, and patch-ownership contracts are specified together.
- Pattern: Split-plane gateway projects move faster when contracts are pinned to existing integration points and tied to explicit @4plan task IDs.
- Root cause: Ambiguous prompt routing without staged control boundaries causes nondeterministic behavior and weak safety guarantees.
- Root cause: Branch-trigger requests can drift into noisy CI expansion when gate scope and required-check semantics are not specified.
- Root cause: CRDT subprocess integrations accumulate latency and reliability risk when boundary contracts are implicit.
- Root cause: Feature documentation efforts often stop at activation prose and omit fallback interpretation plus auditable validation proof requirements.
- Root cause: Immediate threshold gating in early benchmark adoption creates flakiness and slows rollout.
- Root cause: OpenAPI efforts become brittle when scripts, tests, CI, and docs builds all try to own generation at once.
- Root cause: Phase-one gateway slices ship happy-path contracts but leave budget-denied, exception, and telemetry-failure paths as implicit.
- Root cause: Planning drift appears when interface contracts are defined without concrete ownership mapping to integration modules.
- Root cause: Prior handoffs can stall when interfaces are defined but not mapped to executable plan tasks.
- Root cause: Prior workflow stalls happen when architecture contracts exist without executable decomposition mapping.
- Root cause: Refresh-token projects stall when teams leave initial session creation or storage durability as follow-up questions.
- Root cause: Specialized-agent intent can stall when manifests and runtime orchestration are not connected by explicit interface contracts.
- Root cause: Stale or already-fixed defect lanes can drift into unnecessary implementation scope without explicit boundary contracts.
- Root cause: Teams often define strictness goals without deterministic promotion and rollback mechanics, causing gate flapping and ad-hoc bypasses.
- Root cause: Unification tasks fail when teams migrate manifests without explicit command and lockfile contracts.
- lesson:
