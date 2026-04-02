# private-key-remediation - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-28_

## Root Cause Analysis
1. A sensitive private key artifact exists in repository history and current tree (`rust_core/2026-03-11-keys.priv`),
which means compromise must be assumed.
2. Current local and CI guardrails do not include dedicated secret scanning for committed key material.
3. Existing governance favors branch/scope gating and local pre-commit workflows, but there is no equivalent
mandatory secret-detection gate in the active workflow path.
4. Remediation must balance incident response urgency with repository-history safety and contributor workflow
stability.

## Research Evidence
| Task Type | Findings | Evidence |
|---|---|---|
| Literature review | Project scope explicitly requires private-key remediation plus prevention guardrails in commit/CI workflows. | `docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.project.md`, `docs/project/ideas/idea000001-private-key-in-repo.md` |
| Alternative enumeration | Three distinct approaches are viable: immediate path-only cleanup, full history rewrite, and phased containment-first. | `docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.project.md`, `docs/project/kanban.md` |
| Prior-art search | Prior security projects consistently chose minimal-safe v1, explicit guardrails, and deterministic validation paths. | `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.think.md`, `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md`, `docs/project/prj0000075/prj0000075.think.md` |
| Constraint mapping | Branch must match project branch; scope is restricted to remediation and governance artifacts; lane transitions are governed by board + registry sync. | `docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.project.md`, `docs/project/kanban.md`, `data/projects.json`, `/memories/repo/branch-governance.md` |
| Stakeholder impact | Affected stakeholders include security owners, all repository contributors, release/git gate maintainers, and downstream design/testing agents. | `.pre-commit-config.yaml`, `.github/workflows/security.yml`, `.github/agents/9git.agent.md`, `tests/test_precommit.py` |
| Risk enumeration | Repo currently ignores `rust_core/*-keys.*` in `.gitignore`, which helps with future local artifacts but does not remediate historical leak impact; must assume key is exposed. | `.gitignore`, `docs/project/prj0000076/prj0000076.think.md`, `rust_core/2026-03-11-keys.priv` |

## Constraints And Policy Check
1. Branch gate passed: observed branch `prj0000090-private-key-remediation` matches expected branch.
2. Scope boundary respected: this phase only edits project artifact and required registry/lane docs.
3. Naming/conduct policy check: no violations introduced; this phase is documentation-only and keeps existing naming.
4. Security constraint: recommendation must assume compromise and prioritize key rotation + durable prevention.

## Options
### Option A - Path-Only Cleanup Plus Forward Guardrails
Problem addressed:
- Remove key from current tree quickly and add pre-commit/CI secret scanning, without rewriting git history.

Approach:
1. Replace/remove committed private key file from active tree.
2. Rotate/revoke all credentials tied to that key.
3. Add local pre-commit and CI secret scanning gates.
4. Document incident and recovery runbook.

Research coverage used:
- Literature review: project and idea requirements.
- Constraint mapping: minimal blast-radius change path.
- Stakeholder impact: least disruptive to contributors.
- Risk enumeration: historical leak remains even after tree cleanup.

Pros:
- Fastest operational response in current tree.
- Lowest branch/rewrite complexity.
- Minimal disruption to open branches and forks.

Cons:
- Exposed secret still remains discoverable in repository history.
- Ongoing legal/compliance exposure may remain unacceptable.
- Requires strict communication that rotation is mandatory and complete.

Stakeholder impact:
- Security owners: medium.
- Contributors: low.
- @9git/release process: low.

Risk to testability mapping:
| Risk | Likelihood/Impact | Validation signal |
|---|---|---|
| Historical key remains in reachable commits | H/H | Add CI check that scans full git history for key signatures and fails if found |
| Rotation incomplete across dependent systems | M/H | Verification checklist test artifact requiring signed-off rotation IDs |
| Secret scanning hook bypassed locally | M/M | CI-enforced secret scan job that blocks merge regardless of local hook status |

Workspace evidence:
- `docs/project/ideas/idea000001-private-key-in-repo.md`
- `.pre-commit-config.yaml`
- `.github/workflows/security.yml`
- `.gitignore`

### Option B - Full History Rewrite And Hard Secret-Gate Enforcement
Problem addressed:
- Eliminate private key material from both active tree and git history, then enforce prevention at commit and CI boundaries.

Approach:
1. Immediate containment: revoke/rotate affected key and downstream credentials.
2. Rewrite history to purge private key material from all refs.
3. Force coordinated rebase/reclone guidance for contributors.
4. Add local secret hooks and mandatory CI secret scan, with block-on-failure policy.
5. Add regression tests that assert secret-scan tooling is wired and required.

Research coverage used:
- Literature review: idea + project scope require durable prevention.
- Prior-art search: minimal-safe security-first decisions from prior projects.
- Constraint mapping: branch governance, lane movement, and scoped documentation requirements.
- Stakeholder impact: broad impact across all clones and active branches.
- Risk enumeration: high coordination risk but strongest long-term security outcome.

Pros:
- Strongest remediation posture; removes discoverability in normal history traversal.
- Best alignment with "assume compromised" incident response.
- Clear, auditable prevention path via local + CI gates.

Cons:
- Highest operational coordination overhead.
- Risk of developer disruption due to rewritten refs.
- Requires strict communication and rollback planning.

Stakeholder impact:
- Security owners: high.
- Contributors and branch maintainers: high.
- @9git/release process: high.

Risk to testability mapping:
| Risk | Likelihood/Impact | Validation signal |
|---|---|---|
| Rewrite misses alternate refs/tags | M/H | Post-rewrite history scan over all refs and tags with zero secret hits required |
| Contributor branches diverge after force-push | H/M | Migration script dry-run checks plus contributor rebase verification checklist |
| Guardrails degrade over time | M/H | Structure tests for hook/workflow presence and mandatory CI scan status checks |

Workspace evidence:
- `docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.project.md`
- `docs/project/prj0000075/prj0000075.think.md`
- `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.think.md`
- `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md`

### Option C - Phased Containment First, Then Scheduled History Rewrite
Problem addressed:
- Reduce immediate incident risk quickly, then execute history surgery in a controlled second window.

Approach:
1. Day 0: rotate/revoke key and remove key from active tree.
2. Day 0: enforce pre-commit + CI secret scanning to prevent new leaks.
3. Day 1-2: perform controlled history rewrite with freeze window.
4. Day 2+: execute contributor migration and verify all refs.

Research coverage used:
- Literature review: urgency and governance requirements.
- Alternative enumeration: middle path between speed and completeness.
- Prior-art search: phased rollout pattern from prior security projects.
- Constraint mapping: manageable blast radius for one active project.
- Stakeholder impact: distributed burden across two bounded windows.
- Risk enumeration: interim residual history risk before rewrite.

Pros:
- Fast containment with lower immediate disruption.
- Better coordination readiness than immediate big-bang rewrite.
- Keeps security-first trajectory while reducing execution shock.

Cons:
- Residual exposure remains between containment and rewrite completion.
- Requires disciplined follow-through to avoid phase-2 deferral.
- Slightly longer total remediation timeline.

Stakeholder impact:
- Security owners: high.
- Contributors: medium-high.
- @9git/release process: medium.

Risk to testability mapping:
| Risk | Likelihood/Impact | Validation signal |
|---|---|---|
| Phase-2 rewrite gets postponed | M/H | Milestone gate in project docs requiring rewrite completion before lane advance |
| Temporary residual history exposure | H/M | Daily automated history scan until rewrite completion |
| Inconsistent local hook adoption | M/M | CI secret-scan hard gate and test asserting hook config exists |

Workspace evidence:
- `docs/project/kanban.md`
- `data/projects.json`
- `.pre-commit-config.yaml`
- `.github/workflows/security.yml`

## Decision Matrix
| Criterion | Option A: Path-only cleanup | Option B: Full history rewrite | Option C: Phased containment + rewrite |
|---|---|---|---|
| Immediate containment speed | High | Medium | High |
| Long-term security posture | Medium | High | High |
| Contributor disruption | Low | High | Medium |
| Governance/audit clarity | Medium | High | High |
| Execution complexity | Low | High | Medium |
| Residual leak risk after completion | Medium | Low | Low |
| Testability of controls | Medium | High | High |

## Recommendation
**Option C - Phased containment first, then scheduled history rewrite.**

Rationale:
1. It is security-first on day 0 (assume compromise, rotate immediately, prevent re-introduction).
2. It still reaches full-history hygiene (rewrite + verification), but with lower coordination failure risk than a
single-step big-bang rewrite.
3. It aligns with prior-art delivery posture: minimal-safe first control plane, then high-assurance hardening.

Required security-first remediation steps:
1. Containment immediately:
	- Revoke and rotate compromised key material and all dependent credentials.
	- Remove the key artifact from active tree and replace with non-secret placeholder guidance if needed.
2. Prevention immediately:
	- Add pre-commit secret scanning.
	- Add mandatory CI secret scanning (merge-blocking).
3. History hygiene:
	- Perform repository history rewrite to purge private key material from all refs/tags.
	- Force verification scan across all refs after rewrite.
4. Operational hardening:
	- Publish contributor migration instructions (fresh clone/rebase/reset guidance).
	- Add structure tests ensuring secret-scan hooks/workflows remain configured.

Historical prior-art references informing recommendation:
1. `docs/project/prj0000075/prj0000075.think.md` (single-source CI gate simplification and enforcement discipline).
2. `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md` (deterministic,
guardrail-first security rollout pattern).
3. `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.think.md` (minimal-safe
scope with auditable verification path).

## Open Questions For @3design
1. Which secret scanning tool will be the canonical gate for both local hook and CI (single tool vs layered tools)?
2. What is the exact freeze/migration protocol for active contributor branches during history rewrite?
3. Which verification signatures/patterns will be used to assert the old private key is absent from all refs?
4. Should remediation include an incident ADR under `docs/architecture/adr/` for future auditability?
