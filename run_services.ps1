# run_services.ps1 - PowerShell version for Windows
Write-Host "Starting Django server and MQTT consumer..."

# Start Django server
$djangoJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    python manage.py runserver 
}

# Start MQTT consumer
$consumerJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    python manage.py mqtt_consumer 
}

Write-Host "Django server running (Job ID: $($djangoJob.Id))"
Write-Host "MQTT consumer running (Job ID: $($consumerJob.Id))"
Write-Host "Press Ctrl+C to stop both services"

try {
    # Wait for jobs and show output
    while ($true) {
        Receive-Job $djangoJob
        Receive-Job $consumerJob
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host "Stopping services..."
    Stop-Job $djangoJob, $consumerJob
    Remove-Job $djangoJob, $consumerJob
}