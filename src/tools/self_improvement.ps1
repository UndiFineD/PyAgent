Param(
    [Parameter(Position=0)]
    [ValidateSet("start","stop","restart","status","logs","clear-logs","help")]
    [string]$action = "status",
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$scriptArgs = @()
)

# Service manager for the Fleet Self-Improvement loop (Windows PowerShell)
# Controls: long-running self-improvement script: src/infrastructure/services/dev/scripts/analysis/run_fleet_self_improvement.py

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path
$RunDir = Join-Path $ProjectRoot ".run"
if (-not (Test-Path $RunDir)) { New-Item -ItemType Directory -Path $RunDir | Out-Null }

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }

$Name = 'self_improvement'
$PidFile = Join-Path $RunDir "$Name.pid"
$LogDir = Join-Path $ProjectRoot "data\logs\webservices\$Name"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }
$DailyLog = Join-Path $LogDir ("access-{0}.log" -f (Get-Date -Format "yyyyMMdd"))
if (-not (Test-Path $DailyLog)) { New-Item -ItemType File -Path $DailyLog -Force | Out-Null }

$ScriptPath = "src\infrastructure\services\dev\scripts\analysis\run_fleet_self_improvement.py"

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

function Start-Loop {
    if (Test-Path $PidFile) {
        $existing = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if (Is-Running $existing) { Write-Host "$Name already running (PID $existing)" -ForegroundColor Green; return }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    }

    Write-Host "Starting $Name..."
    Add-Content -Path $DailyLog -Value ("[{0}] Starting {1} - args: {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Name, ($scriptArgs -join ' '))

    $argsEsc = $scriptArgs -join ' '
    if ([string]::IsNullOrWhiteSpace($argsEsc)) { $argsEsc = "-c 0 -d 3600" }

    $logEsc = $DailyLog.Replace("'", "''")
    $psCmd = "& '$Python' '$ScriptPath' $argsEsc *>&1 | ForEach-Object { `$line = [string]`$_; if (-not [string]::IsNullOrWhiteSpace(`$line)) { Add-Content -Path '$logEsc' -Value `$line } }"
    try {
        $proc = Start-Process -FilePath powershell.exe -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-Command',$psCmd -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    } catch {
        Add-Content -Path $DailyLog -Value ("[{0}] WARN: powershell redirection start failed: {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $_.Exception.Message)
        $proc = Start-Process -FilePath $Python -ArgumentList $ScriptPath, $scriptArgs -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    }

    if ($proc -and $proc.Id) {
        $proc.Id | Out-File -FilePath $PidFile -Encoding ascii
        Write-Host "$Name started (PID $($proc.Id))"
    } else {
        Write-Host "Failed to start $Name" -ForegroundColor Red
        Add-Content -Path $DailyLog -Value ("[{0}] ERROR: failed to start process" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
    }
}

function Stop-Loop {
    if (Test-Path $PidFile) {
        $procId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($procId) {
            try { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue; Write-Host "Stopped $Name (PID $procId)" } catch { Write-Host "Failed stopping $Name PID $procId" -ForegroundColor Yellow }
            Remove-Item $PidFile -ErrorAction SilentlyContinue
            return
        }
    }
    Write-Host "$Name not running (no PID file)" -ForegroundColor Yellow
}

function Status-Loop {
    $removedStale = Remove-StalePidIfNeeded
    if ($removedStale) {
        Write-Host "${Name}: stale PID file removed" -ForegroundColor Yellow
    }

    if (Test-Path $PidFile) {
        $procId = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        if (Is-Running $procId) { Write-Host "${Name}: running (PID $procId)" -ForegroundColor Green; return }
        Write-Host "${Name}: stale PID file ($procId)" -ForegroundColor Yellow
    } else {
        Write-Host "${Name}: not running" -ForegroundColor Red
    }
}

function Logs-Loop {
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

if ($action -eq 'help') {
    Write-Host "Usage: .\src\tools\self_improvement.ps1 <start|stop|restart|status|logs|clear-logs|help> [-- <args to script>]"
    Write-Host "Example: .\src\tools\self_improvement.ps1 start -- -c 5 -d 120"
    Write-Host "Example: .\src\tools\self_improvement.ps1 clear-logs"
    return
}

switch ($action) {
    'start' { Start-Loop }
    'stop' { Stop-Loop }
    'restart' { Stop-Loop; Start-Sleep -Seconds 1; Start-Loop }
    'status' { Status-Loop }
    'logs' { Logs-Loop }
    'clear-logs' { Clear-Logs }
    default { Write-Host "Unknown action: $action" -ForegroundColor Yellow }
}

Write-Host "Done. Use: .\src\tools\self_improvement.ps1 <start|stop|restart|status|logs|clear-logs|help> [-- <script args>]"
