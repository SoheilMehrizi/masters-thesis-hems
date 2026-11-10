param([string]$BootstrapPython = 'python')
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
function Check-Exit { if ($LASTEXITCODE -ne 0) { throw "Command failed with exit code $LASTEXITCODE" } }
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD '.python'
$env:UV_LINK_MODE = 'copy'
New-Item -ItemType Directory -Force .build-tmp | Out-Null
$env:TEMP = Join-Path $PWD '.build-tmp'
$env:TMP = $env:TEMP
if (-not (Test-Path .tools/bin/uv.exe)) {
    & $BootstrapPython -m pip install --target .tools 'uv==0.13.7'
    Check-Exit
}
$uv = '.\.tools\bin\uv.exe'
if (-not (Test-Path .python/cpython-3.11.9-windows-x86_64-none/python.exe)) {
    & $uv python install 3.11.9
    Check-Exit
}
if (-not (Test-Path vendor/CityLearn/.git)) {
    git clone --depth 1 --branch v3.2.0 https://github.com/citylearn-project/CityLearn.git vendor/CityLearn
    Check-Exit
}
$expected = 'fd86484b8b438f03eb40c3ec06dc90caa349842d'
$head = git -C vendor/CityLearn rev-parse HEAD
Check-Exit
$tag = git -C vendor/CityLearn rev-parse 'v3.2.0^{commit}'
Check-Exit
if ($head -ne $expected -or $tag -ne $expected) { throw 'CityLearn commit or release tag mismatch; existing source preserved.' }
if (-not (Test-Path .venv/Scripts/python.exe)) {
    & $uv venv --python .python/cpython-3.11.9-windows-x86_64-none/python.exe .venv
    Check-Exit
}
& $uv pip install --python .venv/Scripts/python.exe -r requirements.lock
Check-Exit
& $uv pip install --python .venv/Scripts/python.exe --no-build-isolation --no-deps -e vendor/CityLearn -e .
Check-Exit
& $uv pip check --python .venv/Scripts/python.exe
Check-Exit
& .venv/Scripts/python.exe scripts/recover_artifacts.py
Check-Exit
& .venv/Scripts/python.exe scripts/validate_setup.py
Check-Exit
