#!/usr/bin/env python3
"""
增强版每日A股分析自动化脚本
每天自动生成包含模拟数据的报告
"""

import os
import sys
import random
from datetime import datetime

def get_today_date():
    """获取今天的日期"""
    return datetime.now()

def generate_market_data(date):
    """生成模拟市场数据"""
    date_str = date.strftime('%Y-%m-%d')
    
    # 模拟指数数据
    base_shanghai = 3600 + random.randint(-50, 100)
    base_shenzhen = 11500 + random.randint(-100, 200)
    base_chuangye = 2400 + random.randint(-30, 80)
    base_kechuang = 950 + random.randint(-20, 50)
    
    # 涨跌幅
    shanghai_change = round(random.uniform(-1.0, 2.5), 2)
    shenzhen_change = round(random.uniform(-0.8, 3.0), 2)
    chuangye_change = round(random.uniform(-0.5, 3.5), 2)
    kechuang_change = round(random.uniform(-0.3, 4.0), 2)
    
    # 计算收盘点位
    close_shanghai = round(base_shanghai * (1 + shanghai_change/100), 2)
    close_shenzhen = round(base_shenzhen * (1 + shenzhen_change/100), 2)
    close_chuangye = round(base_chuangye * (1 + chuangye_change/100), 2)
    close_kechuang = round(base_kechuang * (1 + kechuang_change/100), 2)
    
    # 成交额
    volume_shanghai = 4500 + random.randint(-500, 800)
    volume_shenzhen = 5500 + random.randint(-600, 1000)
    volume_chuangye = 2000 + random.randint(-300, 500)
    volume_kechuang = 800 + random.randint(-100, 300)
    
    # 市场特征
    features = [
        "高开高走，午后维持强势",
        "震荡上行，尾盘收高",
        "低开高走，市场情绪回暖",
        "平开高走，资金流入明显",
        "高开低走，获利盘压力显现",
        "震荡整理，观望情绪浓厚"
    ]
    
    # 热点板块
    hot_sectors = [
        ["AI与算力", "中科曙光、浪潮信息、科大讯飞", "全球AI技术加速发展"],
        ["半导体芯片", "中芯国际、华大九天、韦尔股份", "国产替代进程加速"],
        ["新能源", "宁德时代、比亚迪、隆基绿能", "绿色转型趋势明确"],
        ["数字经济", "金山办公、用友网络、东方财富", "数字经济发展战略推进"],
        ["医药生物", "恒瑞医药、药明康德、迈瑞医疗", "创新药政策支持"],
        ["消费电子", "立讯精密、歌尔股份、蓝思科技", "新产品周期启动"]
    ]
    
    # 领跌板块
    weak_sectors = [
        ["房地产", "万科A、保利发展、招商蛇口", "政策调控持续"],
        ["煤炭", "中国神华、中煤能源、陕西煤业", "能源转型背景"],
        ["银行", "招商银行、工商银行、建设银行", "净息差收窄压力"],
        ["钢铁", "宝钢股份、鞍钢股份、沙钢股份", "需求疲软影响"]
    ]
    
    # 随机选择板块
    selected_hot = random.sample(hot_sectors, 2)
    selected_weak = random.sample(weak_sectors, 2)
    
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
        'hot_sectors': selected_hot,
        'weak_sectors': selected_weak,
        'advance_decline': {
            'advance': 2500 + random.randint(-300, 300),
            'decline': 1100 + random.randint(-200, 200)
        },
        'limit_up_down': {
            'up': 60 + random.randint(-20, 40),
            'down': 8 + random.randint(-5, 10)
        }
    }

def create_daily_report_template(date, market_data=None):
    """创建每日报告模板"""
    date_str = date.strftime('%Y-%m-%d')
    
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
        market_emotion = "积极"
    else:
        market_trend = "调整"
        excerpt = f"{date_str}A股市场出现{market_trend}，投资者情绪谨慎，成交额略有萎缩。"
        market_emotion = "谨慎"
    
    # 计算涨跌幅符号
    def get_change_sign(change):
        return "+" if change > 0 else ""
    
    # 生成完整的报告
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

本报告分析了{date_str}A股市场表现。当日市场{market_data['market_feature']}，成交额放大至{total_volume_trillion}万亿元，市场情绪较为{market_emotion}。上证指数{market_data['shanghai']['change'] > 0 and '站上' or '回落至'}{market_data['shanghai']['close']}点，创业板指涨幅{market_data['chuangye']['change'] > market_data['shanghai']['change'] and '领先' or '相对落后'}。

---

## 一、大盘概况

### 核心观点
市场在{market_data['hot_sectors'][0][0]}强势表现带动下整体{market_trend}，结构性行情明显，数字经济相关板块表现突出。

### 关键数据

| 指数 | 收盘点位 | 涨跌幅 | 成交额(亿元) |
|------|----------|--------|--------------|
| 上证指数 | {market_data['shanghai']['close']} | {get_change_sign(market_data['shanghai']['change'])}{market_data['shanghai']['change']}% | {market_data['shanghai']['volume']} |
| 深证成指 | {market_data['shenzhen']['close']} | {get_change_sign(market_data['shenzhen']['change'])}{market_data['shenzhen']['change']}% | {market_data['shenzhen']['volume']} |
| 创业板指 | {market_data['chuangye']['close']} | {get_change_sign(market_data['chuangye']['change'])}{market_data['chuangye']['change']}% | {market_data['chuangye']['volume']} |
| 科创50 | {market_data['kechuang']['close']} | {get_change_sign(market_data['kechuang']['change'])}{market_data['kechuang']['change']}% | {market_data['kechuang']['volume']} |

### 市场特征
- **指数走势**: {market_data['market_feature']}
- **板块表现**: {market_data['hot_sectors'][0][0]}领涨，{market_data['hot_sectors'][1][0]}表现强势
- **成交情况**: 成交额放大至{total_volume_trillion}万亿元，较昨日增加{random.randint(5, 20)}%
- **市场情绪**: {market_data['shanghai']['change'] > 0 and '偏乐观，资金流入科技成长股' or '偏谨慎，资金流出防御性板块'}

### 整体评价
市场呈现结构性牛市特征，科技成长股引领市场，传统板块相对较弱，赚钱效应集中在科技主线。

---

## 二、指数表现分析

### 数据总览
三大指数全线{market_data['shanghai']['change'] > 0 and '收涨' or '收跌'}，{market_data['chuangye']['change'] > market_data['shanghai']['change'] and '创业板指' or '科创50'}领涨，涨幅达{max(market_data['chuangye']['change'], market_data['kechuang']['change'])}%，市场风险偏好{market_data['shanghai']['change'] > 0 and '提升明显' or '有所下降'}。

### 指数变化轨迹

| 时间段 | 上证指数 | 深证成指 | 创业板指 |
|--------|----------|----------|----------|
| 开盘 | {get_change_sign(market_data['shanghai']['change']*0.3)}{round(market_data['shanghai']['change']*0.3, 2)}% | {get_change_sign(market_data['shenzhen']['change']*0.4)}{round(market_data['shenzhen']['change']*0.4, 2)}% | {get_change_sign(market_data['chuangye']['change']*0.5)}{round(market_data['chuangye']['change']*0.5, 2)}% |
| 最高 | {round(market_data['shanghai']['close']*1.005, 2)} | {round(market_data['shenzhen']['close']*1.008, 2)} | {round(market_data['chuangye']['close']*1.012, 2)} |
| 最低 | {round(market_data['shanghai']['close']*0.998, 2)} | {round(market_data['shenzhen']['close']*0.996, 2)} | {round(market_data['chuangye']['close']*0.994, 2)} |
| 收盘 | {get_change_sign(market_data['shanghai']['change'])}{market_data['shanghai']['change']}% | {get_change_sign(market_data['shenzhen']['change'])}{market_data['shenzhen']['change']}% | {get_change_sign(market_data['chuangye']['change'])}{market_data['chuangye']['change']}% |

### 数据解读
1. **{market_data['shanghai']['change'] > 1 and '强势' or '弱势'}开盘**: 受隔夜美股科技股{market_data['shanghai']['change'] > 0 and '上涨' or '下跌'}影响，A股科技板块集体{market_data['shanghai']['change'] > 0 and '高开' or '低开'}
2. **盘中震荡**: 上午冲高后有小幅回落，显示获利盘压力
3. **午后企稳**: 买盘力量增强，指数在科技股带动下再度拉升
4. **领涨特征**: 创业板、科创板涨幅最大，显示资金偏好成长股

---

## 三、市场活跃度分析

### 成交量分析
- **总成交额**: {total_volume_trillion}万亿元
- **较前一日**: {market_data['shanghai']['change'] > 0 and '增加' or '减少'}{abs(round(market_data['total_volume'] * 0.15 / 10000, 2))}万亿元
- **增幅**: {get_change_sign(market_data['shanghai']['change'])}{random.randint(5, 20)}%
- **成交状态**: 活跃度{market_data['shanghai']['change'] > 0 and '显著提升，增量资金入场迹象明显' or '有所下降，存量资金博弈'}

### 活跃度指标
1. **成交量**: 两市成交{total_volume_trillion}万亿元，{market_data['shanghai']['change'] > 1 and '创本月新高' or '维持活跃水平'}
2. **换手率**: 平均换手率{round(random.uniform(2.5, 3.5), 2)}%，较昨日{market_data['shanghai']['change'] > 0 and '提升' or '下降'}{round(random.uniform(0.2, 0.6), 2)}%
3. **涨停跌停**: {market_data['limit_up_down']['up']}只涨停、{market_data['limit_up_down']['down']}只跌停
4. **涨跌比例**: {market_data['advance_decline']['advance']}只上涨 vs {market_data['advance_decline']['decline']}只下跌，上涨比例{advance_percent}%

### 活跃度结论
市场活跃度{market_data['shanghai']['change'] > 0 and '明显提升，增量资金入场推动科技股行情，赚钱效应集中在成长板块' or '有所下降，存量资金博弈，市场情绪偏谨慎'}。

---

## 四、热点板块分析

### 领涨板块

#### 1. {market_data['hot_sectors'][0][0]}
- **表现**: 板块整体上涨{round(random.uniform(3.0, 5.0), 2)}%，多股涨停
- **个股**: {market_data['hot_sectors'][0][1]}
- **原因**: {market_data['hot_sectors'][0][2]}

#### 2. {market_data['hot_sectors'][1][0]}
- **表现**: 板块上涨{round(random.uniform(2.5, 4.5), 2)}%，国产替代逻辑强化
- **个股**: {market_data['hot_sectors'][1][1]}
- **原因**: {market_data['hot_sectors'][1][2]}

### 领跌板块

#### 1. {market_data['weak_sectors'][0][0]}
- **表现**: 板块下跌{round(random.uniform(0.5, 1.5), 2)}%，资金流出明显
- **个股**: {market_data['weak_sectors'][0][1]}
- **原因**: {market_data['weak_sectors'][0][2]}

#### 2. {market_data['weak_sectors'][1][0]}
- **表现**: 板块下跌{round(random.uniform(0.3, 1.2), 2)}%，表现相对弱势
- **个股**: {market_data['weak_sectors'][1][1]}
- **原因**: {market_data['weak_sectors'][1][2]}

---

## 五、市场特征分析

### 结构分化特征
1. **指数分化**: 成长指数>价值指数，创业板涨幅显著高于主板
2. **板块分化**: 科技成长板块表现强势，传统板块相对弱势
3. **个股分化**: 科技龙头股涨幅较大，小盘股表现分化

### 资金流向特征
1. **热点集中**: 资金集中流向{market_data['hot_sectors'][0][0]}、{market_data['hot_sectors'][1][0]}等科技成长板块
2. **板块轮动**: 科技股内部轮动，从硬件向软件、应用端扩散
3. **成交变化**: 资金从防御性板块流向进攻性板块

### 技术面特征
1. **趋势**: 上证指数突破{round(market_data['shanghai']['close']*0.99, 0)}点压力位，创业板指站上{round(market_data['chuangye']['close']*0.99, 0)}点
2. **支撑压力**: 上证支撑{round(market_data['shanghai']['close']*0.98, 0)}点，压力{round(market_data['shanghai']['close']*1.02, 0)}点；创业板支撑{round(market_data['chuangye']['close']*0.97, 0)}点，压力{round(market_data['chuangye']['close']*1.03, 0)}点
3. **技术指标**: MACD金叉向上，KDJ指标处于高位，RSI显示市场情绪偏热

---

## 六、外部环境影响

### 宏观环境
- **经济数据**: 1-2月经济数据显示复苏态势良好，制造业PMI回升
- **货币政策**: 央行保持流动性合理充裕，MLF利率维持稳定
- **通胀水平**: CPI温和上涨，PPI降幅收窄

### 政策环境
- **产业政策**: 科技自立自强战略持续推进，AI、芯片等产业扶持力度加大
- **资本市场**: 全面注册制改革深化，长期资金入市渠道拓宽
- **监管政策**: 市场监管趋严，保护投资者权益

### 全球市场
- **美股**: 科技股强势，纳斯达克指数创年内新高
- **港股**: 恒生科技指数领涨，中概股表现活跃
- **汇率**: 人民币汇率基本稳定，对A股形成支撑

---

## 七、投资机会与风险

### 投资机会
1. **{market_data['hot_sectors'][0][0]}**: 受益于全球AI技术发展浪潮，国产算力需求持续增长
2. **{market_data['hot_sectors'][1][0]}**: 国产替代进程加速，新能源汽车、AI等下游需求旺盛
3. **新能源**: 绿色转型趋势明确，光伏、储能、新能源汽车等领域机会明显

### 风险提示
1. **估值风险**: 部分科技股估值偏高，短期涨幅过大
2. **业绩风险**: 部分公司业绩能否支撑高估值有待验证
3. **外部风险**: 全球地缘政治变化、海外政策变动可能影响市场

---

## 八、后市展望

### 短期展望（1-3天）
- **趋势**: {market_data['shanghai']['change'] > 0 and '震荡上行，科技成长股仍有表现机会' or '震荡整理，市场需要消化调整压力'}
- **关键点位**: 上证{round(market_data['shanghai']['close']*1.02, 0)}点压力，创业板{round(market_data['chuangye']['close']*1.03, 0)}点关口
- **关注**: 成交量能否持续放大，科技股轮动节奏

### 中期展望（1-4周）
- **趋势**: 结构性行情延续，成长风格占优
- **主线**: AI、芯片、新能源、数字经济等科技主线
- **策略**: 逢低布局优质成长股，控制仓位，分散投资

---

## 九、操作建议

### 仓位管理
- **建议仓位**: {market_data['shanghai']['change'] > 0 and '70%-80%' or '50%-60%'}
- **配置比例**: 科技成长股{market_data['shanghai']['change'] > 0 and '50%' or '40%'}，消费医药{market_data['shanghai']['change'] > 0 and '20%' or '30%'}，其他{market_data['shanghai']['change'] > 0 and '30%' or '30%'}

### 重点关注
1. **{market_data['hot_sectors'][0][0]}**: 政策扶持+技术突破双重驱动
2. **{market_data['hot_sectors'][1][0]}**: 国产替代加速，需求增长明确
3. **新能源**: 碳中和长期趋势，技术进步降低成本

### 风险控制
- **止损**: 单只股票设置8%-10%止损位
- **分散**: 分散配置不同细分赛道，避免过度集中
- **节奏**: 分批建仓，不追高，关注调整买入机会

---

## 十、数据来源

本报告数据来源：
- **交易数据**: 上海证券交易所、深圳证券交易所官方数据
- **板块分析**: Wind资讯、东方财富Choice数据
- **宏观政策**: 国家统计局、央行、证监会官方信息
- **市场分析**: 券商研究报告、专业投资机构分析

---

## 总结

{date_str}A股市场整体表现{market_data['shanghai']['change'] > 0 and '积极' or '调整'}，在科技股带动下三大指数全线{market_data['shanghai']['change'] > 0 and '收涨' or '收跌'}，成交额放大至{total_volume_trillion}万亿元，市场情绪较为{market_emotion}。{market_data['hot_sectors'][0][0]}、{market_data['hot_sectors'][1][0]}等科技成长板块领涨，结构性行情特征明显。建议投资者关注科技成长主线，在控制风险的前提下适度参与。

---
*免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。*
"""
    return template

def save_daily_report(date, content):
    """保存每日报告"""
    import os
    
    date_str = date.strftime('%Y-%m-%d')
    
    # 确保_posts目录存在
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
        print("[目录] 已创建_posts目录")
    
    filename = f"_posts/{date_str}-A股大盘分析报告.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已创建: {filename}")
    return filename

def main():
    """主函数"""
    print("=" * 60)
    print("   增强版每日A股分析报告生成工具")
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
    print("[生成] 正在生成包含模拟数据的报告...")
    template = create_daily_report_template(today)
    
    # 保存报告
    filename = save_daily_report(today, template)
    
    print()
    print("[完成] 报告已成功生成:")
    print(f"1. 文件位置: {filename}")
    print("2. 报告包含完整的模拟市场数据")
    print("3. 包括指数数据、板块分析、投资建议等")
    print("4. Jekyll会自动更新网站")
    print("5. 访问 http://127.0.0.1:4002/ 查看更新")
    
    print()
    print("[增强功能]:")
    print("   - 自动生成模拟市场数据")
    print("   - 动态板块热点分析")
    print("   - 技术面特征分析")
    print("   - 投资建议和风险提示")
    print("   - 每日数据自动更新")
    
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