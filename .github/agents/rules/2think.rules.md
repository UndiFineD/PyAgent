---
agent: "2think"
description: "Fallback rules and operational constraints for the 2think agent."
---

# Base Rules: 2think

These rules act as a resilient fallback for the `@2think` agent. 
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
    Do not perform tasks outside the explicit capabilities of `@2think`. 
    Escalate to the appropriate workflow or agent if your task crosses domain boundaries.

## Domain Specific Rules
- *(To be dynamically populated during runtime mapping and learning)*

### Learned Rules & Historical Patterns

- Avoids frontend logic duplication and avoids process-heavy generated registry workflows.
- Avoids introducing a new cross-domain `src/infrastructure` tree solely to satisfy one compose reference.
- Avoids large refactors while still creating a blocking non-regression contract.
- Pattern: Dashboard/registry side effects repeatedly cause out-of-scope diffs and closure noise.
- Pattern: Dual linter/type-check config surfaces with opposite defaults can silently dilute intended governance.
- Pattern: For broken deployment paths, prefer deploy-domain normalization over ad hoc cross-tree file creation.
- Pattern: For committed-secret incidents, prefer phased containment plus scheduled full-history cleanup.
- Pattern: For governance-derived filtering logic in Project Manager, centralize semantics in backend APIs and keep frontend as consumer.
- Pattern: For new gateway surfaces, prefer split-plane contracts when both governance controls and hot-path performance are first-class requirements.
- Pattern: For quality gates with low current enforcement fidelity, prefer staged ratchet rollout over immediate high-threshold cutover.
- Pattern: Governance-first sequencing reduces cleanup rework and improves discoverability for multi-surface repo hygiene projects.
- Pattern: Re-validate idea assumptions against current source before selecting architecture options.
- Pattern: Re-validate idea assumptions against current source state before planning deprecation/removal work.
- Pattern: Recurring cross-project drift appears as the trio of partial fail-closed behavior, non-deterministic/insufficient validation signals, and stale lifecycle artifacts.
- Pattern: Refresh-token projects in validator-only JWT backends should first separate token validation, session persistence, and transport/session binding concerns before scoring options.
- Pattern: Revalidate elimination objective against current package implementation state before proposing refactors.
- Pattern: Use scoped blocking strict lanes before broad mypy strict rollout.
- Root cause confirmed: `deploy/compose.yaml` points to non-existent `src/infrastructure/docker/Dockerfile`.
- Root cause is enforcement drift: legacy non-enforcing threshold history plus current CI path without active coverage gate.
- Root cause is governance drift and discoverability gaps, not only raw cleanup volume.
- Root cause: Cleanup efforts drift when policy artifacts are treated as end-of-project documentation rather than continuous operational checkpoints.
- Root cause: Compose referenced a path with no repository-backed ownership or validation guard.
- Root cause: Configuration may exist without blocking CI integration, creating false confidence in policy enforcement.
- Root cause: Exclusion behavior and "implemented" semantics were implicit across markdown metadata and lane registry, causing ambiguity.
- Root cause: Existing auth surfaces often appear “JWT-capable” while still lacking issuance, revocation, and replay-resistant refresh semantics.
- Root cause: Existing capabilities were present but scattered, creating policy sequencing and ownership ambiguity.
- Root cause: Global permissive mypy config turned type checks into non-enforcing signals.
- Root cause: Historical placeholder packages evolved unevenly, leaving mixed maturity under a single "stub" label.
- Root cause: Idea metadata lagged repository state (`/health` present; only `/readyz` and `/livez` missing).
- Root cause: Incremental migration introduced stricter `pyproject.toml` settings while permissive `mypy.ini` remained active.
- Root cause: Project intent lagged repository evolution from stubs to implemented package surfaces.
- Root cause: Projects close phase slices before all failure paths and closure/governance synchronization are bound to mandatory selectors.
- Root cause: Required dashboard refresh and registry updates touch broad shared docs while projects are scoped narrowly.
- Root cause: Secret present in repository without dedicated secret-scanning gates.

### Learned Rules & Historical Patterns

- Avoids frontend logic duplication and avoids process-heavy generated registry workflows.
- Avoids introducing a new cross-domain `src/infrastructure` tree solely to satisfy one compose reference.
- Avoids large refactors while still creating a blocking non-regression contract.
- Pattern: Dashboard/registry side effects repeatedly cause out-of-scope diffs and closure noise.
- Pattern: Dual linter/type-check config surfaces with opposite defaults can silently dilute intended governance.
- Pattern: For broken deployment paths, prefer deploy-domain normalization over ad hoc cross-tree file creation.
- Pattern: For committed-secret incidents, prefer phased containment plus scheduled full-history cleanup.
- Pattern: For governance-derived filtering logic in Project Manager, centralize semantics in backend APIs and keep frontend as consumer.
- Pattern: For new gateway surfaces, prefer split-plane contracts when both governance controls and hot-path performance are first-class requirements.
- Pattern: For quality gates with low current enforcement fidelity, prefer staged ratchet rollout over immediate high-threshold cutover.
- Pattern: Governance-first sequencing reduces cleanup rework and improves discoverability for multi-surface repo hygiene projects.
- Pattern: Re-validate idea assumptions against current source before selecting architecture options.
- Pattern: Re-validate idea assumptions against current source state before planning deprecation/removal work.
- Pattern: Recurring cross-project drift appears as the trio of partial fail-closed behavior, non-deterministic/insufficient validation signals, and stale lifecycle artifacts.
- Pattern: Refresh-token projects in validator-only JWT backends should first separate token validation, session persistence, and transport/session binding concerns before scoring options.
- Pattern: Revalidate elimination objective against current package implementation state before proposing refactors.
- Pattern: Use scoped blocking strict lanes before broad mypy strict rollout.
- Root cause confirmed: `deploy/compose.yaml` points to non-existent `src/infrastructure/docker/Dockerfile`.
- Root cause is enforcement drift: legacy non-enforcing threshold history plus current CI path without active coverage gate.
- Root cause is governance drift and discoverability gaps, not only raw cleanup volume.
- Root cause: Cleanup efforts drift when policy artifacts are treated as end-of-project documentation rather than continuous operational checkpoints.
- Root cause: Compose referenced a path with no repository-backed ownership or validation guard.
- Root cause: Configuration may exist without blocking CI integration, creating false confidence in policy enforcement.
- Root cause: Exclusion behavior and "implemented" semantics were implicit across markdown metadata and lane registry, causing ambiguity.
- Root cause: Existing auth surfaces often appear “JWT-capable” while still lacking issuance, revocation, and replay-resistant refresh semantics.
- Root cause: Existing capabilities were present but scattered, creating policy sequencing and ownership ambiguity.
- Root cause: Global permissive mypy config turned type checks into non-enforcing signals.
- Root cause: Historical placeholder packages evolved unevenly, leaving mixed maturity under a single "stub" label.
- Root cause: Idea metadata lagged repository state (`/health` present; only `/readyz` and `/livez` missing).
- Root cause: Incremental migration introduced stricter `pyproject.toml` settings while permissive `mypy.ini` remained active.
- Root cause: Project intent lagged repository evolution from stubs to implemented package surfaces.
- Root cause: Projects close phase slices before all failure paths and closure/governance synchronization are bound to mandatory selectors.
- Root cause: Required dashboard refresh and registry updates touch broad shared docs while projects are scoped narrowly.
- Root cause: Secret present in repository without dedicated secret-scanning gates.
