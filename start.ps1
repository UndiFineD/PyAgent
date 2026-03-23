#!/usr/bin/env pwsh
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# start.ps1 — Launch PyAgent dev stack (backend + Vite) from .env config
#
# Usage:
#   .\start.ps1              # starts all services
#   .\start.ps1 -NoVite      # skip Vite (API-only mode)
#   .\start.ps1 -Help        # show this help

param(
    [switch]$NoVite,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = $PSScriptRoot

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
if ($Help) {
    Write-Host @"
start.ps1 - PyAgent dev stack launcher

Usage:
  .\start.ps1              Start Rust runtime (embedded), Python backend and Vite
  .\start.ps1 -NoVite      Start backend only (no Vite dev server)
  .\start.ps1 -Help        Show this help

Services:
  backend   Python FastAPI/WebSocket worker  (BACKEND_PORT)
  vite      Vite dev server                  (VITE_PORT)

The Rust runtime (rust_core) is a PyO3 extension embedded in the Python
backend process. A standalone runtime binary (RUNTIME_PORT) will be launched
automatically once built at: rust_core\runtime\target\release\runtime.exe
"@
    exit 0
}

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
$EnvFile = Join-Path $Root ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "[start] ERROR: .env not found. Copy .env.template to .env and configure it." -ForegroundColor Red
    exit 1
}

Write-Host "[start] Loading $EnvFile ..." -ForegroundColor Cyan

$EnvVars = @{}
foreach ($line in Get-Content $EnvFile) {
    # skip blank lines, comments, and powershell-style lines
    if ($line -match '^\s*$' -or $line -match '^\s*#' -or $line -match '^\$env:') { continue }
    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
        $key   = $Matches[1]
        $value = $Matches[2].Trim().Trim('"').Trim("'")
        $EnvVars[$key] = $value
        [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

# Resolve port/host with defaults
$Host_   = if ($EnvVars["HOST"])         { $EnvVars["HOST"] }         else { "0.0.0.0" }
$BackendPort = if ($EnvVars["BACKEND_PORT"]) { $EnvVars["BACKEND_PORT"] } else { "444" }
$VitePort    = if ($EnvVars["VITE_PORT"])    { $EnvVars["VITE_PORT"] }    else { "44" }
$RuntimePort = if ($EnvVars["RUNTIME_PORT"]) { $EnvVars["RUNTIME_PORT"] } else { "4000" }

Write-Host "[start] HOST=$Host_  BACKEND_PORT=$BackendPort  VITE_PORT=$VitePort  RUNTIME_PORT=$RuntimePort" -ForegroundColor Cyan

# ---------------------------------------------------------------------------
# Build shared env block passed into each child window
# ---------------------------------------------------------------------------
# Serialize only the vars loaded from .env so child windows inherit them
$EnvBlock = ($EnvVars.GetEnumerator() | ForEach-Object {
    "`$env:$($_.Key) = '$($_.Value)'"
}) -join "; "

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
function Start-DevWindow {
    param(
        [string]$Title,
        [string]$Command,
        [string]$Cwd = $Root
    )
    $escaped = $Command -replace '"', '\"'
    $fullCmd  = "$EnvBlock; Set-Location '$Cwd'; Write-Host '--- $Title ---' -ForegroundColor Green; $escaped"
    $proc = Start-Process pwsh -ArgumentList "-NoExit", "-Command", $fullCmd `
        -WorkingDirectory $Cwd `
        -PassThru
    Write-Host "[start] Started '$Title'  (PID $($proc.Id))" -ForegroundColor Green
    return $proc
}

# ---------------------------------------------------------------------------
# 1. Standalone Rust runtime binary (optional — skipped if not built yet)
# ---------------------------------------------------------------------------
$RuntimeExe = Join-Path $Root "rust_core\runtime\target\release\runtime.exe"
$RuntimeProc = $null

if (Test-Path $RuntimeExe) {
    Write-Host "[start] Found Rust runtime binary, starting on port $RuntimePort ..." -ForegroundColor Cyan
    $RuntimeProc = Start-DevWindow `
        -Title "runtime (port $RuntimePort)" `
        -Command "& '$RuntimeExe' --port $RuntimePort --host $Host_"
} else {
    Write-Host "[start] Rust runtime binary not found (expected: rust_core\runtime\target\release\runtime.exe)" -ForegroundColor Yellow
    Write-Host "[start] Rust runtime runs embedded inside the Python backend process — OK for development." -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# 2. Python backend  (includes embedded rust_core PyO3 runtime)
# ---------------------------------------------------------------------------
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "[start] ERROR: venv not found at .venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "[start] Run: python -m venv .venv && .venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

$BackendProc = Start-DevWindow `
    -Title "backend (port $BackendPort)" `
    -Command "& '$VenvPython' -m backend"

# ---------------------------------------------------------------------------
# 3. Vite dev server
# ---------------------------------------------------------------------------
$ViteProc = $null
if (-not $NoVite) {
    $WebDir = Join-Path $Root "web"
    $NpmCmd = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $NpmCmd) {
        Write-Host "[start] WARNING: npm not found — skipping Vite. Install Node.js to enable the frontend." -ForegroundColor Yellow
    } elseif (-not (Test-Path (Join-Path $WebDir "node_modules"))) {
        Write-Host "[start] node_modules missing — running npm install first ..." -ForegroundColor Yellow
        Push-Location $WebDir
        npm install
        Pop-Location
    }

    if ($NpmCmd) {
        $ViteProc = Start-DevWindow `
            -Title "vite (port $VitePort)" `
            -Command "npm run dev -- --port $VitePort --host $Host_" `
            -Cwd $WebDir
    }
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "PyAgent dev stack started:" -ForegroundColor Green
if ($RuntimeProc)  { Write-Host "  runtime  http://$Host_`:$RuntimePort  (PID $($RuntimeProc.Id))" }
if ($BackendProc)  { Write-Host "  backend  http://$Host_`:$BackendPort  (PID $($BackendProc.Id))" }
if ($ViteProc)     { Write-Host "  vite     http://$Host_`:$VitePort     (PID $($ViteProc.Id))" }
Write-Host ""
Write-Host "Close the individual windows or press Ctrl+C here to stop all processes." -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------------------------
# Wait and handle Ctrl+C to kill children
# ---------------------------------------------------------------------------
$AllProcs = @($BackendProc, $ViteProc, $RuntimeProc) | Where-Object { $_ -ne $null }

try {
    while ($true) {
        $AllProcs = $AllProcs | Where-Object { -not $_.HasExited }
        if ($AllProcs.Count -eq 0) {
            Write-Host "[start] All processes have exited." -ForegroundColor Yellow
            break
        }
        Start-Sleep -Seconds 2
    }
} finally {
    Write-Host "[start] Stopping all services ..." -ForegroundColor Cyan
    foreach ($proc in $AllProcs) {
        if (-not $proc.HasExited) {
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
            Write-Host "[start] Stopped PID $($proc.Id)" -ForegroundColor Yellow
        }
    }
}
