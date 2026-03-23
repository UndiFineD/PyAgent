# Think: prj0000048 — Taskbar Config

_Status: Complete_
_Analyst: @2think | Updated: 2026-03-23_

## Summary

`App.tsx` is a ~380-line single-file React component (Vite/React 19, Tailwind) implementing all OS shell logic directly.
The taskbar auto-hide is driven by two local functions (`showTaskbar`/`hideTaskbar`) and a 2 s `setTimeout`, with no existing
config persistence of any kind in source code. Three options were analysed; **Option B (OsConfig + Settings modal)** is
recommended as it directly fulfils the user's stated intent ("group alongside other config options") and is forward-compatible.

---

## Codebase Findings

### web/App.tsx — Key State

| Variable | Type | Initial value | Purpose |
|---|---|---|---|
| `isTaskbarVisible` | `boolean` | `true` | Controls taskbar CSS class |
| `menuOpen` | `boolean` | `false` | Dropdown open flag; also keeps taskbar visible |
| `hideTimeoutRef` | `MutableRefObject<ReturnType<typeof setTimeout> \| null>` | `null` | Handle for the 2 s hide delay |
| `theme` | `Theme['id']` | `'dark'` | Persisted only in React state (no localStorage) |
| `isLoggedIn` | `boolean` | `false` | Guards the Login screen |
| `windows` | `WindowState[]` | `[]` (set to INITIAL_WINDOWS on login) | Open window list |
| `activeWindowId` | `string \| null` | `null` | Z-index focus tracking |
| `currentTime` | `Date` | `new Date()` | Clock, updated every 1 s |

### web/App.tsx — Auto-hide Logic

```
showTaskbar():
  clearTimeout(hideTimeoutRef.current)
  setIsTaskbarVisible(true)

hideTaskbar():
  if (menuOpen) return   ← guard: menu open keeps bar visible
  hideTimeoutRef.current = setTimeout(() => setIsTaskbarVisible(false), 2000)

useEffect([menuOpen]):
  if (menuOpen) → showTaskbar()
  else          → hideTaskbar()
```

Additional callsites:
- A 2 px invisible `div.fixed.top-0` trigger zone fires `showTaskbar()` on `onMouseEnter`
- The taskbar `div` itself fires `showTaskbar()` / `hideTaskbar()` on `onMouseEnter` / `onMouseLeave`

CSS transition:  
```
cn(
  "..transition-transform duration-500 ease-in-out",
  !isTaskbarVisible && !menuOpen ? "-translate-y-full" : "translate-y-0"
)
```
Note: the CSS condition is `!isTaskbarVisible && !menuOpen`, so the bar stays visible if **either** flag is true.

### web/App.tsx — Dropdown JSX

The dropdown is an `absolute right-0 top-full w-64` div rendered only when `menuOpen === true`.  
Current structure (in order):

1. Backdrop `div.fixed.inset-0.z-40` → closes dropdown on outside click
2. Container `div.w-64.bg-os-window.z-50`
   - **Section: Applications** (`px-3 py-2` label + 5 app-launch buttons)
   - Separator `h-px`
   - **Section: Appearance** (`px-3 py-2` label + 3-col theme grid: Dark / Light / Retro)
   - Separator `h-px`
   - **Logout** button (`hover:bg-red-500/10`)

The "Appearance" section is the natural home for taskbar toggle UI (Option A / C).
A new "Settings" button in the dropdown (between Appearance and Logout) would be the entry point for Option B.

### Existing Config / LocalStorage

- **No** `localStorage` calls exist in any web source file (`App.tsx`, `types.ts`, `utils.ts`, `apps/*.tsx`, `components/*.tsx`).
- **No** `web/src/config.ts`, `web/settings.ts`, or any config module exists.
- `web/types.ts` defines `AppId`, `WindowState`, `Theme`, `User` — no settings/config type.
- The only localStorage usage in the repo is inside `web/dist/assets/app-codebuilder-DRpwg_AZ.js` (compiled artifact, key `pyagent.codebuilder.ui-state.v1`) — this is the CodeBuilder in-app persistence and is unrelated to OS-level settings.

**Conclusion:** This is a clean slate. No migration needed; introduce localStorage for the first time.

---

## Options Analysed

### Option A — Minimal boolean toggle

**What:** Add a single `taskbarAlwaysVisible: boolean` state, initialised from
`localStorage.getItem('nebula-taskbar-always-visible') === 'true'`.  
Add a checkbox/toggle row inside the existing "Appearance" section of the dropdown.  
In `hideTaskbar()`, add: `if (taskbarAlwaysVisible) return;`  
On toggle, immediately persist to `localStorage`.

**Pros:**
- Smallest diff; ~15–20 lines changed.
- Zero new state management (no modal, no extra hooks).
- Lower risk of introducing regressions in the auto-hide flow.
- Solves exactly what was asked with no over-engineering.

**Cons:**
- Isolated localStorage key (`nebula-taskbar-always-visible`) that cannot group with future settings without a migration.
- If more settings are added later, each one gets its own key → scattered storage.
- Does not match user's stated desire for a "settings panel alongside other config options".
- The dropdown's Appearance section is already occupied by the theme grid; adding a checkbox row breaks the visual rhythm.

**Risk:** Low. The only change to auto-hide logic is adding one additional early-return guard in `hideTaskbar()`.

**Migration cost if Option B is chosen later:** One-time key rename + parse.

---

### Option B — OsConfig + Settings Modal

**What:** Define `OsConfig` in `types.ts`:

```typescript
export interface OsConfig {
  taskbarAlwaysVisible: boolean;
}
```

Persist as JSON to `localStorage` key `nebula-os-config`.  
Add `settingsOpen: boolean` state in `App.tsx`.  
Add a "Settings" button in the dropdown (between Appearance and Logout).  
Render a modal `div.fixed` overlay (backdrop + centered panel) listing all config fields.  
The modal is managed entirely by App.tsx state — it does **not** go through the `WindowState` / `openApp()` pipeline.

**Pros:**
- Directly fulfils user intent: "ideally group this in a settings panel alongside other config options".
- `OsConfig` in `types.ts` is the single source of truth — adding `clockFormat`, `animationSpeed`, etc. later is a one-line type change + one new UI row.
- Single `nebula-os-config` JSON blob → clean storage, easy to inspect and migrate.
- Modal pattern is well-understood (same backdrop pattern already used by the dropdown).
- Keeps the dropdown width (`w-64`) clean; settings are behind a single button.
- Forward-compatible with a future "Settings" app window if the project grows.

**Cons:**
- More code: new `settingsOpen` state, a modal JSX block (~40–60 lines), `OsConfig` type, init/persist hooks.
- Two overlapping overlays possible (dropdown + modal both open) unless the "Settings" button closes the dropdown first — needs care.
- Modal z-index must be above dropdown (`z-50`) → use `z-[60]`.

**Risk:** Medium. Modal state is straightforward but the z-index layering and dropdown-close coordination must be explicit in the design.

**Implementation note:** The "Settings" button handler must do:  
```tsx
onClick={() => { setMenuOpen(false); setSettingsOpen(true); }}
```
This ensures the dropdown backdrop is removed before the modal appears, avoiding two stacked overlay divs.

---

### Option C — OsConfig + Inline dropdown expansion

**What:** No separate modal. Expand the dropdown with a collapsible "Settings" section beneath "Appearance".
Toggle switches rendered inline in the `w-64` dropdown panel.
Uses same `OsConfig` type and `nebula-os-config` key as Option B.

**Pros:**
- No modal state; fewer moving parts than Option B.
- Stays within the single-dropdown interaction pattern already established.
- `menuOpen` guard keeps taskbar visible while user adjusts — no extra logic needed.

**Cons:**
- The dropdown is already `w-64` with 5 app buttons + 3 theme buttons + logout; adding settings rows will make it very tall.
- Unusual UX: settings panels in dropdown are non-standard and hard to extend.
- A collapsible sub-section adds toggle state for the expand/collapse (`settingsSectionOpen: boolean`) — equivalent complexity to Option B's `settingsOpen`, with worse UX outcome.
- If the settings section is **always visible** (non-collapsible), the dropdown height becomes unwieldy.
- Harder to evolve: any future text-input or multi-select settings will not fit comfortably in a `w-64` dropdown.

**Risk:** Low for the initial implementation, but degrades UX immediately if any second setting is added.

---

## Decision Matrix

| Criterion | Option A | Option B | Option C |
|---|:---:|:---:|:---:|
| Matches user intent ("settings panel") | ✗ | ✓ | Partial |
| Implementation scope | Minimal | Moderate | Moderate |
| Future settings extensibility | Poor | Excellent | Poor |
| Storage cleanliness | Poor | Excellent | Excellent |
| UX quality | Acceptable | Good | Marginal |
| Risk to existing auto-hide logic | Low | Low | Low |
| Modal/overlay complexity | None | Low | None |

---

## Recommendation

**Implement Option B — OsConfig + Settings Modal.**

The user explicitly stated "ideally group this in a settings panel alongside other config options."
Option B is the only option that directly honours that intent without creating a future migration burden.
The implementation cost over Option A is ~50 extra lines of JSX and one new state variable — modest for the payoff.
Option C creates equivalent complexity to Option B but with inferior UX and no extensibility benefit.

### Proposed contract for @3design

**Type (add to `web/types.ts`):**
```typescript
export interface OsConfig {
  taskbarAlwaysVisible: boolean;
}

export const DEFAULT_OS_CONFIG: OsConfig = {
  taskbarAlwaysVisible: false,
};
```

**localStorage key:** `nebula-os-config`  
**Serialisation:** `JSON.stringify(config)` / `JSON.parse(raw)` with fallback to `DEFAULT_OS_CONFIG`.

**State to add in `App.tsx`:**
```typescript
const [osConfig, setOsConfig] = useState<OsConfig>(() => {
  try {
    const raw = localStorage.getItem('nebula-os-config');
    return raw ? { ...DEFAULT_OS_CONFIG, ...JSON.parse(raw) } : DEFAULT_OS_CONFIG;
  } catch {
    return DEFAULT_OS_CONFIG;
  }
});
const [settingsOpen, setSettingsOpen] = useState(false);
```

**Persist on change:**
```typescript
useEffect(() => {
  localStorage.setItem('nebula-os-config', JSON.stringify(osConfig));
}, [osConfig]);
```

**Auto-hide guard in `hideTaskbar()`:**  
Add `if (osConfig.taskbarAlwaysVisible) return;` **before** the `if (menuOpen) return;` guard.

**Constraints @3design must respect:**
1. The Settings button handler must `setMenuOpen(false)` before `setSettingsOpen(true)` — never have dropdown and modal open simultaneously.
2. Settings modal z-index must be `z-[60]` or higher (dropdown is `z-50`, taskbar is `z-[1000]`).
3. `OsConfig` changes must use `setOsConfig(prev => ({ ...prev, key: newValue }))` pattern (spread to preserve future keys).
4. The `useEffect([menuOpen])` existing guard already calls `hideTaskbar()` on menu close — the updated `hideTaskbar()` with the `taskbarAlwaysVisible` guard will automatically handle this path correctly without further changes.
5. The CSS condition `!isTaskbarVisible && !menuOpen` remains correct for all options; no CSS changes needed.
6. Do **not** add `settings` as a new `AppId` or route through `openApp()` — the settings modal is App.tsx-local state only.

---

## Open Questions for @3design

1. **Settings trigger placement:** Should the "Settings" button be added between "Appearance" and the Logout separator, or replace the Appearance section label with a "Appearance & Settings" grouped block?
2. **Modal design language:** Centered floating panel (like a dialog) or a right-side slide-in panel? The existing window system uses absolute-positioned divs; a centered modal with backdrop is simplest.
3. **OsConfig expansion scope for this PR:** Should `clockFormat` and `animationSpeed` be included in the initial modal as placeholders (disabled/greyed), or strictly only `taskbarAlwaysVisible`? Keeping it to one setting reduces test surface.
4. **Toggle component:** Inline HTML checkbox styled with Tailwind, or a custom `Toggle` component in `web/components/`? If custom, that component needs to be created as part of this task.
5. **Accessibility:** Should the modal trap focus (`focus-trap`) or is `Escape`-to-close sufficient for this project's scope?
