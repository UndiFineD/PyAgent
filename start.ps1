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
# start.ps1 — PyAgent dev stack manager
#
# Usage:
#   .\start.ps1 [start|stop|restart|status|help] [-NoVite]

param(
    [Parameter(Position = 0)]
    [ValidateSet("start", "stop", "restart", "status", "help", "")]
    [string]$Command = "start",

    [switch]$NoVite
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root    = $PSScriptRoot
$PidFile = Join-Path $Root ".pyagent.pids"

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
function Show-Help {
    Write-Host @"
start.ps1 - PyAgent dev stack manager

Usage:
  .\start.ps1 [command] [-NoVite]

Commands:
  start      Start all services (default)
  stop       Stop all running services
  restart    Stop then start all services
  status     Show which services are running
  help       Show this help

Flags:
  -NoVite    Skip the Vite dev server (backend only)

Services:
  runtime  Rust standalone binary — auto-launched when built  (RUNTIME_PORT)
  backend  Python FastAPI/WebSocket worker                     (BACKEND_PORT)
  vite     Vite dev server                                     (VITE_PORT)

The Rust runtime (rust_core) is a PyO3 extension embedded in the Python
backend process. A standalone binary (RUNTIME_PORT) will be launched
automatically once built at: rust_core\runtime\target\release\runtime.exe

PID file: .pyagent.pids
"@
}

if ($Command -eq "help") { Show-Help; exit 0 }

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
function Load-Env {
    $envFile = Join-Path $Root ".env"
    if (-not (Test-Path $envFile)) {
        Write-Host "[pyagent] ERROR: .env not found. Copy .env.template to .env and configure it." -ForegroundColor Red
        exit 1
    }
    $vars = @{}
    foreach ($line in Get-Content $envFile) {
        if ($line -match '^\s*$' -or $line -match '^\s*#' -or $line -match '^\$env:') { continue }
        if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
            $k = $Matches[1]
            $v = $Matches[2].Trim().Trim('"').Trim("'")
            $vars[$k] = $v
            [System.Environment]::SetEnvironmentVariable($k, $v, "Process")
        }
    }
    return $vars
}

# ---------------------------------------------------------------------------
# PID file helpers
# ---------------------------------------------------------------------------
function Save-Pids {
    param([hashtable]$Procs)
    $lines = $Procs.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }
    $lines | Set-Content $PidFile
}

function Read-Pids {
    if (-not (Test-Path $PidFile)) { return @{} }
    $map = @{}
    foreach ($line in Get-Content $PidFile) {
        if ($line -match '^([^=]+)=(\d+)$') { $map[$Matches[1]] = [int]$Matches[2] }
    }
    return $map
}

function Remove-PidFile {
    if (Test-Path $PidFile) { Remove-Item $PidFile -Force }
}

# ---------------------------------------------------------------------------
# Window launcher
# ---------------------------------------------------------------------------
function Start-DevWindow {
    param(
        [string]$Title,
        [string]$Cmd,
        [string]$Cwd = $Root,
        [string]$EnvBlock
    )
    $fullCmd = "$EnvBlock; Set-Location '$Cwd'; Write-Host '--- $Title ---' -ForegroundColor Green; $Cmd"
    $proc = Start-Process pwsh -ArgumentList "-NoExit", "-Command", $fullCmd `
        -WorkingDirectory $Cwd -PassThru
    Write-Host "[pyagent] Started '$Title'  (PID $($proc.Id))" -ForegroundColor Green
    return $proc
}

# ---------------------------------------------------------------------------
# STOP
# ---------------------------------------------------------------------------
function Invoke-Stop {
    $pids = Read-Pids
    if ($pids.Count -eq 0) {
        Write-Host "[pyagent] No running services found (no .pyagent.pids file)." -ForegroundColor Yellow
        return
    }
    Write-Host "[pyagent] Stopping services ..." -ForegroundColor Cyan
    foreach ($entry in $pids.GetEnumerator()) {
        $name = $entry.Key
        $pid_ = $entry.Value
        try {
            $proc = Get-Process -Id $pid_ -ErrorAction SilentlyContinue
            if ($proc -and -not $proc.HasExited) {
                Stop-Process -Id $pid_ -Force
                Write-Host "[pyagent] Stopped $name  (PID $pid_)" -ForegroundColor Yellow
            } else {
                Write-Host "[pyagent] $name (PID $pid_) was already stopped." -ForegroundColor DarkGray
            }
        } catch {
            Write-Host "[pyagent] Could not stop $name (PID $pid_): $_" -ForegroundColor DarkGray
        }
    }
    Remove-PidFile
    Write-Host "[pyagent] All services stopped." -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# STATUS
# ---------------------------------------------------------------------------
function Invoke-Status {
    $pids = Read-Pids
    if ($pids.Count -eq 0) {
        Write-Host "[pyagent] No services tracked (no .pyagent.pids file)." -ForegroundColor Yellow
        return
    }
    Write-Host ""
    Write-Host "PyAgent service status:" -ForegroundColor Cyan
    foreach ($entry in $pids.GetEnumerator() | Sort-Object Key) {
        $name = $entry.Key
        $pid_ = $entry.Value
        $proc = Get-Process -Id $pid_ -ErrorAction SilentlyContinue
        if ($proc -and -not $proc.HasExited) {
            Write-Host ("  {0,-12} PID {1,-8} RUNNING" -f $name, $pid_) -ForegroundColor Green
        } else {
            Write-Host ("  {0,-12} PID {1,-8} STOPPED" -f $name, $pid_) -ForegroundColor Red
        }
    }
    Write-Host ""
}

# ---------------------------------------------------------------------------
# START
# ---------------------------------------------------------------------------
function Invoke-Start {
    # Check nothing already running
    $existing = Read-Pids
    $alreadyRunning = $existing.GetEnumerator() | Where-Object {
        $proc = Get-Process -Id $_.Value -ErrorAction SilentlyContinue
        $proc -and -not $proc.HasExited
    }
    if ($alreadyRunning) {
        Write-Host "[pyagent] Services already running. Use 'restart' to reload or 'stop' first." -ForegroundColor Yellow
        Invoke-Status
        return
    }

    $EnvVars = Load-Env

    $Host_       = if ($EnvVars["HOST"])         { $EnvVars["HOST"] }         else { "0.0.0.0" }
    $BackendPort = if ($EnvVars["BACKEND_PORT"]) { $EnvVars["BACKEND_PORT"] } else { "444" }
    $VitePort    = if ($EnvVars["VITE_PORT"])    { $EnvVars["VITE_PORT"] }    else { "44" }
    $RuntimePort = if ($EnvVars["RUNTIME_PORT"]) { $EnvVars["RUNTIME_PORT"] } else { "4000" }

    Write-Host "[pyagent] HOST=$Host_  BACKEND_PORT=$BackendPort  VITE_PORT=$VitePort  RUNTIME_PORT=$RuntimePort" -ForegroundColor Cyan

    $EnvBlock = ($EnvVars.GetEnumerator() | ForEach-Object {
        "`$env:$($_.Key) = '$($_.Value)'"
    }) -join "; "

    $TrackedPids = @{}

    # 1. Standalone Rust runtime binary (optional)
    $RuntimeExe = Join-Path $Root "rust_core\runtime\target\release\runtime.exe"
    if (Test-Path $RuntimeExe) {
        Write-Host "[pyagent] Found Rust runtime binary, starting on port $RuntimePort ..." -ForegroundColor Cyan
        $proc = Start-DevWindow -Title "runtime (port $RuntimePort)" -EnvBlock $EnvBlock `
            -Cmd "& '$RuntimeExe' --port $RuntimePort --host $Host_"
        $TrackedPids["runtime"] = $proc.Id
    } else {
        Write-Host "[pyagent] Rust runtime binary not built — runs embedded inside the Python backend (OK for dev)." -ForegroundColor Yellow
    }

    # 2. Python backend
    $VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPython)) {
        Write-Host "[pyagent] ERROR: venv not found at .venv\Scripts\python.exe" -ForegroundColor Red
        Write-Host "[pyagent] Run: python -m venv .venv && .venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
        exit 1
    }
    $proc = Start-DevWindow -Title "backend (port $BackendPort)" -EnvBlock $EnvBlock `
        -Cmd "& '$VenvPython' -m backend"
    $TrackedPids["backend"] = $proc.Id

    # 3. Vite dev server
    if (-not $NoVite) {
        $WebDir = Join-Path $Root "web"
        $NpmCmd = Get-Command npm -ErrorAction SilentlyContinue
        if (-not $NpmCmd) {
            Write-Host "[pyagent] WARNING: npm not found — skipping Vite. Install Node.js to enable the frontend." -ForegroundColor Yellow
        } else {
            if (-not (Test-Path (Join-Path $WebDir "node_modules"))) {
                Write-Host "[pyagent] node_modules missing — running npm install ..." -ForegroundColor Yellow
                Push-Location $WebDir; npm install; Pop-Location
            }
            $proc = Start-DevWindow -Title "vite (port $VitePort)" -EnvBlock $EnvBlock `
                -Cmd "npm run dev -- --port $VitePort --host $Host_" -Cwd $WebDir
            $TrackedPids["vite"] = $proc.Id
        }
    }

    Save-Pids $TrackedPids

    Write-Host ""
    Write-Host "PyAgent dev stack started:" -ForegroundColor Green
    foreach ($entry in $TrackedPids.GetEnumerator() | Sort-Object Key) {
        $port = switch ($entry.Key) {
            "runtime" { $RuntimePort } "backend" { $BackendPort } "vite" { $VitePort } default { "?" }
        }
        Write-Host "  $($entry.Key.PadRight(10)) http://$Host_`:$port  (PID $($entry.Value))"
    }
    Write-Host ""
    Write-Host "Run '.\start.ps1 stop' to stop all services." -ForegroundColor Cyan
    Write-Host "Run '.\start.ps1 status' to check service health." -ForegroundColor Cyan
    Write-Host ""

    # Keep alive and monitor — Ctrl+C exits cleanly
    $allProcs = $TrackedPids.Values | ForEach-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue }
    try {
        while ($true) {
            $allProcs = $allProcs | Where-Object { -not $_.HasExited }
            if ($allProcs.Count -eq 0) {
                Write-Host "[pyagent] All processes have exited." -ForegroundColor Yellow
                Remove-PidFile
                break
            }
            Start-Sleep -Seconds 3
        }
    } finally {
        Write-Host "[pyagent] Launcher exiting — services may still be running." -ForegroundColor Cyan
        Write-Host "[pyagent] Run '.\start.ps1 stop' to stop them." -ForegroundColor Cyan
    }
}

# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
switch ($Command) {
    "start"   { Invoke-Start }
    "stop"    { Invoke-Stop }
    "restart" { Invoke-Stop; Start-Sleep -Seconds 1; Invoke-Start }
    "status"  { Invoke-Status }
    default   { Invoke-Start }
}
