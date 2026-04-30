# A股分析网站自动化一键安装脚本
# 保存为 setup_automation.ps1
# 这个脚本将安装所有必要的自动化功能

Write-Host "=== A股分析网站自动化安装程序 ===" -ForegroundColor Cyan
Write-Host "时间: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# 第一步：检查环境
Write-Host "🔍 步骤1：检查系统环境..." -ForegroundColor Yellow

# 检查Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或不在PATH中" -ForegroundColor Red
    Write-Host "请从 https://python.org 下载并安装Python" -ForegroundColor Yellow
    exit 1
}

# 检查Ruby和Bundler
try {
    $rubyVersion = ruby --version 2>&1
    Write-Host "✅ Ruby已安装: $rubyVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Ruby未安装，但可以继续（如果需要运行Jekyll网站）" -ForegroundColor Yellow
}

# 检查当前目录
if (-not (Test-Path "_config.yml")) {
    Write-Host "❌ 错误：不在Jekyll项目目录中！" -ForegroundColor Red
    Write-Host "请在 D:\GITHUB\373Kice.github.io 目录中运行此脚本" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 步骤2：验证工具脚本..." -ForegroundColor Yellow

# 检查重要脚本文件
$requiredFiles = @(
    "daily_a_stock_analysis.py",
    "run_jekyll_service.ps1",
    "create_daily_report_task.ps1"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file 存在" -ForegroundColor Green
    } else {
        Write-Host "❌ $file 不存在" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 步骤3：选择安装选项" -ForegroundColor Cyan

Write-Host ""
Write-Host "请选择要安装的功能：" -ForegroundColor White
Write-Host "1. 只创建计划任务（每天下午4点自动生成报告）" -ForegroundColor Gray
Write-Host "2. 启动Jekyll网站服务（长期运行）" -ForegroundColor Gray
Write-Host "3. 完整安装（任务 + 服务）" -ForegroundColor Gray
Write-Host "4. 查看帮助信息" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "请输入选项 (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🎯 选项1：创建计划任务" -ForegroundColor Green
        
        Write-Host "需要管理员权限创建计划任务..." -ForegroundColor Yellow
        Write-Host "请用管理员身份运行以下命令：" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "powershell -ExecutionPolicy Bypass -File `"$PWD\create_daily_report_task.ps1`"" -ForegroundColor White -BackgroundColor DarkBlue
        Write-Host ""
        Write-Host "或者手动以管理员身份运行 PowerShell，然后执行：" -ForegroundColor Cyan
        Write-Host "cd `"$PWD`"" -ForegroundColor Gray
        Write-Host ".\create_daily_report_task.ps1" -ForegroundColor Gray
        
        Write-Host ""
        Write-Host "📋 安装后操作：" -ForegroundColor Yellow
        Write-Host "1. 每天下午4点自动运行 python daily_a_stock_analysis.py" -ForegroundColor Gray
        Write-Host "2. 需要保持Jekyll网站运行（运行 run_jekyll_service.ps1）" -ForegroundColor Gray
    }
    
    "2" {
        Write-Host ""
        Write-Host "🌐 选项2：启动Jekyll网站服务" -ForegroundColor Green
        
        # 检查Jekyll依赖
        if (Test-Path "Gemfile") {
            Write-Host "正在检查Gemfile依赖..." -ForegroundColor Yellow
            bundle install
        }
        
        Write-Host "启动Jekyll服务..." -ForegroundColor Green
        Write-Host "执行命令：" -ForegroundColor Cyan
        Write-Host "powershell -ExecutionPolicy Bypass -File `"$PWD\run_jekyll_service.ps1`"" -ForegroundColor White -BackgroundColor DarkBlue
        Write-Host ""
        
        # 启动服务（在新窗口）
        Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PWD\run_jekyll_service.ps1`"" -WindowStyle Normal
        
        Write-Host "Jekyll服务已在新的PowerShell窗口中启动" -ForegroundColor Green
        Write-Host "网站地址: http://127.0.0.1:4001/" -ForegroundColor Cyan
        Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
    }
    
    "3" {
        Write-Host ""
        Write-Host "🎯 选项3：完整安装" -ForegroundColor Green
        
        # 步骤1：启动Jekyll服务
        Write-Host "步骤1：启动Jekyll网站服务..." -ForegroundColor Yellow
        
        # 检查Jekyll依赖
        if (Test-Path "Gemfile") {
            Write-Host "正在检查Gemfile依赖..." -ForegroundColor Gray
            bundle install
        }
        
        # 启动服务（后台进程）
        $job = Start-Job -ScriptBlock {
            Set-Location $using:PWD
            bundle exec jekyll serve --host 127.0.0.1 --port 4001 --livereload
        }
        
        Write-Host "Jekyll服务已启动（后台进程）" -ForegroundColor Green
        Write-Host "网站地址: http://127.0.0.1:4001/" -ForegroundColor Cyan
        Write-Host "进程ID: $($job.Id)" -ForegroundColor Gray
        
        # 步骤2：创建计划任务
        Write-Host ""
        Write-Host "步骤2：创建计划任务..." -ForegroundColor Yellow
        Write-Host "需要管理员权限创建计划任务..." -ForegroundColor Cyan
        Write-Host "请用管理员身份运行以下命令：" -ForegroundColor White
        Write-Host "powershell -ExecutionPolicy Bypass -File `"$PWD\create_daily_report_task.ps1`"" -ForegroundColor White -BackgroundColor DarkBlue
        
        Write-Host ""
        Write-Host "📋 完整安装完成：" -ForegroundColor Green
        Write-Host "1. ✅ Jekyll网站已在后台运行" -ForegroundColor Gray
        Write-Host "2. 🔧 计划任务需要管理员权限手动创建" -ForegroundColor Gray
        Write-Host "3. 📊 网站自动更新新文章" -ForegroundColor Gray
        Write-Host "4. ⏰ 每天下午4点自动生成报告" -ForegroundColor Gray
    }
    
    "4" {
        Write-Host ""
        Write-Host "📖 帮助信息" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "=== 系统架构 ===" -ForegroundColor Yellow
        Write-Host "1. Jekyll网站服务 (run_jekyll_service.ps1)" -ForegroundColor Gray
        Write-Host "   - 长期运行在 http://127.0.0.1:4001/" -ForegroundColor Gray
        Write-Host "   - 自动检测文件变化并重新生成" -ForegroundColor Gray
        Write-Host "   - 无需手动重启" -ForegroundColor Gray
        Write-Host ""
        Write-Host "2. 自动报告生成器 (daily_a_stock_analysis.py)" -ForegroundColor Gray
        Write-Host "   - 自动创建当日A股分析报告模板" -ForegroundColor Gray
        Write-Host "   - 包含完整的分析框架" -ForegroundColor Gray
        Write-Host "   - 需要手动填入当日数据或集成API" -ForegroundColor Gray
        Write-Host ""
        Write-Host "3. Windows计划任务 (create_daily_report_task.ps1)" -ForegroundColor Gray
        Write-Host "   - 每天下午4点自动运行报告生成器" -ForegroundColor Gray
        Write-Host "   - 需要管理员权限创建" -ForegroundColor Gray
        Write-Host ""
        Write-Host "=== 使用方法 ===" -ForegroundColor Yellow
        Write-Host "快速启动: .\setup_automation.ps1" -ForegroundColor Gray
        Write-Host "只启动网站: .\run_jekyll_service.ps1" -ForegroundColor Gray
        Write-Host "创建任务: .\create_daily_report_task.ps1 (管理员)" -ForegroundColor Gray
        Write-Host "手动生成报告: python daily_a_stock_analysis.py" -ForegroundColor Gray
        Write-Host ""
        Write-Host "=== 验证安装 ===" -ForegroundColor Yellow
        Write-Host "1. 访问 http://127.0.0.1:4001/" -ForegroundColor Gray
        Write-Host "2. 检查能否看到文章" -ForegroundColor Gray
        Write-Host "3. 测试添加新文章" -ForegroundColor Gray
        Write-Host "4. 验证自动更新功能" -ForegroundColor Gray
    }
    
    default {
        Write-Host "❌ 无效选项" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host "如有问题，请查看 README_AUTOMATION.md 文档" -ForegroundColor Cyan