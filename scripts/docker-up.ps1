[CmdletBinding()]
param(
    [switch]$NoBuild,
    [switch]$Foreground
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$composeFile = Join-Path $repoRoot 'docker-compose.yml'
$project = 'vulnshop'
Set-Location $repoRoot

function Get-LanAddress {
    try {
        $route = Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction Stop |
            Sort-Object RouteMetric |
            Select-Object -First 1
        if ($route) {
            return Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $route.ifIndex -ErrorAction Stop |
                Where-Object { $_.IPAddress -ne '127.0.0.1' } |
                Select-Object -First 1 -ExpandProperty IPAddress
        }
    } catch {
        return $null
    }
}

function Wait-Url {
    param([string]$Url, [int]$TimeoutSeconds = 180)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
            & curl.exe -fsS -o NUL --max-time 3 $Url 2>$null
            if ($LASTEXITCODE -eq 0) { return $true }
        } else {
            try {
                $request = [System.Net.WebRequest]::Create($Url)
                $request.Timeout = 3000
                $request.Proxy = $null
                $response = $request.GetResponse()
                $status = [int]$response.StatusCode
                $response.Close()
                if ($status -ge 200 -and $status -lt 500) { return $true }
            } catch {
                # Retry until the deadline.
            }
        }
        Start-Sleep -Seconds 2
    }
    return $false
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker CLI not found. Install Docker Desktop (or Docker Engine + Compose v2), start it, then rerun this script.'
}

Write-Host 'Building the VulnShop Docker images...' -ForegroundColor Cyan
if (-not $NoBuild) {
    docker compose -f $composeFile -p $project build
    if ($LASTEXITCODE -ne 0) { throw 'docker compose build failed' }
}

if ($Foreground) {
    Write-Host 'Starting the stack in the foreground. Press Ctrl+C to stop.' -ForegroundColor Cyan
    docker compose -f $composeFile -p $project up
    exit $LASTEXITCODE
}

Write-Host 'Starting the VulnShop stack...' -ForegroundColor Cyan
docker compose -f $composeFile -p $project up -d
if ($LASTEXITCODE -ne 0) { throw 'docker compose up failed' }

Write-Host 'Waiting for the backend and storefront to answer...' -ForegroundColor Cyan
$apiReady = Wait-Url 'http://127.0.0.1:18000/health'
$webReady = Wait-Url 'http://127.0.0.1:13000/'
if (-not ($apiReady -and $webReady)) {
    docker compose -f $composeFile -p $project ps
    docker compose -f $composeFile -p $project logs --tail=80
    throw 'Services did not become ready in time. See the logs above.'
}

$lan = Get-LanAddress
Write-Host ''
Write-Host 'VulnShop is running.' -ForegroundColor Green
Write-Host '  Storefront (this machine): http://127.0.0.1:13000'
if ($lan) { Write-Host "  Storefront (LAN browser):  http://${lan}:13000" }
Write-Host '  Nginx entry point:         http://127.0.0.1:9080'
if ($lan) { Write-Host "  Nginx (LAN browser):       http://${lan}:9080" }
Write-Host '  Backend API:               http://127.0.0.1:18000/health'
Write-Host '  OpenAPI docs:              http://127.0.0.1:18000/docs'
Write-Host '  GraphQL:                   http://127.0.0.1:14000/graphql'
Write-Host '  MailHog inbox:             http://127.0.0.1:18025'
Write-Host ''
Write-Host 'Stop with: scripts/start-app.ps1 -Stop'
