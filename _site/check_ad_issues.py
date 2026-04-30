#!/usr/bin/env python3
"""
检查网站广告问题的诊断工具
重点排查Taboola广告和其他可疑代码
"""

import os
import re
import sys
from urllib.parse import urlparse

def check_html_files_for_ads():
    """检查HTML文件中的广告代码"""
    print("=== 检查HTML文件中的广告代码 ===")
    
    ad_patterns = [
        (r'taboola\.com', 'Taboola广告平台'),
        (r'googlesyndication\.com', 'Google广告联盟'),
        (r'adsbygoogle', 'Google Adsense'),
        (r'ad\.', '广告相关域名'),
        (r'sponsor', '赞助内容'),
        (r'advert', '广告'),
        (r'ads\b', '广告'),
        (r'analytics\.yahoo\.com', 'Yahoo分析'),
        (r'advertising\.com', 'Advertising.com'),
        (r'doubleclick\.net', 'DoubleClick广告'),
        (r'amazon-adsystem\.com', '亚马逊广告'),
        (r'facebook\.com/tr', 'Facebook追踪'),
        (r'outbrain\.com', 'Outbrain内容推荐'),
        (r'revcontent\.com', 'RevContent广告'),
        (r'zemanta\.com', 'Zemanta广告'),
    ]
    
    # 检查_site目录
    site_dir = "_site"
    if not os.path.exists(site_dir):
        print("❌ _site目录不存在，网站可能未生成")
        return False
    
    found_issues = False
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, description in ad_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"\n❌ 发现广告代码: {filepath}")
                            print(f"   类型: {description}")
                            print(f"   匹配模式: {pattern}")
                            
                            # 显示上下文
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if re.search(pattern, line, re.IGNORECASE):
                                    start = max(0, i-2)
                                    end = min(len(lines), i+3)
                                    context = '\n'.join(lines[start:end])
                                    print(f"   上下文:\n{context}")
                                    break
                            
                            found_issues = True
                            
                except Exception as e:
                    print(f"⚠️ 无法读取文件 {filepath}: {e}")
    
    if not found_issues:
        print("✅ 未在HTML文件中发现明显的广告代码")
    
    return found_issues

def check_js_files_for_ads():
    """检查JavaScript文件中的广告代码"""
    print("\n=== 检查JavaScript文件中的广告代码 ===")
    
    js_ad_patterns = [
        (r'\.getElementById\([^)]*ad', '通过ID获取广告元素'),
        (r'\.querySelector\([^)]*ad', '通过选择器获取广告元素'),
        (r'ad\.load', '广告加载代码'),
        (r'ad\.render', '广告渲染代码'),
        (r'taboola', 'Taboola相关'),
        (r'outbrain', 'Outbrain相关'),
    ]
    
    js_dir = "js"
    if not os.path.exists(js_dir):
        print("ℹ️ js目录不存在")
        return False
    
    found_issues = False
    
    for file in os.listdir(js_dir):
        if file.endswith('.js'):
            filepath = os.path.join(js_dir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, description in js_ad_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"\n⚠️ 发现可能的广告相关JS代码: {filepath}")
                        print(f"   类型: {description}")
                        print(f"   匹配模式: {pattern}")
                        found_issues = True
                        
            except Exception as e:
                print(f"⚠️ 无法读取文件 {filepath}: {e}")
    
    if not found_issues:
        print("✅ 未在JavaScript文件中发现明显的广告代码")
    
    return found_issues

def check_external_scripts():
    """检查外部脚本引用"""
    print("\n=== 检查外部脚本引用 ===")
    
    suspicious_domains = [
        'taboola.com',
        'outbrain.com',
        'googlesyndication.com',
        'doubleclick.net',
        'amazon-adsystem.com',
        'revcontent.com',
        'zemanta.com',
    ]
    
    site_dir = "_site"
    if not os.path.exists(site_dir):
        print("❌ _site目录不存在")
        return False
    
    found_issues = False
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 查找所有script标签
                    script_pattern = r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>'
                    scripts = re.findall(script_pattern, content, re.IGNORECASE)
                    
                    for script_src in scripts:
                        parsed = urlparse(script_src)
                        domain = parsed.netloc
                        
                        for suspicious in suspicious_domains:
                            if suspicious in domain:
                                print(f"\n❌ 发现可疑外部脚本: {filepath}")
                                print(f"   脚本地址: {script_src}")
                                print(f"   可疑域名: {suspicious}")
                                found_issues = True
                                break
                                
                except Exception as e:
                    print(f"⚠️ 无法读取文件 {filepath}: {e}")
    
    if not found_issues:
        print("✅ 未发现可疑的外部脚本引用")
    
    return found_issues

def check_third_party_trackers():
    """检查第三方追踪器"""
    print("\n=== 检查第三方追踪器 ===")
    
    tracker_patterns = [
        (r'google-analytics\.com', 'Google Analytics'),
        (r'baidu\.com/hm\.js', '百度统计'),
        (r'facebook\.com/tr', 'Facebook Pixel'),
        (r'linkedin\.com/analytics', 'LinkedIn Analytics'),
        (r'twitter\.com/analytics', 'Twitter Analytics'),
    ]
    
    site_dir = "_site"
    if not os.path.exists(site_dir):
        print("❌ _site目录不存在")
        return False
    
    found_trackers = False
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, description in tracker_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            print(f"\n📊 发现追踪器: {filepath}")
                            print(f"   类型: {description}")
                            found_trackers = True
                            
                except Exception as e:
                    print(f"⚠️ 无法读取文件 {filepath}: {e}")
    
    if not found_trackers:
        print("ℹ️ 未发现第三方追踪器")
    
    return found_trackers

def check_config_files():
    """检查配置文件"""
    print("\n=== 检查配置文件 ===")
    
    config_files = [
        "_config.yml",
        "Gemfile",
        "package.json",
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'taboola' in content.lower():
                    print(f"\n❌ 在配置文件中发现Taboola: {config_file}")
                    return True
                    
            except Exception as e:
                print(f"⚠️ 无法读取配置文件 {config_file}: {e}")
    
    print("✅ 配置文件中未发现Taboola相关配置")
    return False

def create_security_report():
    """创建安全报告"""
    print("\n" + "="*60)
    print("网站安全检查报告")
    print("="*60)
    
    issues_found = False
    
    # 运行各项检查
    issues_found |= check_html_files_for_ads()
    issues_found |= check_js_files_for_ads()
    issues_found |= check_external_scripts()
    issues_found |= check_third_party_trackers()
    issues_found |= check_config_files()
    
    print("\n" + "="*60)
    print("检查结果总结")
    print("="*60)
    
    if issues_found:
        print("❌ 发现问题！")
        print("\n建议立即采取以下措施：")
        print("1. 检查所有HTML文件，移除可疑的script标签")
        print("2. 检查JavaScript文件，移除广告相关代码")
        print("3. 检查外部资源引用，确保只使用可信来源")
        print("4. 考虑使用内容安全策略(CSP)")
        print("5. 定期运行此检查脚本")
    else:
        print("✅ 未发现明显的广告或安全问题")
        print("\n网站看起来是干净的，Taboola广告可能来自：")
        print("1. 浏览器扩展或插件")
        print("2. 网络运营商的广告注入")
        print("3. 路由器或防火墙的广告重定向")
        print("4. 本地网络的中间人攻击")
    
    print("\n" + "="*60)
    print("后续步骤")
    print("="*60)
    print("1. 在无痕/隐私模式下访问网站")
    print("2. 禁用所有浏览器扩展后访问")
    print("3. 使用不同的网络环境测试")
    print("4. 如果问题依然存在，可能是代码注入问题")
    
    return issues_found

def main():
    """主函数"""
    print("开始检查网站广告问题...")
    
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
        create_security_report()
        return True
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()