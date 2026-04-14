<#
.SYNOPSIS
    Clear Python cache files and common test caches in the repository.

.DESCRIPTION
    Recursively deletes `__pycache__` directories, `*.pyc`/`*.pyo` files and common
    test/runtime cache directories such as `.pytest_cache`, `.mypy_cache`, and
    `.hypothesis`. Automatically resolves the repository root based on the script location.
    Optimized to skip environments like `.git`, `.venv`, and `node_modules` for speed
    and safety.

.NOTES
    Usage:
      .\scripts\clear_caches.ps1 [-VerboseOutput] [-DryRun]
#>
[CmdletBinding()]
param (
    [switch]$VerboseOutput,
    [switch]$DryRun
)

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Write-Host "Clearing Python and test caches in $($RepoRoot.Path)..." -ForegroundColor Cyan

$cacheDirNames = @('__pycache__', '.pytest_cache', '.mypy_cache', '.hypothesis', '.ruff_cache', '.tox')
$cacheFileNames = @('*.pyc', '*.pyo')
$excludeDirs = @('.git', '.venv', 'venv', 'node_modules', 'env')

$script:removedCount = 0
$script:failedCount = 0

function Remove-CacheItem {
    param($Item)
    
    if (-not (Test-Path -LiteralPath $Item.FullName)) { return }

    if ($DryRun) {
        Write-Host "Would remove: $($Item.FullName)" -ForegroundColor DarkYellow
        return
    }

    try {
        Remove-Item -LiteralPath $Item.FullName -Recurse -Force -ErrorAction Stop
        if ($VerboseOutput) {
            Write-Host "Removed: $($Item.FullName)" -ForegroundColor DarkGreen
        }
        $script:removedCount++
    } catch {
        Write-Host "Failed removing: $($Item.FullName) -- $($_.Exception.Message)" -ForegroundColor Red
        $script:failedCount++
    }
}

function Get-TargetItems {
    # Recursively find items while skipping excluded directories
    $items = @()
    $stack = new-object System.Collections.Stack
    $stack.Push((Get-Item $RepoRoot.Path))

    while ($stack.Count -gt 0) {
        $current = $stack.Pop()
        # Skip exact excluded names and any .venv* variant (safety)
        if ($excludeDirs -contains $current.Name) { continue }
        if ($current.Name -like '.venv*') { continue }

        # Process current directory files and subdirectories
        try {
            $children = Get-ChildItem -LiteralPath $current.FullName -Force -ErrorAction SilentlyContinue
        } catch { continue }

        foreach ($child in $children) {
            if ($child.PSIsContainer) {
                if ($excludeDirs -contains $child.Name) { continue }
                if ($child.Name -like '.venv*') { continue }
                if ($cacheDirNames -contains $child.Name) {
                    $items += $child
                    # Skip going into a cache dir since we will delete it entirely
                    continue
                }
                $stack.Push($child)
            } else {
                foreach ($pattern in $cacheFileNames) {
                    if ($child.Name -like $pattern) {
                        $items += $child
                        break
                    }
                }
            }
        }
    }
    return $items
}

Write-Host "Scanning for cache files and folder..." -ForegroundColor Gray
$allTargets = @(Get-TargetItems)

Write-Host "Found $($allTargets.Count) items to remove." -ForegroundColor Gray

foreach ($target in $allTargets) {
    Remove-CacheItem -Item $target
}

if ($DryRun) {
    Write-Host "Dry run complete." -ForegroundColor Green
} else {
    Write-Host "Cache cleanup complete. Removed: $script:removedCount, Failed: $script:failedCount." -ForegroundColor Green
}
