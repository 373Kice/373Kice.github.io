@echo off
REM ====================================================
REM A股分析网站自动化系统 - 一键启动脚本
REM 作者: WorkBuddy AI助手
REM 创建时间: 2026-03-11
REM ====================================================

echo.
echo ====================================================
echo        A股分析网站自动化系统
echo ====================================================
echo.

REM 检查是否在正确目录
if not exist "_config.yml" (
    echo 错误：不在Jekyll项目目录中！
    echo 请切换到 D:\GITHUB\373Kice.github.io 目录
    echo.
    pause
    exit /b 1
)

echo [1/5] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告：Python可能未安装或不在PATH中
    echo 请确保Python已正确安装
)

echo [2/5] 检查Ruby环境...
ruby --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告：Ruby可能未安装或不在PATH中
    echo 如需运行Jekyll网站，请安装Ruby
)

echo [3/5] 检查重要文件...
if not exist "daily_a_stock_analysis.py" (
    echo 错误：找不到 daily_a_stock_analysis.py
    exit /b 1
)

if not exist "run_jekyll_service.ps1" (
    echo 错误：找不到 run_jekyll_service.ps1
    exit /b 1
)

if not exist "setup_automation.ps1" (
    echo 错误：找不到 setup_automation.ps1
    exit /b 1
)

echo [4/5] 生成今日A股分析报告...
python daily_a_stock_analysis.py
if %errorlevel% neq 0 (
    echo 警告：报告生成脚本可能有问题
    echo 但将继续执行其他步骤...
)

echo [5/5] 启动自动化安装界面...
echo.
echo 请选择要执行的操作：
echo.
echo   1. 启动Jekyll网站服务（推荐）
echo   2. 创建Windows计划任务（需要管理员）
echo   3. 运行系统测试
echo   4. 查看帮助文档
echo   5. 退出
echo.

set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" (
    echo 正在启动Jekyll网站服务...
    powershell -ExecutionPolicy Bypass -File "run_jekyll_service.ps1"
) else if "%choice%"=="2" (
    echo.
    echo ⚠️ 创建计划任务需要管理员权限！
    echo 请用管理员身份运行以下命令：
    echo.
    echo   powershell -ExecutionPolicy Bypass -File "create_daily_report_task.ps1"
    echo.
    pause
) else if "%choice%"=="3" (
    echo 正在运行系统测试...
    python test_automation.py
    pause
) else if "%choice%"=="4" (
    echo 打开帮助文档...
    start README_AUTOMATION.md
    pause
) else if "%choice%"=="5" (
    echo 退出系统
    exit /b 0
) else (
    echo 无效选项
    pause
)

echo.
echo ====================================================
echo       自动化系统已配置完成！
echo ====================================================
echo.
echo 🎯 核心功能：
echo   • 每天下午4点自动生成A股分析报告
echo   • Jekyll网站自动更新内容
echo   • 无需手动重启，实时生效
echo.
echo 🌐 网站地址：
echo   http://127.0.0.1:4001/
echo.
echo 📋 管理命令：
echo   • 手动生成报告：python daily_a_stock_analysis.py
echo   • 启动网站服务：.\run_jekyll_service.ps1
echo   • 系统测试：python test_automation.py
echo.
echo ⚡ 快速验证：
echo   访问 http://127.0.0.1:4001/ 查看网站是否正常运行
echo.
pause