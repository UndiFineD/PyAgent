# Errors

This page documents all error responses produced by the PyAgent API.

---

## HTTP Status Codes

| Code | Meaning | Common Causes |
|---|---|---|
| `200` | OK | Request succeeded |
| `201` | Created | Resource created (POST /projects, POST /agent-memory) |
| `204` | No Content | Resource deleted (DELETE /agent-memory) |
| `400` | Bad Request | Invalid `project_id` format, unknown `agent_id`, validation error |
| `401` | Unauthorized | Missing or invalid API key / JWT on a protected endpoint |
| `404` | Not Found | Project or pipeline ID does not exist |
| `409` | Conflict | Project with the requested ID already exists (POST /projects) |
| `422` | Unprocessable Entity | Request body failed Pydantic validation (missing required field, wrong type) |
| `429` | Too Many Requests | Rate limit exceeded — see [Rate Limiting](#rate-limiting) |
| `500` | Internal Server Error | Server-side failure (e.g., `data/projects.json` missing) |

---

## Standard Error Body

FastAPI returns a consistent JSON error body for all 4xx/5xx responses:

```json
{"detail": "Human-readable error message"}
```

For **422 Unprocessable Entity**, FastAPI returns a structured list:

```json
{
  "detail": [
    {
      "loc": ["body", "lane"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

---

## WebSocket Close Codes

| Close Code | Meaning | When Issued |
|---|---|---|
| `4401` | Unauthorized | Invalid or missing credential in `?api_key=` / `?token=` |
| `1011` | Internal Error | Decryption failure or unhandled server exception during session |
| `1000` | Normal Closure | Server or client initiated a clean disconnect |

---

## Rate Limiting

By default the server allows **60 requests per 60-second window** per client IP.
The `/health` endpoint is exempt.

Environment variables:

| Variable | Default | Description |
|---|---|---|
| `RATE_LIMIT_REQUESTS` | `60` | Max requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Window duration in seconds |

When the limit is exceeded the server responds with:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{"detail": "Rate limit exceeded", "retry_after": 60}
```

The `Retry-After` header value matches the `RATE_LIMIT_WINDOW` setting.

The rate limiter reads the `X-Forwarded-For` header when present (proxy deployments), falling
back to the direct client IP.

---

## Correlation IDs

Every response — including error responses — carries an `X-Correlation-ID` header. If the
client sends an `X-Correlation-ID` request header the same value is echoed back; otherwise a
new UUID is generated. Use this ID when reporting bugs or tracing requests across logs.

```http
HTTP/1.1 404 Not Found
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{"detail": "Project 'prj9999999' not found"}
```
