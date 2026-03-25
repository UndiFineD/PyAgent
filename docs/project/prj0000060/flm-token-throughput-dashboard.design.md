# flm-token-throughput-dashboard — Design
_Owner: @3design | Status: DONE_

## Architecture

### Backend: GET /api/metrics/flm

Registered directly on `app` (not `_auth_router`) so no authentication is required.
Returns simulated 10-sample window:

```
{
  "samples": [
    { "timestamp": float, "tokens_per_second": float,
      "model": "llama3-8b", "queue_depth": int },
    ...  × 10
  ],
  "avg_tokens_per_second": float,
  "peak_tokens_per_second": float,
  "model": "llama3-8b"
}
```

### Frontend: FLMDashboard.tsx

Component state:
- `data: FLMMetrics | null` — latest API response
- `error: string | null` — fetch error message

Polling:
```
useEffect(() => {
  const tick = async () => { ... fetch /api/metrics/flm ... };
  tick();
  const id = setInterval(tick, 2000);
  return () => clearInterval(id);
}, []);
```

SVG Bar Chart:
- ViewBox: `0 0 200 100`
- 10 bars, each 16px wide, 4px gap
- Bar height: `(tps / maxTps) * 100`
- Colour: `#4ade80` (green, NebulaOS accent-compatible)

### AppId Extension

- `web/types.ts`: add `'flm-dashboard'` to `AppId` union
- `web/App.tsx`: import `FLMDashboard`, add switch case + menu button (📊)

## Component Layout

```
┌─────────────────────────────────┐
│ 📊 FLM Token Throughput         │
│ Model: llama3-8b                │
│ Avg TPS: 275.3  Peak: 498.1     │
│ Queue depth: 4                  │
│                                 │
│ [SVG bar chart — 10 samples]    │
│  ▏▊▌▊▏▌▊▏▊▌                    │
└─────────────────────────────────┘
```
