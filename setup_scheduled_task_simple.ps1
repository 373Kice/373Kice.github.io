# A股分析报告 - Windows定时任务设置脚本（简化版）
# 每天下午4点自动生成A股分析报告

$taskName = "A股每日分析报告"

# Remove existing task if exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Get python path
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "ERROR: Python not found in PATH"
    exit 1
}

Write-Host "Using Python: $pythonPath"

# Create task action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "generate_a_stock_report.py" `
    -WorkingDirectory "d:\GITHUB\373Kice.github.io"

# Create task trigger (daily at 4:00 PM)
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "16:00"

# Create task principal (run whether user is logged on or not)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Generate A-stock market analysis report daily at 4:00 PM"

# Verify
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "`nSUCCESS! Task '$taskName' created!" -ForegroundColor Green
    Write-Host "`nTask Details:"
    Write-Host "  Name: $taskName"
    Write-Host "  Trigger: Daily at 16:00"
    Write-Host "  Action: $pythonPath generate_a_stock_report.py"
    Write-Host "`nYou can manage this task in Task Scheduler (taskschd.msc)"
} else {
    Write-Host "ERROR: Task creation failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nDone!"
