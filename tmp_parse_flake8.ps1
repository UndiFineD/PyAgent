$ErrorActionPreference = 'Stop'
$log = 'c:/Users/Keimpe/AppData/Roaming/Code/User/workspaceStorage/af9ec01d2056641294064d04c9f47a46/GitHub.copilot-chat/chat-session-resources/f817eba4-0d6e-4636-91c9-af565b90f0d9/call_9dz2qoInrdGoJQ1ZeEMFhujT__vscode-1774023016751/content.txt'
$lines = Get-Content $log | Where-Object { $_ -match '^[.]\\.+\.py:\d+:\d+: [A-Z]\d+\b' }
$parsed = foreach ($line in $lines) {
    if ($line -match '^(?<file>.+?\.py):(?<line>\d+):(?<col>\d+): (?<code>[A-Z]\d+)\b') {
        [pscustomobject]@{ File = $matches.file; Code = $matches.code }
    }
}
Write-Output ('TOTAL=' + $parsed.Count)
Write-Output 'TOP_FILES'
$parsed | Group-Object File | Sort-Object Count -Descending | Select-Object -First 12 Count, Name | Format-Table -AutoSize | Out-String | Write-Output
Write-Output 'TOP_CODES'
$parsed | Group-Object Code | Sort-Object Count -Descending | Select-Object Count, Name | Format-Table -AutoSize | Out-String | Write-Output
$targets = @(
    '.\src-old\tools\download_agent\core.py',
    '.\src-old\tools\run_full_pipeline.py',
    '.\src-old\observability\structured_logger.py',
    '.\src-old\tools\mcp\bridge.py',
    '.\src-old\observability\tracing\OpenTelemetryTracer.py',
    '.\src-old\observability\stats\observability_core.py',
    '.\src-old\tools\security\fuzzing.py',
    '.\src-old\pyagent_cli.py',
    '.\src-old\observability\stats\metrics_engine.py',
    '.\src-old\tools\extract_candidates.py'
)
Write-Output 'TARGETS'
$targetRows = foreach ($target in $targets) {
    $count = ($parsed | Where-Object { $_.File -eq $target }).Count
    [pscustomobject]@{ Count = $count; File = $target }
}
$targetRows | Sort-Object Count -Descending | Format-Table -AutoSize | Out-String | Write-Output
