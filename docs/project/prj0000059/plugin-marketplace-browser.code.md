# plugin-marketplace-browser — Code Notes
_Owner: @6code | Status: DONE_

## backend/app.py

Added module-level constant `PLUGIN_REGISTRY` (list of 5 plugin dicts) and a
new public route on `app` (not `_auth_router`):

```python
PLUGIN_REGISTRY = [
    {"id": "coder-enhanced", "name": "CoderAgent Enhanced", ...},
    ...
]

@app.get("/api/plugins")
async def list_plugins():
    return {"plugins": PLUGIN_REGISTRY}
```

The route is intentionally NOT behind `_auth_router` — plugin discovery is
public read-only data that does not require authentication.

## web/apps/PluginMarketplace.tsx

New React component. Key design decisions:
- `useState<Plugin[]>` for local toggled install state
- `useEffect` triggers `fetch('/api/plugins')` on mount
- Search input filters across `name`, `description`, and `tags`
- Each card has an Install/Uninstall toggle button that sets `installed` in local state
- No API calls on toggle — state is ephemeral per session (V1 scope)

## web/types.ts

`AppId` union extended with `'plugins'`.

## web/App.tsx

- Import: `import { PluginMarketplace } from './apps/PluginMarketplace';`
- `openApp` switch: `case 'plugins'` → width 900, height 580, title "Plugin Marketplace"
- Menu entry: `<button onClick={() => openApp('plugins')}>🧩 Plugin Marketplace</button>`

## Key Design Decisions
- PLUGIN_REGISTRY is a module constant rather than a DB call — appropriate for V1 static list
- Local install toggle state is intentional — no backend mutation needed per spec
- Search filters client-side using `.filter()` — appropriate for small static list
