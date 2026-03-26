# pm-swot-risk-ui — Code Artifacts

_Status: HANDED_OFF_
_Coder: @6code | Updated: 2026-03-26_

## Implementation Summary
Implemented SWOT Analysis and Risk Register toolbar buttons in ProjectManager.
- T1: Created `web/vite-env.d.ts` with `/// <reference types="vite/client" />` to enable `?raw` Vite imports.
- T2: Added `BarChart2` to lucide-react imports and `kanbanRaw` import from `docs/project/kanban.md?raw`.
- T3: Added `extractSection(raw, heading)` pure helper above FilterBar.
- T4: Added `sectionModal` state (`null | 'swot' | 'risk'`) with Escape key handler via `useEffect`.
- T5: Extended `FilterBarProps` with `onSwot`/`onRisk`, destructured in FilterBar, added SWOT + Risk buttons before `+ New`, updated call site.
- T6: Added modal overlay JSX (backdrop click + stopPropagation) rendering `extractSection` content.
- T7: Created `web/apps/ProjectManager.test.tsx` with 3 Vitest unit tests for `extractSection`.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `web/vite-env.d.ts` | Created | +2 |
| `web/apps/ProjectManager.tsx` | Modified | +70/-13 |
| `web/apps/ProjectManager.test.tsx` | Created | +30 |

## Test Run Results
```
Not run by @6code — @7exec responsibility.
```

## Deferred Items
None.
