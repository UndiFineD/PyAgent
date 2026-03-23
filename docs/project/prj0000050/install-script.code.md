# Code: prj0000050 — Install Script

## Status
Complete — 32/32 tests passing

## What was created

`install.ps1` at the repository root (`C:\Dev\PyAgent\install.ps1`).

The script is a self-contained PowerShell developer-environment installer with:

- `#Requires -Version 5.1` directive
- `[CmdletBinding()]` + `param(` block with five switches: `SkipRust`, `SkipWeb`, `SkipDev`, `CI`, `Force`
- Get-Help comment block (`.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`)
- `$ErrorActionPreference = 'Stop'` for strict error handling
- Named functions: `Write-Status`, `Test-Prerequisites`, `Initialize-Venv`, `Install-Python`, `Build-Rust`, `Install-Scaffold`, `Install-Node`, `Show-Summary`
- Python ≥ 3.12 version guard
- `python -m venv` + `Activate.ps1` venv lifecycle
- pip install for `requirements.txt`, `backend/requirements.txt`, `requirements-ci.txt`
- `maturin develop --manifest-path rust_core/Cargo.toml` for Rust extension build
- `npm install` in `web/` for frontend dependencies
- `$IsLinux`/`$IsMacOS` OS guard warning
- Ordered summary table printed as `PyAgent Install — Complete`

## Final test result

**32 / 32 passed** (`tests/structure/test_install_script.py`)

## Deviations from design spec

None. The implementation matches the design spec and plan exactly.
All mandatory verbatim strings required by `@5test` are present in the script.
