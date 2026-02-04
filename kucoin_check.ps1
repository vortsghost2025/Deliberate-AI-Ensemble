$envMap = @{}
Get-Content C:\workspace\.env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)\s*=\s*(.*)$') {
    $envMap[$matches[1]] = $matches[2]
  }
}
$apiKey = $envMap['LIVE_API_KEY']
$apiSecret = $envMap['LIVE_API_SECRET']
$passphrase = $envMap['LIVE_API_PASSPHRASE']
if (-not $apiKey -or -not $apiSecret) {
  Write-Host 'MISSING_KEYS'
  exit 1
}
if (-not $passphrase) {
  Write-Host 'MISSING_PASSPHRASE'
  exit 1
}
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds().ToString()
$method = 'GET'
$endpoint = '/api/v1/accounts?type=main'
$body = ''
$prehash = $timestamp + $method + $endpoint + $body
$secretBytes = [Text.Encoding]::UTF8.GetBytes($apiSecret)
$hmac = New-Object System.Security.Cryptography.HMACSHA256 -ArgumentList (, $secretBytes)
$signature = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($prehash)))
$passSig = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($passphrase)))
$headers = @{
  'KC-API-KEY' = $apiKey
  'KC-API-SIGN' = $signature
  'KC-API-TIMESTAMP' = $timestamp
  'KC-API-PASSPHRASE' = $passSig
  'KC-API-KEY-VERSION' = '2'
}
try {
  $resp = Invoke-RestMethod -Method Get -Uri "https://api.kucoin.com$endpoint" -Headers $headers
  if ($resp.code -ne '200000') {
    Write-Host "KUCOIN_API_ERROR:$($resp.code)"
    exit 1
  }
  $accounts = $resp.data
  $count = $accounts.Count
  $usdt = ($accounts | Where-Object { $_.currency -eq 'USDT' } | Measure-Object -Property available -Sum).Sum
  $nonzero = $accounts | Where-Object { [decimal]$_.available -gt 0 } | Select-Object -First 3
  Write-Host 'KUCOIN_OK'
  Write-Host "Accounts:$count"
  Write-Host "USDT_Available:$usdt"
  foreach ($a in $nonzero) {
    Write-Host ("{0}:{1}" -f $a.currency, $a.available)
  }
} catch {
  Write-Host 'KUCOIN_REQUEST_FAILED'
  exit 1
}
