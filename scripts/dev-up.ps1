[CmdletBinding()]
param(
    [switch]$Stop,
    [switch]$NoInstall
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$runDir = Join-Path $repoRoot '.run'
$logDir = Join-Path $runDir 'logs'
$apiPort = 18000
$webPort = 13000
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

function Stop-Tracked {
    param([string]$Name)
    $pidFile = Join-Path $runDir "$Name.pid"
    if (-not (Test-Path $pidFile)) { return }
    $processId = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($processId) {
        $proc = Get-Process -Id ([int]$processId) -ErrorAction SilentlyContinue
        if ($proc) { Stop-Process -Id $proc.Id -Force }
    }
    Remove-Item $pidFile -ErrorAction SilentlyContinue
}

function Wait-Url {
    param([string]$Url, [int]$TimeoutSeconds = 60)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { return $true }
        } catch {
            Start-Sleep -Seconds 1
        }
    }
    return $false
}

if ($Stop) {
    Stop-Tracked 'api'
    Stop-Tracked 'frontend'
    Write-Host 'Native VulnShop processes stopped.'
    return
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Stop-Tracked 'api'
Stop-Tracked 'frontend'

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python not found on PATH. Install Python 3.12 and add it to PATH.'
}

& python -c 'import fastapi, uvicorn' 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Backend dependencies are missing. Run: python -m pip install -r backend/requirements.txt"
}

$expressDir = Join-Path $repoRoot 'frontend\node_modules\express'
if (-not (Test-Path $expressDir)) {
    if ($NoInstall) { throw 'Frontend dependencies are missing and -NoInstall was set. Run: npm --prefix frontend ci' }
    Write-Host 'Installing frontend dependencies...' -ForegroundColor Cyan
    & npm --prefix (Join-Path $repoRoot 'frontend') ci
    if ($LASTEXITCODE -ne 0) { throw 'npm ci failed' }
}

$env:PYTHONUNBUFFERED = '1'
$env:DATABASE_URL = 'postgresql://postgres:postgres123@127.0.0.1:15432/vulnshop'
$env:MYSQL_URL = 'mysql+pymysql://mysql_user:mysql_pass@127.0.0.1:13306/vulnshop_legacy'
$env:MONGODB_URL = 'mongodb://127.0.0.1:27017/vulnshop'
$env:REDIS_URL = 'redis://127.0.0.1:16379/0'
$env:ELASTICSEARCH_URL = 'http://127.0.0.1:19200'
$env:NEO4J_URL = 'bolt://127.0.0.1:17687'
$env:SMTP_HOST = '127.0.0.1'
$env:SMTP_PORT = '11025'
$env:SECRET_KEY = 'local-dev-secret'
$env:JWT_SECRET = 'jwt-secret-weak'
$env:ADMIN_PASSWORD = 'admin123'
$env:DEBUG = 'true'

$api = Start-Process -FilePath 'python' -ArgumentList @('-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', "$apiPort") `
    -WorkingDirectory (Join-Path $repoRoot 'backend') -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $logDir 'api.log') -RedirectStandardError (Join-Path $logDir 'api.err.log')
$api.Id | Set-Content (Join-Path $runDir 'api.pid')

$env:API_URL = "http://127.0.0.1:$apiPort"
$env:GRAPHQL_URL = 'http://127.0.0.1:14000/graphql'
$env:HOST = '0.0.0.0'
$env:PORT = "$webPort"
$env:NODE_ENV = 'development'
$env:SESSION_SECRET = 'session-secret-weak'

$web = Start-Process -FilePath 'node' -ArgumentList @('server.js') `
    -WorkingDirectory (Join-Path $repoRoot 'frontend') -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $logDir 'frontend.log') -RedirectStandardError (Join-Path $logDir 'frontend.err.log')
$web.Id | Set-Content (Join-Path $runDir 'frontend.pid')

Write-Host 'Waiting for the backend and storefront to answer...' -ForegroundColor Cyan
$apiReady = Wait-Url "http://127.0.0.1:$apiPort/health"
$webReady = Wait-Url "http://127.0.0.1:$webPort/"
if (-not ($apiReady -and $webReady)) {
    Stop-Tracked 'api'
    Stop-Tracked 'frontend'
    Get-Content (Join-Path $logDir 'api.err.log'), (Join-Path $logDir 'frontend.err.log') -ErrorAction SilentlyContinue | Select-Object -Last 40
    throw 'Native services did not become ready in time. See the logs above.'
}

$lan = Get-LanAddress
Write-Host ''
Write-Host 'VulnShop is running natively.' -ForegroundColor Green
Write-Host "  Storefront (this machine): http://127.0.0.1:$webPort"
if ($lan) { Write-Host "  Storefront (LAN browser):  http://${lan}:$webPort" }
Write-Host "  Backend API:               http://127.0.0.1:$apiPort/health"
Write-Host "  Logs:                      $logDir"
Write-Host ''
Write-Host 'Stop with: scripts/start-app.ps1 -Stop'
