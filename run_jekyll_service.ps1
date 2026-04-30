# Jekyll网站长期运行脚本
# 在Windows上作为后台服务运行
# 保存为 run_jekyll_service.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Jekyll网站服务启动 ===" -ForegroundColor Cyan
Write-Host "时间: $(Get-Date)" -ForegroundColor Gray
Write-Host "目录: $PWD" -ForegroundColor Gray

# 检查是否在正确的目录
if (-not (Test-Path "_config.yml")) {
    Write-Host "错误: 不在Jekyll项目目录中！" -ForegroundColor Red
    exit 1
}

# 检查Gemfile.lock是否存在
if (-not (Test-Path "Gemfile.lock")) {
    Write-Host "警告: Gemfile.lock不存在，尝试生成..." -ForegroundColor Yellow
    bundle install
}

# 设置环境变量（Windows优化）
$env:JEKYLL_ENV = "production"
$env:LC_ALL = "en_US.UTF-8"

# 启动Jekyll服务器（自动监视文件变化）
Write-Host "启动Jekyll服务器..." -ForegroundColor Green
Write-Host "网站地址: http://127.0.0.1:4002/" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动Jekyll服务
# --livereload 启用实时重载（开发时有用）
# --host 0.0.0.0 可以在局域网访问
# --port 4001 指定端口
# --incremental 增量构建，加快大项目速度
# --watch 监视文件变化（默认启用）

try {
    bundle exec jekyll serve --host 127.0.0.1 --port 4002 --livereload
} catch {
    Write-Host "Jekyll启动失败: $_" -ForegroundColor Red
    Write-Host "尝试安装依赖并重试..." -ForegroundColor Yellow
    
    # 尝试修复依赖
    bundle install
    
    # 再次尝试启动
    Write-Host "重新启动Jekyll..." -ForegroundColor Green
    bundle exec jekyll serve --host 127.0.0.1 --port 4001
}