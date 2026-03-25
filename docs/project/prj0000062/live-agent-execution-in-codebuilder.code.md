# live-agent-execution-in-codebuilder — Code Notes
_Owner: @6code | Status: DONE_

## backend/app.py — Pipeline Endpoints

### New imports added
```python
import uuid
from datetime import datetime
```

### Module-level store
```python
_pipelines: dict = {}
```

In-memory dict keyed by UUID4 pipeline_id. Suitable for demo/dev; does not
persist across server restarts.

### PipelineRunRequest model
```python
class PipelineRunRequest(BaseModel):
    task: str = ""
```

### POST /api/pipeline/run
- Creates a UUID4 `pipeline_id`
- Stores a full pipeline record with 10 pre-initialized stages
- All stages start at `{"status": "pending", "log": ""}`
- Returns `{"pipeline_id": pipeline_id, "status": "running"}`

### GET /api/pipeline/status/{pipeline_id}
- Looks up `_pipelines.get(pipeline_id)`
- Returns 404 if not found
- Returns the full pipeline record dict if found

## web/apps/CodeBuilder.tsx — Pipeline UI

### New import
```tsx
import { ..., Zap } from 'lucide-react';
```

### New state vars (3)
```tsx
const [pipelineId, setPipelineId] = useState<string | null>(null);
const [pipelineStages, setPipelineStages] = useState<Record<string, { status: string; log: string }>>({});
const [isPipelineRunning, setIsPipelineRunning] = useState(false);
```

### handleRunPipeline
- Async function, called on button click
- POSTs `/api/pipeline/run` with `{ task: inputText[activeAgent] || "@{activeAgent}" }`
- Sets `pipelineId` and `isPipelineRunning = true` on success
- Catches and logs errors without crashing

### Polling useEffect
- Triggers when `pipelineId` or `isPipelineRunning` changes
- `setInterval(2000ms)` → GET `/api/pipeline/status/{pipelineId}`
- Updates `pipelineStages` from response
- Clears interval when `status !== "running"`

### Run Pipeline button
- Added to the right-pinned toolbar group
- Icon: `Zap` (yellow), label: "Run Pipeline"
- Disabled while `isPipelineRunning`

### Pipeline Status Panel
- Conditionally rendered below the Body, above the Status Bar
- Shows when `pipelineId` is non-null
- 10 stage chips with emoji status indicators
