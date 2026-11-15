# DHH Media Network - Windows Local Background Keep-Alive & Tick Watchdog
# Pings Render service every 5 minutes while user PC is active.

$renderUrl = "https://dhh-media-network.onrender.com"
$logPath = Join-Path $PSScriptRoot "keepalive.log"

Write-Host "Starting DHH Local Keep-Alive Heartbeat for $renderUrl..."
Add-Content -Path $logPath -Value "=== Heartbeat Started at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="

while ($true) {
    try {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $resp1 = Invoke-RestMethod -Uri "$renderUrl/health" -Method Get -TimeoutSec 15 -ErrorAction SilentlyContinue
        $resp2 = Invoke-RestMethod -Uri "$renderUrl/api/queue/tick" -Method Get -TimeoutSec 15 -ErrorAction SilentlyContinue
        $logLine = "[$timestamp] Heartbeat OK: Health=$($resp1.status) | Queue=$($resp2.action) (Pending=$($resp2.pending_in_queue), Due=$($resp2.due_count))"
        Add-Content -Path $logPath -Value $logLine
        Write-Host $logLine
    } catch {
        $logLine = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Heartbeat notice: $($_.Exception.Message)"
        Add-Content -Path $logPath -Value $logLine
        Write-Host $logLine
    }
    Start-Sleep -Seconds 300
}
