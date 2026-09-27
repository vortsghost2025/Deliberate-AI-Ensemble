$apiKey = $env:KUCOIN_API_KEY
$apiSecret = $env:KUCOIN_API_SECRET
$apiPassphrase = $env:KUCOIN_API_PASSPHRASE
if (-not $apiKey -or -not $apiSecret -or -not $apiPassphrase) { Write-Error "KuCoin API credentials are not set."; exit 1 }

$endpoint = "/api/v1/accounts"
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$strToSign = "$timestamp" + [char]10 + "GET" + [char]10 + "$endpoint" + [char]10

$hmac = New-Object System.Security.Cryptography.HMACSHA256
$hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
$signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))

$headers = @{
    'KC-API-KEY' = $apiKey
    'KC-API-SIGN' = $signature
    'KC-API-TIMESTAMP' = $timestamp
    'KC-API-PASSPHRASE' = $apiPassphrase
    'KC-API-KEY-VERSION' = '2'
}

Write-Host "Testing new API key..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "https://api.kucoin.com$endpoint" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "[SUCCESS] API key is working!" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor Green
}
catch {
    Write-Host "[FAILED] $($_.Exception.Message)" -ForegroundColor Red
}
