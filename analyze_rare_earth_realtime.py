#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取稀土板块龙头股实时数据并生成专业分析
使用 AKShare 获取真实行情数据
"""

import os
import sys
import json
import logging
from datetime import datetime
import akshare as ak
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-8c73c99ec9924c95a82f78d88c945ca9"
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 稀土板块龙头股
RARE_EARTH_STOCKS = [
    {"code": "600111", "name": "北方稀土", "market": "sh"},
    {"code": "000831", "name": "中国稀土", "market": "sz"},
    {"code": "600392", "name": "盛和资源", "market": "sh"},
    {"code": "600549", "name": "厦门钨业", "market": "sh"},
    {"code": "600259", "name": "广晟有色", "market": "sh"},
    {"code": "000758", "name": "中色股份", "market": "sz"},
]

def fetch_stock_realtime_data(stock_code, market):
    """
    获取个股实时行情数据
    
    Args:
        stock_code: 股票代码
        market: 市场（sh/sz）
    
    Returns:
        股票实时数据字典
    """
    try:
        # 获取实时行情
        if market == "sh":
            # 上证股票
            df = ak.stock_sh_a_spot_em()
        else:
            # 深证股票
            df = ak.stock_sz_a_spot_em()
        
        # 查找目标股票
        stock_data = df[df['代码'] == stock_code]
        
        if stock_data.empty:
            logger.warning(f"[数据] 未找到股票 {stock_code}")
            return None
        
        stock_data = stock_data.iloc[0]
        
        return {
            "code": stock_code,
            "name": stock_data['名称'],
            "latest_price": float(stock_data['最新价']),
            "change": float(stock_data['涨跌幅']),
            "change_amount": float(stock_data['涨跌额']),
            "volume": float(stock_data['成交量']),
            "amount": float(stock_data['成交额']),
            "amplitude": float(stock_data['振幅']),
            "max_price": float(stock_data['最高']),
            "min_price": float(stock_data['最低']),
            "open_price": float(stock_data['今开']),
            "prev_close": float(stock_data['昨收']),
            "turnover_rate": float(stock_data['换手率']),
            "pe_ratio": float(stock_data['市盈率-动态']) if stock_data['市盈率-动态'] != '-' else None,
            "pb_ratio": float(stock_data['市净率']) if stock_data['市净率'] != '-' else None,
            "total_market_cap": float(stock_data['总市值']),
            "circulating_market_cap": float(stock_data['流通市值']),
        }
        
    except Exception as e:
        logger.error(f"[数据错误] 获取 {stock_code} 数据失败: {e}")
        return None

def fetch_stock_history(stock_code, market, days=60):
    """
    获取个股历史数据（用于技术分析）
    
    Args:
        stock_code: 股票代码
        market: 市场（sh/sz）
        days: 获取天数
    
    Returns:
        历史数据DataFrame
    """
    try:
        # 获取历史日线数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - pd.Timedelta(days=days)).strftime('%Y%m%d')
        
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if df.empty:
            return None
        
        # 计算技术指标
        df['MA5'] = df['收盘'].rolling(window=5).mean()
        df['MA10'] = df['收盘'].rolling(window=10).mean()
        df['MA20'] = df['收盘'].rolling(window=20).mean()
        
        return df.tail(10)  # 返回最近10天数据
        
    except Exception as e:
        logger.error(f"[数据错误] 获取 {stock_code} 历史数据失败: {e}")
        return None

def fetch_all_stocks_data():
    """
    获取所有稀土龙头股的实时数据（容错版本）
    
    Returns:
        所有股票数据列表
    """
    logger.info("[数据] 开始获取稀土板块龙头股实时数据...")
    
    all_data = []
    failed_stocks = []
    
    for stock in RARE_EARTH_STOCKS:
        logger.info(f"[数据] 正在获取 {stock['name']}({stock['code']})...")
        
        try:
            # 获取实时行情
            realtime_data = fetch_stock_realtime_data(stock['code'], stock['market'])
            
            if realtime_data:
                # 获取历史数据（技术分析用）
                history_data = fetch_stock_history(stock['code'], stock['market'])
                
                if history_data is not None:
                    realtime_data['history'] = history_data.to_dict('records')
                
                all_data.append(realtime_data)
                logger.info(f"[数据] ✅ {stock['name']}: {realtime_data['latest_price']}元 ({realtime_data['change']:+.2f}%)")
            else:
                failed_stocks.append(stock['name'])
                logger.warning(f"[数据] ⚠️ {stock['name']} 数据获取失败，跳过")
        except Exception as e:
            failed_stocks.append(stock['name'])
            logger.warning(f"[数据] ⚠️ {stock['name']} 获取失败: {e}，跳过")
            continue
    
    logger.info(f"\n[数据] 完成! 成功获取 {len(all_data)}/{len(RARE_EARTH_STOCKS)} 只股票数据")
    
    if failed_stocks:
        logger.warning(f"[数据] 未获取的股票: {', '.join(failed_stocks)}")
    
    return all_data

def analyze_with_real_data(stocks_data):
    """
    使用真实数据让 DeepSeek 生成分析
    
    Args:
        stocks_data: 股票实时数据列表
    
    Returns:
        分析报告内容
    """
    if not stocks_data:
        logger.error("[分析] 没有可用的股票数据")
        return None
    
    logger.info("[分析] 开始使用 DeepSeek AI 分析真实数据...")
    
    # 构造提示词（包含真实数据）
    data_section = ""
    for stock in stocks_data:
        data_section += f"""
### {stock['name']}({stock['code']})

**实时行情**:
- 最新价: {stock['latest_price']}元
- 涨跌幅: {stock['change']}%
- 涨跌额: {stock['change_amount']}元
- 今开: {stock['open_price']}元
- 最高: {stock['max_price']}元
- 最低: {stock['min_price']}元
- 昨收: {stock['prev_close']}元
- 成交量: {stock['volume']}手
- 成交额: {stock['amount']}元
- 换手率: {stock['turnover_rate']}%
- 市盈率(动态): {stock['pe_ratio'] if stock['pe_ratio'] else 'N/A'}
- 市净率: {stock['pb_ratio'] if stock['pb_ratio'] else 'N/A'}
- 总市值: {stock['total_market_cap']}元
- 流通市值: {stock['circulating_market_cap']}元

"""
    
    prompt = f"""# 稀土板块龙头股实时分析报告

## 分析任务
基于以下**真实实时行情数据**，对稀土板块6只龙头股进行专业分析，生成投资决策参考。

## 实时行情数据（{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}）

{data_section}

## 分析要求

对每只股票，请基于**上述真实数据**进行专业分析：

1. **技术面分析**（基于真实价格、涨跌幅、换手率）
   - 当前价格位置（高位/低位/中位）
   - 今日走势特征（放量上涨/缩量下跌/震荡）
   - 关键支撑位与压力位（基于今日最高/最低/昨收）
   - 均线形态判断（需要你根据价格区间判断）

2. **估值分析**（基于真实的PE/PB数据）
   - PE/PB估值水平评估
   - 与同行业对比
   - 估值合理性判断

3. **资金面分析**（基于真实的成交额、换手率）
   - 今日资金流向（放量上涨=资金流入，缩量下跌=资金流出）
   - 换手率分析（高换手=活跃，低换手=冷清）
   - 市值与流动性评估

4. **操作建议**（基于真实行情）
   - 操作建议（买入/持有/观望/卖出）
   - 理由（必须基于真实数据，不能假设）
   - 风险提示

## 板块整体判断

- 今日板块表现（基于6只股票的涨跌幅）
- 龙头股表现（北方稀土、中国稀土的涨跌影响）
- 资金流向判断（基于成交额合计）
- 短期操作建议

## 输出要求

1. **必须使用真实数据**，不能出现"假设"、"预计"等字样
2. **数据驱动**：每个结论都要有数据支撑
3. **专业客观**：基于数据客观分析，不夸大、不隐瞒
4. **可操作**：给出明确的操作建议和理由

请以结构化报告形式输出，包含：
- 板块今日表现总结
- 个股详细分析（按投资价值排序）
- 投资组合建议
- 风险提示

使用专业但易懂的语言，适合A股投资者参考。
"""
    
    try:
        import litellm
        
        logger.info("[LLM] 开始调用 DeepSeek API...")
        logger.info(f"[LLM] 模型: {DEEPSEEK_MODEL}")
        logger.info(f"[LLM] 数据条数: {len(stocks_data)}只股票")
        
        # 调用 DeepSeek API
        response = litellm.completion(
            model=f"deepseek/{DEEPSEEK_MODEL}",
            messages=[
                {"role": "system", "content": "你是一位专业的A股有色金属行业分析师，擅长稀土板块研究。你必须基于提供的真实实时数据进行分析，不能假设或推测。你的分析必须数据驱动、客观专业。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 降低温度，提高准确性
            max_tokens=10000,
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

def save_analysis_report(stocks_data, analysis_content, date_str):
    """保存分析报告（包含真实数据）"""
    if not analysis_content:
        logger.error("[错误] 分析内容为空，无法保存")
        return None
    
    # 确保目录存在
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
    
    # 生成文件名
    filename = f"_posts/{date_str}-稀土板块龙头股实时分析报告.md"
    
    # 构造真实数据摘要
    data_summary = "## 📊 实时行情数据摘要\n\n"
    data_summary += "| 股票名称 | 最新价 | 涨跌幅 | 成交额 | 换手率 | PE | PB |\n"
    data_summary += "|---------|--------|--------|---------|---------|-----|-----|\n"
    
    for stock in stocks_data:
        data_summary += f"| {stock['name']} | {stock['latest_price']}元 | {stock['change']}% | {stock['amount']/1e8:.2f}亿 | {stock['turnover_rate']}% | {stock['pe_ratio'] if stock['pe_ratio'] else 'N/A'} | {stock['pb_ratio'] if stock['pb_ratio'] else 'N/A'} |\n"
    
    # 构造完整的Markdown报告
    report = f"""---
title: "{date_str} 稀土板块龙头股实时分析报告"
date: {date_str} 15:30:00 +0800
categories: 股市分析 行业研究
tags: 稀土 有色金属 实时分析 北方稀土 中国稀土 盛和资源
---

# 📊 {date_str} 稀土板块龙头股实时分析报告

> 本报告基于 **AKShare 实时行情数据** + **DeepSeek AI 专业分析**生成
> 
> ⚠️ **数据时效性**: 本报告使用真实实时数据，非假设或推测

---

{data_summary}

---

## 📋 专业分析报告

{analysis_content}

---

## 📝 数据说明

- **数据来源**: AKShare（东方财富、新浪财经等公开数据）
- **数据时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **分析工具**: DeepSeek AI
- **免责声明**: 本报告基于公开信息整理，仅供参考，不构成投资建议。股市有风险，投资需谨慎。

---

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*数据来源: AKShare*
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
        commit_msg = f"自动更新{date_str}稀土板块实时分析报告"
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
    logger.info("=" * 60)
    logger.info("   稀土板块龙头股实时分析系统")
    logger.info("=" * 60)
    
    # 获取今天日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    # 步骤1: 获取真实实时数据
    logger.info("\n[步骤1] 获取真实实时行情数据...")
    stocks_data = fetch_all_stocks_data()
    
    if not stocks_data or len(stocks_data) == 0:
        logger.error("[错误] 无法获取任何股票数据，退出")
        return
    
    logger.info(f"[数据] 成功获取 {len(stocks_data)} 只股票的实时数据，继续分析...")
    
    # 步骤2: 使用真实数据分析
    logger.info("\n[步骤2] 使用 DeepSeek AI 分析真实数据...")
    analysis_content = analyze_with_real_data(stocks_data)
    
    if not analysis_content:
        logger.error("[错误] 分析失败，无法生成报告")
        return
    
    # 步骤3: 保存报告
    logger.info("\n[步骤3] 保存实时分析报告...")
    filename = save_analysis_report(stocks_data, analysis_content, date_str)
    
    if not filename:
        logger.error("[错误] 保存失败")
        return
    
    # 步骤4: 推送到GitHub
    logger.info("\n[步骤4] 开始自动推送到GitHub...")
    git_commit_and_push(filename, date_str)
    
    logger.info("\n" + "=" * 60)
    logger.info("   分析完成!")
    logger.info("=" * 60)
    logger.info(f"[文件] 报告文件: {filename}")
    logger.info(f"[在线] 稍后可在 https://373kice.github.io/ 查看")
    logger.info(f"\n[重要] 本报告使用 **真实实时数据**，非假设或推测！")

if __name__ == "__main__":
    main()
