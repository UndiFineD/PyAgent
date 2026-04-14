#Requires -Version 5.1
<#
.SYNOPSIS
    Install all PyAgent developer dependencies.

.DESCRIPTION
    Sets up a complete PyAgent development environment on Windows:
    • Python virtual environment (.venv)
    • Core and backend Python packages
    • Dev/CI tooling (ruff, mypy, pytest, etc.) — unless -SkipDev
    • Rust extension via maturin — unless -SkipRust
    • Node.js web dependencies — unless -SkipWeb

.PARAMETER SkipRust
    Skip Rust toolchain check and maturin develop build.

.PARAMETER SkipWeb
    Skip Node/npm check and web/node_modules installation.

.PARAMETER SkipDev
    Skip requirements-ci.txt (dev/CI tooling).

.PARAMETER CI
    Non-interactive mode. Missing optional tools are warnings, not prompts.

.PARAMETER Force
    Force recreation of .venv even if it already exists.

.PARAMETER SkipOptionalTooling
    Skip optional developer tooling checks/installs (rg, fd, ast-grep, jq, yq, semgrep, tokei, delta, hyperfine, just, uv).

.PARAMETER InstallPostgresServer
    Attempt optional PostgreSQL server install (non-fatal). Client checks always run in optional tooling phase.

.EXAMPLE
    .\install.ps1
    Full installation.

.EXAMPLE
    .\install.ps1 -SkipRust -SkipWeb
    Python only (no Rust extension, no web deps).

.EXAMPLE
    .\install.ps1 -Force
    Recreate .venv and reinstall everything.
#>
[CmdletBinding()]
param(
    [switch]$SkipRust,
    [switch]$SkipWeb,
    [switch]$SkipDev,
    [switch]$CI,
    [switch]$Force,
    [switch]$SkipOptionalTooling,
    [switch]$InstallPostgresServer
)

$ErrorActionPreference = 'Stop'

# Track state
$script:HasRust  = $false
$script:HasNode  = $false
$script:Summary  = [ordered]@{}

# ── Helpers ──────────────────────────────────────────────────────────────────

function Write-Status {
    param([string]$Icon, [string]$Message, [string]$Color = 'White')
    Write-Host "  [$Icon] $Message" -ForegroundColor $Color
}


function Test-CommandAvailable {
    param([Parameter(Mandatory = $true)][string]$CommandName)
    return [bool](Get-Command $CommandName -ErrorAction SilentlyContinue)
}


function Install-WingetPackage {
    param(
        [Parameter(Mandatory = $true)][string]$PackageId,
        [Parameter(Mandatory = $true)][string]$DisplayName
    )

    if (-not (Test-CommandAvailable -CommandName 'winget')) {
        Write-Status '⚠' "winget not available; cannot install optional package $DisplayName ($PackageId)" 'Yellow'
        return $false
    }

    if ($CI) {
        Write-Status '⚠' "CI mode: check-only for $DisplayName (installation skipped)" 'Yellow'
        return $false
    }

    try {
        & winget install --id $PackageId --accept-package-agreements --accept-source-agreements --silent --disable-interactivity --exact
        if ($LASTEXITCODE -eq 0) {
            Write-Status '✓' "$DisplayName installed via winget ($PackageId)" 'Green'
            return $true
        }
        Write-Status '⚠' "$DisplayName install exited with code $LASTEXITCODE (non-fatal)" 'Yellow'
        return $false
    } catch {
        Write-Status '⚠' "Failed to install $DisplayName ($PackageId): $_" 'Yellow'
        return $false
    }
}


function Ensure-OptionalTooling {
    if ($SkipOptionalTooling) {
        Write-Status '⚠' "Optional tooling phase skipped (-SkipOptionalTooling)" 'Yellow'
        $script:Summary['Optional tooling'] = "skipped (-SkipOptionalTooling)"
        return
    }

    Write-Host "`nOptional developer tooling..." -ForegroundColor Cyan

    $tools = @(
        @{ Name = 'ripgrep'; Command = 'rg'; PackageId = 'BurntSushi.ripgrep.MSVC' },
        @{ Name = 'fd'; Command = 'fd'; PackageId = 'sharkdp.fd' },
        @{ Name = 'ast-grep'; Command = 'ast-grep'; PackageId = 'ast-grep.ast-grep' },
        @{ Name = 'jq'; Command = 'jq'; PackageId = 'jqlang.jq' },
        @{ Name = 'yq'; Command = 'yq'; PackageId = 'MikeFarah.yq' },
        @{ Name = 'semgrep'; Command = 'semgrep'; PackageId = 'Semgrep.Semgrep' },
        @{ Name = 'tokei'; Command = 'tokei'; PackageId = 'XAMPPRocky.tokei' },
        @{ Name = 'delta (difft alternative)'; Command = 'delta'; PackageId = 'dandavison.delta' },
        @{ Name = 'hyperfine'; Command = 'hyperfine'; PackageId = 'sharkdp.hyperfine' },
        @{ Name = 'just'; Command = 'just'; PackageId = 'Casey.Just' },
        @{ Name = 'uv'; Command = 'uv'; PackageId = 'Astral-sh.uv' }
    )

    $installed = 0
    $already = 0
    $missing = 0

    foreach ($tool in $tools) {
        if (Test-CommandAvailable -CommandName $tool.Command) {
            Write-Status '✓' "$($tool.Name) found ($($tool.Command))" 'Green'
            $already++
            continue
        }

        Write-Status '⚠' "$($tool.Name) missing ($($tool.Command))" 'Yellow'
        if (Install-WingetPackage -PackageId $tool.PackageId -DisplayName $tool.Name) {
            $installed++
        } else {
            $missing++
        }
    }

    # PostgreSQL tooling (client first, optional server install path)
    if (Test-CommandAvailable -CommandName 'psql') {
        Write-Status '✓' "PostgreSQL client found (psql)" 'Green'
    } else {
        Write-Status '⚠' "PostgreSQL client (psql) not found" 'Yellow'
        [void](Install-WingetPackage -PackageId 'PostgreSQL.PostgreSQL' -DisplayName 'PostgreSQL client/server bundle')
    }

    if ($InstallPostgresServer) {
        Write-Status '…' "Optional PostgreSQL server install requested" 'Cyan'
        [void](Install-WingetPackage -PackageId 'PostgreSQL.PostgreSQL' -DisplayName 'PostgreSQL server')
    } else {
        Write-Status '⚠' "PostgreSQL server install skipped (use -InstallPostgresServer to opt in)" 'Yellow'
    }

    $script:Summary['Optional tooling'] = "found=$already installed=$installed missing=$missing"
}

# ── Phase 1: Prerequisites ────────────────────────────────────────────────────

function Test-Prerequisites {
    Write-Host "`nChecking prerequisites..." -ForegroundColor Cyan

    # Python (required, ≥ 3.12)
    try {
        $pyVer = & python --version 2>&1
        if ($pyVer -match '(\d+)\.(\d+)') {
            $major = [int]$Matches[1]; $minor = [int]$Matches[2]
            if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
                Write-Status '✗' "Python $major.$minor found — need ≥ 3.12. Install from https://python.org" 'Red'
                throw "Python ≥ 3.12 required. Aborting."
            }
            Write-Status '✓' "Python $major.$minor" 'Green'
            $script:Summary['Python'] = "Python $major.$minor ✓"
        }
    } catch [System.Management.Automation.CommandNotFoundException] {
        Write-Status '✗' "Python not found. Install from https://python.org" 'Red'
        throw "Python not found. Aborting."
    }

    # Git (warn only)
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Status '⚠' "Git not found. Install from https://git-scm.com" 'Yellow'
    } else {
        Write-Status '✓' "Git $(git --version)" 'Green'
    }

    # Rust / cargo (optional)
    if (-not $SkipRust) {
        if (Get-Command cargo -ErrorAction SilentlyContinue) {
            $script:HasRust = $true
            Write-Status '✓' "Rust $(rustc --version)" 'Green'
        } else {
            Write-Status '⚠' "cargo not found — Rust extension will be skipped. Install from https://rustup.rs" 'Yellow'
        }
    } else {
        Write-Status '⚠' "Rust skipped (-SkipRust)" 'Yellow'
    }

    # Node / npm (optional)
    if (-not $SkipWeb) {
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            $script:HasNode = $true
            Write-Status '✓' "Node $(node --version) / npm $(npm --version)" 'Green'
        } else {
            Write-Status '⚠' "npm not found — web deps will be skipped. Install from https://nodejs.org" 'Yellow'
        }
    } else {
        Write-Status '⚠' "Node/npm skipped (-SkipWeb)" 'Yellow'
    }

    # OS guard — warn on non-Windows
    if ($IsLinux -or $IsMacOS) {
        Write-Status '⚠' "Non-Windows OS detected. Script optimised for Windows; some paths may differ." 'Yellow'
    }
}

# ── Phase 2: Virtual environment ─────────────────────────────────────────────

function Initialize-Venv {
    Write-Host "`nPython virtual environment..." -ForegroundColor Cyan
    $venvPath = Join-Path $PSScriptRoot '.venv'

    if ((Test-Path $venvPath) -and -not $Force) {
        Write-Status '✓' "Reusing existing .venv" 'Green'
        $script:Summary['Venv'] = ".venv reused ✓"
    } else {
        if ((Test-Path $venvPath) -and $Force) {
            Write-Status '⚠' "Removing existing .venv (-Force)" 'Yellow'
            try {
                Remove-Item $venvPath -Recurse -Force -ErrorAction Stop
            } catch {
                Write-Status '⚠' "Could not fully remove .venv (some files in use by another process)." 'Yellow'
                Write-Status '⚠' "Close other Python processes / VS Code terminals and retry, or skip -Force." 'Yellow'
                Write-Status '⚠' "Continuing with existing .venv..." 'Yellow'
                $script:Summary['Venv'] = ".venv in-use — reused (Force partial failure)"
                $usedExistingVenv = $true
            }
        }
        if (-not $usedExistingVenv) {
            Write-Status '…' "Creating .venv" 'Cyan'
            & python -m venv $venvPath
            Write-Status '✓' ".venv created" 'Green'
            $script:Summary['Venv'] = ".venv created ✓"
        }
    }

    # Activate
    $activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'
    if (-not (Test-Path $activateScript)) {
        throw "Activate.ps1 not found at $activateScript"
    }
    . $activateScript
    Write-Status '✓' ".venv activated" 'Green'
}

# ── Phase 3: Python packages ──────────────────────────────────────────────────

function Install-Python {
    Write-Host "`nInstalling Python packages..." -ForegroundColor Cyan

    try {
        Write-Status '…' "Upgrading pip" 'Cyan'
        & python -m pip install --upgrade pip --quiet
        Write-Status '✓' "pip upgraded" 'Green'

        Write-Status '…' "Installing requirements.txt" 'Cyan'
        & python -m pip install --prefer-binary -r requirements.txt --quiet
        Write-Status '✓' "requirements.txt installed" 'Green'
        $script:Summary['Core deps'] = "requirements.txt ✓"

        Write-Status '…' "Installing backend/requirements.txt" 'Cyan'
        & python -m pip install --prefer-binary -r backend/requirements.txt --quiet
        Write-Status '✓' "backend/requirements.txt installed" 'Green'
        $script:Summary['Backend deps'] = "backend/requirements.txt ✓"

        if (-not $SkipDev) {
            Write-Status '…' "Installing requirements-ci.txt (dev tools)" 'Cyan'
            & python -m pip install --prefer-binary -r requirements-ci.txt --quiet
            Write-Status '✓' "requirements-ci.txt installed" 'Green'
            $script:Summary['Dev tools'] = "requirements-ci.txt ✓"

            Write-Status '…' "Running dependency parity preflight" 'Cyan'
            & python scripts/deps/check_dependency_parity.py --check
            if ($LASTEXITCODE -ne 0) {
                throw "Dependency parity preflight failed. Regenerate requirements first."
            }
            Write-Status '✓' "Dependency parity preflight passed" 'Green'
        } else {
            Write-Status '⚠' "Dev tools skipped (-SkipDev)" 'Yellow'
            $script:Summary['Dev tools'] = "skipped (-SkipDev)"
        }

        # maturin — needed for Rust build; install inline only when -SkipDev is set
        # (otherwise requirements-ci.txt already covers the exact pin maturin==1.12.5)
        if ($script:HasRust -and -not $SkipRust -and $SkipDev) {
            Write-Status '…' "Installing maturin" 'Cyan'
            & python -m pip install "maturin==1.12.5" --quiet
            Write-Status '✓' "maturin installed" 'Green'
        }
    } catch {
        Write-Status '✗' "Python package install failed: $_" 'Red'
        throw
    }
}

# ── Phase 4: Rust extension ───────────────────────────────────────────────────

function Build-Rust {
    if (-not $script:HasRust -or $SkipRust) { return }
    Write-Host "`nBuilding Rust extension..." -ForegroundColor Cyan
    try {
        & maturin develop --manifest-path rust_core/Cargo.toml
        Write-Status '✓' "Rust extension built (rust_core)" 'Green'
        $script:Summary['Rust extension'] = "rust_core built ✓"
    } catch {
        Write-Status '⚠' "Rust build failed (non-fatal): $_" 'Yellow'
        $script:Summary['Rust extension'] = "build failed ⚠ (see above)"
    }
}

# ── Phase 5: Scaffold ─────────────────────────────────────────────────────────

function Install-Scaffold {
    Write-Host "`nRunning scaffold setup..." -ForegroundColor Cyan
    $scriptPath = Join-Path $PSScriptRoot 'scripts\setup_structure.py'
    if (Test-Path $scriptPath) {
        try {
            & python $scriptPath
            Write-Status '✓' "Scaffolding complete" 'Green'
            $script:Summary['Scaffolding'] = "scripts/setup_structure.py ✓"
        } catch {
            Write-Status '⚠' "Scaffold script failed (non-fatal): $_" 'Yellow'
            $script:Summary['Scaffolding'] = "failed ⚠ (non-fatal)"
        }
    } else {
        Write-Status '⚠' "scripts/setup_structure.py not found — skipping" 'Yellow'
        $script:Summary['Scaffolding'] = "skipped (not found)"
    }
}

# ── Phase 6: Node / web ───────────────────────────────────────────────────────

function Install-Node {
    if (-not $script:HasNode -or $SkipWeb) { return }
    Write-Host "`nInstalling web dependencies..." -ForegroundColor Cyan
    try {
        Push-Location (Join-Path $PSScriptRoot 'web')
        & npm install
        Pop-Location
        Write-Status '✓' "web/node_modules installed" 'Green'
        $script:Summary['Web deps'] = "web/node_modules ✓"
    } catch {
        Pop-Location -ErrorAction SilentlyContinue
        Write-Status '⚠' "npm install failed (non-fatal): $_" 'Yellow'
        $script:Summary['Web deps'] = "failed ⚠ (non-fatal)"
    }
}

# ── Phase 7: Summary ──────────────────────────────────────────────────────────

function Show-Summary {
    $bar = '═' * 54
    Write-Host "`n  $bar" -ForegroundColor Green
    Write-Host "  PyAgent Install — Complete" -ForegroundColor Green
    Write-Host "  $bar" -ForegroundColor Green
    foreach ($key in $script:Summary.Keys) {
        Write-Host ("  {0,-20} {1}" -f $key, $script:Summary[$key]) -ForegroundColor White
    }
    Write-Host "`n  Next steps:" -ForegroundColor Cyan
    Write-Host "    Run tests:       python -m pytest -q" -ForegroundColor White
    Write-Host "    Run backend:     uvicorn backend.app:app --reload" -ForegroundColor White
    Write-Host "    Run frontend:    cd web; npm run dev" -ForegroundColor White
    Write-Host "  $bar`n" -ForegroundColor Green
}

# ── Main ──────────────────────────────────────────────────────────────────────

Write-Host "`n  PyAgent Developer Install" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray

Test-Prerequisites
Initialize-Venv
Install-Python
Ensure-OptionalTooling
Build-Rust
Install-Scaffold
Install-Node
Show-Summary
