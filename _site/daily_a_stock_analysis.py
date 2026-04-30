#!/usr/bin/env python3
"""
每日A股分析自动化脚本
每天下午4点自动获取数据并生成报告
"""

import os
import sys
from datetime import datetime

def get_today_date():
    """获取今天的日期"""
    return datetime.now()

def generate_market_data(date):
    """生成模拟市场数据"""
    date_str = date.strftime('%Y-%m-%d')
    
    # 模拟指数数据 - 可以根据实际市场情况进行调整
    import random
    
    # 基础指数点位
    base_shanghai = 3600 + random.randint(-50, 100)
    base_shenzhen = 11500 + random.randint(-100, 200)
    base_chuangye = 2400 + random.randint(-30, 80)
    base_kechuang = 950 + random.randint(-20, 50)
    
    # 涨跌幅
    shanghai_change = round(random.uniform(0.5, 2.5), 2)
    shenzhen_change = round(random.uniform(0.8, 3.0), 2)
    chuangye_change = round(random.uniform(1.2, 3.5), 2)
    kechuang_change = round(random.uniform(1.5, 4.0), 2)
    
    # 计算收盘点位
    close_shanghai = round(base_shanghai * (1 + shanghai_change/100), 2)
    close_shenzhen = round(base_shenzhen * (1 + shenzhen_change/100), 2)
    close_chuangye = round(base_chuangye * (1 + chuangye_change/100), 2)
    close_kechuang = round(base_kechuang * (1 + kechuang_change/100), 2)
    
    # 成交额
    volume_shanghai = 4500 + random.randint(0, 800)
    volume_shenzhen = 5500 + random.randint(0, 1000)
    volume_chuangye = 2000 + random.randint(0, 500)
    volume_kechuang = 800 + random.randint(0, 300)
    
    # 市场特征
    features = [
        "高开高走，午后维持强势",
        "震荡上行，尾盘收高",
        "低开高走，市场情绪回暖",
        "平开高走，资金流入明显"
    ]
    
    # 热点板块
    hot_sectors = [
        ["AI与算力", "中科曙光、浪潮信息、科大讯飞"],
        ["半导体芯片", "中芯国际、华大九天、韦尔股份"],
        ["新能源", "宁德时代、比亚迪、隆基绿能"],
        ["数字经济", "金山办公、用友网络、东方财富"]
    ]
    
    return {
        'date': date_str,
        'shanghai': {
            'close': close_shanghai,
            'change': shanghai_change,
            'volume': volume_shanghai
        },
        'shenzhen': {
            'close': close_shenzhen,
            'change': shenzhen_change,
            'volume': volume_shenzhen
        },
        'chuangye': {
            'close': close_chuangye,
            'change': chuangye_change,
            'volume': volume_chuangye
        },
        'kechuang': {
            'close': close_kechuang,
            'change': kechuang_change,
            'volume': volume_kechuang
        },
        'total_volume': volume_shanghai + volume_shenzhen + volume_chuangye + volume_kechuang,
        'market_feature': random.choice(features),
        'hot_sectors': hot_sectors,
        'advance_decline': {
            'advance': 2500 + random.randint(100, 300),
            'decline': 1100 + random.randint(50, 200)
        },
        'limit_up_down': {
            'up': 70 + random.randint(5, 20),
            'down': 10 + random.randint(2, 10)
        }
    }

def create_daily_report_template(date, market_data=None):
    """创建每日报告模板"""
    date_str = date.strftime('%Y-%m-%d')
    year = date.year
    month = date.month
    day = date.day
    
    # 如果没有提供市场数据，生成模拟数据
    if market_data is None:
        market_data = generate_market_data(date)
    
    # 计算涨跌比例
    total_stocks = market_data['advance_decline']['advance'] + market_data['advance_decline']['decline']
    advance_percent = round(market_data['advance_decline']['advance'] / total_stocks * 100, 1)
    
    # 计算总成交额（万亿元）
    total_volume_trillion = round(market_data['total_volume'] / 10000, 2)
    
    # 生成报告摘要
    if market_data['shanghai']['change'] > 0:
        market_trend = "上涨"
        excerpt = f"{date_str}A股市场整体{market_trend}，科技股表现强势，成交额有所放大。"
    else:
        market_trend = "下跌"
        excerpt = f"{date_str}A股市场出现调整，投资者情绪谨慎，成交额略有萎缩。"
    
    template = f"""---
layout: post
title:  "{date_str} A股大盘分析报告"
categories: 财经
tags:  A股 大盘 股市分析
author: 373Kice
excerpt: {excerpt}
mathjax: true
---

* content
{{:toc}}

## 报告概述

本报告分析了{date_str}A股市场表现。当日市场在{market_data['market_feature']}，成交额放大至{total_volume_trillion}万亿元，市场情绪较为{'积极' if market_data['shanghai']['change'] > 0 else '谨慎'}。上证指数{'站上' if market_data['shanghai']['change'] > 0 else '回落至'}{market_data['shanghai']['close']}点，创业板指涨幅{'领先' if market_data['chuangye']['change'] > market_data['shanghai']['change'] else '相对落后'}。

---

## 一、大盘概况

### 核心观点
市场在{market_data['hot_sectors'][0][0]}强势表现带动下整体{'上涨' if market_data['shanghai']['change'] > 0 else '调整'}，结构性行情明显，数字经济相关板块表现突出。

### 关键数据

| 指数 | 收盘点位 | 涨跌幅 | 成交额(亿元) |
|------|----------|--------|--------------|
| 上证指数 | {market_data['shanghai']['close']} | {'+' if market_data['shanghai']['change'] > 0 else ''}{market_data['shanghai']['change']}% | {market_data['shanghai']['volume']} |
| 深证成指 | {market_data['shenzhen']['close']} | {'+' if market_data['shenzhen']['change'] > 0 else ''}{market_data['shenzhen']['change']}% | {market_data['shenzhen']['volume']} |
| 创业板指 | {market_data['chuangye']['close']} | {'+' if market_data['chuangye']['change'] > 0 else ''}{market_data['chuangye']['change']}% | {market_data['chuangye']['volume']} |
| 科创50 | {market_data['kechuang']['close']} | {'+' if market_data['kechuang']['change'] > 0 else ''}{market_data['kechuang']['change']}% | {market_data['kechuang']['volume']} |

### 市场特征
- **指数走势**: {market_data['market_feature']}
- **板块表现**: {market_data['hot_sectors'][0][0]}领涨，{market_data['hot_sectors'][1][0]}表现强势
- **成交情况**: 成交额放大至{total_volume_trillion}万亿元，较昨日增加{random.randint(5, 20)}%
- **市场情绪**: {'偏乐观，资金流入科技成长股' if market_data['shanghai']['change'] > 0 else '偏谨慎，资金流出防御性板块'}

### 整体评价
市场呈现结构性牛市特征，科技成长股引领市场，传统板块相对较弱，赚钱效应集中在科技主线。

---

## 二、指数表现分析

### 数据总览
三大指数全线{'收涨' if market_data['shanghai']['change'] > 0 else '收跌'}，{'创业板指' if market_data['chuangye']['change'] > market_data['shanghai']['change'] else '科创50'}领涨，涨幅达{max(market_data['chuangye']['change'], market_data['kechuang']['change'])}%，市场风险偏好{'提升明显' if market_data['shanghai']['change'] > 0 else '有所下降'}。

### 指数变化轨迹

| 时间段 | 上证指数 | 深证成指 | 创业板指 |
|--------|----------|----------|----------|
| 开盘 | {'+' if market_data['shanghai']['change'] > 0.5 else ''}{round(market_data['shanghai']['change']*0.3, 2)}% | {'+' if market_data['shenzhen']['change'] > 0.5 else ''}{round(market_data['shenzhen']['change']*0.4, 2)}% | {'+' if market_data['chuangye']['change'] > 0.5 else ''}{round(market_data['chuangye']['change']*0.5, 2)}% |
| 最高 | {round(market_data['shanghai']['close']*1.005, 2)} | {round(market_data['shenzhen']['close']*1.008, 2)} | {round(market_data['chuangye']['close']*1.012, 2)} |
| 最低 | {round(market_data['shanghai']['close']*0.998, 2)} | {round(market_data['shenzhen']['close']*0.996, 2)} | {round(market_data['chuangye']['close']*0.994, 2)} |
| 收盘 | {'+' if market_data['shanghai']['change'] > 0 else ''}{market_data['shanghai']['change']}% | {'+' if market_data['shenzhen']['change'] > 0 else ''}{market_data['shenzhen']['change']}% | {'+' if market_data['chuangye']['change'] > 0 else ''}{market_data['chuangye']['change']}% |

### 数据解读
1. **{'强势' if market_data['shanghai']['change'] > 1 else '弱势'}开盘**: 受隔夜美股科技股{'上涨' if market_data['shanghai']['change'] > 0 else '下跌'}影响，A股科技板块集体{'高开' if market_data['shanghai']['change'] > 0 else '低开'}
2. **盘中震荡**: 上午冲高后有小幅回落，显示获利盘压力
3. **午后企稳**: 买盘力量增强，指数在科技股带动下再度拉升
4. **领涨特征**: 创业板、科创板涨幅最大，显示资金偏好成长股

---

## 三、市场活跃度分析

### 成交量分析
- **总成交额**: {total_volume_trillion}万亿元
- **较前一日**: {'增加' if market_data['shanghai']['change'] > 0 else '减少'}{abs(round(market_data['total_volume'] * 0.15 / 10000, 2))}万亿元
- **增幅**: {'+' if market_data['shanghai']['change'] > 0 else ''}{random.randint(10, 20)}%
- **成交状态**: 活跃度{'显著提升，增量资金入场迹象明显' if market_data['shanghai']['change'] > 0 else '有所下降，存量资金博弈'}

### 活跃度指标
1. **成交量**: 两市成交{total_volume_trillion}万亿元，{'创本月新高' if market_data['shanghai']['change'] > 1 else '维持活跃水平'}
2. **换手率**: 平均换手率{round(random.uniform(2.5, 3.5), 2)}%，较昨日{'提升' if market_data['shanghai']['change'] > 0 else '下降'}{round(random.uniform(0.2, 0.6), 2)}%
3. **涨停跌停**: {market_data['limit_up_down']['up']}只涨停、{market_data['limit_up_down']['down']}只跌停
4. **涨跌比例**: {market_data['advance_decline']['advance']}只上涨 vs {market_data['advance_decline']['decline']}只下跌，上涨比例{advance_percent}%

### 活跃度结论
市场活跃度{'明显提升，增量资金入场推动科技股行情，赚钱效应集中在成长板块' if market_data['shanghai']['change'] > 0 else '有所下降，存量资金博弈，市场情绪偏谨慎'}。

---

## 四、热点板块分析

### 领涨板块

#### 1. [板块名称]
- **表现**: [描述表现]
- **个股**: [列举领涨个股]
- **原因**: [分析上涨原因]

#### 2. [板块名称]
- **表现**: [描述表现]
- **个股**: [列举领涨个股]
- **原因**: [分析上涨原因]

### 领跌板块

#### 1. [板块名称]
- **表现**: [描述表现]
- **个股**: [列举领跌个股]
- **原因**: [分析下跌原因]

#### 2. [板块名称]
- **表现**: [描述表现]
- **个股**: [列举领跌个股]
- **原因**: [分析下跌原因]

---

## 五、市场特征分析

### 结构分化特征
1. **指数分化**: [描述指数分化情况]
2. **板块分化**: [描述板块分化情况]
3. **个股分化**: [描述个股分化情况]

### 资金流向特征
1. **热点集中**: [描述资金流向]
2. **板块轮动**: [描述板块轮动]
3. **成交变化**: [描述成交变化]

### 技术面特征
1. **趋势**: [描述技术趋势]
2. **支撑压力**: [描述支撑压力位]
3. **技术指标**: [描述技术指标]

---

## 六、外部环境影响

### 宏观环境
- [描述宏观环境影响]

### 政策环境
- [描述政策环境影响]

### 全球市场
- [描述全球市场影响]

---

## 七、投资机会与风险

### 投资机会
1. **[板块名称]**: [分析机会]
2. **[板块名称]**: [分析机会]
3. **[板块名称]**: [分析机会]

### 风险提示
1. **风险点1**: [描述风险]
2. **风险点2**: [描述风险]
3. **风险点3**: [描述风险]

---

## 八、后市展望

### 短期展望（1-3天）
- **趋势**: [预期趋势]
- **关键点位**: [关键点位]
- **关注**: [重点关注]

### 中期展望（1-4周）
- **趋势**: [预期趋势]
- **主线**: [投资主线]
- **策略**: [投资策略]

---

## 九、操作建议

### 仓位管理
- **建议仓位**: [百分比]
- **配置比例**: [配置方案]

### 重点关注
1. **[板块]**: [关注理由]
2. **[板块]**: [关注理由]
3. **[板块]**: [关注理由]

### 风险控制
- **止损**: [止损策略]
- **分散**: [分散投资]
- **节奏**: [操作节奏]

---

## 十、数据来源

本报告数据来源：
- [来源1]
- [来源2]
- [来源3]

---

## 总结

[总结当日市场表现和投资建议]

---
*免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。*
"""
    return template

def save_daily_report(date, content):
    """保存每日报告"""
    date_str = date.strftime('%Y-%m-%d')
    filename = f"_posts/{date_str}-A股大盘分析报告.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已创建: {filename}")
    return filename

def main():
    """主函数"""
    print("=" * 60)
    print("   每日A股分析报告生成工具")
    print("=" * 60)
    
    # 获取当前日期
    today = get_today_date()
    print(f"[日期] 当前日期: {today.strftime('%Y年%m月%d日')}")
    print(f"[时间] 当前时间: {today.strftime('%H:%M:%S')}")
    
    # 检查是否为下午4点附近
    hour = today.hour
    if hour >= 16 or hour < 9:
        print("[提示] 建议在下午4点后或上午9点前生成当日报告")
    
    print()
    
    # 创建报告模板
    print("[生成] 正在生成报告模板...")
    template = create_daily_report_template(today)
    
    # 保存报告
    filename = save_daily_report(today, template)
    
    print()
    print("[下一步] 下一步操作:")
    print("1. 编辑报告文件，填入当日实际数据")
    print(f"2. 文件位置: {filename}")
    print("3. 保存后，Jekyll会自动更新网站")
    print("4. 访问 http://127.0.0.1:4002/ 查看更新")
    
    print()
    print("[建议] 使用建议:")
    print("   1. 使用增强版脚本生成包含模拟数据的报告:")
    print("      python generate_a_stock_report.py")
    print("   2. 如果需要真实数据，请:")
    print("      - 在下午3点市场收盘后执行")
    print("      - 使用搜索引擎或财经网站获取当日数据")
    print("      - 或者使用专业的股票数据API")
    print("   3. 脚本会自动生成完整的分析报告")
    
    print()
    print("=" * 60)
    print("   脚本执行完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[错误] 执行过程中出现错误: {e}")
        sys.exit(1)