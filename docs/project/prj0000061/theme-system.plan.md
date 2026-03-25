# theme-system — Task Plan

_Owner: @4plan | Updated: 2026-03-25_

## Task Breakdown

| # | Task | File | Status |
|---|---|---|---|
| T-01 | Create web/styles/ directory | filesystem | DONE |
| T-02 | Create themes.css with :root, [data-theme=light], [data-theme=retro] | web/styles/themes.css | DONE |
| T-03 | Create useTheme hook | web/hooks/useTheme.ts | DONE |
| T-04 | Create ThemeSelector component | web/components/ThemeSelector.tsx | DONE |
| T-05 | Modify App.tsx — import themes.css + useTheme + ThemeSelector | web/App.tsx | DONE |
| T-06 | Modify index.tsx — import themes.css | web/index.tsx | DONE |
| T-07 | Create test file | tests/test_theme_system.py | DONE |
| T-08 | Run targeted test suite | pytest tests/test_theme_system.py | DONE |
| T-09 | Run full test suite | pytest tests/ | DONE |
| T-10 | Update data/projects.json lane → Review | data/projects.json | DONE |
| T-11 | Update kanban.md — move to Review | docs/project/kanban.md | DONE |
| T-12 | Commit docs artifacts | git | DONE |
| T-13 | Commit code artifacts | git | DONE |
| T-14 | Commit test artifacts | git | DONE |
| T-15 | Push branch & open PR | GitHub | DONE |

## Dependencies

- T-02 must complete before T-05 (import path must exist)
- T-03 must complete before T-04 and T-05 (hook referenced by both)
- T-07 can run in parallel with T-05, T-06
- T-08 depends on T-02..T-07
- T-10, T-11 can run any time after T-09 passes
