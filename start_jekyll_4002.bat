@echo off
echo ============================================
echo     启动Jekyll网站服务（端口4002）
echo ============================================
echo.
echo 启动Jekyll网站服务...
echo 网站地址: http://127.0.0.1:4002/
echo.
cd /d "D:\GITHUB\373Kice.github.io"
jekyll serve --port 4002 --host 127.0.0.1 --livereload
echo.
echo Jekyll服务已停止。
echo ============================================
pause