
# Export a small Windows System event log sample for the validation toolkit.
# Run from the project root.

$OutputDir = "examples/sample_logs"
$OutputFile = Join-Path $OutputDir "windows_system_sample.txt"

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Get-WinEvent -LogName System -MaxEvents 40 |
    Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message |
    Format-List |
    Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "Exported Windows System log sample to: $OutputFile"


# or run manually: 
#Get-WinEvent -LogName System -MaxEvents 50 |
#Select-Object TimeCreated, ProviderName, Id, LevelDisplayName, Message |
#ConvertTo-Json -Depth 3 |
#Out-File examples\system_events.json -Encoding utf8
