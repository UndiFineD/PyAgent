# Design: prj0000050 — Install Script

## Status
Complete

---

## Script Interface

### Synopsis
```powershell
.\install.ps1 [-SkipRust] [-SkipWeb] [-SkipDev] [-CI] [-Force]
```

### Parameters

| Parameter  | Type   | Default  | Purpose                                                                                  |
|------------|--------|----------|------------------------------------------------------------------------------------------|
| `-SkipRust` | Switch | `$false` | Skip Rust/cargo check, maturin install, and `maturin develop` build step               |
| `-SkipWeb`  | Switch | `$false` | Skip Node/npm check and `web/node_modules` install                                      |
| `-SkipDev`  | Switch | `$false` | Skip dev/CI tooling (`requirements-ci.txt`); implies maturin installed standalone if Rust is present |
| `-CI`       | Switch | `$false` | Non-interactive mode: suppress all prompts; treat all warnings as non-fatal              |
| `-Force`    | Switch | `$false` | Force deletion + recreation of `.venv` even if it already exists                        |

### Script-scope flags (set internally by `Test-Prerequisites`)

| Flag              | Type    | Set when                                              |
|-------------------|---------|-------------------------------------------------------|
| `$script:HasRust` | Boolean | `$false` when cargo not found or version check fails  |
| `$script:HasNode` | Boolean | `$false` when node/npm not found                      |

---

## Script Structure

### File header

```powershell
#Requires -Version 5.1
[CmdletBinding()]
param (
    [switch]$SkipRust,
    [switch]$SkipWeb,
    [switch]$SkipDev,
    [switch]$CI,
    [switch]$Force
)
$ErrorActionPreference = 'Stop'
```

A Windows guard at the top of the execution path (not inside a function):
```powershell
if ($IsLinux -or $IsMacOS) {
    Write-Error "install.ps1 is Windows-only. Use bash scripts on Linux/macOS."
    exit 1
}
```

### Functions

#### `Write-Status`
**Purpose:** Centralised coloured output helper.  
**Signature:** `Write-Status [-Ok] [-Warn] [-Fail] [-Skip] [string]$Message`  
- Green `[✓]` for `-Ok`  
- Yellow `[⚠]` for `-Warn`  
- Red `[✗]` for `-Fail`  
- Cyan `[→]` for `-Skip`  

All output via `Write-Host` with `-ForegroundColor`.

#### `Test-Prerequisites`
**Purpose:** Validate required and optional system tools. Sets `$script:HasRust` and `$script:HasNode`.  
**Checks (in order):**
1. **Python ≥ 3.12** — parse `python --version`; hard abort (`exit 1`) with install URL if not satisfied. Minimum is 3.12 per `pyproject.toml requires-python`; `docs/setup.md` saying 3.11+ is outdated.
2. **Git** — `git --version`; warn only if not found (not fatal).
3. **Rust/cargo** — `cargo --version`; if not found: warn + `$script:HasRust = $false`. If found but version < 1.80: warn users to upgrade but allow build to proceed.
4. **Node/npm** — `node --version` + `npm --version`; if not found: warn + `$script:HasNode = $false`. If found but version < v18: warn (no hard fail — Node version is not pinned in the project).

#### `Initialize-Venv`
**Purpose:** Create or reuse the Python virtual environment.  
**Logic:**
- If `-Force` and `.venv` exists: remove `.venv` first.
- If `.venv` exists and not `-Force`: print "Already exists — reusing"; skip creation.
- If `.venv` does not exist: `python -m venv .venv`; print success.
- Activate: `.\.venv\Scripts\Activate.ps1`
- If activation fails → `exit 1` (nothing else can proceed without venv).

#### `Install-Python`
**Purpose:** Upgrade pip and install all Python dependency tiers.  
**Steps (in order, each in its own try/catch):**
1. `pip install --upgrade pip`
2. `pip install --prefer-binary -r requirements.txt`
3. `pip install --prefer-binary -r backend/requirements.txt`
4. Unless `-SkipDev`: `pip install --prefer-binary -r requirements-ci.txt`  
   (This file already includes maturin 1.12.5 via the requirements-ci.txt pin.)
5. If `-SkipDev` **and** `$script:HasRust -and -not $SkipRust`:  
   `pip install --prefer-binary "maturin>=1.0,<2.0"`  
   (Ensures maturin is available for the Rust build even when dev tools are skipped.)

Steps 2 and 3 are **fatal** on failure (core/backend deps are required). Steps 4–5 are non-fatal.

#### `Build-Rust`
**Purpose:** Build the PyO3 Rust extension into the active venv.  
**Guard:** Skipped entirely if `-SkipRust` or `$script:HasRust -eq $false`.  
**Command:** `maturin develop --manifest-path rust_core/Cargo.toml`  
**On failure:** Print red warning + reason; continue (non-fatal). The Python install still works without the Rust extension.  
**Note:** `rust_core/p2p/` is a standalone binary — it is **not** built here.

#### `Install-Scaffold`
**Purpose:** Run `scripts/setup_structure.py` to create required directory scaffolding.  
**Command:** `python scripts/setup_structure.py`  
**On failure:** Non-fatal warning only; continue.

#### `Install-Node`
**Purpose:** Install frontend npm dependencies.  
**Guard:** Skipped entirely if `-SkipWeb` or `$script:HasNode -eq $false`.  
**Commands:**
```powershell
Push-Location web
npm install
Pop-Location
```
**On failure:** Print red warning; `Pop-Location` in `finally` block to restore directory; continue.

#### `Show-Summary`
**Purpose:** Print a final status table and next-steps block.  
**See "Summary block format" below.**

---

## Execution Flow (ordered)

1. **OS guard** — abort on Linux/macOS
2. **Print banner** — project name, date, active switches
3. **`Test-Prerequisites`** — Python (fatal if <3.12), Git (warn), Rust (warn + flag), Node (warn + flag)
4. **`Initialize-Venv`** — create or reuse `.venv`; activate (fatal if activation fails)
5. **`Install-Python`** — upgrade pip → `requirements.txt` → `backend/requirements.txt` → `requirements-ci.txt` (unless `-SkipDev`) → standalone maturin if needed
6. **`Build-Rust`** — `maturin develop` (conditional: `$script:HasRust` and not `-SkipRust`)
7. **`Install-Scaffold`** — `python scripts/setup_structure.py` (non-fatal)
8. **`Install-Node`** — `npm install` in `web/` (conditional: `$script:HasNode` and not `-SkipWeb`)
9. **`Show-Summary`** — coloured summary table + next-steps block

---

## Output Design

### Colours

| Colour | Marker | Meaning                                             |
|--------|--------|-----------------------------------------------------|
| Green  | `[✓]`  | Step succeeded                                      |
| Yellow | `[⚠]`  | Step skipped or optional dependency not found       |
| Red    | `[✗]`  | Step failed (non-fatal) or prerequisite not met     |
| Cyan   | `[→]`  | Informational / progress line                       |

### Banner format

```
══════════════════════════════════════════════════════
  PyAgent — Developer Install Script
  Run: 2026-03-23  Mode: [standard | CI]
══════════════════════════════════════════════════════
```

### Summary block format

```
══════════════════════════════════════════════════════
  PyAgent Install — Complete
══════════════════════════════════════════════════════
  [✓] Python venv      .venv  (Python 3.x.x)
  [✓] Core deps        requirements.txt
  [✓] Backend deps     backend/requirements.txt
  [✓] Dev tools        requirements-ci.txt
  [✓] Rust extension   rust_core/_rust_core built
  [✓] Scaffolding      scripts/setup_structure.py
  [✓] Web deps         web/node_modules

  Next steps:
    Run tests:       python -m pytest -q
    Run backend:     uvicorn backend.app:app --reload
    Run frontend:    cd web; npm run dev
══════════════════════════════════════════════════════
```

Each row uses `[✓]`, `[⚠] Skipped`, or `[✗] Failed` as appropriate. The summary is always printed, even when steps have failed. Rows corresponding to skipped components (e.g. Rust when `-SkipRust`) show `[⚠] Skipped (-SkipRust)`.

---

## Error Handling Strategy

| Phase                     | Failure type    | Action                                                                               |
|---------------------------|-----------------|--------------------------------------------------------------------------------------|
| OS guard                  | Wrong OS        | `Write-Error` + `exit 1` (FATAL)                                                    |
| Python ≥ 3.12 check       | Version fail    | `Write-Error "Python 3.12+ required. Install: https://python.org/downloads/"` + `exit 1` (FATAL) |
| Venv activate             | PS error        | `Write-Error` + `exit 1` (FATAL — nothing works without active venv)               |
| Git not found             | Missing tool    | `Write-Status -Warn`; continue                                                      |
| Rust/cargo not found      | Missing tool    | `Write-Status -Warn`; `$script:HasRust = $false`; continue                         |
| Rust version < 1.80       | Old version     | `Write-Status -Warn "Rust <1.80 — upgrade recommended"`; allow build to proceed    |
| Node/npm not found        | Missing tool    | `Write-Status -Warn`; `$script:HasNode = $false`; continue                         |
| Node version < v18        | Old version     | `Write-Status -Warn "Node <v18 LTS — upgrade recommended"`; continue               |
| pip upgrade fails         | pip error       | `Write-Status -Warn`; continue (usually non-critical)                               |
| `requirements.txt` fail   | pip error       | `Write-Status -Fail`; `exit 1` (FATAL — core deps required)                        |
| `backend/requirements` fail | pip error     | `Write-Status -Fail`; `exit 1` (FATAL — backend deps required)                     |
| `requirements-ci.txt` fail | pip error      | `Write-Status -Warn`; continue (dev tools optional)                                 |
| maturin standalone fail   | pip error       | `Write-Status -Warn`; `$script:HasRust = $false`; skip Rust build                  |
| `maturin develop` fails   | build error     | `Write-Status -Fail` + `$_.Exception.Message`; continue (runtime still works)      |
| `setup_structure.py` fails | script error   | `Write-Status -Warn`; continue                                                      |
| `npm install` fails       | npm error       | `Write-Status -Fail` + error; `Pop-Location` in `finally`; continue                |

**Pattern used in each phase:**
```powershell
try {
    # phase commands
    Write-Status -Ok "Phase description"
} catch {
    Write-Status -Fail "Phase failed: $_"
    # fatal phases only: exit 1
}
```

---

## Constraints for @6code

1. **Target platform:** Windows only. Script must abort early on Linux/macOS.
2. **File location:** `install.ps1` at repo root — not inside `scripts/` or any subdirectory.
3. **PowerShell version:** `#Requires -Version 5.1` (Windows PowerShell compatibility).
4. **Python minimum:** 3.12 exactly — not 3.11 as stated in outdated `docs/setup.md`.
5. **Venv location:** `.venv` at repo root. No alternate paths.
6. **Requirements install order:** pip upgrade → `requirements.txt` → `backend/requirements.txt` → `requirements-ci.txt` → maturin (standalone). Never install `requirements-ci.txt` before `requirements.txt`.
7. **maturin install logic:**
   - If `-SkipDev` is NOT set: maturin comes from `requirements-ci.txt` (pinned at `1.12.5`). Do NOT install it a second time.
   - If `-SkipDev` IS set and Rust build is needed: `pip install --prefer-binary "maturin>=1.0,<2.0"`.
8. **Rust build:** Only `rust_core/Cargo.toml` via `maturin develop`. Do NOT build `rust_core/p2p/`.
9. **Rust build failure:** Non-fatal. Script must not `exit 1` on Rust build failure.
10. **web/ directory change:** Use `Push-Location`/`Pop-Location` pattern, never bare `cd`. Always call `Pop-Location` in a `finally` block.
11. **No `Set-ExecutionPolicy` inside the script.** Add a comment at the very top (before `param()`) noting users may need: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`.
12. **Idempotent design:** Re-running the script on an existing setup must be safe. Venv re-used (not recreated) by default; use `-Force` to recreate.
13. **`$ErrorActionPreference = 'Stop'`** is set at the top of the script. Where individual external commands are expected to exit non-zero without being an error (e.g. version probes), use `2>&1` capture and parse the output rather than relying on exit codes.
14. **No `Write-Error` for non-fatal conditions.** Use `Write-Status -Warn` or `Write-Status -Fail` for non-fatal issues; reserve `Write-Error` + `exit 1` for truly fatal conditions only.
15. **Summary table always printed** — even when steps fail. Use a `$script:Summary` ordered list populated throughout execution and printed in `Show-Summary`.
16. **`scripts/setup_structure.py`** must be called with the venv-activated `python` (not a system python). Since venv is activated before this step, `python` on PATH is sufficient.
17. **Node version floor:** Warn if `node --version` reports < v18 LTS (no hard fail).
18. **No application source code changes.** No CI workflow changes. Only `install.ps1` is created (a `README.md` update referencing the new script is in scope per `project.md`).
19. **Execution policy comment** must suggest the minimal scope: `-Scope Process`, not `-Scope CurrentUser` or `-Scope LocalMachine`.
