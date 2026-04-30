@echo off
chcp 65001 >nul
echo ============================================
echo   A股分析报告 - 定时任务设置
echo ============================================
echo.

REM 任务名称
set TASK_NAME=A股每日分析报告

REM Python路径
set PYTHON_PATH=D:\anaconda3\python.exe

REM 脚本目录
set WORK_DIR=D:\GITHUB\373Kice.github.io

REM 检查Python是否存在
if not exist "%PYTHON_PATH%" (
    echo [错误] Python未找到: %PYTHON_PATH%
    pause
    exit /b 1
)

echo [信息] Python路径: %PYTHON_PATH%
echo [信息] 工作目录: %WORK_DIR%
echo.

REM 删除已存在的任务
echo [步骤1] 检查并删除已存在的任务...
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo 任务已存在，正在删除...
    schtasks /Delete /TN "%TASK_NAME%" /F
)

REM 创建新任务
echo.
echo [步骤2] 创建定时任务...
schtasks /Create /TN "%TASK_NAME%" /TR "%PYTHON_PATH% \"%WORK_DIR%\generate_a_stock_report.py\"" /SC DAILY /ST 16:00 /F /RL HIGHEST

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [成功] 定时任务已创建！
    echo.
    echo 任务详情:
    echo   名称: %TASK_NAME%
    echo   触发器: 每天 16:00
    echo   操作: %PYTHON_PATH% generate_a_stock_report.py
    echo   工作目录: %WORK_DIR%
    echo.
    echo [提示] 可以通过以下方式管理任务:
    echo   - 打开 "任务计划程序" (taskschd.msc)
    echo   - 在 "任务计划程序库" 中找到任务
    echo.
) else (
    echo.
    echo [错误] 任务创建失败！
)

echo ============================================
pause
