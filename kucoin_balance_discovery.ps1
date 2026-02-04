# KuCoin Balance Discovery Script
# Load environment variables
$envFile = "C:\workspace\.env"
$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $envVars[$matches[1]] = $matches[2]
    }
}

$apiKey = $envVars['LIVE_API_KEY']
$apiSecret = $envVars['LIVE_API_SECRET']
$passphrase = $envVars['LIVE_API_PASSPHRASE']
$baseUrl = "https://api.kucoin.com"

function Invoke-KuCoinRequest {
    param (
        [string]$Endpoint,
        [string]$Description
    )
    
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $strToSign = "$timestamp" + "GET" + "$Endpoint"
    
    $hmacsha = New-Object System.Security.Cryptography.HMACSHA256
    $hmacsha.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
    $signature = [Convert]::ToBase64String($hmacsha.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))
    
    $passphraseHmac = New-Object System.Security.Cryptography.HMACSHA256
    $passphraseHmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
    $encryptedPassphrase = [Convert]::ToBase64String($passphraseHmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($passphrase)))
    
    $headers = @{
        "KC-API-KEY" = $apiKey
        "KC-API-SIGN" = $signature
        "KC-API-TIMESTAMP" = $timestamp
        "KC-API-PASSPHRASE" = $encryptedPassphrase
        "KC-API-KEY-VERSION" = "2"
        "Content-Type" = "application/json"
    }
    
    Write-Host ""
    Write-Host "========================================"
    Write-Host "Testing: $Description"
    Write-Host "Endpoint: GET $Endpoint"
    Write-Host "========================================"
    
    try {
        $url = "$baseUrl$Endpoint"
        $response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers -ErrorAction Stop
        
        Write-Host "Status: SUCCESS"
        Write-Host "Response:"
        $jsonResponse = $response | ConvertTo-Json -Depth 10
        Write-Host $jsonResponse
        
        if ($response.data -is [array]) {
            $count = $response.data.Count
            Write-Host ""
            Write-Host "Data Items Found: $count"
            
            if ($count -gt 0) {
                Write-Host ""
                Write-Host "Account Summary:"
                foreach ($account in $response.data) {
                    $currency = $account.currency
                    $balance = $account.balance
                    $available = $account.available
                    $type = $account.type
                    Write-Host "  - Currency: $currency | Type: $type | Balance: $balance | Available: $available"
                }
            }
        }
        
    } catch {
        Write-Host "Status: FAILED"
        Write-Host "Error: $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "========================================================="
Write-Host "  KuCoin Account Balance Discovery Report"
Write-Host "  Searching for 100 USDT Balance"
Write-Host "========================================================="

Invoke-KuCoinRequest -Endpoint "/api/v1/accounts?type=main" -Description "Main Accounts"
Invoke-KuCoinRequest -Endpoint "/api/v1/accounts?type=spot" -Description "Spot Trading Accounts"
Invoke-KuCoinRequest -Endpoint "/api/v1/accounts?type=funding" -Description "Funding Accounts"
Invoke-KuCoinRequest -Endpoint "/api/v1/accounts?type=trade" -Description "Trade Accounts"
Invoke-KuCoinRequest -Endpoint "/api/v1/accounts?type=margin" -Description "Margin Accounts"
Invoke-KuCoinRequest -Endpoint "/api/v1/sub-accounts" -Description "Sub-Accounts List"
Invoke-KuCoinRequest -Endpoint "/api/v1/accounts" -Description "All Accounts No Filter"

Write-Host ""
Write-Host "========================================================="
Write-Host "  Discovery Complete"
Write-Host "========================================================="
