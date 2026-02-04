$envPath = "C:\workspace\.env"
$envVars = @{}
Get-Content $envPath | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $envVars[$matches[1]] = $matches[2]
    }
}

$apiKey = $envVars['LIVE_API_KEY']
$apiSecret = $envVars['LIVE_API_SECRET']
$passphrase = $envVars['LIVE_API_PASSPHRASE']

$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$method = "GET"
$endpoint = "/api/v1/accounts?type=trade"
$body = ""

$strToSign = "$timestamp$method$endpoint$body"
$secretBytes = [System.Text.Encoding]::UTF8.GetBytes($apiSecret)
$hmac = New-Object System.Security.Cryptography.HMACSHA256 -ArgumentList (, $secretBytes)
$signBytes = $hmac.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($strToSign))
$signature = [Convert]::ToBase64String($signBytes)

$passphraseBytes = [System.Text.Encoding]::UTF8.GetBytes($passphrase)
$passphraseHmac = New-Object System.Security.Cryptography.HMACSHA256 -ArgumentList (, $secretBytes)
$passphraseSignBytes = $passphraseHmac.ComputeHash($passphraseBytes)
$passphraseSign = [Convert]::ToBase64String($passphraseSignBytes)

$headers = @{
    "KC-API-KEY" = $apiKey
    "KC-API-SIGN" = $signature
    "KC-API-TIMESTAMP" = $timestamp
    "KC-API-PASSPHRASE" = $passphraseSign
    "KC-API-KEY-VERSION" = "2"
    "Content-Type" = "application/json"
}

$uri = "https://api.kucoin.com$endpoint"

Write-Host "`n=== KuCoin API Request ===" -ForegroundColor Cyan
Write-Host "Endpoint: $endpoint" -ForegroundColor Yellow
Write-Host "Timestamp: $timestamp" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri $uri -Method Get -Headers $headers
    Write-Host "`n=== Raw JSON Response ===" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "`nERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}
