#!/usr/bin/env python3
"""测试增强版脚本"""

import os
import sys
import random
from datetime import datetime

def main():
    print("测试增强版脚本...")
    print("当前目录:", os.getcwd())
    print("Python版本:", sys.version)
    
    today = datetime.now()
    print(f"当前日期: {today.strftime('%Y-%m-%d')}")
    
    # 测试随机数生成
    print(f"随机测试: {random.randint(1, 100)}")
    
    print("测试完成!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")