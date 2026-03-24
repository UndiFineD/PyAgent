# project-management — Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-24_

---

## Root Cause Analysis

PyAgent currently tracks 52 projects—numbered prj0000001 through prj0000052—across git
commits, PR descriptions, `docs/project/` folders, and agent memory files. There is no
single view: contributors and agents must check four disparate sources to understand what
is active, what is waiting, and what has shipped. The problem is not project execution
quality (the 10-agent pipeline is sound) but **project visibility**. Specifically:

1. **No lifecycle overview** — no canonical place shows all projects sorted by stage.
2. **No structured data file** — project metadata exists only in prose and git history.
3. **No UI surface** — NebulaOS has no panel where an agent or developer can quickly
   confirm which projects are In Sprint vs Review vs Released.
4. **Agent coordination gap** — `@0master` and `@1project` have no documented reference
   to a shared board, so future project launches risk step-skipping.
5. **Roadmap invisible** — ten future items from the README roadmap have no project IDs,
   no owner, and no priority signal.

The fix is a Kanban lifecycle board (`docs/project/kanban.md`) backed by a typed JSON
data file (`data/projects.json`) and surfaced in NebulaOS via a `ProjectManager.tsx`
React application.

---

## Research Area 1 — Kanban + PRINCE2 + Agile Hybrid Lane Structure

### Lane count evaluation: 7 vs fewer

Consolidating Design into Discovery loses an important signal: the separation between
**options exploration** (`@2think` artifact, `.think.md`) and **selected design**
(`@3design` artifact, `.design.md`). In the 10-agent pipeline these are distinct pipeline
stops with different agent owners and different exit criteria. Keeping them as separate
lanes makes the Kanban mirror the pipeline.

**Verdict**: 7 lanes is correct and maps exactly to the pipeline segments:

```
Ideas → Discovery → Design → In Sprint → Review → Released → Archived
```

Agents 0–1 gate the Ideas→Discovery transition.  
Agents 2–3 gate the Discovery→Design transition.  
Agents 4–6 gate the Design→In Sprint transition.  
Agents 7–8 gate the In Sprint→Review transition.  
Agent 9 gates the Review→Released transition.  
Archived is a terminal state (stalled, cancelled, or superseded projects).

### Lane definitions with entry and exit criteria

#### 1. Ideas
**Purpose**: Proposed projects not yet formally scoped.  
**Entry**: `@0master` adds an entry with a placeholder prjID, name, and P4 priority.  
**Exit criteria**:
- `@0master` assigns an official `prjNNNNNNN` identifier.
- A project folder `docs/project/prjNNNNNNN/` is created with all 9 stub files.
- Budget tier and priority are set (anything except "unknown").
- A branch plan is confirmed in the `.project.md`.

**PRINCE2 mapping**: Pre-Starting Up phase. No stage authorization yet.

#### 2. Discovery
**Purpose**: Active options exploration — `@2think` is working or has completed `.think.md`.  
**Entry**: `@1project` has created the project folder and delegated to `@2think`.  
**Exit criteria**:
- `<project>.think.md` status is `DONE`.
- At least two options are documented with a recommended option identified.
- All open questions are listed for `@3design`.

**PRINCE2 mapping**: Starting Up and Initiation. The Business Case is formed here.  
**Mandatory fields by this stage**: `id`, `name`, `lane`, `summary`, `priority`, `budget_tier`.

#### 3. Design
**Purpose**: `@3design` is producing the authoritative `<project>.design.md`.  
**Entry**: `.think.md` is `DONE`; `@2think` has handed off to `@3design`.  
**Exit criteria**:
- `<project>.design.md` status is `DONE`.
- Interface contracts, component boundaries, and data shapes are decided.
- `@4plan` has a concrete scope to plan against.

**PRINCE2 mapping**: Late Initiation → Stage authorization gate.  
**Tolerance note**: if the design diverges from the budget tier, it should be flagged here
before implementation begins—this is the cheapest correction point.

#### 4. In Sprint
**Purpose**: Active implementation — `@4plan` through `@6code` are working.  
**Entry**: `<project>.design.md` is `DONE`; work has started on the branch.  
**Exit criteria**:
- All implementation tasks in `.plan.md` are ticked.
- `@7exec` has verified the code runs end-to-end.
- `@8ql` security review is complete (`.ql.md` status `DONE`).
- CI passes.

**PRINCE2 mapping**: Managing Stage Boundary — the sprint is the stage.  
**Tolerance policy**: if actual effort exceeds budget_tier by more than one tier (e.g., M
work is taking L), `@0master` must be notified before continuing.

#### 5. Review
**Purpose**: PR is open; waiting for final merge approval.  
**Entry**: `@9git` has pushed the branch and opened the PR.  
**Exit criteria**:
- PR is approved (or is a solo-dev direct merge decision).
- All CI checks green.
- No outstanding review comments.

**PRINCE2 mapping**: Closing a Stage / Delivering a Work Package.

#### 6. Released
**Purpose**: PR merged to `main`; deliverable is live.  
**Entry**: Merge commit exists on `main`.  
**Exit criteria** (for archival gate): project is stable at least 2 sprints with no
follow-up bugs linked back to it. Can stay Released indefinitely.

**PRINCE2 mapping**: Post-project review phase. Consider Benefits Review.

#### 7. Archived
**Purpose**: Stalled, cancelled, superseded, or deferred projects.  
**Entry**: `@0master` decision — typically when the business case no longer applies,
the work was superseded by another project, or the blocker is external and unresolvable.  
**Exit criteria** (for revival): `@0master` moves back to Discovery with a fresh `.think.md`.

### Mandatory fields per stage (progressive gating)

| Field | Ideas | Discovery | Design | In Sprint | Review | Released |
|---|---|---|---|---|---|---|
| `id` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `name` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `summary` | draft | ✓ | ✓ | ✓ | ✓ | ✓ |
| `priority` | P4 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `budget_tier` | unknown | ✓ | ✓ | ✓ | ✓ | ✓ |
| `branch` | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| `pr` | — | — | — | — | ✓ | ✓ (merged) |
| `tags` | optional | optional | ✓ | ✓ | ✓ | ✓ |

### PRINCE2 concept mapping

| PRINCE2 Concept | Kanban Lane Equivalent |
|---|---|
| Project Brief | `Ideas` lane entry — minimal fields, placeholder ID |
| Business Case | Must be confirmed before leaving `Discovery` |
| Stage Authorization | Lane transition gate (e.g., Discovery → Design) |
| Tolerance (time/cost) | `budget_tier` field; overage triggers `@0master` review |
| Work Package | A task within `In Sprint` (tracked in `.plan.md`) |
| Highlight Report | kanban.md table itself — always current |
| Lessons Learned | `Archived` notes and retrospective in `.exec.md` |
| Benefits Realization | `Released` permanence — project stays visible post-merge |

---

## Research Area 2 — React Kanban Board Implementation

### Available packages (from web/package.json)

```json
{
  "react": "^19.2.4",            // hooks, effects, suspense
  "react-dom": "^19.2.4",
  "lucide-react": "^0.577.0",    // icons: Tag, GitBranch, ExternalLink, Search, Filter
  "clsx": "^2.1.1",              // conditional class merging
  "tailwind-merge": "^3.5.0",   // tailwind class merging
  "recharts": "^3.8.0"          // charts (not needed for kanban)
}
```

**No external kanban library is needed.** A kanban board is fundamentally a row of
flex columns. CSS flexbox handles everything required for v1.

### NebulaOS dark theme conventions

From `AgentChat.tsx` and `Conky.tsx` analysis:

| CSS Variable Class | Usage |
|---|---|
| `bg-os-bg` | Page/container background (near-black) |
| `bg-os-window` | Card/panel background (slightly lighter) |
| `border-os-border` | Dividers and card borders |
| `text-os-text` | Primary text |
| `text-os-text/60` | Secondary/muted text |
| `text-os-accent` | Accent color (used for interactive elements) |
| `bg-os-accent/20` | Subtle accent background |
| `hover:bg-os-hover` | Hover state background |

Font: `font-mono` for data/IDs (Conky pattern), regular sans for names.
Icons: `lucide-react` exclusively. No custom SVGs.

### Lane accent colors (per-lane identity)

| Lane | Tailwind Color | Hex approx | Rationale |
|---|---|---|---|
| Ideas | `blue-500` | #3b82f6 | Future potential |
| Discovery | `violet-500` | #8b5cf6 | Exploration |
| Design | `indigo-500` | #6366f1 | Architecture |
| In Sprint | `amber-400` | #fbbf24 | Active work / urgency |
| Review | `orange-400` | #fb923c | Under examination |
| Released | `emerald-500` | #10b981 | Green = shipped |
| Archived | `gray-500` | #6b7280 | Neutral / inactive |

### Priority chip colors

| Priority | Color |
|---|---|
| P1 | `red-500` |
| P2 | `orange-400` |
| P3 | `blue-400` |
| P4 | `gray-400` |

### Component architecture

```
ProjectManager.tsx
├── Types
│   ├── Lane (union: 'Ideas' | 'Discovery' | 'Design' | 'In Sprint' | 'Review' | 'Released' | 'Archived')
│   ├── Priority ('P1' | 'P2' | 'P3' | 'P4')
│   ├── BudgetTier ('XS' | 'S' | 'M' | 'L' | 'XL')
│   └── Project { id, name, lane, summary, branch, pr, priority, budget_tier, tags, created, updated }
│
├── Constants
│   ├── LANES: Lane[]  (ordered 7-element array)
│   ├── LANE_COLORS: Record<Lane, string>
│   └── PRIORITY_COLORS: Record<Priority, string>
│
├── ProjectManager (default export)
│   ├── State: projects[], loading, error, laneFilter, searchQuery
│   ├── useEffect: fetch('/api/projects') on mount
│   ├── Derived: filteredProjects (search + lane filter applied)
│   ├── FilterBar
│   │   ├── <select> for lane filter (All Lanes + 7 options)
│   │   └── <input type="text"> for name/ID search
│   ├── KanbanBoard
│   │   └── LaneColumn × 7 (one per lane, only shows matching projects)
│   │       └── ProjectCard × N
│   │           ├── ID chip (font-mono, small, lane-colored border)
│   │           ├── Name (semibold)
│   │           ├── Summary (text-os-text/60, 2-line truncate)
│   │           ├── Priority chip (P1/P2/P3 color)
│   │           ├── Budget badge (XS/S/M/L/XL)
│   │           ├── Branch (GitBranch icon, font-mono, truncated if long)
│   │           └── PR link (ExternalLink icon — only if pr !== null)
│   └── LoadingState / ErrorState / EmptyState (conditional render)
```

### Key implementation notes

1. **No drag-and-drop (v1)**: Cards are read-only. Lane advancement is done via git
   (updating `data/projects.json`). This is intentional: the source of truth is the
   JSON file in version control, not a UI state.

2. **Horizontal scroll**: The 7-column board will overflow on small screens.
   Wrap the board in `overflow-x-auto` and give each column `min-w-[240px] w-64`.

3. **Column counts**: Show badge count `(N)` next to each lane name.

4. **Fetch pattern** (mirrors Conky.tsx):
   ```typescript
   useEffect(() => {
     fetch('/api/projects')
       .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
       .then((data: Project[]) => { setProjects(data); setLoading(false); })
       .catch(err => { setError(err.message); setLoading(false); });
   }, []);
   ```

5. **Filter logic** (derived, no useEffect needed):
   ```typescript
   const filtered = projects.filter(p => {
     const matchLane = !laneFilter || p.lane === laneFilter;
     const q = searchQuery.toLowerCase();
     const matchSearch = !q || p.name.toLowerCase().includes(q) || p.id.includes(q);
     return matchLane && matchSearch;
   });
   ```

6. **Loading/Error state** (mirrors AgentChat.tsx pattern): show centered spinner
   with `<Loader2 className="animate-spin" />` during load; show `<AlertTriangle />`
   on error with message.

---

## Research Area 3 — `data/projects.json` Schema Design

### Proposed JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Project",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "name", "lane", "summary", "priority", "budget_tier"],
    "properties": {
      "id":          { "type": "string", "pattern": "^prj[0-9]{7}$" },
      "name":        { "type": "string" },
      "lane":        { "type": "string", "enum": ["Ideas","Discovery","Design","In Sprint","Review","Released","Archived"] },
      "summary":     { "type": "string" },
      "branch":      { "type": ["string", "null"] },
      "pr":          { "type": ["integer", "null"], "description": "PR number (integer)" },
      "priority":    { "type": "string", "enum": ["P1","P2","P3","P4"] },
      "budget_tier": { "type": "string", "enum": ["XS","S","M","L","XL","unknown"] },
      "tags":        { "type": "array", "items": { "type": "string" } },
      "created":     { "type": "string", "format": "date" },
      "updated":     { "type": "string", "format": "date" }
    }
  }
}
```

### Budget tier semantics

| Tier | Scope | Examples |
|---|---|---|
| XS | < 1 working day (hours) | Bug fix, config tweak, doc update |
| S | 1–2 working days | Small feature, single agent update |
| M | 3–5 working days | Medium feature (default for merged projects) |
| L | 1–2 working weeks | Multi-component feature |
| XL | Full sprint (2 weeks+) | Major system-wide feature |
| unknown | Not yet estimated | Ideas lane only |

### Schema evaluation

The proposed schema is correct. Three minor adjustments recommended:

1. **`pr` should be `integer | null`** (not a string like `"#136"`), so the UI can
   construct the PR URL deterministically: `https://github.com/…/pull/{pr}`.
2. **Add `created` and `updated` ISO date fields** for sort/freshness display.
3. **Add `tags: string[]`** (optional) for future filtering by technology area.

### Complete project classification table

All 62 entries (prj0000001–prj0000052 + 10 idea placeholders prj0000053–prj0000062):

#### Released (48 entries)

| ID | Name | Branch | PR | Priority | Budget |
|---|---|---|---|---|---|
| prj0000001 | Async Runtime | merged | — | P3 | M |
| prj0000002 | Core System | merged | — | P3 | M |
| prj0000003 | Hybrid LLM Security | merged | — | P3 | M |
| prj0000004 | LLM Context Consolidation | merged | — | P3 | M |
| prj0000005 | LLM Swarm Architecture | merged | — | P3 | M |
| prj0000006 | Unified Transaction Manager | merged | — | P3 | M |
| prj0000007 | Advanced Research | merged | — | P3 | M |
| prj0000008 | Agent Workflow | merged | — | P3 | M |
| prj0000009 | Community Collaboration | merged | — | P3 | M |
| prj0000010 | Context Management | merged | — | P3 | M |
| prj0000011 | Core Project Structure | merged | — | P3 | M |
| prj0000012 | Deployment Operations | merged | — | P3 | M |
| prj0000013 | Dev Tools Autonomy | merged | — | P3 | M |
| prj0000014 | Dev Tools Capabilities | merged | — | P3 | M |
| prj0000015 | Dev Tools Implementation | merged | — | P3 | M |
| prj0000016 | Dev Tools Structure | merged | — | P3 | M |
| prj0000017 | Dev Tools Utilities | merged | — | P3 | M |
| prj0000018 | Documentation Assets | merged | — | P3 | M |
| prj0000019 | Future Roadmap | merged | — | P3 | S |
| prj0000020 | GitHub Import | merged | — | P3 | M |
| prj0000021 | Project Management Governance | merged | — | P3 | M |
| prj0000022 | External Repos Tracking | merged | — | P3 | S |
| prj0000023 | Naming Standards | merged | — | P3 | S |
| prj0000024 | Code of Conduct | merged | — | P3 | XS |
| prj0000025 | Contributing Guide | merged | — | P3 | S |
| prj0000026 | Architecture ADR Template | merged | — | P3 | S |
| prj0000027 | Onboarding Docs | merged | — | P3 | S |
| prj0000028 | API Reference | merged | — | P3 | S |
| prj0000029 | Performance Docs | merged | — | P3 | S |
| prj0000030 | Standards: Code Style | merged | — | P3 | XS |
| prj0000031 | Standards: Commit Style | merged | — | P3 | XS |
| prj0000032 | Standards: Test Style | merged | — | P3 | XS |
| prj0000033 | Standards: Security | merged | — | P3 | S |
| prj0000034 | Standards: Docs | merged | — | P3 | XS |
| prj0000035 | Standards: CI | merged | — | P3 | S |
| prj0000036 | Standards: Release | merged | — | P3 | XS |
| prj0000037 | Tools CRDT Security | merged | — | P3 | M |
| prj0000038 | Project Management | merged | — | P3 | M |
| prj0000039 | Conftest Typing Fixes | merged | — | P3 | S |
| prj0000040 | FLM Integration | merged | — | P3 | M |
| prj0000041 | FLM Benchmark | merged | — | P3 | M |
| prj0000042 | Agent Workflow Polish | merged | — | P3 | S |
| prj0000045 | Transaction Managers Full | merged | 137 | P2 | L |
| prj0000047 | Conky Real Metrics | merged | 185 | P2 | M |
| prj0000048 | Taskbar Config | merged | 186 | P2 | S |
| prj0000049 | Dependabot Security Fixes | merged | 187 | P2 | S |
| prj0000050 | Install Script | merged | 188 | P2 | S |
| prj0000051 | README Update | merged | 189 | P2 | M |

#### Review (2 entries)

| ID | Name | Branch | PR | Priority | Budget |
|---|---|---|---|---|---|
| prj0000043 | P2P Security Deps | prj0000043-p2p-security-deps | open | P2 | M |
| prj0000044 | Transaction Manager Stubs | prj0000044-transaction-managers-stubs | 136 | P2 | S |

#### In Sprint (1 entry)

| ID | Name | Branch | PR | Priority | Budget |
|---|---|---|---|---|---|
| prj0000052 | Project Management | prj0000052-project-management | null | P2 | L |

#### Archived (1 entry)

| ID | Name | Branch | PR | Priority | Budget |
|---|---|---|---|---|---|
| prj0000046 | FLM TPS Benchmark | prj0000046-flm-tps-benchmark | null | P3 | M |

#### Ideas (10 entries — prj0000053–prj0000062)

| ID | Name | Summary | Priority | Budget |
|---|---|---|---|---|
| prj0000053 | HMAC Webhook Verification | Secure GitHub webhook payloads with HMAC-SHA256 signature validation in `src/github_app.py` | P4 | unknown |
| prj0000054 | Backend Authentication | Add API-key or JWT authentication to all REST and WebSocket endpoints | P4 | unknown |
| prj0000055 | WebSocket E2E Encryption | Wire the documented E2E encryption architecture into production WebSocket transport using the Noise_XX protocol | P4 | unknown |
| prj0000056 | Rust async-transport Activation | Enable `async-transport` feature in `rust_core` to activate QUIC-over-Tokio for faster inter-agent messaging | P4 | unknown |
| prj0000057 | Agent Orchestration Graph | Visual DAG panel in NebulaOS showing live task flow and agent status across all 10 pipeline stages | P4 | unknown |
| prj0000058 | Mobile-Responsive NebulaOS | Add CSS responsive breakpoints and touch-friendly interaction patterns to the NebulaOS shell | P4 | unknown |
| prj0000059 | Plugin Marketplace Browser | In-NebulaOS panel for discovering, installing, and managing third-party agent plugins | P4 | unknown |
| prj0000060 | FLM Token Throughput Dashboard | Real-time tokens-per-second charts fed from FLM telemetry in NebulaOS | P4 | unknown |
| prj0000061 | Theme System | Light mode and retro terminal theme for NebulaOS with theme selector and persisted preference | P4 | unknown |
| prj0000062 | Live Agent Execution in CodeBuilder | Wire the 10-agent pipeline to CodeBuilder UI with streaming per-agent log output and progress indicators | P4 | unknown |

---

## Research Area 4 — FastAPI `GET /api/projects` Endpoint Design

### Existing patterns (from backend/app.py analysis)

| Pattern | Where used | How to replicate |
|---|---|---|
| Module-level state variable | `_prev_net`, `_prev_disk` | `_PROJECTS: list[ProjectModel] = []` |
| Load from file at startup | Agent logs loaded on first request | Load `data/projects.json` at module level via `_load_projects()` called once |
| `Path(_PROJECT_ROOT / ...)` | All path construction | `_PROJECTS_FILE = _PROJECT_ROOT / "data" / "projects.json"` |
| Pydantic `BaseModel` | `SystemMetricsResponse`, `NetworkInterface` | `class ProjectModel(BaseModel)` |
| HTTP 500 via `HTTPException` | Pattern used throughout | `raise HTTPException(status_code=500, detail="...")` |
| `response_model=...` | `/api/metrics/system` | `response_model=list[ProjectModel]` |

### Proposed endpoint design

```python
# ── Project models ────────────────────────────────────────────────────────
from typing import Literal, Optional

Lane = Literal["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
Priority = Literal["P1", "P2", "P3", "P4"]
BudgetTier = Literal["XS", "S", "M", "L", "XL", "unknown"]

class ProjectModel(BaseModel):
    """Single project entry from data/projects.json."""
    id: str
    name: str
    lane: Lane
    summary: str
    branch: Optional[str] = None
    pr: Optional[int] = None
    priority: Priority
    budget_tier: BudgetTier
    tags: list[str] = []
    created: Optional[str] = None
    updated: Optional[str] = None

# Module-level cache loaded once at startup
_PROJECTS_FILE = _PROJECT_ROOT / "data" / "projects.json"

def _load_projects() -> list[ProjectModel]:
    """Load and validate data/projects.json; returns empty list on error."""
    if not _PROJECTS_FILE.exists():
        logger.warning("data/projects.json not found at %s", _PROJECTS_FILE)
        return []
    raw = json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    return [ProjectModel(**entry) for entry in raw]

_PROJECTS: list[ProjectModel] = _load_projects()

@app.get("/api/projects", response_model=list[ProjectModel])
async def get_projects(lane: Optional[str] = None) -> list[ProjectModel]:
    """Return all projects, optionally filtered by lane."""
    if not _PROJECTS and not _PROJECTS_FILE.exists():
        raise HTTPException(status_code=500, detail="data/projects.json not found")
    if lane:
        return [p for p in _PROJECTS if p.lane == lane]
    return _PROJECTS
```

### Design decisions

1. **Module-level load (not async)**: The file is small (<50 KB). Loading at module
   import time (not on first request) avoids race conditions in concurrent startup.
   Pattern is consistent with `_FILTERED_PREFIXES` and `_VALID_AGENT_IDS`.

2. **Optional `?lane=` query parameter**: Avoids multiple endpoints. Consistent with
   REST filtering convention already used by the frontend filter bar.

3. **Validation via Pydantic**: `ProjectModel(**entry)` will raise `ValidationError`
   if any entry has an invalid `lane` enum value. This should be caught during startup
   and logged as a warning rather than crashing the app.

4. **No authentication**: Explicitly out of scope for v1 (project.md § Out of scope).
   The allowlist in `_VALID_AGENT_IDS` pattern is not applicable here.

5. **Error handling**: HTTP 500 only if the file is missing. Malformed entries should
   be soft-skipped with a warning log, not a 500.

---

## Research Area 5 — Agent File Updates

### `.github/agents/0master.agent.md` — proposed minimal additions

Location: Add a new subsection to the **"Where to find key information"** section,
under `### Core documentation and planning`:

```markdown
### Project lifecycle board
- `docs/project/kanban.md` — live Kanban board (source of truth for all project stages)
  - Read this before allocating a new `prjNNNNNNN` to confirm the next available ID.
  - Update this after any lane transition (Ideas→Discovery, Review→Released, etc.).
  - The board is also queryable via `GET /api/projects` in the backend.
```

Add a new rule in **"How the master agent operates"**, after step 3:

```markdown
3a. **Update kanban.md** after allocating a project ID: add the new project to the
    `Ideas` or `Discovery` lane table in `docs/project/kanban.md` and commit the
    change on the project branch.
```

Add to **"Delegation preflight branch gate"**, step 5 (before delegating to @1project):

```markdown
5a. After `@1project` completes and before handing to `@2think`, update the project's
    lane in `docs/project/kanban.md` from `Ideas` → `Discovery`.
```

### `.github/agents/1project.agent.md` — proposed minimal additions

Location: Add a new entry to the **"Project doc conventions"** section:

```markdown
- **Lifecycle board**: `docs/project/kanban.md` is the canonical lane tracking
  artifact for all projects. `@1project` must update this file whenever a project
  moves from Ideas → Discovery (entry) or when its status changes.
```

Add a new step **1a** in the **"Operating procedure"** section (after folder creation):

```markdown
1a. **Update kanban.md**
    - Move the project entry from `Ideas` to `Discovery` in `docs/project/kanban.md`.
    - All new projects default to starting in the `Discovery` lane when `@1project`
      creates the folder (not `Ideas` — Ideas is a pre-project state managed by
      `@0master`).
    - If no entry exists yet, create one in `Discovery` with the assigned prjNNNNNNN,
      name, summary, priority, and budget_tier.
    - Commit this kanban.md update on the project-specific branch.
```

### Why these are the minimal changes

Both agent files are large and complex. The additions above are **additive only** —
they introduce a new section and a new step without changing any existing rules or
removing any content. The behavioral impact is:
- `@0master` now has a documented step to maintain kanban.md on allocation and
  lane transition.
- `@1project` now has a documented step to update kanban.md on project creation.
- No other behavioral changes (the 10-agent pipeline, branch governance, and
  project numbering rules remain unchanged).

---

## Research Area 6 — `docs/project/kanban.md` Final Format

### Proposed structure

```markdown
# PyAgent Project Kanban Board

_Last updated: YYYY-MM-DD | Total projects: N_

## How to use this board

This file is the **single source of truth** for all PyAgent projects (past, present,
and future). It is maintained in source control and updated on every lane transition.

### Lanes
| Lane | Meaning | Agent Owner |
|---|---|---|
| Ideas | Proposed, not yet scoped | @0master |
| Discovery | Options exploration in progress (@2think) | @1project + @2think |
| Design | Architecture selected, design in progress (@3design) | @3design |
| In Sprint | Active implementation (@4plan–@6code) | @4plan–@6code |
| Review | PR open, awaiting merge | @9git |
| Released | Merged to main | — |
| Archived | Stalled, cancelled, or superseded | @0master decision |

### How to advance a project
1. Update `data/projects.json` — change the `lane` field to the new lane.
2. Update `docs/project/kanban.md` — move the row to the correct section.
3. Commit both files on the project-specific branch.
4. `@0master` must confirm lane changes for Ideas → Discovery (new projects).

### Governance rules
- `@0master` owns the project ID (`prjNNNNNNN`) namespace.
- IDs are never reused, even if a project is Archived.
- Ideas placeholders use real IDs allocated by `@0master`.
- Budget and priority must be confirmed before leaving Ideas.

---

## Ideas

Projects proposed but not yet formally scoped.

| ID | Name | Summary | Priority | Budget | Updated |
|---|---|---|---|---|---|
| prj0000053 | HMAC Webhook Verification | … | P4 | unknown | 2026-03-24 |
…

## Discovery

Active options exploration — @2think is working.

| ID | Name | Summary | Branch | Priority | Budget | Updated |
|---|---|---|---|---|---|---|

## Design

@3design producing authoritative design.

| ID | Name | Summary | Branch | Priority | Budget | Updated |
|---|---|---|---|---|---|---|

## In Sprint

Active implementation.

| ID | Name | Summary | Branch | Priority | Budget | Updated |
|---|---|---|---|---|---|---|
| prj0000052 | Project Management | Kanban board + ProjectManager app + /api/projects | prj0000052-project-management | P2 | L | 2026-03-24 |

## Review

PR open, waiting for merge.

| ID | Name | Summary | Branch | PR | Priority | Budget | Updated |
|---|---|---|---|---|---|---|---|
| prj0000043 | P2P Security Deps | libp2p 0.49→0.56, 6 CVE fixes | prj0000043-p2p-security-deps | open | P2 | M | 2026-03-24 |
| prj0000044 | Transaction Manager Stubs | CI stubs for missing tx managers | prj0000044-transaction-managers-stubs | #136 | P2 | S | 2026-03-24 |

## Released

All 48 projects merged to main.

| ID | Name | Summary | Branch | PR | Priority | Budget | Updated |
|---|---|---|---|---|---|---|---|
| prj0000001 | Async Runtime | Tokio-backed async helpers | merged | — | P3 | M | 2026-03-24 |
…

## Archived

Stalled, cancelled, or superseded.

| ID | Name | Summary | Reason | Priority | Budget | Updated |
|---|---|---|---|---|---|---|
| prj0000046 | FLM TPS Benchmark | Per-provider tokens/sec metrics | FLM server offline | P3 | M | 2026-03-24 |

---

## Summary Metrics

| Lane | Count |
|---|---|
| Ideas | 10 |
| Discovery | 0 |
| Design | 0 |
| In Sprint | 1 |
| Review | 2 |
| Released | 48 |
| Archived | 1 |
| **Total** | **62** |
```

### Format decisions

1. **One H2 per lane**: Enables `## Released` anchor links from PR descriptions and
   agent prompts.
2. **Review lane has extra PR column**: Only this lane regularly has an open PR number.
   Released uses it for the merged PR number (historical reference).
3. **Archived has Reason column** instead of Branch: The branch is long gone; the
   reason for archival is more useful.
4. **Summary Metrics footer**: Gives a quick count without scrolling the full file.
5. **Instructions at top**: Needed because this file will be read cold by agents who
   haven't seen it before.

---

## Options

### Option A — Minimal v1 (read-only Kanban, static JSON, no drag-and-drop)
**Description**: Implement exactly what is specified. `kanban.md` is the source of truth.
`data/projects.json` is a static file maintained by hand/agent in git. `ProjectManager.tsx`
is read-only (no UI mutations). Endpoint is a simple file-read.

**Pros**:
- Lowest complexity; shortest path to working UI.
- Source of truth stays in git — version-controlled, diffable, PR-reviewed.
- No database, no auth, no migration risk.
- Fully reversible: no schema migration needed to add features later.

**Cons**:
- Lane advancement requires manual JSON edit + kanban.md update + commit.
- No real-time updates (must refresh browser to see changes).
- Cannot sort/reorder cards in the UI.

### Option B — Editable Kanban with PATCH endpoint
**Description**: Add a `PATCH /api/projects/{id}` endpoint that updates `data/projects.json`
on disk. The UI adds a lane-advancement dropdown on each card.

**Pros**:
- Better UX: lane changes happen in the browser.
- Agents can call the API directly to advance a project.

**Cons**:
- Requires file-write logic in backend (concurrency risk on simultaneous writes).
- Breaks the "git is source of truth" principle — UI changes bypass PR review.
- Out of scope per project.md: "No drag-and-drop in v1 (read-only Kanban; lane changes go via git)".
- Increases test surface significantly.

### Option C — Database-backed Kanban
**Description**: Store projects in SQLite; expose full CRUD API.

**Pros**: Best runtime query performance; enables filtering at the DB level.

**Cons**: 
- Requires migration tooling, schema versioning, and backup strategy.
- Explicitly out of scope (project.md: "no DB").
- Massively overengineered for 62 projects.

---

## Decision Matrix

| Criterion | Option A (Static) | Option B (PATCH) | Option C (DB) |
|---|---|---|---|
| Complexity | Low ✓ | Medium | High ✗ |
| In scope | Yes ✓ | Partial | No ✗ |
| Git-first | Yes ✓ | No | No ✗ |
| Implementation risk | Very low ✓ | Medium | High ✗ |
| Reversibility | High ✓ | Medium | Low ✗ |
| UX (read-only acceptable) | Yes ✓ | Better | Best |
| Maintenance overhead | Minimal ✓ | Medium | High ✗ |

---

## Recommendation

**Option A — Minimal v1 (read-only Kanban, static JSON)**

The project.md acceptance criteria, scope boundaries, and explicit out-of-scope items
all point to Option A. The read-only kanban is not a limitation in this context—it is a
design feature: all lane transitions are git commits, which means they are reviewed,
attributable, and reversible. The backend endpoint is a straightforward file-read pattern
fully consistent with the existing `app.py` code.

@3design should proceed with Option A and design:
1. The exact `data/projects.json` structure (use the schema above).
2. The `ProjectModel` Pydantic class for `backend/app.py`.
3. The `ProjectManager.tsx` component tree (use the architecture above).
4. The `docs/project/kanban.md` markdown (use the format template above).
5. The minimal diff for `0master.agent.md` and `1project.agent.md`.

---

## Open Questions for @3design

1. **Tailwind CSS variable availability**: Are the `os-*` CSS variables (`bg-os-bg`,
   `bg-os-window`, etc.) defined in the Tailwind config or in a CSS file? @3design
   should verify in `web/tailwind.config.*` or `web/src/index.css` before writing
   the ProjectManager styles.

2. **NebulaOS app registration**: `AgentChat.tsx` is registered as an app in the
   NebulaOS shell. Where is this registry? (@3design should check `web/src/` for a
   `apps.ts` or `appRegistry` pattern and add `ProjectManager` there.)

3. **PR number for prj0000043**: The project brief says "PR open" but no number.
   @3design should check the current open PRs to fill in the exact number before
   writing `data/projects.json`.

4. **Project folder names**: Some older projects (prj0000001–prj0000042) may not have
   `docs/project/prjNNNNNNN/` folders at all — they may predate the folder convention.
   For `data/projects.json`, the `branch` field should be `"merged"` (a sentinel value)
   and `pr` should be `null` for these. @3design should decide on the sentinel value.

5. **`created` dates**: The actual creation dates for prj0000001–prj0000042 are not
   available in the brief. @3design should use `"2026-01-01"` as a synthetic placeholder
   for all merged projects and note it in the project plan.

6. **Test coverage requirement**: The project.md includes `tests/structure/test_project_manager.py`
   as a deliverable. @5test should define what structural tests are needed (e.g., validate
   that `data/projects.json` parses correctly, that all lane values are valid, that all
   IDs match the `prjNNNNNNN` pattern).

