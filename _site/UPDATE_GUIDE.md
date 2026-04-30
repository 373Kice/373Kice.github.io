# Jekyll项目依赖更新指南

## 当前状态
- Bundler版本: 4.0.8 (运行中)
- Gemfile.lock生成版本: 2.3.25
- 需要将所有依赖更新到最新版本

## 更新步骤

### 1. 更新Bundler到最新版本
```bash
# 更新Bundler
gem update bundler

# 验证Bundler版本
bundle --version
```

### 2. 更新Gemfile（已完成）
我已经更新了你的Gemfile，移除了版本限制：
- 移除了`jekyll`的`~> 4.2`限制
- 移除了`webrick`的`~> 1.7`限制  
- 移除了`wdm`的`>= 0.1.0`限制
- 注释掉了已弃用的`sassc`（Jekyll 4.4+使用sass-embedded）

### 3. 更新所有gem依赖
执行以下命令更新所有依赖：

```bash
# 先清理旧的依赖缓存
bundle clean --force

# 安装更新后的依赖
bundle install

# 或者直接更新所有gem到最新版本
bundle update --all
```

### 4. 验证更新结果
```bash
# 检查依赖状态
bundle check

# 查看Jekyll版本
bundle exec jekyll --version

# 查看Gemfile.lock中的版本
cat Gemfile.lock | grep -A5 "GEM"
```

## 预期更新

### 主要gem的预期更新
1. **Jekyll**: 从 4.4.1 更新到最新（可能是 4.5.x 或 5.x）
2. **webrick**: 从 1.9.2 更新到最新
3. **其他依赖**: 所有间接依赖也会更新到最新兼容版本

### 注意事项
1. **Jekyll 5.x警告**: 如果更新到Jekyll 5.x，可能会有破坏性变更
   - 检查[官方升级指南](https://jekyllrb.com/docs/upgrading/)
   - 备份现有配置和内容

2. **Windows兼容性**: 
   - `wdm` gem会优化Windows性能
   - 确保所有gem都有Windows兼容版本

3. **Sass处理**:
   - 已移除`sassc`（已弃用）
   - Jekyll 4.4+使用`sass-embedded`，性能更好

## 测试更新后的网站

更新完成后，测试网站：
```bash
# 启动开发服务器
bundle exec jekyll serve

# 或指定端口
bundle exec jekyll serve --port 4001
```

### 验证检查清单
- [ ] 网站正常启动，无错误
- [ ] 所有页面正常显示
- [ ] CSS样式正确应用
- [ ] 导航链接正常工作
- [ ] 代码高亮功能正常
- [ ] 控制台无警告或错误

## 故障排除

### 如果更新失败
1. **恢复备份**: 使用`Gemfile.lock.backup-*`文件恢复
2. **锁定版本**: 在Gemfile中重新添加版本限制
3. **逐步更新**: 逐个更新gem而不是一次性全部更新

### 常见问题
1. **版本冲突**: 运行`bundle exec jekyll doctor`诊断
2. **缺少依赖**: 检查错误信息，可能需要额外gem
3. **配置兼容性**: 检查`_config.yml`是否需要更新

## 备份文件
- `Gemfile.lock.backup-*`: 原始依赖锁定文件备份
- 建议在更新前备份整个项目

## 执行更新
我已经为你准备了更新脚本：
- `update_all_deps.bat` - Windows批处理脚本
- `update_dependencies.rb` - Ruby脚本

你可以运行：
```bash
# 在项目根目录执行
update_all_deps.bat
```

更新完成后，我将帮你测试网站功能。