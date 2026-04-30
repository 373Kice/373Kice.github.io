@echo off
REM Windows批处理脚本：更新Jekyll项目所有依赖
echo ============================================
echo    Jekyll项目依赖更新工具 - Windows版本
echo ============================================
echo.

REM 检查是否在正确目录
if not exist "Gemfile" (
    echo ❌ 错误: 当前目录没有Gemfile文件
    echo 请确保在Jekyll项目根目录运行此脚本
    pause
    exit /b 1
)

REM 备份现有的Gemfile.lock
set timestamp=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
if exist "Gemfile.lock" (
    copy "Gemfile.lock" "Gemfile.lock.backup-%timestamp%" >nul
    echo ✅ 已备份Gemfile.lock到: Gemfile.lock.backup-%timestamp%
) else (
    echo ℹ️  未找到Gemfile.lock，可能是新项目
)

echo.
echo 1. 检查当前Bundler版本...
call bundle --version
if errorlevel 1 (
    echo ❌ Bundler未正确安装
    echo 请确保Ruby和Bundler已正确安装
    pause
    exit /b 1
)

echo.
echo 2. 更新Bundler到最新版本...
call gem update bundler
if errorlevel 1 (
    echo ⚠️  更新Bundler时出错，但可能不影响后续操作
)

echo.
echo 3. 清理旧的gem缓存...
call bundle clean --force
if errorlevel 1 (
    echo ℹ️  清理缓存时遇到问题，继续执行...
)

echo.
echo 4. 安装所有gem依赖（首次或重新安装）...
call bundle install
if errorlevel 1 (
    echo ❌ 依赖安装失败
    echo 请检查错误信息
    pause
    exit /b 1
)

echo.
echo 5. 更新所有gem到最新版本...
echo 注意: 这可能需要一些时间...
call bundle update --all
if errorlevel 1 (
    echo ⚠️  更新过程中遇到问题
    echo 尝试只更新主要gem...
    call bundle update jekyll jekyll-paginate kramdown rouge webrick
)

echo.
echo 6. 检查依赖状态...
call bundle check
if errorlevel 1 (
    echo ❌ 依赖检查失败
    echo 尝试修复...
    call bundle install
) else (
    echo ✅ 依赖状态正常
)

echo.
echo 7. 显示关键gem版本信息...
echo Jekyll版本:
for /f "tokens=*" %%i in ('bundle exec jekyll --version') do echo   %%i
echo.
echo Bundler版本:
for /f "tokens=*" %%i in ('bundle --version') do echo   %%i

echo.
echo ============================================
echo               更新完成！
echo ============================================
echo.
echo 下一步操作建议:
echo 1. 运行 'bundle exec jekyll serve' 启动网站
echo 2. 访问 http://127.0.0.1:4000/ 测试网站
echo 3. 检查控制台是否有任何错误或警告
echo 4. 如有问题，可使用备份文件恢复
if exist "Gemfile.lock.backup-%timestamp%" (
    echo    恢复命令: copy "Gemfile.lock.backup-%timestamp%" "Gemfile.lock"
)
echo.
echo 注意: 如果更新后网站出现问题:
echo   a. 检查Jekyll日志中的错误信息
echo   b. 可能需要调整配置文件以适应新版本
echo   c. 如有需要，可以使用备份文件回滚
echo.
pause