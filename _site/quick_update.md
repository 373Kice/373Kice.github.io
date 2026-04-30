# 快速更新指南

## 已完成的更新
✅ Gemfile已更新（移除了版本限制）
✅ Sass弃用警告已修复
✅ wdm gem已添加

## 需要执行的手动步骤

### 步骤1: 停止当前服务器
1. 在当前终端按 **Ctrl+C** 停止Jekyll服务器

### 步骤2: 更新Bundler和所有依赖
在项目目录中执行：

```bash
# 1. 更新Bundler
gem update bundler

# 2. 清理旧缓存
bundle clean --force

# 3. 安装最新依赖
bundle install

# 4. 验证依赖
bundle check
```

### 步骤3: 重新启动网站
```bash
# 启动开发服务器
bundle exec jekyll serve

# 或指定端口
bundle exec jekyll serve --port 4001
```

## 预期结果

### 版本更新
- **Bundler**: 从4.0.8更新到最新（~4.x）
- **Jekyll**: 从4.4.1更新到最新兼容版本
- **其他gem**: 全部更新到最新稳定版

### 性能改进
1. **Windows优化**: wdm gem提升文件监听性能
2. **Sass现代化**: 使用@use代替弃用的@import
3. **依赖更新**: 所有安全更新和性能改进

## 验证更新成功

更新后检查：
1. **控制台输出**: 应该没有Bundler版本警告
2. **Sass警告**: 应该没有弃用警告
3. **网站功能**: 所有页面正常显示
4. **性能**: 文件修改检测应该更快

## 备用方案

如果更新失败，可以：

### 方案A: 保留当前稳定版本
```bash
# 恢复版本限制
# 编辑Gemfile，将 "gem \"jekyll\"" 改回 "gem \"jekyll\", \"~> 4.2\""
# 然后运行 bundle install
```

### 方案B: 逐步更新
```bash
# 只更新关键gem
bundle update jekyll webrick kramdown rouge
```

### 方案C: 创建新环境
```bash
# 备份当前
cp Gemfile Gemfile.backup
cp Gemfile.lock Gemfile.lock.backup

# 使用新Gemfile
bundle install
```

## 立即执行的命令

如果你现在想更新，执行：

```bash
# 先停止服务器 (Ctrl+C)
# 然后执行
gem update bundler && bundle clean --force && bundle install && bundle exec jekyll serve
```

## 技术支持
如有问题：
1. 检查错误信息
2. 查看Gemfile.lock中的版本
3. 运行 `bundle exec jekyll doctor`
4. 如有需要，使用备份文件恢复