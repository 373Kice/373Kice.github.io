#!/usr/bin/env python3
"""
验证Jekyll网站修复的脚本
"""

import os
import sys
import requests
import time

def check_sass_fix():
    """检查Sass修复是否成功"""
    print("=== 检查Sass修复 ===")
    
    main_scss_path = "css/main.scss"
    if os.path.exists(main_scss_path):
        with open(main_scss_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "@import" in content and "@use" not in content:
            print("❌ 警告: main.scss中仍包含弃用的@import语句")
            return False
        elif "@use" in content:
            print("✅ Sass修复成功: 已使用@use代替@import")
            return True
        else:
            print("⚠️ 未知状态: 未检测到@import或@use语句")
            return True
    else:
        print("❌ 错误: 未找到main.scss文件")
        return False

def check_gemfile_fix():
    """检查Gemfile修复是否成功"""
    print("\n=== 检查Gemfile修复 ===")
    
    gemfile_path = "Gemfile"
    if os.path.exists(gemfile_path):
        with open(gemfile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "gem \"wdm\"" in content:
            print("✅ Gemfile修复成功: 已添加wdm gem")
            return True
        else:
            print("❌ 警告: Gemfile中未找到wdm gem")
            return False
    else:
        print("❌ 错误: 未找到Gemfile文件")
        return False

def check_website_running():
    """检查网站是否在运行"""
    print("\n=== 检查网站运行状态 ===")
    
    try:
        # 尝试访问本地服务器
        response = requests.get('http://127.0.0.1:4001/', timeout=5)
        if response.status_code == 200:
            print(f"✅ 网站运行正常: HTTP {response.status_code}")
            return True
        else:
            print(f"⚠️ 网站返回非200状态码: HTTP {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ 无法连接到网站服务器，可能未运行")
        return False
    except Exception as e:
        print(f"❌ 检查网站时出错: {e}")
        return False

def main():
    """主验证函数"""
    print("开始验证Jekyll网站修复...\n")
    
    # 切换到项目目录
    original_dir = os.getcwd()
    project_dir = "D:/GITHUB/373Kice.github.io"
    
    try:
        os.chdir(project_dir)
        print(f"切换到项目目录: {project_dir}")
    except Exception as e:
        print(f"❌ 无法切换到项目目录: {e}")
        return False
    
    try:
        # 运行各项检查
        sass_ok = check_sass_fix()
        gemfile_ok = check_gemfile_fix()
        website_ok = check_website_running()
        
        print("\n=== 验证总结 ===")
        print(f"Sass修复: {'✅ 通过' if sass_ok else '❌ 失败'}")
        print(f"Gemfile修复: {'✅ 通过' if gemfile_ok else '❌ 失败'}")
        print(f"网站运行: {'✅ 通过' if website_ok else '❌ 失败'}")
        
        overall = sass_ok and gemfile_ok and website_ok
        print(f"\n总体状态: {'✅ 所有检查通过!' if overall else '❌ 部分检查失败'}")
        
        if overall:
            print("\n🎉 网站修复完成！现在你的Jekyll网站应该：")
            print("1. 没有Sass弃用警告")
            print("2. 包含wdm gem以优化Windows性能")
            print("3. 正常运行在 http://127.0.0.1:4001/")
            print("\n你可以访问网站，查看是否有任何显示问题。")
        
        return overall
        
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)