# agent-orchestration-graph — Plan
_Owner: @4plan | Status: DONE_

## TDD Plan

### Red phase (tests first — test_orchestration_graph.py)
1. `test_agent_log_endpoint_returns_200` — GET /api/agent-log/0master → 200
2. `test_agent_log_response_has_correct_fields` — response has `"content"` key
3. `test_agent_log_accepts_put_request` — PUT /api/agent-log/0master → 200
4. `test_agent_log_put_stores_data` — PUT content is persisted
5. `test_agent_log_roundtrip` — PUT then GET returns same content

### Green phase (implementation)
1. Create `web/apps/OrchestrationGraph.tsx`
2. Modify `web/App.tsx` — import + register
3. Modify `web/types.ts` — add AppId

### Task breakdown

| # | Task | Owner | Effort |
|---|---|---|---|
| T1 | Write test file (5 tests) | @5test | XS |
| T2 | Create OrchestrationGraph.tsx | @6code | S |
| T3 | Update web/App.tsx | @6code | XS |
| T4 | Update web/types.ts | @6code | XS |
| T5 | Run tests — verify pass | @7exec | XS |
| T6 | Update data/projects.json | @9git | XS |
| T7 | Update docs/project/kanban.md | @9git | XS |
| T8 | Commit and push | @9git | XS |
| T9 | Open PR | @9git | XS |

## Acceptance Criteria
- All 5 tests in `test_orchestration_graph.py` pass
- Full test suite: no new failures introduced
- OrchestrationGraph visible as "Orchestration" in NebulaOS app menu
- Stage pipeline renders 10 boxes with correct labels
- Progress bar reflects done/total ratio
- Polling interval of 3 seconds confirmed in component code
