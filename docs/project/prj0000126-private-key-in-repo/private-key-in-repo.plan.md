# private-key-in-repo - Implementation Plan

_Status: DONE_
_Planner: @1project | Updated: 2026-04-04_
## Overview
Rapid rollout bootstrap plan for the first 24 idea-backed projects, sequenced in 6 waves of 4 projects each.

## Rapid Sequence Waves (6 x 4)
| Wave | Projects |
|---|---|
| Wave 1 | prj0000126 private-key-in-repo, prj0000127 mypy-strict-enforcement, prj0000128 coverage-minimum-enforcement, prj0000129 requirements-ci-deduplication |
| Wave 2 | prj0000130 docker-compose-consolidation, prj0000131 dependabot-renovate, prj0000132 backend-health-check-endpoint, prj0000133 rust-criterion-benchmarks |
| Wave 3 | prj0000134 jwt-refresh-token-support, prj0000135 tailwind-config-missing, prj0000136 frontend-e2e-tests, prj0000137 global-state-management |
| Wave 4 | prj0000138 frontend-url-routing, prj0000139 windows-ci-matrix, prj0000140 property-based-test-expansion, prj0000141 backend-integration-test-suite |
| Wave 5 | prj0000142 adr-backfill, prj0000143 automated-api-docs-ci, prj0000144 changelog-automation, prj0000145 pre-commit-ruff-version-drift |
| Wave 6 | prj0000146 projects-json-schema-validation, prj0000147 torch-optional-dependency-split, prj0000148 rl-module-implementation, prj0000149 docs-work-folder-cleanup |

## Task List
- [ ] T1 - Hand off Wave 1 to @2think with constrained discovery scope.
- [ ] T2 - Keep Waves 2-6 queued in Ideas until capacity opens.
- [ ] T3 - Promote queued waves by lane update as each prior wave reaches plan readiness.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Wave sequencing approved | T1 | NOT_STARTED |
| M2 | Queue governance active | T2 | NOT_STARTED |
| M3 | Promotion protocol active | T3 | NOT_STARTED |

## Validation Commands
`powershell
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python scripts/project_registry_governance.py validate
`

