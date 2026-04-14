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

<#
.SYNOPSIS
    Download and install the CodeQL CLI bundle to C:\Dev\codeql (or a custom path).

.DESCRIPTION
    Downloads the latest CodeQL CLI bundle from the official GitHub release and
    extracts it to the target directory.  After installation, add the directory
    to your PATH so the tests can find codeql.exe automatically.

    Resolution order used by the test suite:
      1. CODEQL_EXE environment variable (absolute path to codeql.exe)
      2. codeql.exe on PATH
      3. <repo-root>\codeql\codeql.exe  (repo-local fallback, gitignored)

.PARAMETER InstallDir
    Destination directory.  Defaults to C:\Dev\codeql.

.PARAMETER Version
    CodeQL CLI version to install.  Defaults to "latest" which queries the
    GitHub Releases API for the most recent tag.

.EXAMPLE
    # Install to default location (C:\Dev\codeql)
    .\scripts\install_codeql.ps1

.EXAMPLE
    # Install to repo-local path (legacy, still works)
    .\scripts\install_codeql.ps1 -InstallDir (Join-Path $PSScriptRoot "..\codeql")

.EXAMPLE
    # Pin a specific version
    .\scripts\install_codeql.ps1 -Version "v2.20.3"
#>

param(
    [string]$InstallDir = "C:\Dev\CodeQL",
    [string]$Version    = "latest"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Resolve version
# ---------------------------------------------------------------------------
if ($Version -eq "latest") {
    Write-Host "Querying GitHub for latest CodeQL release..."
    $releaseInfo = Invoke-RestMethod `
        -Uri "https://api.github.com/repos/github/codeql-action/releases/latest" `
        -Headers @{ "Accept" = "application/vnd.github+json"; "X-GitHub-Api-Version" = "2022-11-28" }
    $Version = $releaseInfo.tag_name   # e.g. "codeql-bundle-v2.20.3"
    Write-Host "Latest release: $Version"
}

# Strip leading "codeql-bundle-" prefix if present so we can form the asset URL
$semver = $Version -replace '^codeql-bundle-', ''

$assetName = "codeql-bundle-win64.tar.gz"
$downloadUrl = "https://github.com/github/codeql-action/releases/download/codeql-bundle-$semver/$assetName"

# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
$tempFile = Join-Path $env:TEMP $assetName

if (-not (Test-Path $tempFile)) {
    Write-Host "Downloading $downloadUrl ..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $tempFile -UseBasicParsing
} else {
    Write-Host "Using cached download: $tempFile"
}

# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------
$parentDir = Split-Path $InstallDir -Parent
if (-not (Test-Path $parentDir)) {
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
}

Write-Host "Extracting to $InstallDir ..."
# tar is included in Windows 10 1803+ and Server 2019+
tar -xzf $tempFile --strip-components=1 -C $InstallDir 2>&1 | Out-Null

$exePath = Join-Path $InstallDir "codeql.exe"
if (-not (Test-Path $exePath)) {
    # Some archive layouts nest under a "codeql/" subdirectory
    $nested = Join-Path $InstallDir "codeql\codeql.exe"
    if (Test-Path $nested) {
        # Move up one level
        Get-ChildItem (Join-Path $InstallDir "codeql") | Move-Item -Destination $InstallDir -Force
        Remove-Item (Join-Path $InstallDir "codeql") -ErrorAction SilentlyContinue
    }
}

if (-not (Test-Path $exePath)) {
    Write-Error "Installation failed: codeql.exe not found at $exePath after extraction."
    exit 1
}

Write-Host ""
Write-Host "CodeQL CLI installed successfully:"
Write-Host "  $exePath"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  # Add to your PowerShell profile so it persists:"
Write-Host "  `$env:PATH = `"$InstallDir;`$env:PATH`""
Write-Host "  # Or run this once per session:"
Write-Host "  `$env:PATH = `"$InstallDir;`$env:PATH`""
Write-Host ""
Write-Host "  # Verify:"
Write-Host "  codeql version"
