@echo off
echo ============================================
echo     创建每日A股分析报告自动生成任务
echo ============================================
echo.
echo 注意：请以管理员身份运行此批处理文件
echo.
pause

echo 检查任务是否已存在...
schtasks /query /tn "每日A股分析报告生成" >nul 2>&1
if %errorlevel% equ 0 (
    echo 任务已存在，删除旧任务...
    schtasks /delete /tn "每日A股分析报告生成" /f
    echo 旧任务已删除
)

echo.
echo 创建新任务...
schtasks /create /tn "每日A股分析报告生成" /tr "python \"D:\GITHUB\373Kice.github.io\daily_a_stock_analysis.py\"" /sc DAILY /st 16:00 /ru "SYSTEM" /rl HIGHEST

if %errorlevel% equ 0 (
    echo.
    echo [成功] 计划任务创建成功！
    echo 任务名称: 每日A股分析报告生成
    echo 执行时间: 每天下午4:00
    echo 执行命令: python daily_a_stock_analysis.py
    echo.
    echo [信息] 任务详情:
    echo 1. 任务将在每天下午4点自动运行
    echo 2. 系统帐户权限执行
    echo 3. 无需登录即可运行
    echo.
    echo [操作] 管理任务命令:
    echo 查看任务: schtasks /query /tn "每日A股分析报告生成"
    echo 立即运行: schtasks /run /tn "每日A股分析报告生成"
    echo 删除任务: schtasks /delete /tn "每日A股分析报告生成"
) else (
    echo.
    echo [错误] 创建任务失败，可能需要管理员权限
    echo 请手动打开任务计划程序:
    echo 1. 按 Win+R，输入 taskschd.msc
    echo 2. 创建基本任务
    echo 3. 名称: 每日A股分析报告生成
    echo 4. 触发器: 每天 16:00
    echo 5. 操作: 启动程序 -> python
    echo 6. 参数: "D:\GITHUB\373Kice.github.io\daily_a_stock_analysis.py"
    echo 7. 起始于: "D:\GITHUB\373Kice.github.io"
)

echo.
echo ============================================
pause