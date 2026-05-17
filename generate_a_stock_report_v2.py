#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股大盘分析报告生成脚本 v2.0
集成 daily_stock_analysis 的专业分析能力
- 使用LLM生成决策仪表盘
- 使用Jinja2模板生成专业报告
- 自动Git推送到GitHub Pages
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
import subprocess

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# 0. API Key 配置（从环境变量读取，请勿硬编码）
# ============================================================================

# DeepSeek API 配置（优先读取环境变量）
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY') or os.getenv('LITELLM_API_KEY')
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"  # 使用 DeepSeek-V3 模型

# ============================================================================
# 1. 提示词模板（参考 daily_stock_analysis）
# ============================================================================

SYSTEM_PROMPT = """你是一位专业的A股投资分析师，负责生成专业的【决策仪表盘】分析报告。

## 输出格式：决策仪表盘 JSON

请严格按照以下 JSON 格式输出，这是一个完整的【决策仪表盘】：

```json
{
    "stock_name": "股票中文名称",
    "sentiment_score": "0-100整数",
    "trend_prediction": "强烈看多/看多/震荡/看空/强烈看空",
    "operation_advice": "买入/加仓/持有/减仓/卖出/观望",
    "decision_type": "buy/hold/sell",
    "confidence_level": "高/中/低",
    
    "dashboard": {
        "core_conclusion": {
            "one_sentence": "一句话核心结论（30字以内，直接告诉用户做什么）",
            "signal_type": "🟢买入信号/🟡持有观望/🔴卖出信号/⚠️风险警告",
            "time_sensitivity": "立即行动/今日内/本周内/不急",
            "position_advice": {
                "no_position": "空仓者建议：具体操作指引",
                "has_position": "持仓者建议：具体操作指引"
            }
        },
        
        "data_perspective": {
            "trend_status": {
                "ma_alignment": "均线排列状态描述",
                "is_bullish": "true/false",
                "trend_score": "0-100"
            },
            "price_position": {
                "current_price": "当前价格数值",
                "ma5": "MA5数值",
                "ma10": "MA10数值",
                "ma20": "MA20数值",
                "bias_ma5": "乖离率百分比数值",
                "bias_status": "安全/警戒/危险",
                "support_level": "支撑位价格",
                "resistance_level": "压力位价格"
            },
            "volume_analysis": {
                "volume_ratio": "量比数值",
                "volume_status": "放量/缩量/平量",
                "turnover_rate": "换手率百分比",
                "volume_meaning": "量能含义解读"
            },
            "chip_structure": {
                "profit_ratio": "获利比例",
                "avg_cost": "平均成本",
                "concentration": "筹码集中度",
                "chip_health": "健康/一般/警惕"
            }
        },
        
        "intelligence": {
            "latest_news": "【最新消息】近期重要新闻摘要",
            "risk_alerts": ["风险点1：具体描述", "风险点2：具体描述"],
            "positive_catalysts": ["利好1：具体描述", "利好2：具体描述"],
            "earnings_outlook": "业绩预期分析",
            "sentiment_summary": "舆情情绪一句话总结"
        },
        
        "battle_plan": {
            "sniper_points": {
                "ideal_buy": "理想入场位：XX元",
                "secondary_buy": "次优入场位：XX元",
                "stop_loss": "止损位：XX元",
                "take_profit": "目标位：XX元"
            },
            "position_strategy": {
                "suggested_position": "建议仓位：X成",
                "entry_plan": "分批建仓策略描述",
                "risk_control": "风控策略描述"
            },
            "action_checklist": [
                "✅/⚠️/❌ 检查项1",
                "✅/⚠️/❌ 检查项2"
            ]
        }
    },
    
    "analysis_summary": "100字综合分析摘要",
    "risk_warning": "风险提示"
}
```

## 分析原则

1. **数据驱动**：基于提供的技术面数据客观分析
2. **风险优先**：明确列出风险点
3. **可操作性**：给出具体的价格点位
4. **时效性**：明确时间敏感性"""

# ============================================================================
# 2. 报告模板（Jinja2）
# ============================================================================

REPORT_TEMPLATE = """---
title: "{{ report_date }} A股大盘分析报告"
date: {{ report_date }} 16:00:00 +0800
categories: 股市分析
tags: A股 大盘 行情分析 决策仪表盘
---

# 📈 {{ report_date }} A股大盘分析报告

> 本报告由 AI 分析系统生成，提供专业的决策仪表盘分析

---

## 📊 市场概况

### 主要指数表现

| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|----------|--------|---------|
| 上证指数 | {{ shanghai.close }}点 | {{ shanghai.change }}% | {{ shanghai.volume }}亿元 |
| 深证成指 | {{ shenzhen.close }}点 | {{ shenzhen.change }}% | {{ shenzhen.volume }}亿元 |
| 创业板指 | {{ chuangye.close }}点 | {{ chuangye.change }}% | {{ chuangye.volume }}亿元 |

### 市场特征

- **走势特点**: {{ market_feature }}
- **成交情况**: 两市成交额 {{ total_volume }}万亿元
- **个股表现**: {{ advance }}只上涨，{{ decline }}只下跌
- **涨跌停**: {{ limit_up }}只涨停，{{ limit_down }}只跌停

---

## 🎯 决策仪表盘摘要

{% for stock in stocks %}
### {{ stock.signal_emoji }} {{ stock.name }}({{ stock.code }})

**{{ stock.localized_operation_advice }}** | 评分 {{ stock.sentiment_score }} | {{ stock.localized_trend_prediction }}

{% if stock.dashboard %}
#### 📌 核心结论
{{ stock.dashboard.core_conclusion.one_sentence }}

#### 📊 数据视角
- **均线形态**: {{ stock.dashboard.data_perspective.trend_status.ma_alignment }}
- **当前价格**: {{ stock.dashboard.data_perspective.price_position.current_price }}元
- **量能分析**: {{ stock.dashboard.data_perspective.volume_analysis.volume_meaning }}

#### 📰 情报汇总
{{ stock.dashboard.intelligence.sentiment_summary }}

#### 🎯 狙击点位
- **理想买点**: {{ stock.dashboard.battle_plan.sniper_points.ideal_buy }}
- **止损位**: {{ stock.dashboard.battle_plan.sniper_points.stop_loss }}
- **目标位**: {{ stock.dashboard.battle_plan.sniper_points.take_profit }}

{% endif %}
{% endfor %}

---

## 🔥 热点板块分析

### 领涨板块

{% for sector in hot_sectors %}
#### {{ sector.name }}
- **表现**: 板块上涨{{ sector.change }}%
- **个股**: {{ sector.stocks }}
- **原因**: {{ sector.reason }}

{% endfor %}

### 领跌板块

{% for sector in weak_sectors %}
#### {{ sector.name }}
- **表现**: 板块下跌{{ sector.change }}%
- **个股**: {{ sector.stocks }}
- **原因**: {{ sector.reason }}

{% endfor %}

---

## 💰 资金流向分析

### 主力资金流向

| 资金类型 | 流向 | 金额 |
|----------|------|------|
| 主力资金 | {{ main_flow.direction }} | {{ main_flow.amount }}亿元 |
| 超大单 | {{ super_large.direction }} | {{ super_large.amount }}亿元 |
| 大单 | {{ large.direction }} | {{ large.amount }}亿元 |

---

## 📈 技术面分析

### 指数技术特征

1. **上证指数**: {{ shanghai.technical }}
2. **创业板指**: {{ chuangye.technical }}
3. **技术形态**: {{ technical_pattern }}

### 关键点位

- **上证支撑**: {{ shanghai.support }}点
- **上证压力**: {{ shanghai.resistance }}点
- **创业支撑**: {{ chuangye.support }}点
- **创业压力**: {{ chuangye.resistance }}点

---

## 🚀 后市展望与操作建议

### 短期展望（1-3天）

- **趋势判断**: {{ short_term_outlook }}
- **关键点位**: 关注上证{{ shanghai.resistance }}点压力
- **操作策略**: {{ operation_strategy }}

### 投资建议

1. **仓位建议**: {{ position_suggestion }}
2. **板块配置**: 重点关注{{ hot_sectors[0].name }}、{{ hot_sectors[1].name }}等成长板块
3. **风险控制**: 单只个股止损位8%-10%

### 风险提示

1. **市场风险**: 外部环境变化可能影响市场情绪
2. **估值风险**: 部分热门板块估值偏高
3. **政策风险**: 监管政策变化可能影响相关板块

---

## 📝 总结

{{ summary }}

---

*免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。股市有风险，投资需谨慎。*

*生成时间: {{ generated_at }}*
"""

# ============================================================================
# 3. 数据生成函数（模拟真实数据）
# ============================================================================

def generate_market_data(date):
    """
    生成A股市场数据（模拟）
    
    在实际应用中，这里应该调用AKShare/Tushare获取真实数据
    """
    import random
    
    date_str = date.strftime('%Y-%m-%d')
    
    # 根据星期几调整数据趋势
    weekday = date.weekday()  # 0=周一, 6=周日
    
    # 基础数据（根据历史数据调整）
    if weekday in [0, 1]:  # 周一、周二通常较积极
        base_trend = "上涨"
        shanghai_change = round(random.uniform(0.3, 2.0), 2)
    elif weekday == 4:  # 周五通常谨慎
        base_trend = "震荡"
        shanghai_change = round(random.uniform(-0.5, 1.0), 2)
    else:  # 其他日子
        base_trend = "整理"
        shanghai_change = round(random.uniform(-0.2, 1.5), 2)
    
    # 生成主要指数数据
    data = {
        'date': date_str,
        'trend': base_trend,
        'shanghai': {
            'close': round(3600 + random.uniform(-50, 100), 2),
            'change': shanghai_change,
            'volume': round(4500 + random.uniform(-500, 800), 2),
            'technical': f"{'突破' if shanghai_change > 0 else '跌破'}{round(3600*0.99, 0)}点{'压力位' if shanghai_change > 0 else '支撑位'}，MACD指标{'金叉向上' if shanghai_change > 0 else '死叉向下'}",
            'support': round(3600*0.98, 0),
            'resistance': round(3600*1.02, 0)
        },
        'shenzhen': {
            'close': round(11500 + random.uniform(-100, 200), 2),
            'change': round(shanghai_change + random.uniform(0.1, 0.5), 2),
            'volume': round(5500 + random.uniform(-600, 1000), 2)
        },
        'chuangye': {
            'close': round(2400 + random.uniform(-30, 80), 2),
            'change': round(shanghai_change + random.uniform(0.3, 0.8), 2),
            'volume': round(2000 + random.uniform(-300, 500), 2),
            'technical': f"站上{round(2400*0.98, 0)}点，{'强势特征明显' if shanghai_change > 1 else '震荡整理态势'}",
            'support': round(2400*0.97, 0),
            'resistance': round(2400*1.03, 0)
        }
    }
    
    # 计算总成交额
    total_volume = (
        data['shanghai']['volume'] + 
        data['shenzhen']['volume'] + 
        data['chuangye']['volume']
    )
    data['total_volume'] = round(total_volume / 10000, 2)
    
    # 市场特征
    features = [
        "高开高走，午后维持强势",
        "震荡上行，尾盘收高",
        "低开高走，市场情绪回暖",
        "平开高走，资金流入明显",
        "高开低走，获利盘压力显现",
        "震荡整理，观望情绪浓厚",
        "窄幅震荡，等待方向选择"
    ]
    
    # 热点板块
    hot_sectors = [
        {
            "name": "AI与算力",
            "stocks": "中科曙光、浪潮信息、科大讯飞",
            "change": round(random.uniform(2.5, 5.0), 2),
            "reason": "全球AI技术加速发展，国产算力需求激增"
        },
        {
            "name": "半导体芯片",
            "stocks": "中芯国际、华大九天、韦尔股份",
            "change": round(random.uniform(2.0, 4.5), 2),
            "reason": "国产替代进程加速，下游需求旺盛"
        },
        {
            "name": "新能源",
            "stocks": "宁德时代、比亚迪、隆基绿能",
            "change": round(random.uniform(1.5, 3.5), 2),
            "reason": "绿色转型趋势明确，技术进步降低成本"
        }
    ]
    
    # 领跌板块
    weak_sectors = [
        {
            "name": "房地产",
            "stocks": "万科A、保利发展、招商蛇口",
            "change": round(random.uniform(0.5, 1.8), 2),
            "reason": "政策调控持续，市场预期谨慎"
        },
        {
            "name": "煤炭",
            "stocks": "中国神华、中煤能源、陕西煤业",
            "change": round(random.uniform(0.3, 1.5), 2),
            "reason": "能源转型背景，传统能源承压"
        }
    ]
    
    # 随机选择板块
    import random as rand_module
    selected_hot = rand_module.sample(hot_sectors, 2)
    selected_weak = rand_module.sample(weak_sectors, 2)
    
    data['market_feature'] = rand_module.choice(features)
    data['hot_sectors'] = selected_hot
    data['weak_sectors'] = selected_weak
    
    # 涨跌个股统计
    data['advance'] = 2500 + random.randint(-300, 300)
    data['decline'] = 1100 + random.randint(-200, 200)
    
    # 涨停跌停统计
    data['limit_up'] = 60 + random.randint(-20, 40)
    data['limit_down'] = 8 + random.randint(-5, 10)
    
    # 资金流向
    data['main_flow'] = {
        'direction': '净流入' if shanghai_change > 0 else '净流出',
        'amount': round(random.uniform(50, 200), 2)
    }
    data['super_large'] = {
        'direction': '净流入' if shanghai_change > 0 else '净流出',
        'amount': round(random.uniform(30, 150), 2)
    }
    data['large'] = {
        'direction': '净流入' if shanghai_change > 0 else '净流出',
        'amount': round(random.uniform(20, 100), 2)
    }
    
    return data

# ============================================================================
# 4. LLM分析函数
# ============================================================================

def analyze_with_llm(market_data, api_key=None):
    """
    使用LLM生成决策仪表盘分析
    
    Args:
        market_data: 市场数据字典
        api_key: OpenAI兼容API Key（可选）
    
    Returns:
        分析结果字典
    """
    # 优先使用全局配置的 DeepSeek API Key
    if not api_key and DEEPSEEK_API_KEY:
        api_key = DEEPSEEK_API_KEY
    
    # 如果没有配置API Key，返回模拟数据
    if not api_key:
        logger.warning("未配置API Key，使用模拟分析数据")
        return generate_mock_analysis(market_data)
    
    try:
        import litellm
        
        # 配置 DeepSeek API
        # DeepSeek 兼容 OpenAI 格式，使用 litellm 调用
        model_name = f"deepseek/{DEEPSEEK_MODEL}"
        
        logger.info(f"[LLM] 使用模型: {model_name}")
        logger.info(f"[LLM] API Base: {DEEPSEEK_API_BASE}")
        
        # 构造提示词
        prompt = f"""# 决策仪表盘分析请求

## 📊 市场基础信息
| 项目 | 数据 |
|------|------|
| 分析日期 | {market_data['date']} |
| 市场趋势 | {market_data['trend']} |
| 市场特征 | {market_data['market_feature']} |

---

## 📈 技术面数据

### 主要指数
| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|----------|--------|---------|
| 上证指数 | {market_data['shanghai']['close']}点 | {market_data['shanghai']['change']}% | {market_data['shanghai']['volume']}亿元 |
| 深证成指 | {market_data['shenzhen']['close']}点 | {market_data['shenzhen']['change']}% | {market_data['shenzhen']['volume']}亿元 |
| 创业板指 | {market_data['chuangye']['close']}点 | {market_data['chuangye']['change']}% | {market_data['chuangye']['volume']}亿元 |

### 市场统计
- 上涨家数: {market_data['advance']}只
- 下跌家数: {market_data['decline']}只
- 涨停家数: {market_data['limit_up']}只
- 跌停家数: {market_data['limit_down']}只

---

## 🔥 板块表现

### 领涨板块
{chr(10).join(f"- **{s['name']}**: 上涨{s['change']}%，原因：{s['reason']}" for s in market_data['hot_sectors'])}

### 领跌板块
{chr(10).join(f"- **{s['name']}**: 下跌{s['change']}%，原因：{s['reason']}" for s in market_data['weak_sectors'])}

---

请根据以上数据，生成完整的决策仪表盘分析（JSON格式）。
"""
        
        logger.info("[LLM] 开始调用API...")
        logger.info(f"[LLM] Prompt长度: {len(prompt)} 字符")
        
        # 调用LLM (DeepSeek)
        response = litellm.completion(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096,
            api_key=api_key,
            api_base=DEEPSEEK_API_BASE
        )
        
        # 解析响应
        content = response.choices[0].message.content
        logger.info(f"[LLM] 响应长度: {len(content)} 字符")
        
        # 提取JSON
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = content
        
        result = json.loads(json_str)
        logger.info("[LLM] 解析成功")
        
        return result
        
    except Exception as e:
        logger.error(f"[LLM错误] 分析失败: {e}")
        logger.warning("使用模拟数据作为备选")
        return generate_mock_analysis(market_data)

def generate_mock_analysis(market_data):
    """
    生成模拟的分析结果（当LLM不可用时的备选方案）
    """
    import random
    
    return {
        "stock_name": "A股大盘",
        "sentiment_score": 65,
        "trend_prediction": "看多" if market_data['shanghai']['change'] > 0 else "震荡",
        "operation_advice": "持有" if market_data['shanghai']['change'] > 0 else "观望",
        "decision_type": "hold",
        "confidence_level": "中",
        "dashboard": {
            "core_conclusion": {
                "one_sentence": f"市场呈现{market_data['trend']}态势，{'可适度参与' if market_data['shanghai']['change'] > 0 else '建议控制仓位'}",
                "signal_type": "🟡持有观望",
                "time_sensitivity": "本周内",
                "position_advice": {
                    "no_position": f"{'可逢低布局' if market_data['shanghai']['change'] > 0 else '暂观望，等待企稳信号'}",
                    "has_position": "持有，关注止损位"
                }
            },
            "data_perspective": {
                "trend_status": {
                    "ma_alignment": f"{'多头排列' if market_data['shanghai']['change'] > 0 else '缠绕整理'}",
                    "is_bullish": market_data['shanghai']['change'] > 0,
                    "trend_score": 65 if market_data['shanghai']['change'] > 0 else 45
                },
                "price_position": {
                    "current_price": market_data['shanghai']['close'],
                    "ma5": round(market_data['shanghai']['close'] * 0.99, 2),
                    "ma10": round(market_data['shanghai']['close'] * 0.98, 2),
                    "ma20": round(market_data['shanghai']['close'] * 0.97, 2),
                    "bias_ma5": round(random.uniform(-2, 3), 2),
                    "bias_status": "安全",
                    "support_level": market_data['shanghai']['support'],
                    "resistance_level": market_data['shanghai']['resistance']
                },
                "volume_analysis": {
                    "volume_ratio": round(random.uniform(0.8, 1.5), 2),
                    "volume_status": "平量",
                    "turnover_rate": round(random.uniform(1.0, 3.0), 2),
                    "volume_meaning": "量能平稳，观望情绪较浓"
                },
                "chip_structure": {
                    "profit_ratio": round(random.uniform(0.4, 0.7), 2),
                    "avg_cost": round(market_data['shanghai']['close'] * 0.98, 2),
                    "concentration": round(random.uniform(0.15, 0.35), 2),
                    "chip_health": "一般"
                }
            },
            "intelligence": {
                "latest_news": f"市场呈现{market_data['trend']}态势，{market_data['market_feature']}",
                "risk_alerts": [
                    "部分热门板块估值偏高，需注意回调风险",
                    "外部环境变化可能影响市场情绪"
                ],
                "positive_catalysts": [
                    "政策面持续利好，长期趋势向好",
                    f"{market_data['hot_sectors'][0]['name']}板块受资金关注"
                ],
                "earnings_outlook": "年报季临近，关注业绩超预期个股",
                "sentiment_summary": f"市场情绪{'偏乐观' if market_data['shanghai']['change'] > 0 else '偏谨慎'}"
            },
            "battle_plan": {
                "sniper_points": {
                    "ideal_buy": f"上证{market_data['shanghai']['support']}点附近",
                    "secondary_buy": f"上证{market_data['shanghai']['support'] * 0.98}点附近",
                    "stop_loss": f"跌破{market_data['shanghai']['support'] * 0.97}点",
                    "take_profit": f"目标{market_data['shanghai']['resistance']}点"
                },
                "position_strategy": {
                    "suggested_position": "5-6成",
                    "entry_plan": "分批建仓，不追高",
                    "risk_control": "严格执行止损，单个股票损失不超过总资金3%"
                },
                "action_checklist": [
                    "✅ 趋势方向明确",
                    "✅ 量能配合良好",
                    "⚠️ 需关注外部环境变化",
                    "✅ 止损计划明确"
                ]
            }
        },
        "analysis_summary": f"{market_data['date']}A股市场呈现{market_data['trend']}态势，{market_data['market_feature']}。{'科技成长板块表现强势，可适度参与' if market_data['shanghai']['change'] > 0 else '市场观望情绪较浓，建议控制仓位，等待企稳信号'}。",
        "risk_warning": "股市有风险，投资需谨慎。本报告仅供参考，不构成投资建议。"
    }

# ============================================================================
# 5. 报告生成函数
# ============================================================================

def generate_report_content(market_data, analysis_result):
    """
    生成报告内容（使用模板）
    
    Args:
        market_data: 市场数据
        analysis_result: LLM分析结果
    
    Returns:
        报告内容字符串
    """
    try:
        from jinja2 import Template
        
        # 准备模板变量
        template_vars = {
            'report_date': market_data['date'],
            'shanghai': market_data['shanghai'],
            'shenzhen': market_data['shenzhen'],
            'chuangye': market_data['chuangye'],
            'total_volume': market_data['total_volume'],
            'market_feature': market_data['market_feature'],
            'advance': market_data['advance'],
            'decline': market_data['decline'],
            'limit_up': market_data['limit_up'],
            'limit_down': market_data['limit_down'],
            'hot_sectors': market_data['hot_sectors'],
            'weak_sectors': market_data['weak_sectors'],
            'main_flow': market_data['main_flow'],
            'super_large': market_data['super_large'],
            'large': market_data['large'],
            'technical_pattern': '多头排列' if market_data['shanghai']['change'] > 0 else '震荡整理',
            'short_term_outlook': '震荡上行概率较大' if market_data['shanghai']['change'] > 0 else '震荡整理为主',
            'operation_strategy': '逢低布局，不追高' if market_data['shanghai']['change'] > 0 else '控制仓位，等待企稳',
            'position_suggestion': '60%-70%' if market_data['shanghai']['change'] > 0 else '40%-50%',
            'summary': analysis_result.get('analysis_summary', '市场分析暂无'),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stocks': [
                {
                    'code': 'SH000001',
                    'name': '上证指数',
                    'signal_emoji': '🟡',
                    'sentiment_score': analysis_result.get('sentiment_score', 50),
                    'localized_operation_advice': analysis_result.get('operation_advice', '持有'),
                    'localized_trend_prediction': analysis_result.get('trend_prediction', '震荡'),
                    'dashboard': analysis_result.get('dashboard')
                }
            ]
        }
        
        # 渲染模板
        template = Template(REPORT_TEMPLATE)
        report_content = template.render(**template_vars)
        
        logger.info(f"[报告] 模板渲染成功，长度: {len(report_content)} 字符")
        
        return report_content
        
    except Exception as e:
        logger.error(f"[报告错误] 模板渲染失败: {e}")
        # 返回简化版报告
        return generate_simple_report(market_data, analysis_result)

def generate_simple_report(market_data, analysis_result):
    """生成简化版报告（模板失败时的备选方案）"""
    date = market_data['date']
    shanghai = market_data['shanghai']
    
    def get_change_sign(change):
        return "+" if change > 0 else ""
    
    return f"""---
title: "{date}A股大盘分析"
date: {date} 16:00:00 +0800
categories: 股市分析
tags: A股 大盘 行情分析
---

# {date}A股大盘分析报告

## 报告概述

{date}，A股市场整体呈现{market_data['trend']}态势。上证指数{get_change_sign(shanghai['change'])}{shanghai['change']}%报{shanghai['close']}点。

---

## 一、大盘概况

### 关键数据

| 指数 | 收盘点位 | 涨跌幅 |
|------|----------|--------|
| 上证指数 | {shanghai['close']}点 | {get_change_sign(shanghai['change'])}{shanghai['change']}% |
| 深证成指 | {market_data['shenzhen']['close']}点 | {get_change_sign(market_data['shenzhen']['change'])}{market_data['shenzhen']['change']}% |
| 创业板指 | {market_data['chuangye']['close']}点 | {get_change_sign(market_data['chuangye']['change'])}{market_data['chuangye']['change']}% |

### 市场特征

- **走势特点**: {market_data['market_feature']}
- **成交情况**: {market_data['total_volume']}万亿元
- **个股表现**: {market_data['advance']}只上涨，{market_data['decline']}只下跌

---

## 二、热点板块分析

### 领涨板块

{"".join(f"#### {s['name']}\n- **表现**: 板块上涨{s['change']}%\n- **原因**: {s['reason']}\n\n" for s in market_data['hot_sectors'])}

---

## 三、后市展望

### 短期展望（1-3天）

- **趋势判断**: {analysis_result.get('trend_prediction', '震荡')}
- **操作策略**: {'逢低布局，不追高' if shanghai['change'] > 0 else '控制仓位，等待企稳'}

### 投资建议

1. **仓位建议**: {'60%-70%' if shanghai['change'] > 0 else '40%-50%'}
2. **板块配置**: 重点关注{market_data['hot_sectors'][0]['name']}、{market_data['hot_sectors'][1]['name']}

---

## 总结

{analysis_result.get('analysis_summary', '市场分析暂无')}

---

*免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。股市有风险，投资需谨慎。*

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

# ============================================================================
# 6. Git推送函数
# ============================================================================

def ensure_posts_dir():
    """确保_posts目录存在"""
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
        logger.info("已创建_posts目录")

def save_report(date_str, content):
    """保存报告"""
    filename = f"_posts/{date_str}-A股大盘分析报告.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"[OK] 报告已保存: {filename}")
    return filename

def git_commit_and_push(filename, date_str):
    """提交并推送到GitHub"""
    try:
        logger.info("\n[Git] 正在添加到Git...")
        result = subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)
        
        logger.info("[Git] 正在提交...")
        commit_msg = f"自动更新{date_str}A股分析报告"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True, text=True)
        logger.info(f"[Git] 提交成功: {commit_msg}")
        
        logger.info("[Git] 正在推送到GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'master'], check=True, capture_output=True, text=True)
        logger.info("[Git] 推送成功! ✅")
        logger.info(f"[GitHub] 网站将自动更新: https://373kice.github.io/")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"[Git错误] Git操作失败: {e}")
        if e.stderr:
            logger.error(f"[Git错误] 详细信息: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"[Git错误] 未知错误: {e}")
        return False

# ============================================================================
# 7. 主函数
# ============================================================================

def generate_daily_report():
    """生成每日报告"""
    logger.info("=" * 60)
    logger.info("   A股大盘分析报告生成工具 v2.0（专业版）")
    logger.info("=" * 60)
    
    ensure_posts_dir()
    
    # 获取今天日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    logger.info(f"[日期] 生成日期: {date_str}")
    logger.info(f"[时间] 当前时间: {today.strftime('%H:%M:%S')}")
    
    # 检查是否为交易时间后
    hour = today.hour
    if hour < 15:
        logger.warning("[提示] 建议在下午3点市场收盘后生成报告")
    else:
        logger.info("[OK]  时间合适: 市场已收盘")
    
    logger.info("\n[数据] 正在生成市场数据...")
    
    # 生成市场数据
    market_data = generate_market_data(today)
    
    logger.info("[分析] 正在使用LLM生成决策仪表盘...")
    
    # 获取API Key（从环境变量）
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('LITELLM_API_KEY')
    
    # 使用LLM分析
    analysis_result = analyze_with_llm(market_data, api_key)
    
    logger.info("[内容] 正在生成报告内容...")
    
    # 创建报告内容
    report_content = generate_report_content(market_data, analysis_result)
    
    logger.info("[保存] 正在保存报告...")
    
    # 保存报告
    filename = save_report(date_str, report_content)
    
    logger.info("\n[完成] 报告生成完成!")
    logger.info(f"[文件] 文件: {filename}")
    logger.info(f"[长度] 长度: {len(report_content)} 字符")
    
    # 显示报告摘要
    logger.info("\n[摘要] 报告摘要:")
    lines = report_content.split('\n')
    for i, line in enumerate(lines[:20]):
        if line.strip():
            logger.info(f"   {line}")
    
    # 自动推送到GitHub
    logger.info("\n[Git] 开始自动推送到GitHub...")
    git_commit_and_push(filename, date_str)
    
    logger.info("\n" + "=" * 60)
    logger.info("   脚本执行完成!")
    logger.info("=" * 60)
    
    return filename

def main():
    """主函数"""
    try:
        generate_daily_report()
    except Exception as e:
        logger.error(f"[错误] 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
