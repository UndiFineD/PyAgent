# Rename generated docs and tests to final names under src/
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $cwd

Get-ChildItem -Path src -Recurse -Filter '*.py.description.md' -File | ForEach-Object {
    $old = $_.FullName
    $new = $old -replace '\.py\.description\.md$','.description.md'
    if (-not (Test-Path $new)) {
        $newName = Split-Path $new -Leaf
        try { Rename-Item -Path $old -NewName $newName -ErrorAction Stop; Write-Host "Renamed: $old -> $new" } catch { Write-Host "Failed to rename $old" }
    } else { Write-Host "Skipped (exists): $new" }
}

Get-ChildItem -Path src -Recurse -Filter '*.py.improvements.md' -File | ForEach-Object {
    $old = $_.FullName
    $new = $old -replace '\.py\.improvements\.md$','.improvements.md'
    if (-not (Test-Path $new)) {
        $newName = Split-Path $new -Leaf
        try { Rename-Item -Path $old -NewName $newName -ErrorAction Stop; Write-Host "Renamed: $old -> $new" } catch { Write-Host "Failed to rename $old" }
    } else { Write-Host "Skipped (exists): $new" }
}

Get-ChildItem -Path src -Recurse -Filter '*.py.splice.md' -File | ForEach-Object {
    $old = $_.FullName
    $new = $old -replace '\.py\.splice\.md$','.splice.md'
    if (-not (Test-Path $new)) {
        $newName = Split-Path $new -Leaf
        try { Rename-Item -Path $old -NewName $newName -ErrorAction Stop; Write-Host "Renamed: $old -> $new" } catch { Write-Host "Failed to rename $old" }
    } else { Write-Host "Skipped (exists): $new" }
}

Get-ChildItem -Path src -Recurse -Filter '*_generated_test.py' -File | ForEach-Object {
    $old = $_.FullName
    $new = $old -replace '_generated_test\.py$','_test.py'
    $newName = Split-Path $new -Leaf
    if (Test-Path $new) {
        try { Remove-Item -Path $new -Force -ErrorAction Stop; Write-Host "Removed existing: $new" } catch { Write-Host "Failed to remove existing $new" }
    }
    try { Rename-Item -Path $old -NewName $newName -ErrorAction Stop; Write-Host "Renamed: $old -> $new" } catch { Write-Host "Failed to rename $old" }
}
