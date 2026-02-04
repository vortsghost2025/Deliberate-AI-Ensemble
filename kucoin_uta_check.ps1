$apiKey = "6971cd16b64e920001e7f2f6"
$apiSecret = "8c29bebc-af48-4a78-8976-7a0ca4a03876"
$apiPassphrase = "Mypassw0rd1994"
$baseUrl = "https://api.kucoin.com"

function Invoke-KuCoinRequest {
    param(
        [string]$endpoint,
        [string]$method = "GET"
    )
    
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $strToSign = "$timestamp$method$endpoint"
    
    $hmac = New-Object System.Security.Cryptography.HMACSHA256
    $hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
    $signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))
    
    $passphraseHmac = New-Object System.Security.Cryptography.HMACSHA256
    $passphraseHmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
    $encryptedPassphrase = [Convert]::ToBase64String($passphraseHmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($apiPassphrase)))
    
    $headers = @{
        "KC-API-KEY" = $apiKey
        "KC-API-SIGN" = $signature
        "KC-API-TIMESTAMP" = $timestamp
        "KC-API-PASSPHRASE" = $encryptedPassphrase
        "KC-API-KEY-VERSION" = "2"
        "Content-Type" = "application/json"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method $method -Headers $headers
        return $response
    } catch {
        return @{
            error = $_.Exception.Message
            status = $_.Exception.Response.StatusCode.value__
        }
    }
}

Write-Host "`n=== QUERYING UTA ENDPOINTS ===" -ForegroundColor Cyan

Write-Host "`n[1] GET /api/v1/accounts/ledgers?currency=USDT" -ForegroundColor Yellow
$ledgers = Invoke-KuCoinRequest -endpoint "/api/v1/accounts/ledgers?currency=USDT"
Write-Host "`nRaw JSON Response:" -ForegroundColor Green
$ledgers | ConvertTo-Json -Depth 10

Write-Host "`n`n[2] GET /api/v1/accounts?type=trade-hf" -ForegroundColor Yellow
$tradeHf = Invoke-KuCoinRequest -endpoint "/api/v1/accounts?type=trade-hf"
Write-Host "`nRaw JSON Response:" -ForegroundColor Green
$tradeHf | ConvertTo-Json -Depth 10

Write-Host "`n=== QUERY COMPLETE ===" -ForegroundColor Cyan
