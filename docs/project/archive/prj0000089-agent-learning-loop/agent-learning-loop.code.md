# agent-learning-loop - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-27_

## Implementation Summary
Implemented a cross-agent learning loop policy across all 10 `.agent.md` definitions.
Added concise, enforceable rules in each agent file covering a shared lesson schema,
recurrence-based promotion threshold, and 5-project review cadence.
Added role-specific hard-rule gates to reduce recurring failures and improve handoff quality.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `.github/agents/0master.agent.md` | Added Learning loop rules + pre-delegation scorecard gate | +16/-0 |
| `.github/agents/1project.agent.md` | Added Learning loop rules + canonical artifact completeness gate | +12/-0 |
| `.github/agents/2think.agent.md` | Added Learning loop rules + prior-art and risk-to-testability gate | +13/-0 |
| `.github/agents/3design.agent.md` | Added Learning loop rules + AC table and interface-to-task traceability gate | +12/-0 |
| `.github/agents/4plan.agent.md` | Added Learning loop rules + task target-files/validation-command gate | +12/-0 |
| `.github/agents/5test.agent.md` | Added Learning loop rules + AC-to-test matrix and weak-test gate | +13/-0 |
| `.github/agents/6code.agent.md` | Added Learning loop rules + AC->code/tests evidence mapping gate | +11/-0 |
| `.github/agents/7exec.agent.md` | Added Learning loop rules + dependency warning classification policy | +13/-0 |
| `.github/agents/8ql.agent.md` | Added Learning loop rules + promotion lifecycle and debt ledger gate | +15/-0 |
| `.github/agents/9git.agent.md` | Added Learning loop rules + pre-commit evidence and scope manifest gate | +13/-0 |
| `docs/project/prj0000089-agent-learning-loop/agent-learning-loop.code.md` | Updated status, summary, changed-file ledger, and validation evidence | +24/-4 |

## Test Run Results
Lightweight markdown textual validation executed for touched files:

```powershell
$files=@('.github/agents/0master.agent.md','.github/agents/1project.agent.md','.github/agents/2think.agent.md','.github/agents/3design.agent.md','.github/agents/4plan.agent.md','.github/agents/5test.agent.md','.github/agents/6code.agent.md','.github/agents/7exec.agent.md','.github/agents/8ql.agent.md','.github/agents/9git.agent.md','docs/project/prj0000089-agent-learning-loop/agent-learning-loop.code.md'); $bad=@(); foreach($f in $files){$count=(Get-Content $f | Where-Object { $_ -match '^\s*```+' }).Count; if(($count % 2) -ne 0){$bad += "$f : odd fence count $count"}}; if($bad.Count -eq 0){'MARKDOWN_FENCE_CHECK=PASS'} else {'MARKDOWN_FENCE_CHECK=FAIL'; $bad}
```

Result: `MARKDOWN_FENCE_CHECK=PASS`

## Deferred Items
none
