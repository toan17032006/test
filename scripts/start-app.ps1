[CmdletBinding()]
param(
    [switch]$Local,
    [switch]$Stop,
    [switch]$NoBuild,
    [switch]$Foreground
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = $PSScriptRoot
$composeFile = Join-Path $repoRoot 'docker-compose.yml'

if ($Stop) {
    & (Join-Path $scriptDir 'dev-up.ps1') -Stop
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        docker compose -f $composeFile -p vulnshop down
    }
    Write-Host 'VulnShop stopped.'
    return
}

if ($Local) {
    & (Join-Path $scriptDir 'dev-up.ps1')
} else {
    $arguments = @{}
    if ($NoBuild) { $arguments['NoBuild'] = $true }
    if ($Foreground) { $arguments['Foreground'] = $true }
    & (Join-Path $scriptDir 'docker-up.ps1') @arguments
}
