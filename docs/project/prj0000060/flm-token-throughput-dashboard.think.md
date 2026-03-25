# flm-token-throughput-dashboard — Think / Analysis
_Owner: @2think | Status: DONE_

## Problem Statement

NebulaOS has no visibility into FLM (Federated Language Model) throughput.
Operators cannot observe whether the model is handling requests at acceptable
tokens-per-second rates. A lightweight dashboard panel closes this gap.

## Existing Metrics Infrastructure

The Conky (system monitor) app (prj0000047) demonstrated that:
1. The backend successfully serves live metrics via `/api/metrics/system`
2. React polling with `useEffect + setInterval` works reliably
3. SVG-based charts (in Conky) render efficiently without external libs

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| Recharts / Chart.js | Feature-rich | External dependency, bundle bloat |
| D3.js | Powerful | Complex API, heavy |
| Pure SVG `<rect>` bars | Zero dependencies, tiny, fully controlled | Manual scaling math |
| Canvas-based | Fast redraws | More code than SVG for static charts |

## Decision: Pure SVG Bar Chart

- Consistent with NebulaOS philosophy of minimal external dependencies
- SVG scales cleanly with CSS
- 10-sample window is small enough that manual `<rect>` scaling is straightforward
- Bar height = `(tps / maxTps) * 100` pixels

## Polling Strategy

- `useEffect` + `setInterval` at 2-second interval
- AbortController not needed at this scale; component unmount cleanup via `clearInterval`
- Simulated data on backend eliminates need for a live FLM server

## Security

- Public endpoint (no auth required) — metrics data is not sensitive
- No user-supplied input; output is purely numeric, no injection surface
