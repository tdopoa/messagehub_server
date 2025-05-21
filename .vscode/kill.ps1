$connection = Get-NetTCPConnection -LocalPort 7071 -ErrorAction SilentlyContinue

if ($connection) {
    $targetPid = $connection.OwningProcess
    Stop-Process -Id $targetPid -Force -ErrorAction SilentlyContinue
    Write-Host "Info: Process $targetPid using port 7071 has been stopped."
} else {
    Write-Host "Info: Port 7071 is not in use. No process to stop."
}
