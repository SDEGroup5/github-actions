$ErrorActionPreference = "Stop"

Write-Host "Open http://localhost:5000/json/getData"
Write-Host "Press Ctrl+C to stop."

$dockerArgs = @(
    "run", "--rm", "-it",
    "--platform", "linux/amd64",
    "-p", "5000:5000",
    "-v", "${PSScriptRoot}:/work:ro",
    "-w", "/work",
    "alpine:3.24.2",
    "./app"
)

docker @dockerArgs
exit $LASTEXITCODE