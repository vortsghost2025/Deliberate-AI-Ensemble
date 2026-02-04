# Load credentials from .env
$envFile = "C:\workspace\.env"
$env_content = Get-Content $envFile -Raw
$apiKey = ($env_content | Select-String "LIVE_API_KEY=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value })
$apiSecret = ($env_content | Select-String "LIVE_API_SECRET=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value })
$apiPassphrase = ($env_content | Select-String "LIVE_API_PASSPHRASE=(.+)" | ForEach-Object { $_.Matches[0].Groups[1].Value })

Write-Host "API Key: $($apiKey.Substring(0,8))..." -ForegroundColor Gray
Write-Host "API Passphrase: $($apiPassphrase.Substring(0,5))..." -ForegroundColor Gray

$baseUrl = "https://api.kucoin.com"

# Function to make signed API request
function Invoke-KuCoinAPI {
    param(
        [string]$endpoint,
        [string]$method = "GET",
        [string]$body = ""
    )
    
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $strToSign = "$timestamp$method$endpoint$body"
    
    $hmac = New-Object System.Security.Cryptography.HMACSHA256
    $hmac.Key = [Text.Encoding]::UTF8.GetBytes($apiSecret)
    $signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($strToSign)))
    
    Write-Host "  Timestamp: $timestamp" -ForegroundColor DarkGray
    Write-Host "  Signature: $($signature.Substring(0,20))..." -ForegroundColor DarkGray
    
    $headers = @{
        'KC-API-KEY' = $apiKey
        'KC-API-SIGN' = $signature
        'KC-API-TIMESTAMP' = $timestamp
        'KC-API-PASSPHRASE' = $apiPassphrase
        'KC-API-KEY-VERSION' = '2'
        'Content-Type' = 'application/json'
    }
    
    Write-Host "  URL: $baseUrl$endpoint" -ForegroundColor DarkGray
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Method $method -Headers $headers -TimeoutSec 10
        return @{ success = $true; data = $response }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $statusDescription = $_.Exception.Response.StatusDescription
        $errorBody = $_.Exception.Response.Content
        
        if ($errorBody) {
            try {
                $errorContent = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream()).ReadToEnd()
                return @{ success = $false; statusCode = $statusCode; description = $statusDescription; body = $errorContent }
            }
            catch {
                return @{ success = $false; statusCode = $statusCode; description = $statusDescription; body = "Unable to read error body" }
            }
        } else {
            return @{ success = $false; statusCode = $statusCode; description = $statusDescription; body = $_.Exception.Message }
        }
    }
}

# Query 1: GET /api/v1/accounts?type=spot
Write-Host "`n[QUERY 1] GET /api/v1/accounts?type=spot" -ForegroundColor Cyan
$result1 = Invoke-KuCoinAPI -endpoint "/api/v1/accounts?type=spot" -method "GET"

if ($result1.success) {
    Write-Host "SUCCESS" -ForegroundColor Green
    Write-Host ($result1.data | ConvertTo-Json -Depth 10)
} else {
    Write-Host "ERROR: HTTP $($result1.statusCode) - $($result1.description)" -ForegroundColor Red
    Write-Host $result1.body -ForegroundColor Yellow
}

# Query 2: GET /api/v1/accounts?type=main
Write-Host "`n[QUERY 2] GET /api/v1/accounts?type=main" -ForegroundColor Cyan
$result2 = Invoke-KuCoinAPI -endpoint "/api/v1/accounts?type=main" -method "GET"

if ($result2.success) {
    Write-Host "SUCCESS" -ForegroundColor Green
    Write-Host ($result2.data | ConvertTo-Json -Depth 10)
} else {
    Write-Host "ERROR: HTTP $($result2.statusCode) - $($result2.description)" -ForegroundColor Red
    Write-Host $result2.body -ForegroundColor Yellow
}
