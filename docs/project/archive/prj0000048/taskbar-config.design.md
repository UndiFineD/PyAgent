# Design: prj0000048 — Taskbar Config

_Status: Complete_  
_Designer: @3design | Updated: 2026-03-23_

---

## Selected Approach

**Option B — OsConfig + Settings Modal**

Single JSON blob in `localStorage` under key `nebula-os-config`. Settings are accessed via a "Settings" button in the existing
dropdown that opens a centered modal overlay managed entirely by local `App.tsx` state.

---

## TypeScript Interface

**File:** `web/types.ts`  
**Placement:** Append after the existing `User` interface (end of file, line ~26).

```typescript
export interface OsConfig {
  taskbarAlwaysVisible: boolean;
}

export const DEFAULT_OS_CONFIG: OsConfig = {
  taskbarAlwaysVisible: false,
};
```

**Note on existing `AppId`:** `'settings'` is already present in the `AppId` union in `web/types.ts` (line 3). It must **not** be
used for the settings modal — the modal is App.tsx-local state only. No change to `AppId` is required or desired.

---

## Persistence Helpers

**File:** `web/App.tsx`  
**Placement:** After the `INITIAL_WINDOWS` constant (after line 27), before the `export default function App()` declaration.

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

`loadOsConfig` is called once as the `useState` lazy initializer (no repeated reads).  
`saveOsConfig` is the target of the persistence `useEffect`.  
Both functions are module-level (not inside the component) — no closure issues; extractable for future unit-testing.

---

## Import Changes

**File:** `web/App.tsx` — line 11 (the lucide-react import line).

Add `Settings` and `X` to the existing import:

```typescript
import {
  Menu, Monitor, Terminal, Palette, Calculator as CalcIcon,
  LogOut, Moon, Sun, MonitorPlay, Bot, Settings, X
} from 'lucide-react';
```

Also add `OsConfig` and `DEFAULT_OS_CONFIG` to the `web/types` import on line 9:

```typescript
import { WindowState, AppId, Theme, OsConfig, DEFAULT_OS_CONFIG } from './types';
```

---

## State Variables

**File:** `web/App.tsx`  
**Placement:** Immediately after the `hideTimeoutRef` declaration (after line 41, inside the App component body).

| Variable | Type | Initializer | Location in App.tsx |
|---|---|---|---|
| `osConfig` | `OsConfig` | `loadOsConfig` (lazy ref) | After `hideTimeoutRef` (after line 41) |
| `settingsOpen` | `boolean` | `false` | Immediately after `osConfig` |

Exact declarations:

```typescript
const [osConfig, setOsConfig] = useState<OsConfig>(loadOsConfig);
const [settingsOpen, setSettingsOpen] = useState(false);
```

**Note:** `loadOsConfig` is passed as a function reference (not called: `loadOsConfig` not `loadOsConfig()`), which is React's
lazy initializer form — runs once on mount only.

---

## Persistence Side-Effect

**File:** `web/App.tsx`  
**Placement:** After the existing `useEffect([menuOpen])` block (approximately after line 72).

```typescript
// Persist OS config to localStorage on every change
useEffect(() => {
  saveOsConfig(osConfig);
}, [osConfig]);
```

---

## `hideTaskbar()` Guard Change

**File:** `web/App.tsx`  
**Location:** The `hideTaskbar` function (approximately lines 55–61).

Current body:
```typescript
const hideTaskbar = () => {
  if (menuOpen) return; // Don't hide if menu is open
  hideTimeoutRef.current = setTimeout(() => {
    setIsTaskbarVisible(false);
  }, 2000);
};
```

Updated body — add `osConfig.taskbarAlwaysVisible` guard **before** the `menuOpen` guard:
```typescript
const hideTaskbar = () => {
  if (osConfig.taskbarAlwaysVisible) return; // Don't hide if pinned
  if (menuOpen) return; // Don't hide if menu is open
  hideTimeoutRef.current = setTimeout(() => {
    setIsTaskbarVisible(false);
  }, 2000);
};
```

**Why this order matters:** The `taskbarAlwaysVisible` guard is the user-preference override and is conceptually prior to any
transient UI state. The existing `useEffect([menuOpen])` calls `hideTaskbar()` on menu close — the updated guard handles that
path correctly without any further changes.

---

## Escape-to-Close Side-Effect

**File:** `web/App.tsx`  
**Placement:** After the `saveOsConfig` `useEffect`.

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

---

## Settings Button in Dropdown

**File:** `web/App.tsx`  
**Placement:** Inside the dropdown `<div className="p-2 space-y-1">`, immediately **before** the existing Logout button, with a
new separator between Settings and Logout.

Replace the current final separator + Logout block (approximately):
```tsx
                    <div className="h-px bg-os-border my-2" />
                    
                    <button onClick={() => setIsLoggedIn(false)} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-red-500/10 hover:text-red-500 text-left text-sm transition-colors">
                      <LogOut size={16} /> Logout
                    </button>
```

With:
```tsx
                    <div className="h-px bg-os-border my-2" />

                    <button
                      onClick={() => { setMenuOpen(false); setSettingsOpen(true); }}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors"
                    >
                      <Settings size={16} className="text-os-text/70" /> Settings
                    </button>

                    <div className="h-px bg-os-border my-2" />

                    <button onClick={() => setIsLoggedIn(false)} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-red-500/10 hover:text-red-500 text-left text-sm transition-colors">
                      <LogOut size={16} /> Logout
                    </button>
```

**Critical:** `setMenuOpen(false)` executes before `setSettingsOpen(true)` in the same handler. React batches these in a single
render, ensuring the dropdown backdrop div is unmounted in the same frame the modal appears — no dual overlay state.

---

## Settings Modal JSX

**File:** `web/App.tsx`  
**Placement:** Inside the root `return` JSX, as the **last child** of the outermost `<div className="h-screen w-screen ...">`,
placed after the `{/* Desktop Area */}` section (after the `</div>` that closes the Desktop area, before the final `</div>`
that closes the root).

```tsx
      {/* Settings Modal */}
      {settingsOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-[60] bg-black/50 backdrop-blur-sm"
            onClick={() => setSettingsOpen(false)}
          />
          {/* Panel */}
          <div className="fixed inset-0 z-[61] flex items-center justify-center pointer-events-none">
            <div className="w-96 bg-os-window border border-os-border rounded-xl shadow-2xl pointer-events-auto animate-in fade-in zoom-in-95 duration-200">
              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-os-border">
                <span className="font-semibold text-sm">Settings</span>
                <button
                  onClick={() => setSettingsOpen(false)}
                  className="p-1 rounded hover:bg-os-border transition-colors"
                  aria-label="Close settings"
                >
                  <X size={16} />
                </button>
              </div>
              {/* Body */}
              <div className="p-4 space-y-4">
                {/* Taskbar section */}
                <div>
                  <div className="px-0 py-1 text-xs font-semibold text-os-text/50 uppercase tracking-wider mb-3">
                    Taskbar
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Always visible</span>
                    {/* Toggle switch — inline Tailwind, no component file */}
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        className="sr-only peer"
                        checked={osConfig.taskbarAlwaysVisible}
                        onChange={e =>
                          setOsConfig(prev => ({ ...prev, taskbarAlwaysVisible: e.target.checked }))
                        }
                      />
                      <div className="w-10 h-6 rounded-full bg-os-border transition-colors duration-200 peer-checked:bg-os-accent peer-focus-visible:ring-2 peer-focus-visible:ring-os-accent/50" />
                      <div className="absolute left-1 top-1 w-4 h-4 rounded-full bg-white shadow transition-transform duration-200 peer-checked:translate-x-4" />
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
```

### Toggle Switch Pattern

The toggle is a pure CSS/Tailwind pattern using a visually-hidden `<input type="checkbox">` and a styled `<div>` track + thumb.
No new component file.

| Element | Key Classes | Purpose |
|---|---|---|
| `<input>` | `sr-only peer` | Hidden but keyboard-accessible; drives `peer-*` variants on siblings |
| Track `<div>` | `w-10 h-6 rounded-full bg-os-border peer-checked:bg-os-accent` | Turns accent colour when checked |
| Thumb `<div>` | `absolute left-1 top-1 w-4 h-4 rounded-full bg-white peer-checked:translate-x-4` | Slides right 16 px when checked |

---

## Z-Index Layer Reference

| Element | z-index | Notes |
|---|---|---|
| Desktop windows | `1+` (dynamic) | Managed by `zIndex` in `WindowState` |
| Dropdown backdrop | `z-40` | `fixed inset-0`, existing |
| Dropdown panel | `z-50` | `absolute`, existing |
| Settings backdrop | `z-[60]` | Semi-transparent, `fixed inset-0` |
| Settings panel | `z-[61]` | Centered flex container |
| Taskbar trigger zone | `z-[1001]` | `fixed top-0`, existing |
| Taskbar | `z-[1000]` | `fixed top-0`, existing |

The taskbar remains accessible above the settings modal (1000 > 61). Moving the mouse to the trigger zone while settings are
open calls `showTaskbar()` as expected.

---

## Open Questions Resolved

1. **Settings trigger placement:** "Settings" button added between Appearance section and Logout button (new separators on both sides). The Appearance section label and theme grid are unchanged.

2. **Modal design language:** Centered floating panel with semi-transparent backdrop (`bg-black/50 backdrop-blur-sm`), matching the OS window aesthetic (`bg-os-window`, `border-os-border`, `rounded-xl`, `shadow-2xl`). Same `animate-in fade-in` animation class used by the existing dropdown.

3. **OsConfig expansion scope:** Strictly `taskbarAlwaysVisible` only in this PR. No placeholder rows for future settings — adding them is a one-line type change + one JSX row. Minimises test surface.

4. **Toggle component:** Inline Tailwind pattern, no new component file. Pattern fully documented above for @6code.

5. **Accessibility:** `Escape`-to-close via `keydown` `useEffect`. No `focus-trap` library. Close button carries `aria-label="Close settings"`. Checkbox input is `sr-only` but natively keyboard-accessible. Sufficient for project scope.

---

## Constraints Carried Forward to @4plan and @6code

1. **Dropdown-close before modal-open:** The Settings button `onClick` must call `setMenuOpen(false)` and `setSettingsOpen(true)` in the same handler (React batches). Never open the modal without closing the dropdown.

2. **Guard order in `hideTaskbar()`:** `taskbarAlwaysVisible` guard must be the FIRST early return, before `menuOpen`.

3. **`OsConfig` mutation pattern:** Always `setOsConfig(prev => ({ ...prev, key: value }))` — never replace the whole object.

4. **`Settings` is NOT an `AppId` route:** Do not call `openApp()` or use `setActiveWindowId` for the settings modal. `settingsOpen: boolean` local state only.

5. **No CSS changes:** The existing `!isTaskbarVisible && !menuOpen` taskbar CSS condition is correct and must not be altered.

6. **`loadOsConfig` lazy initializer form:** `useState<OsConfig>(loadOsConfig)` without parentheses — not `useState<OsConfig>(loadOsConfig())`.

7. **Modal placement in JSX:** The `{settingsOpen && ...}` block must be a direct sibling of `{/* Desktop Area */}`, not nested inside the `z-0` desktop div.

8. **`X` and `Settings` icons:** Must be added to the lucide-react import. No other new npm dependencies.

9. **`DEFAULT_OS_CONFIG` import:** Must be imported from `./types` in `App.tsx` (referenced by `loadOsConfig`).

10. **localStorage error handling:** `loadOsConfig` must wrap `JSON.parse` in `try/catch` returning `DEFAULT_OS_CONFIG` on failure.

## Interfaces & Contracts
_To be completed by @3design._

## Non-Functional Requirements
- Performance: _TBD_
- Security: _TBD_

## Open Questions
_To be completed by @3design, for @4plan._
