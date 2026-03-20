# Update all prjNNN references to prj0000NNN throughout the codebase

$replacements = @(
    'prj001' => 'prj0000001'
    'prj002' => 'prj0000002'
    'prj003' => 'prj0000003'
    'prj004' => 'prj0000004'
    'prj005' => 'prj0000005'
    'prj006' => 'prj0000006'
    'prj007' => 'prj0000007'
    'prj008' => 'prj0000008'
    'prj009' => 'prj0000009'
    'prj010' => 'prj0000010'
    'prj011' => 'prj0000011'
    'prj012' => 'prj0000012'
    'prj013' => 'prj0000013'
    'prj014' => 'prj0000014'
    'prj015' => 'prj0000015'
    'prj016' => 'prj0000016'
    'prj017' => 'prj0000017'
    'prj018' => 'prj0000018'
    'prj019' => 'prj0000019'
    'prj020' => 'prj0000020'
    'prj021' => 'prj0000021'
    'prj022' => 'prj0000022'
    'prj023' => 'prj0000023'
    'prj024' => 'prj0000024'
    'prj025' => 'prj0000025'
    'prj026' => 'prj0000026'
    'prj027' => 'prj0000027'
    'prj028' => 'prj0000028'
    'prj029' => 'prj0000029'
    'prj030' => 'prj0000030'
    'prj031' => 'prj0000031'
    'prj032' => 'prj0000032'
    'prj033' => 'prj0000033'
    'prj034' => 'prj0000034'
    'prj035' => 'prj0000035'
    'prj036' => 'prj0000036'
    'prj037' => 'prj0000037'
    'prj038' => 'prj0000038'
    # Duplicates renamed to new numbers
    'prj0000039' => 'prj0000039'  # placeholder for now
    'prj0000040' => 'prj0000040'  # placeholder
    'prj0000041' => 'prj0000041'  # placeholder
    'prj0000042' => 'prj0000042'  # placeholder
)

# Files to search and update (exclude git, node_modules, binaries)
$filesToUpdate = @(
    '.github/agents/**/*.md'
    '.github/agents/**/*.agent.md'
    'docs/agents/**/*.md'
    'docs/project/**/*.md'
    'tests/**/*.py'
)

Write-Host "Updating prjNNN references..."

foreach ($pattern in $filesToUpdate) {
    $files = Get-ChildItem -Recurse -Filter (Split-Path -Leaf $pattern) -Path (Split-Path $pattern) -ErrorAction SilentlyContinue
    
    $files | ForEach-Object {
        $file = $_
        $content = $file.FullName | Get-Content -Raw -ErrorAction SilentlyContinue
        if ($content) {
            $modified = $content
            foreach ($old in $replacements.Keys) {
                $new = $replacements[$old]
                if ($old -ne $new) {
                    $modified = $modified -replace [regex]::Escape($old), $new
                }
            }
            
            if ($modified -ne $content) {
                Set-Content -LiteralPath $file.FullName -Value $modified -Encoding UTF8
                Write-Host "Updated: $($file.FullName)"
            }
        }
    }
}

Write-Host "Done!"
