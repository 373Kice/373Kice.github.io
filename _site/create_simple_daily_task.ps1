# 简单的Windows计划任务创建脚本
# 以管理员身份运行此脚本

# 检查是否以管理员身份运行
$adminCheck = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $adminCheck.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    exit 1
}

# 任务配置
$TaskName = "每日A股分析报告生成"
$TaskDescription = "每天下午4点自动生成A股大盘分析报告"
$ScriptPath = "D:\GITHUB\373Kice.github.io\daily_a_stock_analysis.py"
$WorkingDir = "D:\GITHUB\373Kice.github.io"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    创建每日A股分析报告自动生成任务" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查任务是否已存在
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "任务 '$TaskName' 已存在，删除旧任务..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "旧任务已删除" -ForegroundColor Green
}

# 创建触发器（每天下午4点）
$trigger = New-ScheduledTaskTrigger -Daily -At "16:00"

# 创建操作（运行Python脚本）
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$ScriptPath`"" -WorkingDirectory $WorkingDir

# 创建任务设置
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

# 创建任务
try {
    $task = Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $TaskDescription `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -RunLevel Highest `
        -Force

    Write-Host ""
    Write-Host "[成功] 计划任务创建成功！" -ForegroundColor Green
    Write-Host "任务名称: $TaskName" -ForegroundColor Cyan
    Write-Host "执行时间: 每天下午4:00" -ForegroundColor Cyan
    Write-Host "执行命令: python `"$ScriptPath`"" -ForegroundColor Cyan
    Write-Host "工作目录: $WorkingDir" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "[信息] 计划任务详情:" -ForegroundColor Yellow
    Write-Host "1. 任务将在每天下午4点自动运行" -ForegroundColor Gray
    Write-Host "2. 即使计算机使用电池也会运行" -ForegroundColor Gray
    Write-Host "3. 会自动唤醒休眠的计算机" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "[操作] 管理任务命令:" -ForegroundColor Yellow
    Write-Host "查看任务:   Get-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "立即运行:   Start-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "禁用任务:   Disable-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "启用任务:   Enable-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "删除任务:   Unregister-ScheduledTask -TaskName `"$TaskName`" -Confirm:`$false" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "[测试] 立即测试任务运行:" -ForegroundColor Yellow
    Write-Host "python `"$ScriptPath`"" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host "[错误] 创建任务失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "[帮助] 手动创建方法:" -ForegroundColor Yellow
    Write-Host "1. 按 Win+R，输入 taskschd.msc" -ForegroundColor Gray
    Write-Host "2. 创建基本任务" -ForegroundColor Gray
    Write-Host "3. 名称: 每日A股分析报告生成" -ForegroundColor Gray
    Write-Host "4. 触发器: 每天 16:00" -ForegroundColor Gray
    Write-Host "5. 操作: 启动程序 -> python" -ForegroundColor Gray
    Write-Host "6. 参数: `"$ScriptPath`"" -ForegroundColor Gray
    Write-Host "7. 起始于: `"$WorkingDir`"" -ForegroundColor Gray
}

Write-Host "============================================" -ForegroundColor DarkGray
Write-Host ""