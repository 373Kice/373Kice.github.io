#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稀土板块龙头股分析
使用 DeepSeek API 生成专业分析
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# DeepSeek API 配置（从环境变量读取，请勿硬编码）
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY') or os.getenv('LITELLM_API_KEY')
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 稀土板块龙头股代码
RARE_EARTH_STOCKS = [
    {"code": "600111", "name": "北方稀土", "role": "轻稀土龙头"},
    {"code": "000831", "name": "中国稀土", "role": "中重稀土龙头"},
    {"code": "600392", "name": "盛和资源", "role": "全产业链布局"},
    {"code": "600549", "name": "厦门钨业", "role": "钨稀土双主业"},
    {"code": "600259", "name": "广晟有色", "role": "中重稀土"},
    {"code": "000758", "name": "中色股份", "role": "海外资源布局"},
]

def analyze_rare_earth_stocks():
    """使用 DeepSeek 分析稀土板块龙头股"""
    
    logger.info("=" * 60)
    logger.info("   稀土板块龙头股分析")
    logger.info("=" * 60)
    
    # 构造分析提示词
    prompt = """# 稀土板块龙头股分析请求

## 分析任务
请对以下A股稀土板块龙头股进行专业分析，生成投资决策参考。

## 龙头股列表

| 股票代码 | 股票名称 | 市场地位 |
|---------|---------|----------|
| 600111 | 北方稀土 | 轻稀土龙头，全球最大稀土生产商 |
| 000831 | 中国稀土 | 中重稀土龙头，央企背景 |
| 600392 | 盛和资源 | 全产业链布局，海外资源 |
| 600549 | 厦门钨业 | 钨稀土双主业，硬质合金 |
| 600259 | 广晟有色 | 中重稀土，区域龙头 |
| 000758 | 中色股份 | 海外稀土资源布局 |

## 分析要求

对每只股票，请提供：

1. **基本面分析**
   - 公司概况与核心竞争力
   - 稀土资源储量与产量
   - 产业链布局（开采、冶炼、深加工）

2. **技术面分析**
   - 当前价格位置（高位/低位/中位）
   - 关键支撑位与压力位
   - 均线形态与趋势判断

3. **估值分析**
   - PE/PB估值水平
   - 与同行业对比
   - 估值合理性判断

4. **催化剂与风险**
   - 价格上涨预期
   - 政策利好（稀土开采指标、出口管制）
   - 下游需求（新能源汽车、风电、机器人）
   - 主要风险点

5. **投资建议**
   - 操作建议（买入/持有/观望/卖出）
   - 目标价位
   - 止损位设置

## 板块整体判断

- 稀土价格走势预判
- 政策环境分析（国家稀土集团整合、出口管制）
- 供需格局判断
- 板块投资时机评估

## 输出格式

请以结构化报告形式输出，包含：
- 板块概览
- 个股详细分析（按投资价值排序）
- 投资组合建议（龙头+弹性品种组合）
- 风险提示

使用专业但易懂的语言，适合A股投资者参考。
"""
    
    try:
        import litellm
        
        logger.info("[LLM] 开始调用 DeepSeek API...")
        logger.info(f"[LLM] 模型: {DEEPSEEK_MODEL}")
        
        # 调用 DeepSeek API
        response = litellm.completion(
            model=f"deepseek/{DEEPSEEK_MODEL}",
            messages=[
                {"role": "system", "content": "你是一位专业的A股有色金属行业分析师，擅长稀土板块研究。你的分析基于基本面、技术面和产业政策，提供客观、专业的投资建议。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=8000,
            api_key=DEEPSEEK_API_KEY,
            api_base=DEEPSEEK_API_BASE
        )
        
        # 获取分析结果
        analysis_content = response.choices[0].message.content
        
        logger.info("[LLM] 分析完成")
        logger.info(f"[LLM] 响应长度: {len(analysis_content)} 字符")
        
        return analysis_content
        
    except Exception as e:
        logger.error(f"[LLM错误] 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_analysis_report(analysis_content, date_str):
    """保存分析报告"""
    if not analysis_content:
        logger.error("[错误] 分析内容为空，无法保存")
        return None
    
    # 确保目录存在
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
    
    # 生成文件名
    filename = f"_posts/{date_str}-稀土板块龙头股分析报告.md"
    
    # 构造完整的Markdown报告
    report = f"""---
title: "{date_str} 稀土板块龙头股分析报告"
date: {date_str} 15:00:00 +0800
categories: 股市分析 行业研究
tags: 稀土 有色金属 北方稀土 中国稀土 盛和资源 投资策略
---

# 📊 {date_str} 稀土板块龙头股分析报告

> 本报告由 AI 分析系统生成，基于 DeepSeek 大模型专业分析

---

{analysis_content}

---

## 📝 投资总结

### 配置建议

1. **核心仓位（60%）**：北方稀土（轻稀土龙头）+ 中国稀土（中重稀土龙头）
2. **弹性仓位（30%）**：盛和资源（产业链完整）+ 厦门钨业（钨稀土双主业）
3. **观察仓位（10%）**：广晟有色、中色股份

### 操作策略

- **长期投资者**：逢低布局龙头股，持有周期6-12个月
- **中期投资者**：关注稀土价格走势，把握波段机会
- **短期投资者**：谨慎参与，注意止损

---

*免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。股市有风险，投资需谨慎。*

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*分析工具: DeepSeek AI*
"""
    
    # 保存文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"[保存] 报告已保存: {filename}")
    
    return filename

def git_commit_and_push(filename, date_str):
    """提交并推送到GitHub"""
    import subprocess
    
    try:
        logger.info("\n[Git] 正在添加到Git...")
        subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)
        
        logger.info("[Git] 正在提交...")
        commit_msg = f"自动更新{date_str}稀土板块分析报告"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True, text=True)
        logger.info(f"[Git] 提交成功: {commit_msg}")
        
        logger.info("[Git] 正在推送到GitHub...")
        subprocess.run(['git', 'push', 'origin', 'master'], check=True, capture_output=True, text=True)
        logger.info("[Git] 推送成功! ✅")
        logger.info(f"[GitHub] 网站将自动更新: https://373kice.github.io/")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"[Git错误] Git操作失败: {e}")
        return False
    except Exception as e:
        logger.error(f"[Git错误] 未知错误: {e}")
        return False

def main():
    """主函数"""
    logger.info("\n[启动] 稀土板块龙头股分析系统")
    
    # 获取今天日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    # 分析稀土板块龙头股
    logger.info("\n[分析] 正在使用 DeepSeek AI 分析稀土板块...")
    analysis_content = analyze_rare_earth_stocks()
    
    if not analysis_content:
        logger.error("[错误] 分析失败，无法生成报告")
        return
    
    # 保存报告
    logger.info("\n[保存] 正在保存分析报告...")
    filename = save_analysis_report(analysis_content, date_str)
    
    if not filename:
        logger.error("[错误] 保存失败")
        return
    
    # 推送到GitHub
    logger.info("\n[Git] 开始自动推送到GitHub...")
    git_commit_and_push(filename, date_str)
    
    logger.info("\n" + "=" * 60)
    logger.info("   分析完成!")
    logger.info("=" * 60)
    logger.info(f"[文件] 报告文件: {filename}")
    logger.info(f"[在线] 稍后可在 https://373kice.github.io/ 查看")

if __name__ == "__main__":
    main()
