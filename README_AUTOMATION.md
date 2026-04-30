# A股分析网站自动化系统

## 🎯 系统概述

这是一个完整的自动化系统，用于：
1. 每天下午4点自动生成A股大盘分析报告
2. 在Jekyll网站上自动发布新文章
3. 网站长期运行并支持实时更新

## 📁 文件说明

### 核心文件
| 文件 | 用途 | 说明 |
|------|------|------|
| `daily_a_stock_analysis.py` | 报告生成器 | 自动创建当日分析报告模板 |
| `run_jekyll_service.ps1` | 网站服务 | 在Windows上长期运行Jekyll网站 |
| `create_daily_report_task.ps1` | 计划任务创建 | 创建Windows计划任务（需要管理员） |
| `setup_automation.ps1` | 一键安装 | 用户友好的安装界面 |

### 配置文件
| 文件 | 用途 | 说明 |
|------|------|------|
| `_posts/` | 文章目录 | Jekyll博客文章存放位置 |
| `_config.yml` | Jekyll配置 | 网站基本配置 |
| `Gemfile` | Ruby依赖 | Jekyll运行所需gem |

## 🚀 快速开始

### 方法1：一键安装（推荐）
```powershell
# 打开PowerShell，切换到项目目录
cd "D:\GITHUB\373Kice.github.io"

# 运行一键安装脚本
.\setup_automation.ps1
```

选择选项 **3. 完整安装（任务 + 服务）**，按提示操作。

### 方法2：分步安装

#### 步骤1：启动Jekyll网站服务
```powershell
# 普通用户权限即可
.\run_jekyll_service.ps1
```
网站将在 http://127.0.0.1:4001/ 启动。

#### 步骤2：创建自动化任务（需要管理员）
```powershell
# 以管理员身份运行PowerShell，然后执行：
.\create_daily_report_task.ps1
```

## ⚙️ 自动化流程详解

### 1. Jekyll网站服务
- 长期运行在后台
- 自动监视文件变化
- 实时更新网站内容
- 无需手动重启

### 2. 报告生成流程
```
每天16:00 → Windows任务计划 → 运行Python脚本 → 生成新文章 → Jekyll自动更新网站
```

### 3. 文件生成位置
新报告会自动保存到：
```
_posts/YYYY-MM-DD-A股大盘分析报告.md
```

## 📅 计划任务配置

### 默认配置
- **触发时间**：每天下午4:00
- **工作日触发**：周一至周五下午4:00
- **执行命令**：`python daily_a_stock_analysis.py`
- **工作目录**：`D:\GITHUB\373Kice.github.io`

### 管理任务
```powershell
# 查看任务状态
Get-ScheduledTask -TaskName "每日A股分析报告生成"

# 立即运行任务
Start-ScheduledTask -TaskName "每日A股分析报告生成"

# 禁用任务
Disable-ScheduledTask -TaskName "每日A股分析报告生成"

# 删除任务
Unregister-ScheduledTask -TaskName "每日A股分析报告生成" -Confirm:$false
```

## 🔧 手动操作指南

### 手动生成报告
```powershell
# 随时手动生成当日报告
python daily_a_stock_analysis.py
```

### 手动启动网站
```powershell
# 启动Jekyll网站（开发模式）
bundle exec jekyll serve --port 4001

# 启动Jekyll网站（生产模式）
bundle exec jekyll serve --host 127.0.0.1 --port 4001 --incremental --watch
```

### 验证网站状态
1. 访问 http://127.0.0.1:4001/
2. 检查是否有最新文章
3. 尝试添加测试文章验证自动更新

## 🛠️ 故障排除

### 常见问题

#### 1. Python脚本运行失败
```powershell
# 检查Python安装
python --version

# 检查脚本依赖
pip install requests beautifulsoup4 pandas
```

#### 2. Jekyll无法启动
```powershell
# 检查Ruby和Bundler
ruby --version
bundle --version

# 安装依赖
bundle install

# 修复权限问题（Windows）
gem uninstall bundler
gem install bundler
```

#### 3. 计划任务不运行
```powershell
# 以管理员身份重新创建任务
.\create_daily_report_task.ps1

# 检查任务计划程序
taskschd.msc
```

#### 4. 网站无法访问
- 检查Jekyll是否正在运行
- 确认端口4001没有被占用
- 检查防火墙设置

### 日志查看
```powershell
# 查看Jekyll日志（控制台输出）
# 查看Python脚本输出（任务计划程序日志）

# Windows事件查看器
eventvwr.msc
# 查看应用程序和服务日志 -> Microsoft -> Windows -> TaskScheduler -> Operational
```

## 📊 报告模板自定义

### 修改报告模板
编辑 `daily_a_stock_analysis.py` 中的 `generate_report_template()` 函数。

### 添加数据源
```python
# 可以集成以下数据源：
# 1. 新浪财经API
# 2. 东方财富数据
# 3. 腾讯财经接口
# 4. Yahoo Finance API（国际数据）
```

### 自动化数据获取
```python
# 示例：添加自动数据获取
import requests
import pandas as pd

def get_stock_data():
    """获取A股市场数据"""
    # 实现数据获取逻辑
    pass
```

## 🔄 系统维护

### 日常维护
1. **检查Jekyll运行状态**：确保网站服务正常
2. **验证计划任务**：确认每天按时执行
3. **监控磁盘空间**：文章会随时间增加
4. **定期备份**：备份重要文章和配置

### 更新依赖
```powershell
# 更新Ruby gem依赖
bundle update

# 更新Python包
pip install --upgrade requests beautifulsoup4 pandas
```

### 清理旧文件
```powershell
# 清理临时文件（可选）
Remove-Item -Path "*.pyc" -Force
Remove-Item -Path "__pycache__" -Recurse -Force
```

## 📈 扩展功能

### 可以添加的功能
1. **邮件通知**：报告生成后发送邮件提醒
2. **数据分析图表**：自动生成可视化图表
3. **多数据源整合**：整合更多财经数据
4. **AI分析**：使用AI生成更深入的分析
5. **移动端适配**：优化移动设备显示

### 集成GitHub自动部署
```yaml
# .github/workflows/daily-report.yml
# 可以配置GitHub Actions每天自动生成并部署
```

## 📞 技术支持

### 遇到问题时
1. 首先查看本文档的故障排除部分
2. 检查所有脚本文件是否完整
3. 确认环境依赖已安装
4. 查看错误日志获取详细信息

### 联系方式
如有无法解决的问题，可以：
1. 查看脚本中的注释和文档
2. 搜索相关技术问题
3. 寻求社区帮助

## 🎉 系统优势

### 自动化程度高
- ✅ 每天自动生成报告
- ✅ 网站自动更新
- ✅ 无需人工干预

### 稳定性好
- ✅ Jekyll长期稳定运行
- ✅ Windows计划任务可靠性高
- ✅ 错误处理和日志记录

### 扩展性强
- ✅ Python脚本易于修改
- ✅ Jekyll模板可自定义
- ✅ 支持多种数据源集成

---

**最后更新**: 2026年3月11日  
**版本**: 1.0  
**适用平台**: Windows 10/11  
**依赖**: Python 3.7+, Ruby 2.7+, Jekyll 4.2+