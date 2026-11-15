param([int]$Port = 8768)
$projectDirectory = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$pythonExecutable = Join-Path $projectDirectory '.venv\Scripts\python.exe'
$docsDirectory = Join-Path $projectDirectory 'docs'
Write-Host "Landing: http://127.0.0.1:$Port/literature/index.html"
Write-Host "First report: http://127.0.0.1:$Port/literature/la-upahem.html"
Write-Host 'Keep this terminal open. Press Ctrl+C to stop.'
& $pythonExecutable -u -m http.server $Port --bind 127.0.0.1 --directory $docsDirectory
