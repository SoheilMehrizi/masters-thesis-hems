param(
    [Parameter(Mandatory=$true)][string]$InputPath,
    [Parameter(Mandatory=$true)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $word.Options.SaveNormalPrompt = $false
    $document = $word.Documents.Open($InputPath, $false, $true, $false)
    $document.Repaginate()
    $pages = $document.ComputeStatistics(2)
    $document.ExportAsFixedFormat($OutputPath, 17)
    Write-Output "Word rendered $pages pages."
}
finally {
    if ($null -ne $document) {
        $document.Saved = $true
        $discardChanges = 0
        $document.Close([ref]$discardChanges)
    }
    if ($null -ne $word) {
        $discardChanges = 0
        $word.Quit([ref]$discardChanges)
    }
}
