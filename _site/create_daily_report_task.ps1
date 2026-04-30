# 创建Windows计划任务：每天下午4点自动生成A股分析报告
# 保存为 create_daily_report_task.ps1
# 以管理员身份运行此脚本创建任务

# 检查是否以管理员身份运行
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    exit 1
}
}

# 脚本配置
$TaskName = "每日A股分析报告生成"
$TaskDescription = "每天下午4点自动生成A股大盘分析报告，更新Jekyll网站"
$ScriptPath = "D:\GITHUB\373Kice.github.io\daily_a_stock_analysis.py"
$WorkingDirectory = "D:\GITHUB\373Kice.github.io"
$PythonPath = "python"  # 或者指定完整路径 "C:\Python39\python.exe"

# 触发器：每天下午4:00
$Trigger = New-ScheduledTaskTrigger -Daily -At "16:00"

# 触发器2：也可以添加每周工作日（周一到周五）下午4点
$WorkdayTrigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday `
    -At "16:00"

# 触发器3：测试触发器（1分钟后运行，用于测试）
$TestTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)

# 操作：运行Python脚本
$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$ScriptPath`"" `
    -WorkingDirectory $WorkingDirectory

# 任务设置
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun

# 尝试创建任务
try {
    # 检查任务是否已存在
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($ExistingTask) {
        Write-Host "任务 '$TaskName' 已存在，将更新它..." -ForegroundColor Yellow
        
        # 先删除现有任务
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        
        Write-Host "已删除旧任务。" -ForegroundColor Green
    }
    
    # 创建新任务
    $Task = Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $TaskDescription `
        -Trigger $Trigger, $WorkdayTrigger `
        -Action $Action `
        -Settings $Settings `
        -RunLevel Highest `
        -Force
    
    Write-Host ""
    Write-Host "✅ 任务创建成功！" -ForegroundColor Green
    Write-Host "任务名称: $TaskName" -ForegroundColor Cyan
    Write-Host "任务描述: $TaskDescription" -ForegroundColor Cyan
    Write-Host "执行时间: 每天下午4:00 + 工作日（周一到周五）下午4:00" -ForegroundColor Cyan
    Write-Host "执行命令: $PythonPath `"$ScriptPath`"" -ForegroundColor Cyan
    Write-Host "工作目录: $WorkingDirectory" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "📋 任务详情:" -ForegroundColor Yellow
    Write-Host "1. 任务将在指定时间自动运行" -ForegroundColor Gray
    Write-Host "2. 即使计算机使用电池也会运行" -ForegroundColor Gray
    Write-Host "3. 需要网络连接（获取股票数据）" -ForegroundColor Gray
    Write-Host "4. 会唤醒休眠的计算机执行任务" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "🔧 管理任务方法:" -ForegroundColor Yellow
    Write-Host "查看任务:   taskschd.msc" -ForegroundColor Gray
    Write-Host "启用任务:   Enable-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "禁用任务:   Disable-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    Write-Host "删除任务:   Unregister-ScheduledTask -TaskName `"$TaskName`" -Confirm:`$false" -ForegroundColor Gray
    Write-Host "立即运行:   Start-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "🎯 手动测试（可选）:" -ForegroundColor Yellow
    Write-Host "手动运行脚本: python `"$ScriptPath`"" -ForegroundColor Gray
    
    # 测试触发器（注释掉，需要时启用）
    # Write-Host "创建测试任务（1分钟后运行）..." -ForegroundColor Yellow
    # $TestTask = Register-ScheduledTask `
    #     -TaskName "$TaskName-测试" `
    #     -Description "测试任务 - $TaskDescription" `
    #     -Trigger $TestTrigger `
    #     -Action $Action `
    #     -Settings $Settings `
    #     -RunLevel Highest `
    #     -Force
    
} catch {
    Write-Host "[错误] 创建任务失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "[提示] 手动创建任务方法:" -ForegroundColor Yellow
    Write-Host "1. 按 Win+R 打开运行对话框" -ForegroundColor Gray
    Write-Host "2. 输入 taskschd.msc 并回车" -ForegroundColor Gray
    Write-Host "3. 创建基本任务" -ForegroundColor Gray
    Write-Host "4. 名称: 每日A股分析报告生成" -ForegroundColor Gray
    Write-Host "5. 触发器: 每天 16:00" -ForegroundColor Gray
    Write-Host "6. 操作: 启动程序" -ForegroundColor Gray
    Write-Host "7. 程序: python" -ForegroundColor Gray
    Write-Host "8. 参数: `"D:\GITHUB\373Kice.github.io\daily_a_stock_analysis.py`"" -ForegroundColor Gray
    Write-Host "9. 起始于: `"D:\GITHUB\373Kice.github.io`"" -ForegroundColor Gray
}
finally {
    Write-Host "============================================" -ForegroundColor DarkGray
}