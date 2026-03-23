# Plan: prj0000048 — Taskbar Config

_Status: Complete_  
_Planner: @4plan | Updated: 2026-03-23_

---

## Summary

Implements a persistent OS settings system for NebulaOS using a Settings modal accessible from the hamburger dropdown. Introduces the `OsConfig` type and `DEFAULT_OS_CONFIG` constant to `web/types.ts`, adds module-level `loadOsConfig`/`saveOsConfig` helpers and two new state variables to `web/App.tsx`, and wires the `hideTaskbar()` guard to respect the user's pinned-taskbar preference stored in `localStorage` under key `nebula-os-config`.

---

## File Inventory

| File | Exists? | Action |
|------|---------|--------|
| web/App.tsx | Yes | Modify — 9 targeted edits (Tasks 2–10) |
| web/types.ts | Yes | Append — OsConfig interface + DEFAULT_OS_CONFIG (Task 1) |

> **Decision on types.ts:** `web/types.ts` exists at line 27 (ends after the `User` interface). `OsConfig` and `DEFAULT_OS_CONFIG` are appended there per design doc instructions. No new file is created.

---

## Design Doc Coverage Note

The design doc (`taskbar-config.design.md`) is fully specified for Tasks 1–7. It does **not** include the JSX for the Settings button (Task 8) or the Settings modal (Task 9). Both are derived from the think doc (`taskbar-config.think.md`) and the existing dropdown patterns in `App.tsx`. The JSX specified in Tasks 8 and 9 below is the authoritative specification for @6code.

---

## Implementation Tasks

### Task 1 — Append OsConfig and DEFAULT_OS_CONFIG to web/types.ts

- **File:** web/types.ts
- **Edit type:** append
- **Location:** End of file, after the closing `}` of the `User` interface (currently line 27 — the last line of the file).
- **What to add/change:**
  ```typescript
  export interface OsConfig {
    taskbarAlwaysVisible: boolean;
  }

  export const DEFAULT_OS_CONFIG: OsConfig = {
    taskbarAlwaysVisible: false,
  };
  ```
- **Validation:** `web/types.ts` now exports `OsConfig` and `DEFAULT_OS_CONFIG`. No existing exports are modified. TypeScript resolves both symbols from `'./types'`.

---

### Task 2 — Expand ./types import in App.tsx

- **File:** web/App.tsx
- **Edit type:** replace
- **Location:** Line 9 — `import { WindowState, AppId, Theme } from './types';`
- **What to add/change:**
  ```typescript
  import { WindowState, AppId, Theme, OsConfig, DEFAULT_OS_CONFIG } from './types';
  ```
- **Validation:** Both `OsConfig` and `DEFAULT_OS_CONFIG` are imported. No other import lines are touched.

---

### Task 3 — Add Settings and X icons to lucide-react import in App.tsx

- **File:** web/App.tsx
- **Edit type:** replace
- **Location:** Line 11 — the single-line `import { Menu, Monitor, Terminal, Palette, Calculator as CalcIcon, LogOut, Moon, Sun, MonitorPlay, Bot } from 'lucide-react';`
- **What to add/change:** Expand to a multi-line import adding `Settings` and `X`:
  ```typescript
  import {
    Menu, Monitor, Terminal, Palette, Calculator as CalcIcon,
    LogOut, Moon, Sun, MonitorPlay, Bot, Settings, X
  } from 'lucide-react';
  ```
- **Validation:** `Settings` and `X` are importable without TypeScript errors. Both are referenced in Tasks 8 and 9.

---

### Task 4 — Insert loadOsConfig and saveOsConfig module-level helpers in App.tsx

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** After the closing `];` of the `INITIAL_WINDOWS` constant (after line 27 of the current file), immediately before the `export default function App()` declaration.
- **What to add/change:**
  ```typescript
  function loadOsConfig(): OsConfig {
    try {
      const raw = localStorage.getItem('nebula-os-config');
      return raw ? { ...DEFAULT_OS_CONFIG, ...JSON.parse(raw) } : DEFAULT_OS_CONFIG;
    } catch {
      return DEFAULT_OS_CONFIG;
    }
  }

  function saveOsConfig(cfg: OsConfig): void {
    localStorage.setItem('nebula-os-config', JSON.stringify(cfg));
  }
  ```
- **Validation:** Both functions are at module scope (outside the `App` component). `loadOsConfig` returns `OsConfig`; `saveOsConfig` accepts `OsConfig`. No component state closure.

---

### Task 5 — Insert osConfig and settingsOpen state declarations in App.tsx

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** Inside the `App` component body, immediately after the `hideTimeoutRef` declaration:
  `const hideTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);`
- **What to add/change:**
  ```typescript
  const [osConfig, setOsConfig] = useState<OsConfig>(loadOsConfig);
  const [settingsOpen, setSettingsOpen] = useState(false);
  ```
  > **Critical:** `loadOsConfig` is passed as a function **reference** (no parentheses) — React's lazy initializer form. It runs exactly once on mount.
- **Validation:** `osConfig` has type `OsConfig`. `settingsOpen` has type `boolean`. Both are in component scope after `hideTimeoutRef`.

---

### Task 6 — Insert saveOsConfig persistence useEffect in App.tsx

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** After the closing `}, [menuOpen]);` of the existing `useEffect` that calls `showTaskbar`/`hideTaskbar` based on `menuOpen`.
- **What to add/change:**
  ```typescript
  // Persist OS config to localStorage on every change
  useEffect(() => {
    saveOsConfig(osConfig);
  }, [osConfig]);
  ```
- **Validation:** Effect fires on every `osConfig` state update. On first render it writes the loaded (or default) config once to ensure the key is always present.

---

### Task 7 — Update hideTaskbar function body to respect osConfig guard

- **File:** web/App.tsx
- **Edit type:** replace
- **Location:** The `hideTaskbar` function body. Current first line of body: `if (menuOpen) return; // Don't hide if menu is open`
- **What to add/change:** Insert `taskbarAlwaysVisible` guard as the **first** guard, before `menuOpen`:
  ```typescript
  const hideTaskbar = () => {
    if (osConfig.taskbarAlwaysVisible) return; // Don't hide if pinned
    if (menuOpen) return; // Don't hide if menu is open
    hideTimeoutRef.current = setTimeout(() => {
      setIsTaskbarVisible(false);
    }, 2000);
  };
  ```
- **Validation:** When `osConfig.taskbarAlwaysVisible === true`, `hideTaskbar()` returns at the first guard. When `false`, behavior is identical to the current code. The existing `useEffect([menuOpen])` that calls `hideTaskbar()` on menu-close is handled correctly by the new guard without further changes.

---

### Task 8 — Insert Settings button into dropdown JSX

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** Inside the dropdown `<div className="p-2 space-y-1">` block, between the **second** `<div className="h-px bg-os-border my-2" />` separator (the one after the Appearance grid) and the existing Logout `<button>`.
- **What to add/change:**
  ```tsx
  <button
    onClick={() => { setMenuOpen(false); setSettingsOpen(true); }}
    className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors"
  >
    <Settings size={16} className="text-os-text/70" /> Settings
  </button>
  ```
  > **Critical:** The handler calls `setMenuOpen(false)` simultaneously with `setSettingsOpen(true)`. This collapses the dropdown backdrop before the modal backdrop mounts, preventing two `fixed inset-0` overlays from stacking.
- **Validation:** "Settings" button with gear icon is visible in the dropdown below the Appearance section and above Logout. Clicking it closes the dropdown (`menuOpen → false`) and opens the Settings modal (`settingsOpen → true`).

---

### Task 9 — Insert Settings modal JSX into App.tsx return block

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** In the component return JSX, after the closing `</div>` of the Top Bar (Taskbar) block and immediately before the `{/* Desktop Area */}` comment.
- **What to add/change:**
  ```tsx
  {/* Settings Modal */}
  {settingsOpen && (
    <>
      <div
        className="fixed inset-0 z-[60] bg-black/50"
        onClick={() => setSettingsOpen(false)}
      />
      <div className="fixed inset-0 z-[61] flex items-center justify-center pointer-events-none">
        <div className="bg-os-window border border-os-border rounded-xl shadow-2xl w-80 pointer-events-auto">
          <div className="flex items-center justify-between px-4 py-3 border-b border-os-border">
            <span className="font-semibold text-sm">Settings</span>
            <button
              onClick={() => setSettingsOpen(false)}
              className="p-1 rounded hover:bg-os-border transition-colors"
            >
              <X size={16} />
            </button>
          </div>
          <div className="p-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Always show taskbar</span>
              <button
                role="switch"
                aria-checked={osConfig.taskbarAlwaysVisible}
                onClick={() =>
                  setOsConfig(prev => ({
                    ...prev,
                    taskbarAlwaysVisible: !prev.taskbarAlwaysVisible,
                  }))
                }
                className={cn(
                  "relative w-10 h-5 rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-os-accent",
                  osConfig.taskbarAlwaysVisible ? "bg-os-accent" : "bg-os-border"
                )}
              >
                <span
                  className={cn(
                    "absolute top-0.5 left-0.5 block w-4 h-4 rounded-full bg-white shadow-sm transition-transform duration-200",
                    osConfig.taskbarAlwaysVisible ? "translate-x-5" : "translate-x-0"
                  )}
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )}
  ```
  > **z-index breakdown:** Backdrop `z-[60]` > dropdown container `z-50`. Panel wrapper `z-[61]`. Panel itself uses `pointer-events-auto` while wrapper uses `pointer-events-none` to prevent the wrapper from blocking desktop clicks when modal is open.
- **Validation:** Modal renders centered. `settingsOpen` controls visibility. Toggle button flips `osConfig.taskbarAlwaysVisible` via functional `setOsConfig` update. Backdrop click closes modal. X button closes modal.

---

### Task 10 — Insert Escape key useEffect for settingsOpen in App.tsx

- **File:** web/App.tsx
- **Edit type:** insert
- **Location:** Immediately after the `useEffect(() => { saveOsConfig(osConfig); }, [osConfig]);` block added in Task 6.
- **What to add/change:**
  ```typescript
  // Close settings modal on Escape key
  useEffect(() => {
    if (!settingsOpen) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setSettingsOpen(false);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [settingsOpen]);
  ```
- **Validation:** When modal is open, pressing Escape closes it. Event listener is registered only while `settingsOpen === true` and is cleaned up on close or unmount. No listener leaks.

---

## Acceptance Criteria

1. A "Settings" button with a gear icon appears in the hamburger dropdown, positioned between the Appearance section and the Logout button.
2. Clicking "Settings" closes the dropdown and opens a centered modal overlay; both state transitions happen in the same click handler.
3. The Settings modal contains a "Always show taskbar" pill/switch toggle.
4. Toggling "Always show taskbar" to ON: the taskbar no longer hides after `mouseleave` — it stays visible indefinitely.
5. Toggling "Always show taskbar" to OFF: the taskbar resumes auto-hide behavior (disappears ~2 s after `mouseleave` when no menu is open).
6. `localStorage.getItem('nebula-os-config')` returns `{"taskbarAlwaysVisible":true}` after enabling; `{"taskbarAlwaysVisible":false}` after disabling.
7. Reloading the page preserves the toggle state — the setting is read from `localStorage` on mount via the lazy `useState` initializer.
8. The Settings modal closes when the backdrop (area outside the panel) is clicked.
9. The Settings modal closes when the Escape key is pressed while the modal is open.
10. The Settings modal closes when the X button in the modal header is clicked.
11. The existing theme toggle (Dark / Light / Retro) still applies the correct `theme-*` class to `document.body`.
12. The existing application launchers (AgentFlow Builder, Text Editor, Calculator, Paint Studio, System Monitor) in the dropdown still open windows correctly.
13. TypeScript type-checks cleanly: `npx tsc --noEmit` produces no errors.
14. The Vite build completes without errors: `npm run build` in `web/`.

---

## Validation Commands

Run from `c:\Dev\PyAgent\web\`:

```powershell
npx tsc --noEmit
npm run build
```

Manual smoke test (run `npm run dev` then open browser):

1. Log in → move mouse off the taskbar → confirm it hides after ~2 s.
2. Open hamburger menu → confirm "Settings" button appears between Appearance and Logout.
3. Click "Settings" → confirm dropdown closes and modal appears centered.
4. Toggle "Always show taskbar" ON → close modal → move mouse off taskbar → confirm taskbar stays visible.
5. Open browser DevTools console → run `localStorage.getItem('nebula-os-config')` → confirm `{"taskbarAlwaysVisible":true}`.
6. Reload page → open Settings → confirm toggle is still ON.
7. Toggle OFF → confirm auto-hide resumes after ~2 s of mouse-off.
8. Open modal → press Escape → confirm modal closes.
9. Open modal → click backdrop → confirm modal closes.
10. Verify all three theme buttons and all five app launchers still work.

---

## Constraints for @6code

- Do **NOT** create a new `web/types.ts` — it already exists. Append `OsConfig` and `DEFAULT_OS_CONFIG` at the end.
- Do **NOT** use the `'settings'` `AppId` or call `openApp('settings')`. The modal is managed by `settingsOpen` local state only, completely outside the `WindowState` pipeline.
- `loadOsConfig` and `saveOsConfig` **MUST** be module-level functions (outside the `App` component) — not inline arrows or hooks.
- `useState<OsConfig>(loadOsConfig)` — pass as a function reference without parentheses (lazy initializer). Do NOT write `useState<OsConfig>(loadOsConfig())`.
- The Settings button `onClick` handler **MUST** call `setMenuOpen(false)` in the same handler (not in a separate effect) to prevent two simultaneous `fixed inset-0` backdrop divs.
- Modal backdrop z-index **MUST** be `z-[60]`; modal panel wrapper **MUST** be `z-[61]`. Both must be above `z-50` (the dropdown).
- The `osConfig.taskbarAlwaysVisible` guard in `hideTaskbar()` **MUST** be the first guard (before `menuOpen`).
- Do **NOT** modify the CSS transition on the Taskbar — only the `hideTaskbar()` function body changes.
- Do **NOT** add a `'settings'` case to the `openApp` switch statement.

---

## Handoff to @5test

@5test must cover the following scenarios:

1. **Persistence ON → reload**: Toggle ON, reload, assert `osConfig.taskbarAlwaysVisible === true` and toggle renders as ON.
2. **Persistence OFF → reload**: Toggle OFF, reload, assert toggle is OFF and `localStorage` value reflects `false`.
3. **hideTaskbar guard — pinned ON**: Set `taskbarAlwaysVisible = true`, trigger `mouseLeave` on taskbar, assert `isTaskbarVisible` remains `true` after 2+ s.
4. **hideTaskbar guard — pinned OFF**: Set `taskbarAlwaysVisible = false`, trigger `mouseLeave`, assert `isTaskbarVisible` becomes `false` after 2 s.
5. **Modal open via Settings button**: Click Settings button → assert `settingsOpen === true` and `menuOpen === false`.
6. **Modal close via X button**: Open modal → click X → assert `settingsOpen === false`.
7. **Modal close via backdrop click**: Open modal → click backdrop div → assert `settingsOpen === false`.
8. **Modal close via Escape key**: Open modal → dispatch `keydown` Escape → assert `settingsOpen === false`.
9. **Escape key no-op when modal closed**: Dispatch Escape when `settingsOpen === false` → no state change.
10. **No regression — theme toggle**: All three theme buttons produce correct `document.body` class.
11. **No regression — app launchers**: Each dropdown app button opens a `WindowState` with the correct `appId`.
12. **Dropdown/modal overlap prevention**: Verify Settings button handler sets `menuOpen = false` before or simultaneously with `settingsOpen = true` (no frame where both are `true`).

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|

## Validation Commands
```powershell
python -m pytest -q
```
