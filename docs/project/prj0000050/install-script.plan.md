# Plan: prj0000050 — Install Script

## Status
Ready for implementation

## Pre-flight checks

| Item | Result |
|------|--------|
| `install.ps1` exists at repo root | **No** — must be created |
| `scripts/setup_structure.py` exists | **Yes** — call with venv-activated `python` |
| `tests/structure/` exists | **Yes** — add `test_install_script.py` there |

---

## Task 1 — Create `install.ps1`

**File:** `install.ps1` (repo root)  
**Action:** Create new file  
**Branch:** `prj0000050-install-script`

### 1.1 File header (lines 1–20)

```powershell
# To run: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# Then:   .\install.ps1 [-SkipRust] [-SkipWeb] [-SkipDev] [-CI] [-Force]
#Requires -Version 5.1
<#
.SYNOPSIS
    Developer setup script for PyAgent.
.DESCRIPTION
    Creates the Python .venv, installs core/backend/dev Python deps,
    optionally builds the Rust PyO3 extension, runs directory scaffolding,
    and installs frontend npm dependencies.
.PARAMETER SkipRust
    Skip Rust/cargo checks, maturin install, and maturin develop build.
.PARAMETER SkipWeb
    Skip Node/npm check and web/node_modules install.
.PARAMETER SkipDev
    Skip dev/CI tooling (requirements-ci.txt).
.PARAMETER CI
    Non-interactive mode; suppress prompts; treat optional warnings as non-fatal.
.PARAMETER Force
    Delete and recreate .venv even if it already exists.
#>
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

### 1.2 OS guard (immediately after `param` block)

```powershell
if ($IsLinux -or $IsMacOS) {
    Write-Error "install.ps1 is Windows-only. Use bash scripts on Linux/macOS."
    exit 1
}
```

### 1.3 Script-scope state variables

```powershell
$script:HasRust    = $true
$script:HasNode    = $true
$script:Summary    = [System.Collections.Generic.List[string]]::new()
```

### 1.4 Function: `Write-Status`

**Signature:** `Write-Status [string]$Message [-Ok] [-Warn] [-Fail] [-Skip]`

Exactly one style switch must be provided. Outputs via `Write-Host` with the colour and prefix defined below:

| Switch  | Prefix  | ForegroundColor |
|---------|---------|-----------------|
| `-Ok`   | `[✓]`   | Green           |
| `-Warn` | `[⚠]`   | Yellow          |
| `-Fail` | `[✗]`   | Red             |
| `-Skip` | `[→]`   | Cyan            |

No switch → default to Cyan `[→]`.

### 1.5 Function: `Test-Prerequisites`

Sets `$script:HasRust` and `$script:HasNode`. Called before any install step.

**Step 1 — Python version (FATAL on failure)**
- Run: `$v = python --version 2>&1`
- Parse the version number using regex `(\d+)\.(\d+)`.
- If major < 3 or (major == 3 and minor < 12): `Write-Error "Python 3.12+ required. Install: https://python.org/downloads/"` then `exit 1`.
- On success: `Write-Status -Ok "Python $v"`

**Step 2 — Git (warn only)**
- Run: `git --version 2>&1`; if error or not found: `Write-Status -Warn "Git not found — version control unavailable"`.

**Step 3 — Rust/cargo (warn + flag)**
- Run: `$cv = cargo --version 2>&1`
- If command fails: `$script:HasRust = $false`; `Write-Status -Warn "cargo not found — Rust build will be skipped. Install via rustup.rs"`.
- If found: parse version number `(\d+)\.(\d+)`; if minor < 80 (i.e., version < 1.80): `Write-Status -Warn "Rust <1.80 detected — upgrade recommended"`.
- On success with sufficient version: `Write-Status -Ok "cargo $cv"`.

**Step 4 — Node/npm (warn + flag)**
- Run: `$nv = node --version 2>&1`; if fails: `$script:HasNode = $false`; `Write-Status -Warn "node not found — frontend install will be skipped"`.
- Run: `npm --version 2>&1`; if fails: `$script:HasNode = $false`; `Write-Status -Warn "npm not found — frontend install will be skipped"`.
- If node found: parse major version from `v(\d+)`; if major < 18: `Write-Status -Warn "Node <v18 LTS — upgrade recommended"`.
- On success: `Write-Status -Ok "node $nv"`.

### 1.6 Function: `Initialize-Venv`

```
if ($Force -and (Test-Path .venv)) {
    Remove-Item -Recurse -Force .venv
    Write-Status -Skip "Removed existing .venv (-Force)"
}
if (Test-Path .venv) {
    Write-Status -Skip "Reusing existing .venv"
} else {
    python -m venv .venv
    Write-Status -Ok "Created .venv"
}
# Activate — fatal if fails
try {
    .\.venv\Scripts\Activate.ps1
    Write-Status -Ok "Activated .venv"
} catch {
    Write-Error "Failed to activate .venv: $_"
    exit 1
}
```

Append `"[✓] Python venv .venv"` to `$script:Summary`.

### 1.7 Function: `Install-Python`

Each sub-step uses `try/catch`. Steps 2 and 3 are **fatal**; all others are non-fatal.

| # | Command | Fatal? | Summary label |
|---|---------|--------|---------------|
| 1 | `pip install --upgrade pip` | No | — |
| 2 | `pip install --prefer-binary -r requirements.txt` | **Yes** | `[✓] Core deps requirements.txt` |
| 3 | `pip install --prefer-binary -r backend/requirements.txt` | **Yes** | `[✓] Backend deps backend/requirements.txt` |
| 4 | `pip install --prefer-binary -r requirements-ci.txt` (unless `-SkipDev`) | No | `[✓] Dev tools requirements-ci.txt` |
| 5 | `pip install --prefer-binary "maturin>=1.0,<2.0"` (only if `-SkipDev` AND `$script:HasRust -and -not $SkipRust`) | No | — |

Step 5 must NOT run when `-SkipDev` is false (maturin already comes from `requirements-ci.txt`).  
If step 5 fails: `$script:HasRust = $false`; skip Rust build.

### 1.8 Function: `Build-Rust`

**Guard:** Return immediately if `$SkipRust` or `-not $script:HasRust`.  
If skipping: `$script:Summary.Add("[⚠] Rust extension Skipped")`.

```
try {
    maturin develop --manifest-path rust_core/Cargo.toml
    Write-Status -Ok "Rust extension built"
    $script:Summary.Add("[✓] Rust extension rust_core/_rust_core built")
} catch {
    Write-Status -Fail "maturin develop failed: $_"
    $script:Summary.Add("[✗] Rust extension FAILED")
    # NON-FATAL — do not exit 1
}
```

### 1.9 Function: `Install-Scaffold`

```
try {
    python scripts/setup_structure.py
    Write-Status -Ok "Directory scaffolding complete"
    $script:Summary.Add("[✓] Scaffolding scripts/setup_structure.py")
} catch {
    Write-Status -Warn "setup_structure.py failed (non-fatal): $_"
    $script:Summary.Add("[⚠] Scaffolding FAILED (non-fatal)")
}
```

### 1.10 Function: `Install-Node`

**Guard:** Return immediately if `$SkipWeb` or `-not $script:HasNode`.  
If skipping: `$script:Summary.Add("[⚠] Web deps Skipped")`.

```
try {
    Push-Location web
    npm install
    $script:Summary.Add("[✓] Web deps web/node_modules")
} catch {
    Write-Status -Fail "npm install failed: $_"
    $script:Summary.Add("[✗] Web deps FAILED")
} finally {
    Pop-Location
}
```

### 1.11 Function: `Show-Summary`

Prints the decorated summary block:

```
══════════════════════════════════════════════════════
  PyAgent Install — Complete
══════════════════════════════════════════════════════
  [each $script:Summary line]

  Next steps:
    Run tests:       python -m pytest -q
    Run backend:     uvicorn backend.app:app --reload
    Run frontend:    cd web; npm run dev
══════════════════════════════════════════════════════
```

Always printed, even if steps failed.

### 1.12 Execution flow (main body, after function definitions)

```powershell
# Banner
Write-Host ("═" * 54) -ForegroundColor Cyan
$mode = if ($CI) { "CI" } else { "standard" }
Write-Host "  PyAgent — Developer Install Script"
Write-Host "  Run: $(Get-Date -Format 'yyyy-MM-dd')  Mode: $mode"
Write-Host ("═" * 54) -ForegroundColor Cyan

Test-Prerequisites
Initialize-Venv
Install-Python
Build-Rust
Install-Scaffold
Install-Node
Show-Summary
```

---

## Task 2 — Write code notes

**File:** `docs/project/prj0000050/install-script.code.md`  
**Action:** Create new file

### Content specification

The file must capture implementation notes for @6code. Required sections:

1. **Constraint checklist** — numbered list reproducing the 19 constraints from `install-script.design.md §Constraints for @6code`, each marked `[ ]` for @6code to check off.
2. **Version parsing patterns** — exact PowerShell regex snippets for:
   - Python: `if ($v -match '(\d+)\.(\d+)') { [int]$Matches[1]; [int]$Matches[2] }`
   - Rust: `if ($cv -match '(\d+)\.(\d+)') { [int]$Matches[2] }` (minor only matters; major is always 1)
   - Node: `if ($nv -match 'v(\d+)') { [int]$Matches[1] }`
3. **Idempotency notes** — explain why re-running is safe (venv reuse, `--prefer-binary` for fast skips when already installed).
4. **`$script:Summary` population guide** — table showing which function adds which string in which outcome state.
5. **Test file specification** — `tests/structure/test_install_script.py`: list the exact test functions `@6code` must implement (see §Acceptance Criteria below).

---

## Acceptance Criteria

The following criteria are testable by @7exec:

1. `.\install.ps1 -SkipRust -SkipWeb -SkipDev` completes with exit code 0 in an environment that has Python ≥ 3.12.
2. A `.venv` directory exists after the run.
3. `.\install.ps1 -SkipRust -SkipWeb -SkipDev` run a second time detects the existing `.venv` and does not recreate it (script prints `Reusing existing .venv`).
4. `.\install.ps1 -Force -SkipRust -SkipWeb -SkipDev` recreates the `.venv` (old `.venv` removed and new one created).
5. `.\install.ps1 -SkipRust -SkipWeb` (dev deps included) installs ruff, mypy, and pytest — verifiable by checking that `.venv\Scripts\ruff.exe` exists.
6. Script prints a summary block at the end (output contains `PyAgent Install — Complete`).
7. `Get-Help .\install.ps1` shows synopsis and parameter descriptions (requires `.SYNOPSIS`, `.DESCRIPTION`, and `.PARAMETER` comment blocks).
8. `python -m pytest tests/structure/test_install_script.py -v` passes.

---

## Validation Commands

Run these commands exactly (in order) to verify all acceptance criteria:

```powershell
# AC1 + AC2 — Basic install completes and .venv created
.\install.ps1 -SkipRust -SkipWeb -SkipDev
$LASTEXITCODE    # must be 0
Test-Path .venv  # must be True

# AC3 — Second run reuses .venv
$out = .\install.ps1 -SkipRust -SkipWeb -SkipDev 2>&1 | Out-String
$out -match 'Reusing existing .venv'  # must be True

# AC4 — Force recreates .venv
$ts_before = (Get-Item .venv).CreationTime
.\install.ps1 -Force -SkipRust -SkipWeb -SkipDev
$ts_after  = (Get-Item .venv).CreationTime
$ts_after -gt $ts_before  # must be True

# AC5 — Dev deps install (ruff present in venv)
.\install.ps1 -SkipRust -SkipWeb
Test-Path .venv\Scripts\ruff.exe  # must be True

# AC6 — Summary block in output
$out = .\install.ps1 -SkipRust -SkipWeb -SkipDev 2>&1 | Out-String
$out -match 'PyAgent Install — Complete'  # must be True

# AC7 — Get-Help works
Get-Help .\install.ps1  # must display SYNOPSIS and PARAMETERS (no error)

# AC8 — Pytest test suite passes
python -m pytest tests/structure/test_install_script.py -v
```

---

## Test file specification

`tests/structure/test_install_script.py` must be created by @6code and contain the following test functions:

| Function | What it tests | Method |
|----------|---------------|--------|
| `test_install_ps1_exists` | `install.ps1` file exists at repo root | `os.path.isfile` |
| `test_requires_version_header` | First 30 lines contain `#Requires -Version 5.1` | `read + in` |
| `test_has_synopsis_block` | File contains `.SYNOPSIS` comment | `read + in` |
| `test_has_parameter_docs` | File contains `.PARAMETER SkipRust`, `.PARAMETER Force`, `.PARAMETER CI` | string scan |
| `test_os_guard_present` | File contains `$IsLinux -or $IsMacOS` | string scan |
| `test_param_block_present` | File contains all 5 parameters: `SkipRust`, `SkipWeb`, `SkipDev`, `CI`, `Force` | string scan |
| `test_venv_path_is_dot_venv` | File does not reference `.virtualenv`, `venv/` (non-standard paths) | negative string scan |
| `test_force_param_present` | File contains `Remove-Item` (for `-Force` logic) | string scan |
| `test_summary_function_present` | File contains `Show-Summary` function | string scan |
| `test_push_location_pattern` | File uses `Push-Location web` and `Pop-Location` (not bare `cd`) | string scan |
| `test_no_set_execution_policy_in_script` | File does NOT contain `Set-ExecutionPolicy` as a command (only as a comment) | verify only in comment |
| `test_error_action_preference_stop` | File contains `$ErrorActionPreference = 'Stop'` | string scan |
| `test_execution_policy_comment` | File contains `Set-ExecutionPolicy` in a comment (for user guidance) | string scan |

All tests use only the standard library (`os`, `pathlib`). No subprocess calls that actually invoke the script.

---

## Dependencies

| Dependency | Status |
|-----------|--------|
| `install-script.think.md` | Complete |
| `install-script.design.md` | Complete |
| `scripts/setup_structure.py` | Exists at repo |
| `requirements.txt` | Exists at repo root |
| `backend/requirements.txt` | Exists at `backend/` |
| `requirements-ci.txt` | Exists at repo root |
| `web/` with `package.json` | Exists at repo |
| `rust_core/Cargo.toml` | Exists at `rust_core/` |

---

## File deliverables

| File | Status |
|------|--------|
| `install.ps1` | To create (Task 1) |
| `docs/project/prj0000050/install-script.code.md` | To create (Task 2) |
| `tests/structure/test_install_script.py` | To create (part of Task 2 spec) |
