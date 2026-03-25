# PyAgent API Reference

The PyAgent backend exposes a REST API and an end-to-end encrypted WebSocket API.
Use the REST API to query system metrics, manage projects, inspect agent memory, and
control pipelines. Use the WebSocket to receive real-time agent stream output.

---

## Base URLs

| Environment | Base URL |
|---|---|
| Local dev | `http://localhost:8000` |
| Docker Compose | `http://backend:8000` |

All REST endpoints are available under both `/api/` (legacy) and `/api/v1/` (current).
Prefer `/api/v1/` — the bare `/api/` path carries a `Deprecation: true` response header.

---

## Versioning Headers

Every response includes versioning information:

| Header | Present on | Value |
|---|---|---|
| `X-API-Version` | `/api/v1/` responses | `1` |
| `Deprecation` | `/api/` (non-v1) responses | `true` |
| `Link` | `/api/` (non-v1) responses | `<v1-path>; rel="successor-version"` |
| `X-Correlation-ID` | All responses | UUID (echoed or auto-generated) |

---

## Quick-Start

```http
# 1. Health check (no auth)
GET /health HTTP/1.1
Host: localhost:8000

# 2. Authenticated request
GET /api/v1/projects HTTP/1.1
Host: localhost:8000
X-API-Key: your-api-key
```

---

## Contents

| Topic | Description |
|---|---|
| [Authentication](authentication.md) | API Key, JWT, DEV\_MODE, WebSocket auth |
| [REST Endpoints](rest-endpoints.md) | All endpoints with request/response schemas |
| [WebSocket](websocket.md) | E2E encrypted real-time channel |
| [Errors](errors.md) | HTTP status codes, WS close codes, rate limiting |

