Param(
    [Parameter(Position=0)]
    [ValidateSet("start","run","stop","restart","status","logs","clear-logs","help")]
    [string]$action = "run",
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$taskArgs = @()
)

# Simple runner for delegation tasks that call Copilot CLI via tools/delegate_architecture_task.py
# Actions: run (execute once in background and capture log), logs (show last run), help

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path
$RunDir = Join-Path $ProjectRoot ".run"
if (-not (Test-Path $RunDir)) { New-Item -ItemType Directory -Path $RunDir | Out-Null }

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }

$Name = 'delegate_task'
$PidFile = Join-Path $RunDir "$Name.pid"
$LogDir = Join-Path $ProjectRoot "data\logs\webservices\$Name"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }
$DailyLog = Join-Path $LogDir ("access-{0}.log" -f (Get-Date -Format "yyyyMMdd"))
if (-not (Test-Path $DailyLog)) { New-Item -ItemType File -Path $DailyLog -Force | Out-Null }

$ScriptPath = "tools\delegate_architecture_task.py"

if ($action -eq 'help') {
    Write-Host "Usage: .\src\tools\delegate_task.ps1 <start|run|stop|restart|status|logs|clear-logs|help> [-- <args>]"
    Write-Host "Example: .\src\tools\delegate_task.ps1 run -- --spec temp/implement_architecture.json"
    Write-Host "Example: .\src\tools\delegate_task.ps1 start -- --spec temp/implement_architecture.json"
    Write-Host "Example: .\src\tools\delegate_task.ps1 clear-logs"
    return
}

function Is-Running {
    param($procId)
    if (-not $procId) { return $false }
    try { return (Get-Process -Id $procId -ErrorAction SilentlyContinue) -ne $null } catch { return $false }
}

function Remove-StalePidIfNeeded {
    if (-not (Test-Path $PidFile)) { return $false }
    $procId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $procId -or -not (Is-Running $procId)) {
        Remove-Item $PidFile -ErrorAction SilentlyContinue
        return $true
    }
    return $false
}

function Run-Once {
    if (Test-Path $PidFile) {
        $existingId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if (Is-Running $existingId) {
            Write-Host "$Name already running (PID $existingId). Use status/logs/stop." -ForegroundColor Yellow
            return
        }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    }

    # Compose command
    $argsEsc = $taskArgs -join ' '
    if ([string]::IsNullOrWhiteSpace($argsEsc)) { Write-Host "No args provided; pass -- --spec <file> to run." }
    Add-Content -Path $DailyLog -Value ("[{0}] Running {1} - args: {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Name, $argsEsc)

    $logEsc = $DailyLog.Replace("'", "''")
    $psCmd = "& '$Python' '$ScriptPath' $argsEsc *>&1 | ForEach-Object { `$line = [string]`$_; if (-not [string]::IsNullOrWhiteSpace(`$line)) { Add-Content -Path '$logEsc' -Value `$line } }"
    try {
        $proc = Start-Process -FilePath powershell.exe -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-Command',$psCmd -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    } catch {
        Add-Content -Path $DailyLog -Value ("[{0}] WARN: powershell redirection start failed: {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $_.Exception.Message)
        $proc = Start-Process -FilePath $Python -ArgumentList $ScriptPath, $taskArgs -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    }

    if ($proc -and $proc.Id) { $proc.Id | Out-File -FilePath $PidFile -Encoding ascii; Write-Host "Started delegate task (PID $($proc.Id)). Logs: $DailyLog" } else { Write-Host "Failed to start delegate task" -ForegroundColor Red }
}

function Stop-Task {
    if (Test-Path $PidFile) {
        $procId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($procId -and (Is-Running $procId)) {
            try {
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped $Name (PID $procId)" -ForegroundColor Green
            } catch {
                Write-Host "Failed stopping $Name PID $procId" -ForegroundColor Yellow
            }
        } else {
            Write-Host "$Name not running (stale PID file)" -ForegroundColor Yellow
        }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    } else {
        Write-Host "$Name not running" -ForegroundColor Yellow
    }
}

function Status-Task {
    $removedStale = Remove-StalePidIfNeeded
    if ($removedStale) {
        Write-Host "${Name}: stale PID file removed" -ForegroundColor Yellow
    }

    if (Test-Path $PidFile) {
        $procId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if (Is-Running $procId) {
            Write-Host "${Name}: running (PID $procId)" -ForegroundColor Green
        } else {
            Write-Host "${Name}: stale PID file ($procId)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "${Name}: not running" -ForegroundColor Red
    }
}

function Logs-Task {
    [void](Remove-StalePidIfNeeded)
    Write-Host "===== ${Name}: ${DailyLog} ====="
    if (Test-Path $DailyLog) { Get-Content $DailyLog -Tail 200 | ForEach-Object { Write-Host $_ } } else { Write-Host "(no log file for today)" -ForegroundColor Yellow }
}

function Clear-Logs {
    if (Test-Path $DailyLog) {
        Clear-Content -Path $DailyLog -ErrorAction SilentlyContinue
        Write-Host "Cleared log file: $DailyLog" -ForegroundColor Green
    } else {
        New-Item -ItemType File -Path $DailyLog -Force | Out-Null
        Write-Host "Created empty log file: $DailyLog" -ForegroundColor Green
    }
}

switch ($action) {
    'start' { Run-Once }
    'run' { Run-Once }
    'stop' { Stop-Task }
    'restart' { Stop-Task; Start-Sleep -Seconds 1; Run-Once }
    'status' { Status-Task }
    'logs' { Logs-Task }
    'clear-logs' { Clear-Logs }
}

Write-Host "Done. Use: .\src\tools\delegate_task.ps1 <start|run|stop|restart|status|logs|clear-logs|help> [-- <args>]"
