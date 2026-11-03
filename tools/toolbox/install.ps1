# shash.builds Toolbox installer for Windows (PowerShell). Untested on Windows yet.
#   powershell -ExecutionPolicy Bypass -File install.ps1              every tool
#   powershell -ExecutionPolicy Bypass -File install.ps1 transcribe   only the tools you name
# Installs Python and ffmpeg with winget if they're missing, then a virtual environment in
# tools\toolbox\.venv with each tool's requirements.txt.
param([string[]]$Tools)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

if (-not (Have "python") -and -not (Have "py")) {
  Write-Host "Installing Python..."
  winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
  Write-Host "Python installed. Close this window, open a new PowerShell, and run the installer again."
  exit 0
}
if (-not (Have "ffmpeg")) {
  Write-Host "Installing ffmpeg..."
  winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
  Write-Host "ffmpeg installed. Open a new PowerShell window so it's on PATH."
}

$py = if (Have "py") { "py" } else { "python" }
if (-not (Test-Path ".venv")) { & $py -m venv .venv }
$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $venvPy -m pip install --quiet --upgrade pip

if (-not $Tools) { $Tools = Get-ChildItem -Directory | Where-Object { Test-Path (Join-Path $_.FullName "requirements.txt") } | ForEach-Object Name }
foreach ($t in $Tools) {
  $req = Join-Path $t "requirements.txt"
  if (-not (Test-Path $req)) { throw "No tool called $t" }
  Write-Host "Installing $t..."
  & $venvPy -m pip install --quiet -r $req
}

Write-Host ""
Write-Host "Done. Start each session with:  .\tools\toolbox\.venv\Scripts\Activate.ps1"
Write-Host "Then try:                        python .\tools\toolbox\transcribe\transcribe.py your-file.mp4"
