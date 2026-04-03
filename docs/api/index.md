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

All REST endpoints are available under both `/v1/api/` (current) and legacy aliases (`/api/`, `/api/v1/`).
Prefer `/v1/api/` — legacy paths carry a `Deprecation: true` response header.

---

## Versioning Headers

Every response includes versioning information:

| Header | Present on | Value |
|---|---|---|
| `X-API-Version` | `/v1/api/` responses | `1` |
| `Deprecation` | legacy responses (`/api/*`, unversioned probes) | `true` |
| `Link` | legacy responses | `<v1-path>; rel="successor-version"` |
| `X-Correlation-ID` | All responses | UUID (echoed or auto-generated) |

---

## Quick-Start

```http
# 1. Health check (no auth)
GET /v1/health HTTP/1.1
Host: localhost:8000

# 2. Authenticated request
GET /v1/api/projects HTTP/1.1
Host: localhost:8000
X-API-Key: your-api-key
```

## OpenAPI Artifact

The committed machine-readable backend worker schema is published as a static docs asset at
[openapi/backend_openapi.json](openapi/backend_openapi.json). This file is generated explicitly from
`backend.app` and reviewed in Git; the docs site consumes it and does not generate it during builds.

---

## Contents

| Topic | Description |
|---|---|
| [Authentication](authentication.md) | API Key, JWT, DEV\_MODE, WebSocket auth |
| [REST Endpoints](rest-endpoints.md) | All endpoints with request/response schemas |
| [WebSocket](websocket.md) | E2E encrypted real-time channel |
| [Errors](errors.md) | HTTP status codes, WS close codes, rate limiting |

