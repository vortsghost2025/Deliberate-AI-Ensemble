$envMap = @{}
Get-Content C:\workspace\.env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)\s*=\s*(.*)$') {
    $envMap[$matches[1]] = $matches[2]
  }
}
$apiKey = $envMap['LIVE_API_KEY']
$apiSecret = $envMap['LIVE_API_SECRET']
$passphrase = $envMap['LIVE_API_PASSPHRASE']

$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds().ToString()
$method = 'GET'
$endpoint = '/api/v1/accounts'
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
  Write-Host "RAW_RESPONSE:"
  $resp | ConvertTo-Json -Depth 10
} catch {
  Write-Host "ERROR: $_"
  $_.Exception.Response
}
