# Load credentials from .env
$envFile = "C:\workspace\.env"
$env_content = Get-Content $envFile -Raw
$apiKey = ($env_content | Select-String "LIVE_API_KEY=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value }).Trim()
$apiSecret = ($env_content | Select-String "LIVE_API_SECRET=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value }).Trim()
$apiPassphrase = ($env_content | Select-String "LIVE_API_PASSPHRASE=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value }).Trim()

Write-Host "Loaded Credentials:" -ForegroundColor Cyan
Write-Host "  Key: '$apiKey'" -ForegroundColor Yellow

$baseUrl = "https://api.kucoin.com"

# Test 1: /api/v1/accounts (no params)
Write-Host "`n[TEST 1] GET /api/v1/accounts" -ForegroundColor Cyan

$endpoint = "/api/v1/accounts"
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$strToSign = "$timestamp" + [char]10 + "GET" + [char]10 + "$endpoint" + [char]10

$hmac = New-Object System.Security.Cryptography.HMACSHA256
$hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
$signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))

Write-Host "  Timestamp: $timestamp" -ForegroundColor DarkGray
Write-Host "  Signature: $($signature.Substring(0,30))..." -ForegroundColor DarkGray

$headers = @{
    'KC-API-KEY' = $apiKey
    'KC-API-SIGN' = $signature
    'KC-API-TIMESTAMP' = $timestamp
    'KC-API-PASSPHRASE' = $apiPassphrase
    'KC-API-KEY-VERSION' = '2'
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "[SUCCESS]" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Green
}
catch {
    Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: /api/v1/accounts?type=spot
Write-Host "`n[TEST 2] GET /api/v1/accounts?type=spot" -ForegroundColor Cyan

$endpoint = "/api/v1/accounts?type=spot"
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$strToSign = "$timestamp" + [char]10 + "GET" + [char]10 + "$endpoint" + [char]10

$hmac = New-Object System.Security.Cryptography.HMACSHA256
$hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
$signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))

Write-Host "  Timestamp: $timestamp" -ForegroundColor DarkGray
Write-Host "  Signature: $($signature.Substring(0,30))..." -ForegroundColor DarkGray

$headers = @{
    'KC-API-KEY' = $apiKey
    'KC-API-SIGN' = $signature
    'KC-API-TIMESTAMP' = $timestamp
    'KC-API-PASSPHRASE' = $apiPassphrase
    'KC-API-KEY-VERSION' = '2'
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "[SUCCESS]" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Green
}
catch {
    Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: /api/v1/accounts?type=main
Write-Host "`n[TEST 3] GET /api/v1/accounts?type=main" -ForegroundColor Cyan

$endpoint = "/api/v1/accounts?type=main"
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$strToSign = "$timestamp" + [char]10 + "GET" + [char]10 + "$endpoint" + [char]10

$hmac = New-Object System.Security.Cryptography.HMACSHA256
$hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
$signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))

Write-Host "  Timestamp: $timestamp" -ForegroundColor DarkGray
Write-Host "  Signature: $($signature.Substring(0,30))..." -ForegroundColor DarkGray

$headers = @{
    'KC-API-KEY' = $apiKey
    'KC-API-SIGN' = $signature
    'KC-API-TIMESTAMP' = $timestamp
    'KC-API-PASSPHRASE' = $apiPassphrase
    'KC-API-KEY-VERSION' = '2'
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "[SUCCESS]" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Green
}
catch {
    Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
}
