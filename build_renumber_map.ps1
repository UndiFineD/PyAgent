# Build complete renumbering map with NO duplicates
# Keep one per unique NNN, assign new sequential for duplicates

$duplicates = @{
    '001' = @('prj001-async-runtime', 'prj001-conftest-typing-fixes', 'prj001-core-system')
    '002' = @('prj002-core-system', 'prj002-flm')
    '037' = @('prj037-tools', 'prj037-tools-crdt-security')
}

$mapping = @{}
$nextExtra = 39

# Add deterministic duplicates to mapping
foreach ($nnn in @('001', '002', '037')) {
    $folders = $duplicates[$nnn]
    # Keep first, renumber rest
    $kept = $folders[0]
    $mapping[$kept] = "prj{0:D7}" -f [int]$nnn
    for ($i = 1; $i -lt $folders.Count; $i++) {
        $mapping[$folders[$i]] = "prj{0:D7}" -f $nextExtra
        $nextExtra++
    }
}

# Add all non-duplicate folders
Get-ChildItem docs/project -Directory | Where-Object { $_.Name -match '^prj\d{3}-' } | Select-Object -ExpandProperty Name | Sort-Object | ForEach-Object {
    $num = [int]$_.Substring(3, 3)
    if (-not $mapping.ContainsKey($_)) {
        $mapping[$_] = "prj{0:D7}" -f $num
    }
}

# Display the mapping sorted by new name
$mapping.GetEnumerator() | Sort-Object -Property Value | ForEach-Object { "$($_.Key) => $($_.Value)" }

Write-Host "`nTotal folders: $($mapping.Count)"
