# amd-npu-feature-documentation - Git Summary

_Status: BLOCKED_
_Git: @9git | Updated: 2026-04-03 (validation gate failed on baseline infra debt)_

## Branch Plan
**Expected branch:** `prj0000118-amd-npu-feature-documentation`
**Observed branch:** `prj0000118-amd-npu-feature-documentation`
**Project match:** PASS

## Branch Validation
| Check | Result | Notes |
|---|---|---|
| Expected branch recorded in project overview | PASS | Project overview includes the assigned branch plan. |
| Observed branch matches project | PASS | `git branch --show-current` returned the expected branch. |
| No inherited branch from another `prjNNNNNNN` | PASS | Branch naming matches the assigned project boundary. |

## Scope Validation
| File or scope | Result | Notes |
|---|---|---|
| `docs/project/prj0000118-amd-npu-feature-documentation/**` | PASS | All canonical artifacts remain inside the assigned project boundary. |
| `docs/project/kanban.json` | PASS | Discovery entry remains scoped to prj0000118. |
| `data/projects.json` | PASS | Matching registry entry remains present for prj0000118. |
| `data/nextproject.md` | PASS | Next project counter remains advanced to `prj0000119`. |
| `docs/project/ideas/idea000020-amd-npu-feature-documentation.md` | PASS | Idea mapping remains pointed at `prj0000118`. |
| `.github/agents/data/current.1project.memory.md` | PASS | Current task lifecycle note remains scoped to this initialization attempt. |
| `.github/agents/data/2026-04-03.1project.log.md` | PASS | Daily log includes the resumed validation attempt. |

## Commit Hash
`BLOCKED`

## Files Changed
| File | Change |
|---|---|
| docs/project/prj0000118-amd-npu-feature-documentation/* | Created canonical initialization artifacts |
| docs/project/kanban.json | Added Discovery registry entry for prj0000118 |
| data/projects.json | Added Discovery registry entry for prj0000118 |
| data/nextproject.md | Advanced next project counter to prj0000119 |
| docs/project/ideas/idea000020-amd-npu-feature-documentation.md | Mapped idea000020 to prj0000118 |
| .github/agents/data/current.1project.memory.md | Recorded blocked task state |
| .github/agents/data/2026-04-03.1project.log.md | Recorded initialization attempt and blocker |

## PR Link
N/A

## Legacy Branch Exception
None

## Failure Disposition
**BLOCKED by out-of-scope baseline debt — return to @0master.**

The mandatory pre-commit policy test (`tests/docs/test_agent_workflow_policy_docs.py::test_legacy_git_summaries_document_branch_exception_and_corrective_ownership`) failed while validating this docs-only closure.

Failing check: Missing legacy project baseline file
- File: `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`
- Scope: Out of prj0000118 boundary
- Remediation: Create the missing legacy git artifact or update test to exclude non-existent legacy projects

**Branch/Scope Validation Status:** Both PASS
- Project branch matches expected: `prj0000118-amd-npu-feature-documentation` ✅
- All changed files within scope boundary ✅
- Registry governance validation: PASS ✅

**Staged Files Ready:**
- prj0000118 canonical artifacts (think, design, plan, test, code, exec, ql, git)
- Feature documentation: `docs/performance/HARDWARE_ACCELERATION.md`
- Test contracts: `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py`
- Registry updates: `kanban.json`, `projects.json`, `nextproject.md`, idea mapping

**Next Steps for @0master:**
1. Create or confirm status of `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`
2. Or update test to skip non-existent legacy projects
3. Trigger @9git handoff again when baseline is remediated

## Lessons Learned
Resume checks must rerun the exact mandatory selectors instead of relying on earlier summaries, because inherited branch-local documentation debt can still invalidate a supposedly clean initialization handoff.