# pm-swot-risk-ui — Implementation Plan

_Status: HANDED_OFF_
_Planner: @4plan | Updated: 2026-03-26_

## Overview

Add **SWOT Analysis** and **Risk Register** toolbar buttons to the `ProjectManager`
`FilterBar`. Each button opens an in-app modal overlay displaying the corresponding
section sliced from `docs/project/kanban.md`, bundled at build time via Vite's native
`?raw` import.

**Design choice: Option C — `?raw` static import + inline modal**

Rationale confirmed by source inspection (2026-03-26):
- `ProjectManager` has **zero** props; no `openApp` is passed to it.
- `Editor` has **zero** props and no way to receive content or an anchor.
- Threading a callback through `App.tsx → ProjectManager → FilterBar` is two files of
  unrelated churn for an S-budget ticket.
- Option C is self-contained in one component file. Vite supports `?raw` natively — no
  plugin or `assetsInclude` config needed (Vite ≥ 2.x).
- `no react-markdown` in `web/package.json`; `<pre>` rendering is acceptable for S tier.

**Files changed:**
| File | Change type |
|---|---|
| `web/vite-env.d.ts` | **new** — TypeScript declaration for Vite `?raw` imports |
| `web/apps/ProjectManager.tsx` | **modified** — `?raw` import, helper, state, buttons, modal |
| `web/apps/ProjectManager.test.tsx` | **new** — Vitest unit + smoke tests |

**Files NOT changed:** `web/App.tsx`, `web/apps/Editor.tsx`, `web/types.ts`,
`web/vite.config.ts`, any Python/backend file.

---

## Source-read findings

### kanban.md heading locations (confirmed)
- `## Risk Register` — line 196
- `## SWOT Analysis` — line 210
- Next `## ` after SWOT Analysis: `## Future Ideas` — used as the stop sentinel in
  `extractSection`.

### FilterBar current state (confirmed)
`FilterBarProps` has: `selectedLane`, `onLaneChange`, `searchQuery`, `onSearchChange`,
`onNew`. The two new callbacks (`onOpenSwot`, `onOpenRisk`) will be added.

`FilterBar` renders: lane pill buttons · search input · `+ New` button.
New buttons go **after** `+ New` in the same flex row.

### Lucide icons available (confirmed)
`AlertTriangle` is already imported in `ProjectManager.tsx`.
`BarChart2` must be added to the lucide-react import line (it is in lucide-react ≥ 0.x).

### TypeScript / Vite `?raw` support (confirmed gap)
`web/tsconfig.json` has `"moduleResolution": "bundler"` but no `vite/client` reference.
`web/vite-env.d.ts` does **not** exist. Without `/// <reference types="vite/client" />`
TypeScript will error on `import foo from '...?raw'`. T1 fixes this.

---

## Task List

- [ ] T1 — `web/vite-env.d.ts` (new) — TypeScript `?raw` declaration
- [ ] T2 — `web/apps/ProjectManager.tsx` — Add `?raw` import + `BarChart2` icon import
- [ ] T3 — `web/apps/ProjectManager.tsx` — Add `extractSection` pure helper function
- [ ] T4 — `web/apps/ProjectManager.tsx` — Add `sectionModal` state to `ProjectManager`
- [ ] T5 — `web/apps/ProjectManager.tsx` — Extend `FilterBarProps` + add SWOT/Risk buttons
- [ ] T6 — `web/apps/ProjectManager.tsx` — Add modal JSX + Escape key handler
- [ ] T7 — `web/apps/ProjectManager.test.tsx` (new) — Vitest unit + smoke tests

---

## Detailed Tasks

### T1 — `web/vite-env.d.ts` (new file)

**File:** `web/vite-env.d.ts`  
**Change type:** Create new file

**Content:**
```ts
/// <reference types="vite/client" />
```

**Why:** `vite/client` declares the `?raw` query suffix as returning `string`, and
`?url` as returning `string`. Without it, TypeScript sees `import x from '...?raw'`
as a module with an unknown default export and raises `TS2307`.

**Acceptance check:**
- `cd web && npx tsc --noEmit` produces no error on the `?raw` import line.
- Alternatively, `npm run build` in `web/` succeeds.

---

### T2 — `?raw` import + `BarChart2` icon

**File:** `web/apps/ProjectManager.tsx`  
**Change type:** Modify import block (top of file)

**Add at line 1 (before or after existing import block), as a module-level import:**
```ts
import kanbanRaw from '../../docs/project/kanban.md?raw';
```

**Modify the existing lucide-react import** to add `BarChart2`:
```ts
import {
  GitBranch, ExternalLink, Search, Loader2, AlertTriangle,
  ChevronDown, ChevronUp, Tag, Pencil, FolderOpen, Plus, X, Check, BarChart2,
} from 'lucide-react';
```

**Why:** `kanbanRaw` provides the full markdown text at build time — no network round
trip, no backend dep. `BarChart2` is the SWOT chart icon.

**Acceptance check:**
- `npm run build` in `web/` succeeds.
- `typeof kanbanRaw` is `'string'` at runtime (verifiable with `console.log`).
- No TypeScript error.

---

### T3 — `extractSection` helper

**File:** `web/apps/ProjectManager.tsx`  
**Location:** Insert immediately above the `// ── FilterBar` comment line  
**Change type:** Add new pure function

**Implementation:**
```ts
// ── Section extractor ────────────────────────────────────────────────────────

/**
 * Slice one `## Heading` section out of a markdown string.
 * Returns the lines from `## {heading}` up to (but not including) the next `## `.
 */
function extractSection(raw: string, heading: string): string {
  const lines = raw.split('\n');
  const start = lines.findIndex(l => l.trimEnd() === `## ${heading}`);
  if (start === -1) return `Section "${heading}" not found.`;
  const end = lines.findIndex((l, i) => i > start && l.startsWith('## '));
  return (end === -1 ? lines.slice(start) : lines.slice(start, end)).join('\n');
}
```

**Acceptance check:**
- `extractSection(kanbanRaw, 'SWOT Analysis')` returns a string that:
  - Starts with `## SWOT Analysis`
  - Contains `| **Internal** |`
  - Does **not** contain `## Future Ideas`
- `extractSection(kanbanRaw, 'Risk Register')` returns a string starting with
  `## Risk Register` and containing `RSK-001`.
- `extractSection('', 'Nonexistent')` returns `'Section "Nonexistent" not found.'`

---

### T4 — `sectionModal` state

**File:** `web/apps/ProjectManager.tsx`  
**Location:** Inside `ProjectManager` component, after existing `useState` declarations  
**Change type:** Add one `useState` line

**Implementation:**
```ts
const [sectionModal, setSectionModal] = useState<'swot' | 'risk' | null>(null);
```

**Why:** Controls which modal (if any) is currently visible. `null` = no modal.

**Acceptance check:**
- Component renders without error with `sectionModal` initialized as `null`.
- No TypeScript error.

---

### T5 — `FilterBarProps` extension + SWOT / Risk buttons

**File:** `web/apps/ProjectManager.tsx`  
**Change type:** Modify interface + component

**Step 5a — Extend `FilterBarProps`:**
```ts
interface FilterBarProps {
  selectedLane: Lane | null;
  onLaneChange: (lane: Lane | null) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onNew: () => void;
  onOpenSwot: () => void;
  onOpenRisk: () => void;
}
```

**Step 5b — Destructure the new props in `FilterBar`:**
```ts
const FilterBar: React.FC<FilterBarProps> = ({
  selectedLane, onLaneChange, searchQuery, onSearchChange, onNew,
  onOpenSwot, onOpenRisk,
}) => (
```

**Step 5c — Add two buttons immediately after the `+ New` button in `FilterBar` JSX:**
```tsx
<button
  onClick={onOpenSwot}
  title="SWOT Analysis"
  className="flex items-center gap-1 text-[10px] px-2 py-1.5 border border-os-border
             rounded hover:border-os-accent text-os-text/70 hover:text-os-text"
>
  <BarChart2 size={11} /> SWOT
</button>
<button
  onClick={onOpenRisk}
  title="Risk Register"
  className="flex items-center gap-1 text-[10px] px-2 py-1.5 border border-os-border
             rounded hover:border-amber-400 text-os-text/70 hover:text-amber-400"
>
  <AlertTriangle size={11} /> Risk
</button>
```

**Step 5d — Pass the new props at the `<FilterBar />` call site inside `ProjectManager`:**
```tsx
<FilterBar
  selectedLane={selectedLane}
  onLaneChange={setSelectedLane}
  searchQuery={searchQuery}
  onSearchChange={setSearchQuery}
  onNew={() => setEditTarget('new')}
  onOpenSwot={() => setSectionModal('swot')}
  onOpenRisk={() => setSectionModal('risk')}
/>
```

**Acceptance check:**
- Two new buttons labeled "SWOT" and "Risk" are visible in the `FilterBar`.
- Clicking "SWOT" sets `sectionModal` to `'swot'`; clicking "Risk" sets it to `'risk'`.
- TypeScript: no `TS2339` or `TS2345` errors.
- No regressions to existing lane pills, search input, or `+ New` button.

---

### T6 — Modal JSX + Escape key handler

**File:** `web/apps/ProjectManager.tsx`  
**Location:** Inside `ProjectManager` return JSX, after the `{editTarget !== null && ...}` block  
**Change type:** Add state effect + modal overlay markup

**Step 6a — Add Escape key handler** (alongside other `useEffect` hooks in `ProjectManager`):
```ts
useEffect(() => {
  if (!sectionModal) return;
  const handleKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setSectionModal(null); };
  window.addEventListener('keydown', handleKey);
  return () => window.removeEventListener('keydown', handleKey);
}, [sectionModal]);
```

**Step 6b — Add modal overlay** (after the `EditModal` block in the return JSX):
```tsx
{sectionModal !== null && (
  <div
    className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
    onClick={() => setSectionModal(null)}
  >
    <div
      className="relative bg-os-window border border-os-border rounded-lg shadow-2xl
                 w-[min(90vw,760px)] max-h-[80vh] flex flex-col"
      onClick={e => e.stopPropagation()}
    >
      <div className="flex items-center justify-between px-4 py-2 border-b border-os-border">
        <span className="text-sm font-semibold text-os-text">
          {sectionModal === 'swot' ? '📊 SWOT Analysis' : '⚠️ Risk Register'}
        </span>
        <button
          onClick={() => setSectionModal(null)}
          className="text-os-text/50 hover:text-os-text transition-colors"
          aria-label="Close"
        >
          <X size={16} />
        </button>
      </div>
      <pre className="flex-1 overflow-auto p-4 text-[11px] font-mono text-os-text
                      leading-relaxed whitespace-pre-wrap break-words">
        {extractSection(
          kanbanRaw,
          sectionModal === 'swot' ? 'SWOT Analysis' : 'Risk Register'
        )}
      </pre>
    </div>
  </div>
)}
```

**Acceptance check:**
- Clicking "SWOT" shows modal with title "📊 SWOT Analysis" and text starting with
  `## SWOT Analysis`.
- Clicking "Risk" shows modal with title "⚠️ Risk Register" and text starting with
  `## Risk Register`.
- `X` button dismisses modal.
- Clicking backdrop (outside modal box) dismisses modal.
- Pressing `Escape` dismisses modal.
- Modal does not appear when `sectionModal === null`.
- No layout shift to existing kanban board behind the modal.

---

### T7 — `web/apps/ProjectManager.test.tsx` (new test file)

**File:** `web/apps/ProjectManager.test.tsx`  
**Change type:** Create new file

**Tests to implement:**

**Suite 1 — `extractSection` pure function (no DOM)**
```ts
describe('extractSection', () => {
  const sample = '# Title\n\n## Alpha\ncontent a\n\n## Beta\ncontent b\n\n## Gamma\nend';
  it('returns the correct section slice', () => {
    expect(extractSection(sample, 'Beta')).toBe('## Beta\ncontent b\n');
  });
  it('handles missing heading gracefully', () => {
    expect(extractSection(sample, 'Delta')).toBe('Section "Delta" not found.');
  });
  it('returns to end of string when no subsequent heading', () => {
    expect(extractSection(sample, 'Gamma')).toBe('## Gamma\nend');
  });
});
```

Note: `extractSection` must be exported (or tested via a barrel re-export) for this
suite to work WITHOUT rendering the component.  
**If `@6code` keeps it as a module-level function (not exported)**, move suite 1 into
the render-based suite and test it implicitly through the modal content.

**Suite 2 — Render smoke (SWOT + Risk buttons visible)**
```ts
describe('ProjectManager FilterBar buttons', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [],
    } as unknown as Response));
  });
  afterEach(() => vi.unstubAllGlobals());

  it('renders SWOT and Risk buttons', async () => {
    render(<ProjectManager />);
    expect(await screen.findByTitle('SWOT Analysis')).toBeInTheDocument();
    expect(screen.getByTitle('Risk Register')).toBeInTheDocument();
  });
});
```

**Suite 3 — Modal interaction**
```ts
  it('shows SWOT modal on SWOT button click', async () => {
    render(<ProjectManager />);
    await screen.findByTitle('SWOT Analysis');     // wait for load
    await userEvent.click(screen.getByTitle('SWOT Analysis'));
    expect(screen.getByText(/📊 SWOT Analysis/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Close' })).toBeInTheDocument();
  });

  it('dismisses modal on close button click', async () => {
    render(<ProjectManager />);
    await screen.findByTitle('SWOT Analysis');
    await userEvent.click(screen.getByTitle('SWOT Analysis'));
    await userEvent.click(screen.getByRole('button', { name: 'Close' }));
    expect(screen.queryByText(/📊 SWOT Analysis/)).not.toBeInTheDocument();
  });
```

**Acceptance check (all suites):**
- `cd web && npm test -- --reporter=verbose` exits 0.
- All 5+ tests pass.
- No TypeScript errors in the test file.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | TypeScript `?raw` support | T1 | |
| M2 | Data layer (import + helper) | T2, T3 | |
| M3 | State + buttons | T4, T5 | |
| M4 | Modal UI | T6 | |
| M5 | Tests green | T7 | |

---

## Dependency order

```
T1 (vite-env.d.ts)
  └─▶ T2 (?raw import — needs T1 for TS to accept it)
        └─▶ T3 (extractSection — depends on kanbanRaw being importable)
              ├─▶ T4 (state — independent but logically after T3)
              │     └─▶ T5 (buttons — needs sectionModal from T4)
              │           └─▶ T6 (modal JSX — needs T3 + T5)
              │                 └─▶ T7 (tests — verify T2–T6 end-to-end)
              └─▶ T7 (suite 1: pure function test, depends on T3 only)
```

All 7 tasks target a single sprint. No chunked plan files needed at S budget.

---

## Constraints (repeated from project brief)

- No new npm packages
- No backend changes
- No prop threading through `App.tsx`
- Line length ≤ 120 chars (project convention)
- PascalCase filenames; standard React + TypeScript style

---

## Validation Commands

```powershell
# Run Python structure tests (must stay green)
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest tests/structure/ -x -q

# Run web unit tests
Set-Location c:\Dev\PyAgent\web
npm test -- --reporter=verbose

# TypeScript check
npx tsc --noEmit

# Vite build smoke
npm run build
```
