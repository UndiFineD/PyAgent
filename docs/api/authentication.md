# Authentication

The PyAgent API supports two authentication schemes for REST endpoints and two
equivalent schemes for the WebSocket endpoint. A development bypass mode is also
available for local testing.

---

## REST Authentication

### Option 1 — API Key

Pass the key in the `X-API-Key` request header:

```http
GET /api/v1/projects HTTP/1.1
Host: localhost:8000
X-API-Key: your-api-key
```

The API key value is configured via the `PYAGENT_API_KEY` environment variable on the server.

---

### Option 2 — JWT Bearer Token

Pass a signed JWT (HS256) in the `Authorization` header:

```http
GET /api/v1/projects HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The JWT signing secret is configured via the `PYAGENT_JWT_SECRET` environment variable.
Algorithm: `HS256`. No specific claims are required beyond a valid signature.

---

## WebSocket Authentication

The WebSocket endpoint does not support HTTP headers after the initial upgrade.
Pass credentials as query parameters instead:

| Method | Query Param | Example |
|---|---|---|
| API Key | `api_key` | `ws://localhost:8000/ws?api_key=your-api-key` |
| JWT | `token` | `ws://localhost:8000/ws?token=eyJ...` |

On authentication failure the server closes the WebSocket with **close code 4401**.

---

## Authentication Method Comparison

| Feature | API Key | JWT Bearer |
|---|---|---|
| Header (REST) | `X-API-Key: <key>` | `Authorization: Bearer <token>` |
| Query param (WS) | `?api_key=<key>` | `?token=<jwt>` |
| Revocable by rotating env var | Yes | Yes (rotate `PYAGENT_JWT_SECRET`) |
| Carries user identity claims | No | Yes (standard JWT claims) |
| Expiry | No | Optional (`exp` claim) |

---

## DEV\_MODE (Development Bypass)

When **neither** `PYAGENT_API_KEY` nor `PYAGENT_JWT_SECRET` is set on the server, the
backend enters **DEV\_MODE**. In this mode all requests are authenticated automatically and
a one-time `WARNING` is emitted to the server log:

```
WARNING: DEV_MODE active — all authentication is bypassed
```

> **Security Warning:** Never run in DEV\_MODE in production. Set at least one of
> `PYAGENT_API_KEY` or `PYAGENT_JWT_SECRET` before exposing the server.

---

## Environment Variables

| Variable | Used For | Required |
|---|---|---|
| `PYAGENT_API_KEY` | API Key authentication | One of the two must be set in production |
| `PYAGENT_JWT_SECRET` | JWT HS256 signing secret | One of the two must be set in production |

---

## Security Recommendations

1. Rotate `PYAGENT_API_KEY` and `PYAGENT_JWT_SECRET` periodically.
2. Use HTTPS / WSS in any environment that is not loop-back localhost.
3. Do not pass credentials in URL query params in production logs — use header-based auth for REST.
4. Use short-lived JWTs with an `exp` claim for automated agent calls.
