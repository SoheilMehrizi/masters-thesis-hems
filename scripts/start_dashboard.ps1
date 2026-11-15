$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\.venv\Scripts\python.exe -m streamlit run scripts/dashboard.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
exit $LASTEXITCODE
