# api-versioning — Design

_Owner: @3design_

## Implementation approach

1. Create a versioned router: `_v1_router = APIRouter(prefix="/api/v1", dependencies=[Depends(require_auth)])`
2. Register the same endpoint functions on both `_auth_router` (prefix `/api`) and `_v1_router` (prefix `/api/v1`)
3. To avoid duplicating handler functions, define handlers once and mount to both routers
4. Add `X-API-Version: 1` response header on all `/api/v1/` responses
5. Add `Deprecation: true` response header on all bare `/api/` responses (except `/health`)

## Router structure

```python
# Unversioned (deprecated)
_auth_router = APIRouter(dependencies=[Depends(require_auth)])
# Versioned
_v1_router = APIRouter(prefix="/api/v1", dependencies=[Depends(require_auth)])

# All endpoint functions registered on both:
_v1_router.get("/agent-log/{agent_id}")(...handler...)
_auth_router.get("/api/agent-log/{agent_id}")(...handler...)
# etc.

app.include_router(_v1_router)
app.include_router(_auth_router)
```

## Deprecation header approach

Simple `BaseHTTPMiddleware` that injects headers based on path prefix — no duplication of handler logic.

```python
class VersionHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        path = request.url.path
        if path.startswith("/api/v1/"):
            response.headers["X-API-Version"] = "1"
        elif path.startswith("/api/") and not path.startswith("/api/v1/"):
            response.headers["Deprecation"] = "true"
            response.headers["Link"] = f'<{path.replace("/api/", "/api/v1/", 1)}>; rel="successor-version"'
        return response
```
