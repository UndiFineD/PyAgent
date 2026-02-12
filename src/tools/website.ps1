Param(
    [Parameter(Position=0)]
    [ValidateSet("start","stop","restart","status","logs","clear-logs","help")]
    [string]$action = "status",
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$services = @("all")
)

# Simple service manager for the local development web stack (Windows PowerShell)
# Controls: uvicorn (web), api (agent api), downloads (streamlit), improvement (streamlit)

# Ensure services defaults to 'all' when no service name is provided or an empty array is passed
if ($null -eq $services -or $services.Count -eq 0 -or ($services.Count -eq 1 -and [string]::IsNullOrWhiteSpace($services[0]))) {
    $services = @('all')
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# Project root is the parent directory of the tools folder
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path
$RunDir = Join-Path $ProjectRoot ".run"
if (-not (Test-Path $RunDir)) { New-Item -ItemType Directory -Path $RunDir | Out-Null }

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    # Fall back to python on PATH if no venv python found
    $Python = "python"
}

$ServicesMap = @{
    uvicorn = @{ exe = $Python; args = "-m uvicorn src.interface.ui.web.py_agent_web:app --host 127.0.0.1 --port 8000"; port = 8000; pid = "uvicorn.pid" }
    api = @{ exe = $Python; args = "-m uvicorn src.infrastructure.services.api.agent_api_server:app --host 127.0.0.1 --port 8001"; port = 8001; pid = "api.pid" }
    downloads = @{ exe = $Python; args = "-m streamlit run src/interface/ui/web/download_web.py --server.port 8501 --server.headless true"; port = 8501; pid = "downloads.pid" }
    improvement = @{ exe = $Python; args = "-m streamlit run src/interface/ui/web/improvement_web.py --server.port 8502 --server.headless true"; port = 8502; pid = "improvement.pid" }
}

$ServiceOrder = @("uvicorn", "api", "downloads", "improvement")
$LogOnlyServices = @("delegate_task", "self_improvement")

function Get-PidFilePath($name){ Join-Path $RunDir $($ServicesMap[$name].pid) }

function Get-ListeningPids($port){
    try {
        $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        if ($conns) { return ($conns | Select-Object -ExpandProperty OwningProcess -Unique) }
        return @()
    }
    catch {
        return @()
    }
}

function Is-RunningPort($port){
    return (Get-ListeningPids $port).Count -gt 0
}

function Start-ServiceTask($name){
    $svc = $ServicesMap[$name]
    if (-not $svc) { Write-Host "Unknown service: $name" -ForegroundColor Yellow; return }

    if (Is-RunningPort $svc.port){ Write-Host "$name already listening on port $($svc.port)" -ForegroundColor Green; return }

    $pidFile = Get-PidFilePath $name
    if (Test-Path $pidFile){
        $existingPid = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
        if ($existingPid){
            $procExists = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
            if (-not $procExists){ Remove-Item $pidFile -ErrorAction SilentlyContinue }
        }
    }
    # Prepare per-service daily log under data/logs/webservices/<service>/access-YYYYMMDD.log
    $serviceLogDir = Join-Path $ProjectRoot "data\logs\webservices\$name"
    if (-not (Test-Path $serviceLogDir)) { New-Item -ItemType Directory -Path $serviceLogDir -Force | Out-Null }
    $dailyLog = Join-Path $serviceLogDir ("access-{0}.log" -f (Get-Date -Format "yyyyMMdd"))
    if (-not (Test-Path $dailyLog)) { New-Item -ItemType File -Path $dailyLog -Force | Out-Null }
    Write-Host "Starting $name..."

    # Start process through PowerShell so all streams are redirected into the daily log
    $exeEsc = $svc.exe.Replace("'", "''")
    $argsEsc = $svc.args.Replace("'", "''")
    $logEsc = $dailyLog.Replace("'", "''")
    $psCmd = "& '$exeEsc' $argsEsc *>&1 | ForEach-Object { `$line = [string]`$_; if (-not [string]::IsNullOrWhiteSpace(`$line)) { Add-Content -Path '$logEsc' -Value `$line } }"
    Add-Content -Path $dailyLog -Value ("[{0}] Starting {1} with command: {2} {3}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $name, $svc.exe, $svc.args)
    try {
        $proc = Start-Process -FilePath powershell.exe -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $psCmd -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    } catch {
        # Fall back to direct start without redirection
        Add-Content -Path $dailyLog -Value ("[{0}] WARN: powershell redirection start failed: {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $_.Exception.Message)
        $proc = Start-Process -FilePath $svc.exe -ArgumentList $svc.args -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    }

    if ($proc -and $proc.Id){
        $proc.Id | Out-File -FilePath $pidFile -Encoding ascii

        # Wait up to 30s for the service to bind its port (some services have heavy startup)
        $bound = $false
        for ($i=0; $i -lt 60; $i++){
            Start-Sleep -Milliseconds 500
            if (Is-RunningPort $svc.port){ $bound = $true; break }
        }

        if ($bound){
            Write-Host "$name started (PID $($proc.Id))"
        } else {
            $procState = Get-Process -Id $proc.Id -ErrorAction SilentlyContinue
            if ($procState) {
                Write-Host "$name started (PID $($proc.Id)); still initializing, port $($svc.port) not bound yet" -ForegroundColor Yellow
                Add-Content -Path $dailyLog -Value ("[{0}] WARN: process alive but port {1} not bound yet after wait window" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $svc.port)
            } else {
                Write-Host "$name started (PID $($proc.Id)) but port $($svc.port) not detected" -ForegroundColor Yellow
                Write-Host "$name process exited before binding port $($svc.port)" -ForegroundColor Yellow
                Add-Content -Path $dailyLog -Value ("[{0}] ERROR: process exited before binding port {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $svc.port)
            }
            if (Test-Path $dailyLog){
                Write-Host "Last lines from ${dailyLog}:"
                Get-Content $dailyLog -Tail 200 | ForEach-Object { Write-Host $_ }
            }
        }
    } else {
        Write-Host "Failed to start $name" -ForegroundColor Red
        Add-Content -Path $dailyLog -Value ("[{0}] ERROR: failed to start process" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
    }
}

function Stop-ServiceTask($name){
    $svc = $ServicesMap[$name]
    if (-not $svc) { Write-Host "Unknown service: $name" -ForegroundColor Yellow; return }
    $pidFile = Get-PidFilePath $name
    if (Test-Path $pidFile){
        $filePid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($filePid){
            try {
                Stop-Process -Id $filePid -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped $name (PID $filePid)"
            } catch {
                Write-Host "Failed stopping $name PID $filePid" -ForegroundColor Yellow
            }
            Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
    }
    # Fallback: stop by port
    if (Is-RunningPort $svc.port){
        $pids = Get-ListeningPids $svc.port
        foreach($pidVal in $pids){
            try {
                Stop-Process -Id $pidVal -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped $name (PID $pidVal)"
            } catch {}
        }
    } else { Write-Host "$name not running" }
}

function Status-ServiceTask($name){
    $svc = $ServicesMap[$name]
    if (-not $svc){ Write-Host "Unknown service: $name" -ForegroundColor Yellow; return }
    $pidFile = Get-PidFilePath $name
    $running = Is-RunningPort $svc.port
    if ($running){
        $pids = (Get-ListeningPids $svc.port) -join ','
        Write-Host "${name}: listening on port $($svc.port) (PIDs: $pids)" -ForegroundColor Green
    } else {
        if (Test-Path $pidFile){
            $filePid = Get-Content $pidFile -ErrorAction SilentlyContinue
            $procExists = if ($filePid) { Get-Process -Id $filePid -ErrorAction SilentlyContinue } else { $null }
            if ($procExists) {
                Write-Host "${name}: process alive (PID $filePid) but port $($svc.port) not listening" -ForegroundColor Yellow
            } else {
                Write-Host "${name}: stale PID file ($filePid) and port $($svc.port) not listening" -ForegroundColor Yellow
            }
        } else {
            Write-Host "${name}: not running" -ForegroundColor Red
        }
    }
}

function Logs-ServiceTask($name){
    if ((-not $ServicesMap.ContainsKey($name)) -and (-not ($LogOnlyServices -contains $name))) { Write-Host "Unknown service: $name" -ForegroundColor Yellow; return }

    $serviceLogDir = Join-Path $ProjectRoot "data\logs\webservices\$name"
    $dailyLog = Join-Path $serviceLogDir ("access-{0}.log" -f (Get-Date -Format "yyyyMMdd"))

    Write-Host "===== ${name}: ${dailyLog} ====="
    if (Test-Path $dailyLog) {
        Get-Content $dailyLog -Tail 200 | ForEach-Object { Write-Host $_ }
    } else {
        Write-Host "(no log file for today)" -ForegroundColor Yellow
    }
}

function Clear-LogsServiceTask($name){
    if ((-not $ServicesMap.ContainsKey($name)) -and (-not ($LogOnlyServices -contains $name))) { Write-Host "Unknown service: $name" -ForegroundColor Yellow; return }

    $serviceLogDir = Join-Path $ProjectRoot "data\logs\webservices\$name"
    if (-not (Test-Path $serviceLogDir)) { New-Item -ItemType Directory -Path $serviceLogDir -Force | Out-Null }
    $dailyLog = Join-Path $serviceLogDir ("access-{0}.log" -f (Get-Date -Format "yyyyMMdd"))

    if (Test-Path $dailyLog) {
        Clear-Content -Path $dailyLog -ErrorAction SilentlyContinue
        Write-Host "Cleared log file for ${name}: ${dailyLog}" -ForegroundColor Green
    } else {
        New-Item -ItemType File -Path $dailyLog -Force | Out-Null
        Write-Host "Created empty log file for ${name}: ${dailyLog}" -ForegroundColor Green
    }
}

if ($action -eq 'help') {
    Write-Host "Usage: .\src\tools\website.ps1 <start|stop|restart|status|logs|clear-logs|help> [all|uvicorn|api|downloads|improvement|delegate_task|self_improvement]"
    return
}

if ($services -contains 'all') { $targets = $ServiceOrder } else { $targets = $services }

foreach($t in $targets){
    $isPrimary = $ServicesMap.ContainsKey($t)
    $isLogOnly = $LogOnlyServices -contains $t

    if (-not ($isPrimary -or $isLogOnly)) { Write-Host "Skipping unknown service: $t"; continue }

    if ($isLogOnly -and @('start','stop','restart','status') -contains $action) {
        Write-Host "Skipping unsupported action '$action' for log-only service: $t" -ForegroundColor Yellow
        continue
    }

    switch ($action){
        'start' { Start-ServiceTask $t }
        'stop' { Stop-ServiceTask $t }
        'restart' { Stop-ServiceTask $t; Start-Sleep -Seconds 1; Start-ServiceTask $t }
        'status' { Status-ServiceTask $t }
        'logs' { Logs-ServiceTask $t }
        'clear-logs' { Clear-LogsServiceTask $t }
    }
}

Write-Host "Done. Use: .\src\tools\website.ps1 <start|stop|restart|status|logs|clear-logs|help> [all|uvicorn|api|downloads|improvement|delegate_task|self_improvement]"
