# A股分析报告 - Windows定时任务设置脚本
# 每天下午4点自动生成A股分析报告

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[警告] 建议以管理员身份运行此脚本" -ForegroundColor Yellow
}

# 任务名称
$taskName = "A股每日分析报告"

# 检查任务是否已存在
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[提示] 任务 '$taskName' 已存在，将先删除旧任务" -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# 设置任务操作
# 注意：需要确保python在PATH中，或者使用完整路径
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "[错误] 未找到python命令，请确保Python已安装并添加到PATH" -ForegroundColor Red
    exit 1
}

Write-Host "[信息] 使用Python路径: $pythonPath" -ForegroundColor Green

$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "generate_a_stock_report.py" `
    -WorkingDirectory "d:\GITHUB\373Kice.github.io"

# 设置任务触发器（每天下午4点）
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "16:00"

# 设置任务主体（使用当前用户，无论是否登录都运行）
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

# 设置任务设置
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun

# 注册任务
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "每天下午4点自动生成A股大盘分析报告"

# 验证任务是否创建成功
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "`n[成功] 定时任务 '$taskName' 已创建！" -ForegroundColor Green
    Write-Host "`n任务详情:" -ForegroundColor Cyan
    Write-Host "  名称: $taskName"
    Write-Host "  触发器: 每天 16:00"
    Write-Host "  操作: $pythonPath generate_a_stock_report.py"
    Write-Host "  工作目录: d:\GITHUB\373Kice.github.io"
    
    Write-Host "`n[提示] 可以通过以下方式管理任务:" -ForegroundColor Yellow
    Write-Host "  - 打开 '任务计划程序' (taskschd.msc)"
    Write-Host "  - 在左侧导航栏找到 '任务计划程序库'"
    Write-Host "  - 找到任务: $taskName"
    Write-Host "`n  ɖ或使用PowerShell命令:"
    Write-Host "  - 查看任务: Get-ScheduledTask -TaskName '$taskName'"
    Write-Host "  - 运行任务: Start-ScheduledTask -TaskName '$taskName'"
    Write-Host "  - 删除任务: Unregister-ScheduledTask -TaskName '$taskName'"
} else {
    Write-Host "[错误] 任务创建失败" -ForegroundColor Red
    exit 1
}

Write-Host "`n[完成] 脚本执行完成！" -ForegroundColor Green
