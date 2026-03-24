# project-management — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-24_

## Overview

Implement the canonical PyAgent project management system:

- `data/projects.json` — 62-entry machine-readable project registry (source of truth)
- `docs/project/kanban.md` — human-readable 7-lane Kanban board (source of truth)
- `backend/app.py` — `GET /api/projects` endpoint with `ProjectModel` Pydantic validation
- `web/apps/ProjectManager.tsx` — NebulaOS Kanban app (read-only, fetches backend)
- `web/src/App.tsx` + `web/src/types.ts` — register `ProjectManager` in NebulaOS
- `.github/agents/0master.agent.md` + `1project.agent.md` — kanban lifecycle conventions
- `tests/structure/test_kanban.py` — structural validation tests (AC-01 + AC-02)

Design option: **Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop)**  
All lane transitions are git commits; the board is queryable via the backend but never
written from the UI.

---

## Task List

- [ ] T1 — Create `data/projects.json` | Files: `data/projects.json` | Acceptance: AC-01
- [ ] T2 — Create `docs/project/kanban.md` | Files: `docs/project/kanban.md` | Acceptance: AC-02
- [ ] T3 — Add `GET /api/projects` to `backend/app.py` | Files: `backend/app.py` | Acceptance: AC-05
- [ ] T4 — Create `web/apps/ProjectManager.tsx` | Files: `web/apps/ProjectManager.tsx` | Acceptance: AC-03
- [ ] T5 — Register ProjectManager in `web/src/App.tsx` + `web/src/types.ts` | Files: `web/src/App.tsx`, `web/src/types.ts` | Acceptance: AC-04
- [ ] T6 — Update `0master.agent.md` with kanban.md lifecycle section | Files: `.github/agents/0master.agent.md` | Acceptance: AC-06
- [ ] T7 — Update `1project.agent.md` with kanban.md lifecycle convention | Files: `.github/agents/1project.agent.md` | Acceptance: AC-06

---

## Detailed Tasks

---

### T1 — Create `data/projects.json`

**Objective**: Write the full 62-entry JSON array to `data/projects.json`. This file is
the machine-readable source of truth for all project metadata and drives the backend
`/api/projects` endpoint and `ProjectManager` UI.

**File**: `data/projects.json`

**Content specification** (from design doc, write verbatim):
- Array of 62 JSON objects
- Each object has exactly these fields:
  - `id` (string, pattern `prj[0-9]{7}`) — `prj0000001` through `prj0000062`
  - `name` (string) — kebab-case project name
  - `lane` (string) — one of `"Ideas"`, `"Discovery"`, `"Design"`, `"In Sprint"`, `"Review"`, `"Released"`, `"Archived"`
  - `summary` (string) — one-sentence description
  - `branch` (string | null) — git branch name, `"merged"` sentinel for historical projects, `null` for ideas
  - `pr` (integer | null) — GitHub PR number or null
  - `priority` (string) — one of `"P1"`, `"P2"`, `"P3"`, `"P4"`
  - `budget_tier` (string) — one of `"XS"`, `"S"`, `"M"`, `"L"`, `"XL"`, `"unknown"`
  - `tags` (array of strings)
  - `created` (string, ISO date `YYYY-MM-DD`)
  - `updated` (string, ISO date `YYYY-MM-DD`)

**Lane distribution** (as specified in design):
- `Released` — prj0000001–prj0000042, prj0000045, prj0000047–prj0000051 (48 entries)
- `Review` — prj0000043, prj0000044 (2 entries)
- `In Sprint` — prj0000052 (1 entry)
- `Archived` — prj0000046 (1 entry)
- `Ideas` — prj0000053–prj0000062 (10 entries)
- `Discovery` — 0 entries
- `Design` — 0 entries

**Special values**:
- `prj0000043` (`p2p-security-deps`): `"branch": "prj0000043-p2p-security-deps"`, `"pr": null`
  (PR open but number unconfirmed — @6code must verify on GitHub before finalizing)
- `prj0000044`: `"pr": 136`
- `prj0000045`: `"pr": 137`
- `prj0000047`: `"pr": 185`
- `prj0000048`: `"pr": 186`
- `prj0000049`: `"pr": 187`
- `prj0000050`: `"pr": 188`
- `prj0000051`: `"pr": 189`
- `prj0000052`: `"lane": "In Sprint"`, `"branch": "prj0000052-project-management"`, `"pr": null`
- Ideas lane entries (prj0000053–prj0000062): `"branch": null`, `"pr": null`,
  `"priority": "P4"`, `"budget_tier": "unknown"`

**Dependencies**: None (can be created first)

**Acceptance criteria**: AC-01

---

### T2 — Create `docs/project/kanban.md`

**Objective**: Write the full 7-lane Kanban board as a Markdown file. This is the
human-readable source of truth for project status, read by agents before task allocation.

**File**: `docs/project/kanban.md`

**Content specification** (from design doc, write verbatim):

Structure (top-to-bottom):
1. `# PyAgent Project Kanban Board` (H1)
2. Subtitle line: `_Last updated: 2026-03-24 | Total projects: 62_`
3. `## How to use this board` section with lane table and governance rules
4. `---` separator
5. `## Ideas` section — 10 rows (prj0000053–prj0000062), columns: `ID, Name, Summary, Priority, Budget, Tags, Updated`
6. `## Discovery` section — empty table (headers only), columns: `ID, Name, Summary, Branch, Priority, Budget, Tags, Updated`
7. `## Design` section — empty table (headers only), same columns as Discovery
8. `## In Sprint` section — 1 row (prj0000052), columns: `ID, Name, Summary, Branch, Priority, Budget, Updated`
9. `## Review` section — 2 rows (prj0000043, prj0000044), columns: `ID, Name, Branch, PR, Priority, Budget, Updated`
10. `## Released` section — 48 rows (prj0000001–prj0000042 + prj0000045 + prj0000047–prj0000051), columns: `ID, Name, Summary, Branch, PR, Priority, Budget, Released`
11. `## Archived` section — 1 row (prj0000046), columns: `ID, Name, Summary, Reason, Updated`
12. `## Summary Metrics` section — table of lane counts summing to 62

**Consistency with T1**: Every project ID appearing in `kanban.md` must also appear in
`data/projects.json` with the same `lane` value. The two files must be consistent.

**No stubs**: No `TODO`, `FIXME`, or `TBD` strings in the file.

**Dependencies**: T1 (reference for ID consistency; can be created concurrently in practice)

**Acceptance criteria**: AC-02

---

### T3 — Add `GET /api/projects` to `backend/app.py`

**Objective**: Add a read-only projects endpoint to the existing FastAPI backend. The
endpoint loads `data/projects.json` at module startup and serves filtered or unfiltered
project lists with full Pydantic validation.

**File**: `backend/app.py`

**Pre-read required**: @6code must read the current `backend/app.py` before editing to
verify import state (`Optional`, `Literal`, `json`, `BaseModel` — check which are already
imported).

**Insertion point A** — after `_AGENTS_DIR` assignment, before `_VALID_AGENT_IDS`:

```python
# ── Project data ─────────────────────────────────────────────────────────────
_PROJECTS_FILE = _PROJECT_ROOT / "data" / "projects.json"


def _load_projects() -> list[dict]:
    """Load data/projects.json at module startup. Returns [] on missing/corrupt file."""
    if not _PROJECTS_FILE.exists():
        logger.warning("data/projects.json not found at %s", _PROJECTS_FILE)
        return []
    try:
        return json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load data/projects.json: %s", exc)
        return []


_PROJECTS: list[dict] = _load_projects()
```

**Insertion point B** — after `write_agent_doc` endpoint, before `@app.websocket("/ws")`:

```python
# ── Project models + endpoint ─────────────────────────────────────────────────

Lane = Literal["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
_PriorityLit = Literal["P1", "P2", "P3", "P4"]
_BudgetLit = Literal["XS", "S", "M", "L", "XL", "unknown"]


class ProjectModel(BaseModel):
    """Single project entry from data/projects.json."""
    id: str
    name: str
    lane: Lane
    summary: str
    branch: Optional[str] = None
    pr: Optional[int] = None
    priority: _PriorityLit = "P3"
    budget_tier: _BudgetLit = "M"
    tags: list[str] = []
    created: Optional[str] = None
    updated: Optional[str] = None


@app.get("/api/projects", response_model=list[ProjectModel])
async def get_projects(lane: Optional[str] = None) -> list[ProjectModel]:
    """Return all projects from data/projects.json, optionally filtered by lane."""
    if not _PROJECTS and not _PROJECTS_FILE.exists():
        raise HTTPException(status_code=500, detail="data/projects.json not found")
    valid: list[ProjectModel] = []
    for entry in _PROJECTS:
        try:
            valid.append(ProjectModel(**entry))
        except Exception as exc:
            logger.warning("Skipping malformed project entry %s: %s", entry.get("id"), exc)
    if lane:
        return [p for p in valid if p.lane == lane]
    return valid
```

**Import merge note**: `Literal` and `Optional` may already be in scope via
`from typing import …` at the top of `app.py`. Merge into existing import — do not
duplicate. Similarly verify `json` is already imported.

**Unknown lane**: The design specifies a 422 response for unknown lanes. Because
`ProjectModel.lane` is a `Literal` type and the filter is applied after validation,
passing an unknown `?lane=` value simply returns an empty list (the Pydantic validation
rejects entries with the wrong lane, and the filter finds no matches). This is acceptable
for v1 — @5test should test `?lane=UnknownLane` returns `[]` (200), not 422. If strict
422 is desired in v2, add an explicit allowlist check before filtering.

**Dependencies**: T1 (`data/projects.json` must exist for runtime behavior; not a code
dependency — the backend handles missing file gracefully)

**Acceptance criteria**: AC-05

---

### T4 — Create `web/apps/ProjectManager.tsx`

**Objective**: Create the full NebulaOS ProjectManager app as a single TypeScript/React
file. The component renders a horizontal-scroll Kanban board with 7 lane columns,
expandable project cards, and a filter/search bar.

**File**: `web/apps/ProjectManager.tsx`

**Component hierarchy**:
```
ProjectManager (main export)
├─ FilterBar (lane toggle buttons + text search)
└─ KanbanBoard (flex row, horizontal scroll)
    └─ LaneColumn × 7 (per-lane column with count badge)
        └─ ProjectCard × N (expandable, shows detail on click)
```

**Exported symbol**: `export const ProjectManager: React.FC`

**Data fetch**: `fetch('/api/projects')` on mount via `useEffect`. No polling.

**State variables**:
- `projects: Project[]` — raw data from backend
- `loading: boolean` — true while fetch in progress
- `error: string | null` — error message if fetch fails
- `selectedLane: Lane | null` — active lane filter (null = show all lanes)
- `searchQuery: string` — text filter against `name` and `id`

**Derived state** (no `useEffect`):
- `filtered` — `projects` filtered by `selectedLane` and `searchQuery`
- `byLane` — `filtered` grouped into `Record<Lane, Project[]>`

**ProjectCard detail** (expanded on click):
- Branch (if not `"merged"`)
- `merged` badge (if `branch === "merged"`)
- PR link to `https://github.com/UndiFineD/PyAgent/pull/{pr}` (if `pr !== null`)
  - Uses `target="_blank" rel="noopener noreferrer"` — no SSRF risk (static GitHub base URL)
- Tags with `Tag` icon
- Created/updated dates

**Styling**: `AgentChat.tsx`-style outer shell (uses CSS vars: `bg-os-bg`, `bg-os-window`,
`border-os-border`, `text-os-text`, `text-os-accent`). Lane colors and priority colors
use inline `style={{ }}` with hex values.

**Icons** (all from `lucide-react`): `GitBranch`, `ExternalLink`, `Search`, `Loader2`,
`AlertTriangle`, `ChevronDown`, `ChevronUp`, `Tag`

**TypeScript**: No type errors. All interfaces defined inline (no external type imports
needed beyond React and lucide-react).

**Pre-check before creating**: Verify `web/utils.ts` (or `web/src/utils.ts`) exports `cn`
— the design references `import { cn } from '../utils'`. Adjust the import path if needed.

**Dependencies**: T3 (endpoint shape confirmed by design), T1 (data format)

**Acceptance criteria**: AC-03

---

### T5 — Register ProjectManager in `web/src/App.tsx` + `web/src/types.ts`

**Objective**: Wire the `ProjectManager` component into the NebulaOS app launcher so it
appears in the Applications menu and opens as a window.

**Files**: `web/src/App.tsx`, `web/src/types.ts`

**Pre-read required**: @6code must read both files before editing to find the exact
insertion points.

#### `web/src/types.ts`

Change the `AppId` union type:

```typescript
// Before:
export type AppId = 'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder';

// After:
export type AppId = 'calculator' | 'editor' | 'paint' | 'conky' | 'settings' | 'codebuilder' | 'projectmanager';
```

(Note: design uses lowercase `'projectmanager'` — match exactly)

#### `web/src/App.tsx` — Three targeted changes

**Change 1 — Add import** (after the last `import { … } from './apps/…'` line):
```typescript
import { ProjectManager } from './apps/ProjectManager';
```

**Change 2 — Add switch case** (in the `renderApp` function / `openApp` switch, after
the `codebuilder` case):
```typescript
      case 'projectmanager':
        component = <ProjectManager />;
        title = 'Project Manager';
        width = 1100;
        height = 650;
        break;
```

**Change 3 — Add menu button** (in the Applications dropdown, after the last existing
app button):
```tsx
<button onClick={() => openApp('projectmanager')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
  <Monitor size={16} className="text-indigo-400" /> Project Manager
</button>
```

**Icon note**: `Monitor` is already imported in `App.tsx`. If `lucide-react@^0.577.0`
exports `LayoutKanban`, substitute it — otherwise use `Monitor` (safe fallback).

**Dependencies**: T4 (`ProjectManager` component must exist)

**Acceptance criteria**: AC-04

---

### T6 — Update `.github/agents/0master.agent.md`

**Objective**: Document the kanban.md lifecycle board in the master agent's knowledge
base so `@0master` reads and updates it on every project allocation.

**File**: `.github/agents/0master.agent.md`

**Pre-read required**: @6code must read the file to find the exact insertion points.

**Insertion A** — In `## Where to find key information`, after the bullet ending with
`` `docs/agents/` — agent memory + plan artifacts ``:

```markdown
### Project lifecycle board
- `docs/project/kanban.md` — single source of truth for project status across all
  lifecycle lanes (Ideas → Discovery → Design → In Sprint → Review → Released → Archived).
  - Read this before allocating a new `prjNNNNNNN` to confirm the next available ID.
  - Update this after any lane transition.
  - The board is also queryable via `GET /api/projects` in the backend.
```

**Insertion B** — In `## How the master agent operates`, after step 3 (Assign the
project boundary), insert step 3a:

```markdown
3a. **Update kanban.md** after allocating a project ID: add the new project to the
    `Ideas` or `Discovery` lane in `docs/project/kanban.md` and commit the change (or
    include it in the first commit on the project branch). Update `data/projects.json`
    to match.
```

**Validation**: After edit, `kanban.md` must appear at least twice in the file.

**Dependencies**: T2 (`kanban.md` must exist before referencing it)

**Acceptance criteria**: AC-06

---

### T7 — Update `.github/agents/1project.agent.md`

**Objective**: Add kanban.md lifecycle convention to the project agent's operating
procedure so new projects are always registered in the board when created.

**File**: `.github/agents/1project.agent.md`

**Pre-read required**: @6code must read the file to find the exact insertion points.

**Insertion A** — In `**Project doc conventions**`, after the final bullet (optional
chunked plan files):

```markdown
- **Lifecycle board**: When a new project is created, ensure `docs/project/kanban.md`
  has an entry in the correct lane. New projects without started discovery go in `Ideas`;
  projects handed off to `@2think` advance to `Discovery`. Move the row when the lane
  changes, and always update `data/projects.json` to match.
```

**Insertion B** — In `## Operating procedure`, after step 1, insert step 1a:

```markdown
1a. **Update kanban.md and data/projects.json**
    - Move the project entry from `Ideas` to `Discovery` in `docs/project/kanban.md`.
    - If no entry exists yet (project was not pre-registered by `@0master`), create a
      new row in `Discovery` with the assigned `prjNNNNNNN`, name, summary, priority,
      and `budget_tier`.
    - Update `data/projects.json`: set `"lane": "Discovery"` for this project entry
      (add the entry if missing).
    - Commit both files on the project-specific branch alongside the project folder
      creation commit.
```

**Validation**: After edit, `kanban.md` must appear at least twice in the file.

**Dependencies**: T2 (`kanban.md` must exist before referencing it)

**Acceptance criteria**: AC-06

---

## Acceptance Criteria

### AC-01: `data/projects.json` exists and is valid

| Check | Detail |
|---|---|
| File exists | `data/projects.json` present in repo root |
| Valid JSON | Parse without error (no trailing commas, no comments) |
| Entry count | Exactly **62** entries in the top-level array |
| Required fields | Every entry has: `id`, `name`, `lane`, `summary`, `branch`, `pr`, `priority`, `budget_tier`, `tags`, `created`, `updated` |
| ID pattern | Every `id` matches `^prj[0-9]{7}$` |
| No duplicate IDs | All 62 `id` values are unique |
| Lane values | All from: `["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]` |
| Priority values | All from: `["P1", "P2", "P3", "P4"]` |
| Budget tier values | All from: `["XS", "S", "M", "L", "XL", "unknown"]` |
| `prj0000052` present | Entry exists with `"lane": "In Sprint"` (will be `"Released"` after merge) |

---

### AC-02: `docs/project/kanban.md` structure

| Check | Detail |
|---|---|
| File exists | `docs/project/kanban.md` present |
| H1 heading | `# PyAgent Project Kanban Board` (exact text) |
| Required H2s | All 7: `## Ideas`, `## Discovery`, `## Design`, `## In Sprint`, `## Review`, `## Released`, `## Archived` |
| Summary Metrics H2 | `## Summary Metrics` section present |
| Project row count | Exactly 62 project rows across all lane tables |
| `prj0000052` present | Appears exactly once (in `## In Sprint`) |
| No stubs | No `TODO`, `FIXME`, or `TBD` strings |

---

### AC-03: `web/apps/ProjectManager.tsx` is complete

| Check | Detail |
|---|---|
| File exists | `web/apps/ProjectManager.tsx` present |
| Export | Contains `export const ProjectManager` |
| Data fetch | Contains `fetch('/api/projects')` |
| Filter logic | Contains `FilterBar` function/component or equivalent inline lane filter |
| Lane rendering | Contains `LaneColumn` function/component or equivalent per-lane rendering |
| TypeScript validity | `npx tsc --noEmit` in `web/` reports no errors for this file |

---

### AC-04: `web/src/App.tsx` registers ProjectManager

| Check | Detail |
|---|---|
| Import present | `import { ProjectManager }` appears in `App.tsx` |
| AppId registered | `'projectmanager'` string appears in `types.ts` AppId union |
| Switch case | `case 'projectmanager':` present in `App.tsx` |
| Menu button | `openApp('projectmanager')` appears in `App.tsx` |

---

### AC-05: `backend/app.py` has `/api/projects`

| Check | Detail |
|---|---|
| Route defined | `@app.get("/api/projects"` present in `app.py` |
| Model defined | `class ProjectModel(BaseModel):` present with all required fields |
| Startup loader | `_load_projects` function present |
| Graceful missing file | `_load_projects()` returns `[]` if `data/projects.json` not found |
| Filter param | `lane` query parameter accepted |
| No crash on startup | Module imports without error even when `data/projects.json` is absent |

---

### AC-06: Agent files updated

| Check | Detail |
|---|---|
| `0master.agent.md` | `kanban.md` appears at least **twice** in file |
| `0master.agent.md` | Contains `### Project lifecycle board` subsection |
| `0master.agent.md` | Contains step `3a.` in operating procedure |
| `1project.agent.md` | `kanban.md` appears at least **twice** in file |
| `1project.agent.md` | Contains `Lifecycle board` bullet in conventions |
| `1project.agent.md` | Contains step `1a.` in operating procedure |

---

## Tests to Create

File: `tests/structure/test_kanban.py`

| Test name | What it validates |
|---|---|
| `test_projects_json_exists` | `data/projects.json` file exists |
| `test_projects_json_valid` | File parses as valid JSON |
| `test_projects_json_entry_count` | Array length == 62 |
| `test_projects_json_required_fields` | Every entry has all 11 required keys |
| `test_projects_json_lane_values` | All `lane` values are in the 7-member allowlist |
| `test_projects_json_priority_values` | All `priority` values are in `["P1","P2","P3","P4"]` |
| `test_projects_json_budget_tier_values` | All `budget_tier` values are in `["XS","S","M","L","XL","unknown"]` |
| `test_projects_json_prj0000052_present` | Entry with `id == "prj0000052"` exists |
| `test_kanban_exists` | `docs/project/kanban.md` file exists |
| `test_kanban_h1` | First H1 is `# PyAgent Project Kanban Board` |
| `test_kanban_required_h2s` | All 7 lane H2 headings present |
| `test_kanban_summary_metrics_section` | `## Summary Metrics` section present |
| `test_kanban_total_rows` | Exactly 62 project rows across all lane tables |
| `test_kanban_prj0000052_present` | `prj0000052` appears exactly once in the file |
| `test_kanban_no_todo_fixme` | No `TODO`, `FIXME`, or `TBD` strings in file |

**Note on row-counting methodology for `test_kanban_total_rows`**: Count table body rows
(lines matching `| prj` prefix). Summary Metrics table and header rows must be excluded.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Data layer complete | T1, T2 | ☐ |
| M2 | Backend endpoint live | T3 | ☐ |
| M3 | UI complete | T4, T5 | ☐ |
| M4 | Agent instructions updated | T6, T7 | ☐ |
| M5 | All tests passing | AC-01, AC-02 | ☐ |

---

## Implementation Order

```
T1 (data/projects.json)  ──────────────────────┐
T2 (kanban.md)           ─────────── parallel ──┤──► T6, T7 (agent files)
                                                │
T3 (backend/app.py)      ◄── depends on T1 shape┘──► T4 (ProjectManager.tsx)
                                                         │
                                                         ▼
                                                    T5 (App.tsx + types.ts)
```

No circular dependencies. T1 and T2 can be written simultaneously. T3 can begin once
T1's JSON schema is confirmed. T4 begins once T3's endpoint shape is confirmed. T5 is
the last code change.

---

## Validation Commands

```powershell
# Activate venv first
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Run structural tests (AC-01 + AC-02)
python -m pytest tests/structure/test_kanban.py -v

# TypeScript type check (AC-03 + AC-04)
Set-Location web
npx tsc --noEmit
Set-Location ..

# Full test suite smoke check
python -m pytest -q --tb=short
```

---

## Open Questions (for @6code to resolve before finalizing)

1. **prj0000043 PR number**: Check `https://github.com/UndiFineD/PyAgent/pulls` for
   the PR number for `p2p-security-deps`. Fill in the integer or leave `null`.
2. **`typing.Optional` + `Literal` imports in `app.py`**: Verify before inserting the
   project endpoint block. Merge into existing import statements.
3. **`LayoutKanban` icon**: Check `lucide-react@^0.577.0` exports. Use `Monitor` as
   the guaranteed fallback.
4. **`line-clamp-2` Tailwind class**: Verify JIT / plugin support in `tailwind.config.*`.
   Substitute `overflow-hidden` + `max-h-[2.8rem]` if not available.
5. **`cn` utility path**: Verify whether `web/utils.ts` or `web/src/utils.ts` — adjust
   import path in `ProjectManager.tsx` accordingly.
6. **`test_kanban_total_rows` scope**: Confirm `tests/test_readme.py` only scans
   `README.md` and will not inflate counts from `kanban.md` references.
