# plugin-marketplace-browser — Design
_Owner: @3design | Status: DONE_

## Architecture

### Backend: GET /api/plugins

Added directly to the `app` FastAPI instance (not `_auth_router`) so no auth
token is required. Returns a JSON object `{"plugins": [...]}`.

```
GET /api/plugins
→ 200 {"plugins": [ {id, name, description, author, version, tags, installed}, ... ]}
```

Registry is a module-level constant `PLUGIN_REGISTRY` — a list of dicts.
No persistence layer needed in V1.

### Frontend: PluginMarketplace.tsx

React component rendered inside a NebulaOS `WindowState`:

```
PluginMarketplace
├── search input (filters plugin cards)
├── loading state (fetching)
├── error state (fetch failed)
└── plugin grid
    └── PluginCard (per plugin)
        ├── name + version badge
        ├── description
        ├── author
        ├── tags
        └── Install / Uninstall button (local toggle)
```

### TypeScript Interfaces

```typescript
interface Plugin {
  id: string;
  name: string;
  description: string;
  author: string;
  version: string;
  tags: string[];
  installed: boolean;
}
```

Local state: `plugins: Plugin[]` (copy of fetched data, toggled in place).

### AppId Extension

`web/types.ts`:
```
AppId = '...' | 'plugins'
```

`web/App.tsx`:
- Import `PluginMarketplace`
- Add `case 'plugins':` in `openApp` switch (width: 900, height: 580)
- Add menu entry with icon 🧩

### Window Parameters
- Width: 900, Height: 580
- Title: "Plugin Marketplace"
- `hasMenu: false`
