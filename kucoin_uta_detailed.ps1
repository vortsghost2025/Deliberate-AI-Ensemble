$apiKey = "69713960cb7e89000126f2f6"
$apiSecret = "a6b08fdc-045e-4cf4-bafb-c60984fb7b05"
$apiPassphrase = "134679Rosebud!"
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
        $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method $method -Headers $headers -ErrorAction Stop
        return @{
            success = $true
            data = $response
        }
    } catch {
        $errorBody = ""
        if ($_.ErrorDetails.Message) {
            $errorBody = $_.ErrorDetails.Message
        }
        return @{
            success = $false
            error = $_.Exception.Message
            status = $_.Exception.Response.StatusCode.value__
            body = $errorBody
        }
    }
}

Write-Host "`n=== KUCOIN UTA & BALANCE DETECTION ===" -ForegroundColor Cyan

# Test 1: Universal Account (should work)
Write-Host "`n[TEST 1] GET /api/v1/accounts" -ForegroundColor Yellow
$universal = Invoke-KuCoinRequest -endpoint "/api/v1/accounts"
if ($universal.success) {
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Raw JSON:" -ForegroundColor White
    $universal.data | ConvertTo-Json -Depth 10
} else {
    Write-Host "Status: FAILED - $($universal.error)" -ForegroundColor Red
    Write-Host "HTTP Status: $($universal.status)" -ForegroundColor Red
    Write-Host "Body: $($universal.body)" -ForegroundColor DarkRed
}

# Test 2: Ledgers with USDT filter
Write-Host "`n`n[TEST 2] GET /api/v1/accounts/ledgers?currency=USDT" -ForegroundColor Yellow
$ledgers = Invoke-KuCoinRequest -endpoint "/api/v1/accounts/ledgers?currency=USDT"
if ($ledgers.success) {
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Raw JSON:" -ForegroundColor White
    $ledgers.data | ConvertTo-Json -Depth 10
} else {
    Write-Host "Status: FAILED - $($ledgers.error)" -ForegroundColor Red
    Write-Host "HTTP Status: $($ledgers.status)" -ForegroundColor Red
    Write-Host "Body: $($ledgers.body)" -ForegroundColor DarkRed
}

# Test 3: High-Frequency Trade Account
Write-Host "`n`n[TEST 3] GET /api/v1/accounts?type=trade-hf" -ForegroundColor Yellow
$tradeHf = Invoke-KuCoinRequest -endpoint "/api/v1/accounts?type=trade-hf"
if ($tradeHf.success) {
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Raw JSON:" -ForegroundColor White
    $tradeHf.data | ConvertTo-Json -Depth 10
} else {
    Write-Host "Status: FAILED - $($tradeHf.error)" -ForegroundColor Red
    Write-Host "HTTP Status: $($tradeHf.status)" -ForegroundColor Red
    Write-Host "Body: $($tradeHf.body)" -ForegroundColor DarkRed
}

# Test 4: HF Account Details (V3 endpoint)
Write-Host "`n`n[TEST 4] GET /api/v3/hf/accounts?type=trade" -ForegroundColor Yellow
$hfV3 = Invoke-KuCoinRequest -endpoint "/api/v3/hf/accounts?type=trade"
if ($hfV3.success) {
    Write-Host "Status: SUCCESS" -ForegroundColor Green
    Write-Host "Raw JSON:" -ForegroundColor White
    $hfV3.data | ConvertTo-Json -Depth 10
} else {
    Write-Host "Status: FAILED - $($hfV3.error)" -ForegroundColor Red
    Write-Host "HTTP Status: $($hfV3.status)" -ForegroundColor Red
    Write-Host "Body: $($hfV3.body)" -ForegroundColor DarkRed
}

Write-Host "`n=== QUERY COMPLETE ===" -ForegroundColor Cyan
