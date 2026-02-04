# KuCoin Balance Discovery Script
# Queries multiple account endpoints to locate $100 USDT

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

# Function to make authenticated KuCoin API request
function Invoke-KuCoinRequest {
    param (
        [string]$Method,
        [string]$Endpoint,
        [string]$Description
    )
    
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $strToSign = "$timestamp$Method$Endpoint"
    
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
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Testing: $Description" -ForegroundColor Yellow
    Write-Host "Endpoint: $Method $Endpoint" -ForegroundColor Gray
    Write-Host "========================================" -ForegroundColor Cyan
    
    try {
        $url = "$baseUrl$Endpoint"
        $response = Invoke-RestMethod -Uri $url -Method $Method -Headers $headers -ErrorAction Stop
        
        Write-Host "Status: SUCCESS (200)" -ForegroundColor Green
        Write-Host "Response:" -ForegroundColor White
        $response | ConvertTo-Json -Depth 10
        
        # Check if data array has items
        if ($response.data -is [array]) {
            $count = $response.data.Count
            Write-Host "`nData Items Found: $count" -ForegroundColor $(if ($count -gt 0) { "Green" } else { "Red" })
            
            # If items found, show summary
            if ($count -gt 0) {
                Write-Host "`nAccount Summary:" -ForegroundColor Magenta
                foreach ($account in $response.data) {
                    $currency = $account.currency
                    $balance = $account.balance
                    $available = $account.available
                    $type = $account.type
                    Write-Host "  - $currency | Type: $type | Balance: $balance | Available: $available" -ForegroundColor Yellow
                }
            }
        } elseif ($response.data) {
            Write-Host "`nData Type: Object (not array)" -ForegroundColor Magenta
        }
        
    } catch {
        Write-Host "Status: FAILED" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $statusCode = $_.Exception.Response.StatusCode.value__
            Write-Host "HTTP Status Code: $statusCode" -ForegroundColor Red
        }
    }
}

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       KuCoin Account Balance Discovery Report          ║" -ForegroundColor Cyan
Write-Host "║           Searching for 100 USDT Balance               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Query 1: Main accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts?type=main" -Description "Main Accounts"

# Query 2: Spot accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts?type=spot" -Description "Spot Trading Accounts"

# Query 3: Funding accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts?type=funding" -Description "Funding Accounts"

# Query 4: Trade accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts?type=trade" -Description "Trade Accounts"

# Query 5: Margin accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts?type=margin" -Description "Margin Accounts"

# Query 6: Sub-accounts
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/sub-accounts" -Description "Sub-Accounts List"

# Query 7: All accounts (no filter)
Invoke-KuCoinRequest -Method "GET" -Endpoint "/api/v1/accounts" -Description "All Accounts - No Filter"

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                   Discovery Complete                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
