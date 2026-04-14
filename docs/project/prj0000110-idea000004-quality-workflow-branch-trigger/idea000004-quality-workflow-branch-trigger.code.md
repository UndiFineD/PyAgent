# idea000004-quality-workflow-branch-trigger - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-01_

## Implementation Summary
Applied a minimal CI workflow contract fix in `.github/workflows/ci.yml` to satisfy red-phase requirements while preserving workload-reduction behavior.

Changes implemented:
- Updated workflow name to `CI / Branch Governance` for required-check identity stability.
- Replaced ambiguous pull request project branch glob `prj*` with explicit policy pattern `prj[0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*`.

No job logic, shard layout, or Rust-build skip behavior was modified.

Scoped remediation applied on 2026-04-01:
- Fixed formatter drift in `tests/docs/test_agent_workflow_policy_docs.py` by normalizing a quote style in one
	assertion string literal without changing behavior.
- Kept scope strict by not staging unrelated pre-existing changes in `scripts/project_registry_governance.py`.

## AC Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-QWB-001 / IFACE-QWB-001 | `.github/workflows/ci.yml` (`on.pull_request.branches`) | `tests/ci/test_ci_workflow.py::test_ci_workflow_pull_request_trigger_includes_project_branches` | PASS |
| AC-QWB-004 / IFACE-QWB-004 | `.github/workflows/ci.yml` (`name`) | `tests/ci/test_ci_workflow.py::test_ci_workflow_required_check_identity_contract` | PASS |
| AC-QWB-003 | `tests/docs/test_agent_workflow_policy_docs.py` | `tests/docs/test_agent_workflow_policy_docs.py::test_project_registry_governance_supports_idea_archive_sync` and full selector run | PASS |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `.github/workflows/ci.yml` | Rename workflow to required-check identity and tighten project branch trigger glob | +2/-2 |
| `tests/docs/test_agent_workflow_policy_docs.py` | Formatter-only quote normalization in governance assertion | +1/-1 |
| `docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.code.md` | Record implementation and AC/test evidence | +33/-16 |

## Test Run Results
```text
python -m pytest -q tests/ci/test_ci_workflow.py tests/test_enforce_branch.py
27 passed in 1.73s

python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
17 passed in 1.25s

python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py tests/ci/test_ci_workflow.py tests/test_enforce_branch.py
44 passed in 2.03s
```

## Deferred Items
none