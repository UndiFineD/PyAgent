# live-agent-execution-in-codebuilder — Plan
_Owner: @4plan | Status: DONE_

## Implementation Tasks

### T1 — Backend: import additions
- Add `import uuid` and `from datetime import datetime` to `backend/app.py`
- Add `Request` to `fastapi` imports
- Add `_pipelines: dict = {}` module-level store

### T2 — Backend: POST /api/pipeline/run
- Model: `PipelineRunRequest(task: str = "")` Pydantic model
- Create pipeline_id with `uuid.uuid4()`
- Store complete record in `_pipelines[pipeline_id]`
- Return `{ "pipeline_id": pipeline_id, "status": "running" }`

### T3 — Backend: GET /api/pipeline/status/{pipeline_id}
- Lookup in `_pipelines`; 404 if missing
- Return full pipeline record as-is

### T4 — Frontend: state + ref additions (CodeBuilder.tsx)
- State: `pipelineId`, `pipelineStages`, `isPipelineRunning`
- Import `Zap` from lucide-react

### T5 — Frontend: handleRunPipeline
- POST `/api/pipeline/run` with task text
- On success: set `pipelineId` and `isPipelineRunning = true`

### T6 — Frontend: polling useEffect
- Triggers on `pipelineId` / `isPipelineRunning` change
- `setInterval(2000)` → fetch status → `setPipelineStages`
- Stop on `status !== "running"`

### T7 — Frontend: "Run Pipeline" button in toolbar
- Add beside existing Start/Stop and Reset buttons
- Uses `Zap` icon, label "Run Pipeline"
- Disabled while `isPipelineRunning = true`

### T8 — Frontend: Pipeline Status Panel
- Rendered only when `pipelineId != null`
- Shows 10 stage chips with status indicators

### T9 — Tests: 5 tests in test_pipeline_execution.py
- test_pipeline_run_endpoint_returns_pipeline_id
- test_pipeline_status_endpoint_returns_pipeline_data
- test_pipeline_status_404_for_unknown_id
- test_pipeline_has_10_stages
- test_pipeline_stages_have_status_and_log_fields

## TDD Order

T9 red phase (write tests first conceptually), then T1-T3 to make them green,
then T4-T8 for UI (manually verified, no automated UI tests).
