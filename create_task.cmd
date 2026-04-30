@echo off
schtasks /Create /TN "A股每日分析报告" /TR "D:\anaconda3\python.exe D:\GITHUB\373Kice.github.io\generate_a_stock_report.py" /SC DAILY /ST 16:00 /F /RL HIGHEST
if %ERRORLEVEL% EQU 0 (echo Task created successfully!) else (echo Task creation failed!)
