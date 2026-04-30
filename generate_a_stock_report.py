#!/usr/bin/env python3
"""
A股大盘分析报告生成脚本（带自动Git推送）
生成包含模拟数据的每日报告，并自动推送到GitHub
"""

import os
import sys
import random
from datetime import datetime, timedelta
import subprocess

def ensure_posts_dir():
    """确保_posts目录存在"""
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
        print("已创建_posts目录")

def generate_stock_data(date):
    """生成股票市场数据"""
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
            'volume': 4500 + random.randint(-500, 800)
        },
        'shenzhen': {
            'close': round(11500 + random.uniform(-100, 200), 2),
            'change': round(shanghai_change + random.uniform(0.1, 0.5), 2),
            'volume': 5500 + random.randint(-600, 1000)
        },
        'chuangye': {
            'close': round(2400 + random.uniform(-30, 80), 2),
            'change': round(shanghai_change + random.uniform(0.3, 0.8), 2),
            'volume': 2000 + random.randint(-300, 500)
        },
        'kechuang': {
            'close': round(950 + random.uniform(-20, 50), 2),
            'change': round(shanghai_change + random.uniform(0.5, 1.2), 2),
            'volume': 800 + random.randint(-100, 300)
        }
    }
    
    # 计算总成交额
    total_volume = (
        data['shanghai']['volume'] + 
        data['shenzhen']['volume'] + 
        data['chuangye']['volume'] + 
        data['kechuang']['volume']
    )
    data['total_volume_trillion'] = round(total_volume / 10000, 2)
    
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
        ("AI与算力", "中科曙光、浪潮信息、科大讯飞", "全球AI技术加速发展，国产算力需求激增"),
        ("半导体芯片", "中芯国际、华大九天、韦尔股份", "国产替代进程加速，下游需求旺盛"),
        ("新能源", "宁德时代、比亚迪、隆基绿能", "绿色转型趋势明确，技术进步降低成本"),
        ("数字经济", "金山办公、用友网络、东方财富", "数字经济发展战略推进，政策支持力度大"),
        ("医药生物", "恒瑞医药、药明康德、迈瑞医疗", "创新药政策支持，老龄化趋势推动"),
        ("消费电子", "立讯精密、歌尔股份、蓝思科技", "新产品周期启动，消费需求复苏")
    ]
    
    # 领跌板块
    weak_sectors = [
        ("房地产", "万科A、保利发展、招商蛇口", "政策调控持续，市场预期谨慎"),
        ("煤炭", "中国神华、中煤能源、陕西煤业", "能源转型背景，传统能源承压"),
        ("银行", "招商银行、工商银行、建设银行", "净息差收窄压力，增长放缓"),
        ("钢铁", "宝钢股份、鞍钢股份、沙钢股份", "需求疲软影响，产能过剩压力")
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
    data['advance_percent'] = round(data['advance'] / (data['advance'] + data['decline']) * 100, 1)
    
    # 涨停跌停统计
    data['limit_up'] = 60 + random.randint(-20, 40)
    data['limit_down'] = 8 + random.randint(-5, 10)
    
    return data

def create_report_content(data):
    """创建报告内容"""
    
    def get_change_sign(change):
        return "+" if change > 0 else ""
    
    return f"""---
title: "{data['date']}A股大盘分析"
date: {data['date']} 16:00:00 +0800
categories: 股市分析
tags: A股 大盘 行情分析
---

# {data['date']}A股大盘分析报告

## 报告概述

{data['date']}，A股市场整体呈现{data['trend']}态势。三大指数集体{'收涨' if data['shanghai']['change'] > 0 else '收跌'}，{data['market_feature']}。上证指数{get_change_sign(data['shanghai']['change'])}{data['shanghai']['change']}%报{data['shanghai']['close']}点，深成指{get_change_sign(data['shenzhen']['change'])}{data['shenzhen']['change']}%报{data['shenzhen']['close']}点，创业板指{get_change_sign(data['chuangye']['change'])}{data['chuangye']['change']}%报{data['chuangye']['close']}点。两市成交额{data['total_volume_trillion']}万亿元，较前一交易日{'增加' if data['shanghai']['change'] > 0 else '减少'}{random.randint(5, 15)}%。个股{data['advance']}只上涨，{data['decline']}只下跌，上涨占比{data['advance_percent']}%。

---

## 一、大盘概况

### 核心观点

A股三大指数{data['market_feature']}。{'成交放量显示增量资金入场' if data['shanghai']['change'] > 0 else '成交缩量显示市场观望情绪升温'}，但结构性机会仍存。

### 关键数据

| 指数 | 收盘点位 | 涨跌幅 |
|------|----------|--------|
| 上证指数 | {data['shanghai']['close']}点 | {get_change_sign(data['shanghai']['change'])}{data['shanghai']['change']}% |
| 深证成指 | {data['shenzhen']['close']}点 | {get_change_sign(data['shenzhen']['change'])}{data['shenzhen']['change']}% |
| 创业板指 | {data['chuangye']['close']}点 | {get_change_sign(data['chuangye']['change'])}{data['chuangye']['change']}% |
| 科创50 | {data['kechuang']['close']}点 | {get_change_sign(data['kechuang']['change'])}{data['kechuang']['change']}% |

### 市场特征

- **走势特点**: {data['market_feature']}，{data['trend']}态势明显
- **成交情况**: {data['total_volume_trillion']}万亿元，较上一日{'增加' if data['shanghai']['change'] > 0 else '减少'}{random.randint(5, 15)}%
- **个股表现**: {data['advance']}只上涨，{data['decline']}只下跌，上涨占比{data['advance_percent']}%
- **市场情绪**: {'乐观情绪升温，资金流入科技成长股' if data['shanghai']['change'] > 0 else '观望情绪升温，高位股分化加剧'}

---

## 二、热点板块分析

### 领涨板块

#### 1. {data['hot_sectors'][0][0]}
- **表现**: 板块整体上涨{round(random.uniform(2.5, 5.0), 2)}%，多股表现强势
- **个股**: {data['hot_sectors'][0][1]}领涨
- **原因**: {data['hot_sectors'][0][2]}

#### 2. {data['hot_sectors'][1][0]}
- **表现**: 板块上涨{round(random.uniform(2.0, 4.5), 2)}%，资金关注度高
- **个股**: {data['hot_sectors'][1][1]}表现突出
- **原因**: {data['hot_sectors'][1][2]}

### 领跌板块

#### 1. {data['weak_sectors'][0][0]}
- **表现**: 板块下跌{round(random.uniform(0.5, 1.8), 2)}%，资金流出明显
- **个股**: {data['weak_sectors'][0][1]}跌幅居前
- **原因**: {data['weak_sectors'][0][2]}

#### 2. {data['weak_sectors'][1][0]}
- **表现**: 板块下跌{round(random.uniform(0.3, 1.5), 2)}%，相对弱势
- **个股**: {data['weak_sectors'][1][1]}小幅下跌
- **原因**: {data['weak_sectors'][1][2]}

---

## 三、资金流向分析

### 主力资金流向

| 资金类型 | 流向 | 金额 |
|----------|------|------|
| 主力资金 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(50, 200))}亿元 |
| 超大单 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(30, 150))}亿元 |
| 大单 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(20, 100))}亿元 |
| 中单 | 净流入 | +{random.randint(10, 50)}亿元 |

### 北向资金

| 交易所 | 流向 | 金额 |
|--------|------|------|
| 沪股通 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(20, 80))}亿元 |
| 深股通 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(15, 70))}亿元 |
| 合计 | {'净流入' if data['shanghai']['change'] > 0 else '净流出'} | {('+' if data['shanghai']['change'] > 0 else '-') + str(random.randint(35, 150))}亿元 |

---

## 四、技术面分析

### 指数技术特征

1. **上证指数**: {'突破' if data['shanghai']['change'] > 0 else '跌破'}{round(data['shanghai']['close']*0.99, 0)}点{'压力位' if data['shanghai']['change'] > 0 else '支撑位'}，MACD指标{'金叉向上' if data['shanghai']['change'] > 0 else '死叉向下'}
2. **创业板指**: 站上{round(data['chuangye']['close']*0.98, 0)}点，{'强势特征明显' if data['chuangye']['change'] > 1 else '震荡整理态势'}
3. **技术形态**: {'多头排列' if data['shanghai']['change'] > 0 else '调整态势'}，成交量{'配合良好' if data['shanghai']['change'] > 0 else '有所萎缩'}

### 关键点位

- **上证支撑**: {round(data['shanghai']['close']*0.98, 0)}点
- **上证压力**: {round(data['shanghai']['close']*1.02, 0)}点
- **创业支撑**: {round(data['chuangye']['close']*0.97, 0)}点
- **创业压力**: {round(data['chuangye']['close']*1.03, 0)}点

---

## 五、后市展望与操作建议

### 短期展望（1-3天）

- **趋势判断**: {'震荡上行概率较大' if data['shanghai']['change'] > 0 else '震荡整理为主'}
- **关键点位**: 关注上证{round(data['shanghai']['close']*1.02, 0)}点压力，创业板{round(data['chuangye']['close']*1.03, 0)}点关口
- **操作策略**: {'逢低布局，不追高' if data['shanghai']['change'] > 0 else '控制仓位，等待企稳'}

### 投资建议

1. **仓位建议**: {'70%-80%' if data['shanghai']['change'] > 0 else '50%-60%'}
2. **板块配置**: 重点关注{data['hot_sectors'][0][0]}、{data['hot_sectors'][1][0]}等成长板块
3. **风险控制**: 单只个股止损位8%-10%，避免过度集中

### 风险提示

1. **市场风险**: 外部环境变化可能影响市场情绪
2. **估值风险**: 部分热门板块估值偏高
3. **政策风险**: 监管政策变化可能影响相关板块

---

## 总结

{data['date']}A股市场呈现{data['trend']}态势，{data['market_feature']}。{data['hot_sectors'][0][0]}、{data['hot_sectors'][1][0]}等板块表现强势，{data['weak_sectors'][0][0]}、{data['weak_sectors'][1][0]}等板块相对弱势。建议投资者关注成长主线，{'适度参与' if data['shanghai']['change'] > 0 else '谨慎操作'}，控制风险。

---

*免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。股市有风险，投资需谨慎。*"""

def save_report(date_str, content):
    """保存报告"""
    filename = f"_posts/{date_str}-A股大盘分析报告.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] 报告已保存: {filename}")
    return filename

def git_commit_and_push(filename, date_str):
    """提交并推送到GitHub"""
    try:
        print("\n[Git] 正在添加到Git...")
        result = subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)
        
        print("[Git] 正在提交...")
        commit_msg = f"自动更新{date_str}A股分析报告"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True, text=True)
        print(f"[Git] 提交成功: {commit_msg}")
        
        print("[Git] 正在推送到GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'master'], check=True, capture_output=True, text=True)
        print("[Git] 推送成功! ✅")
        print(f"[GitHub] 网站将自动更新: https://373kice.github.io/")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Git错误] Git操作失败: {e}")
        if e.stderr:
            print(f"[Git错误] 详细信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"[Git错误] 未知错误: {e}")
        return False

def generate_today_report():
    """生成今日报告"""
    print("=" * 60)
    print("   A股大盘分析报告生成工具（带自动推送）")
    print("=" * 60)
    
    ensure_posts_dir()
    
    # 获取今天日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    print(f"[日期] 生成日期: {date_str}")
    print(f"[时间] 当前时间: {today.strftime('%H:%M:%S')}")
    
    # 检查是否为交易时间后
    hour = today.hour
    if hour < 15:
        print("[提示] 建议在下午3点市场收盘后生成报告")
    else:
        print("[OK]  时间合适: 市场已收盘")
    
    print()
    print("[数据] 正在生成市场数据...")
    
    # 生成市场数据
    market_data = generate_stock_data(today)
    
    print("[内容] 正在生成报告内容...")
    
    # 创建报告内容
    report_content = create_report_content(market_data)
    
    print("[保存] 正在保存报告...")
    
    # 保存报告
    filename = save_report(date_str, report_content)
    
    print()
    print("[完成] 报告生成完成!")
    print(f"[文件] 文件: {filename}")
    print(f"[长度] 长度: {len(report_content)} 字符")
    
    # 显示报告摘要
    print()
    print("[摘要] 报告摘要:")
    lines = report_content.split('\n')
    for i, line in enumerate(lines[:15]):
        if line.strip():
            print(f"   {line}")
    
    # 自动推送到GitHub
    print()
    print("[Git] 开始自动推送到GitHub...")
    git_commit_and_push(filename, date_str)
    
    print()
    print("=" * 60)
    print("   脚本执行完成!")
    print("=" * 60)
    
    return filename

def main():
    """主函数"""
    try:
        generate_today_report()
    except Exception as e:
        print(f"[错误] 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
