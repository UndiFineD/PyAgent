# flm-token-throughput-dashboard — Code Notes
_Owner: @6code | Status: DONE_

## backend/app.py — GET /api/metrics/flm

New public endpoint (registered directly on `app`, not on `_auth_router`).
Uses `import random` and `import time` (both stdlib, no new dependencies).

Response shape:
```python
{
    "samples": [
        {
            "timestamp": float,        # UTC epoch seconds
            "tokens_per_second": float, # uniform(50, 500) rounded to 1 dp
            "model": "llama3-8b",
            "queue_depth": int          # randint(0, 10)
        }
        ... × 10
    ],
    "avg_tokens_per_second": float,  # mean of the 10 samples
    "peak_tokens_per_second": float, # max of the 10 samples
    "model": "llama3-8b"
}
```

## web/apps/FLMDashboard.tsx

New React component. Key implementation details:
- Polls `/api/metrics/flm` every 2 seconds via `setInterval` in `useEffect`
- SVG viewBox `"0 0 220 110"`, 10 bars × (18px wide + 4px gap), max bar height 100px
- Bar colour `#4ade80` on dark backgrounds
- Shows: model, avg TPS, peak TPS, queue depth of latest sample
- Loading state renders "Loading…" text; error state renders red error message

## web/types.ts

Added `'flm-dashboard'` to the `AppId` union type.

## web/App.tsx

- Added `import { FLMDashboard } from './apps/FLMDashboard'`
- Added `case 'flm-dashboard':` in `openApp` switch (title = "FLM Dashboard", width = 500, height = 420)
- Added menu button with "📊" emoji icon before the Project Manager entry
