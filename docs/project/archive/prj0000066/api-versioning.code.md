# api-versioning — Code Notes

_Owner: @6code_

## Modified: `backend/app.py`

### `VersionHeaderMiddleware` (BaseHTTPMiddleware)
Added after `RateLimitMiddleware`:
```python
class VersionHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        path = request.url.path
        if path.startswith("/api/v1/"):
            response.headers["X-API-Version"] = "1"
        elif path.startswith("/api/") and not path.startswith("/api/v1/"):
            response.headers["Deprecation"] = "true"
            response.headers["Link"] = (
                f'<{path.replace("/api/", "/api/v1/", 1)}>; rel="successor-version"'
            )
        return response
```

### Additional `include_router` call
```python
app.include_router(_auth_router, prefix="/api/v1")
```
This mounts all existing `_auth_router` routes under the `/api/v1/` prefix with zero duplication of handler functions.

## No new files required
- All changes are within `backend/app.py`
- `tests/test_api_versioning.py` is new
