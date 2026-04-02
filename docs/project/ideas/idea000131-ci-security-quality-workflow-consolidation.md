# idea000131 - ci-security-quality-workflow-consolidation

Planned project mapping: prj0000115

## Idea summary
Shift quality and security enforcement to pre-commit hooks first, with GitHub workflows kept minimal as verification-only safeguards.

## Problem statement
Current CI and security coverage is split across overlapping ideas and leaves gaps:
- branch trigger patterns are outdated for quality gates
- Rust-specific checks are not first-class in CI
- repository CodeQL assets are present but not wired end-to-end
- dependency vulnerability scanning is partially manual and stale

At the same time, putting all checks into GitHub Actions increases runtime and maintenance cost. The project needs local-first guardrails that fail fast before code is pushed.

Maintaining these as separate old ideas creates duplication in planning and execution.

## Why this matters now
A pre-commit-first approach keeps contributor feedback immediate, reduces noisy CI churn, and preserves lightweight GitHub workflows for fast repository throughput.

## Detailed proposal
1. Move core checks into pre-commit (Python lint/format/test selectors, Rust fmt/clippy/test selectors, secret/config sanity checks).
2. Keep GitHub workflows light: run only quick verification and required policy checks, relying on pre-commit as the main gate.
3. Use scoped hooks and changed-file targeting so local runs stay fast.
4. Keep heavyweight security scans scheduled or manual-on-demand, not on every push.
5. Document contributor workflow: run pre-commit locally before push, and keep CI as confirmation.

## Scope suggestion
- In scope: pre-commit configuration, lightweight CI workflow tuning, and contributor documentation for local-first validation.
- Out of scope: unrelated application feature work or broad architecture redesign.

## Non-goals
- Replacing all existing CI jobs in one change.
- Migrating every historical workflow file without compatibility checks.

## Requirements
- One deterministic pre-commit baseline with explicit hook ownership and fast feedback.
- GitHub workflows remain minimal and focused on confirmation, not full local replacement.
- Clear rollback path if new gates block critical delivery.

## Dependencies and constraints
- Must comply with docs/project/code_of_conduct.md and docs/project/naming_standards.md.
- Must keep one-project-one-branch and governance handoff standards.
- Must preserve repository build/test reliability while tightening security checks.

## Candidate implementation paths
- Path A: Incremental rollout by pre-commit hook groups (quality, rust, security).
- Path B: Pre-commit baseline + minimal CI verifier workflow from day one.

## Success metrics
- Most issues are caught by local pre-commit before push.
- GitHub workflow runtime and queue pressure decrease while pass rate remains stable or improves.
- CI remains focused on fast confirmation and governance checks.
- Duplicate idea threads are reduced into one tracked project plan.

## Validation commands
- pre-commit run --all-files
- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- python scripts/project_registry_governance.py validate

## Risks and mitigations
- Risk: stricter hooks increase local friction initially. Mitigation: staged hook rollout and targeted selectors.
- Risk: CI duplicates local work. Mitigation: keep CI to minimal verification and policy checks only.
- Risk: policy drift over time. Mitigation: codify checks in tests and governance scripts.

## Failure handling and rollback
Use branch-isolated changes and disable or downgrade specific pre-commit hooks if they block delivery unexpectedly, while preserving minimal CI verification.

## Readiness status
ready

## Priority scoring
- impact_score: 5
- confidence_score: 4
- effort_score: 3
- risk_score: 2
- alignment_score: 5
- priority_score: 9

## Merged from
- idea000004
- idea000005
- idea000006
- idea000007

## Source references
- docs/project/ideas/archive/idea000004-quality-workflow-branch-trigger.md
- docs/project/ideas/archive/idea000005-rust-ci-workflow.md
- docs/project/ideas/archive/idea000006-codeql-ci-integration.md
- docs/project/ideas/archive/idea000007-security-scanning-ci.md
