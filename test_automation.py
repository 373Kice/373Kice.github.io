#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化系统测试脚本
用于测试和验证A股分析网站自动化系统的各个组件
"""

import os
import sys
import subprocess
import datetime
import json
from pathlib import Path

class AutomationTester:
    """自动化系统测试类"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.test_results = []
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def log_result(self, test_name, status, message):
        """记录测试结果"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
        return result
    
    def check_file_exists(self, filename):
        """检查文件是否存在"""
        test_name = f"检查文件 {filename}"
        file_path = self.project_path / filename
        
        if file_path.exists():
            return self.log_result(test_name, "PASS", f"文件存在: {file_path}")
        else:
            return self.log_result(test_name, "FAIL", f"文件不存在: {file_path}")
    
    def check_python_env(self):
        """检查Python环境"""
        test_name = "检查Python环境"
        
        try:
            # 检查Python版本
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            if result.returncode == 0:
                python_version = result.stdout.strip()
                return self.log_result(test_name, "PASS", f"Python可用: {python_version}")
            else:
                return self.log_result(test_name, "FAIL", "Python不可用")
                
        except Exception as e:
            return self.log_result(test_name, "FAIL", f"Python检查失败: {e}")
    
    def check_ruby_env(self):
        """检查Ruby环境"""
        test_name = "检查Ruby环境"
        
        try:
            # 检查Ruby版本
            result = subprocess.run(
                ["ruby", "--version"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            if result.returncode == 0:
                ruby_version = result.stdout.strip().split()[1]
                return self.log_result(test_name, "PASS", f"Ruby可用: {ruby_version}")
            else:
                return self.log_result(test_name, "WARN", "Ruby不可用（如果没有Jekyll需求可忽略）")
                
        except Exception as e:
            return self.log_result(test_name, "WARN", f"Ruby检查失败: {e}")
    
    def check_bundler(self):
        """检查Bundler"""
        test_name = "检查Bundler"
        
        try:
            # 检查Bundler版本
            result = subprocess.run(
                ["bundle", "--version"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            if result.returncode == 0:
                bundler_version = result.stdout.strip()
                return self.log_result(test_name, "PASS", f"Bundler可用: {bundler_version}")
            else:
                return self.log_result(test_name, "WARN", "Bundler不可用")
                
        except Exception as e:
            return self.log_result(test_name, "WARN", f"Bundler检查失败: {e}")
    
    def test_daily_report_script(self):
        """测试每日报告生成脚本"""
        test_name = "测试报告生成脚本"
        
        try:
            # 运行报告生成脚本
            result = subprocess.run(
                ["python", "daily_a_stock_analysis.py"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            if result.returncode == 0:
                # 检查是否生成了新文件
                expected_file = self.project_path / "_posts" / f"{self.today}-A股大盘分析报告.md"
                if expected_file.exists():
                    return self.log_result(test_name, "PASS", "报告生成成功，已创建新文章")
                else:
                    return self.log_result(test_name, "FAIL", "脚本运行成功但未生成文件")
            else:
                return self.log_result(test_name, "FAIL", f"脚本运行失败: {result.stderr}")
                
        except Exception as e:
            return self.log_result(test_name, "FAIL", f"脚本测试失败: {e}")
    
    def check_jekyll_config(self):
        """检查Jekyll配置"""
        test_name = "检查Jekyll配置"
        
        config_file = self.project_path / "_config.yml"
        if not config_file.exists():
            return self.log_result(test_name, "FAIL", "Jekyll配置文件不存在")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查基本配置项
            required_keys = ["title", "description", "url"]
            missing_keys = []
            
            for key in required_keys:
                if f"{key}:" not in content:
                    missing_keys.append(key)
            
            if missing_keys:
                return self.log_result(test_name, "WARN", f"缺少配置项: {', '.join(missing_keys)}")
            else:
                return self.log_result(test_name, "PASS", "Jekyll配置基本完整")
                
        except Exception as e:
            return self.log_result(test_name, "FAIL", f"配置文件读取失败: {e}")
    
    def test_powershell_scripts(self):
        """测试PowerShell脚本"""
        test_name = "测试PowerShell脚本"
        
        ps_scripts = ["run_jekyll_service.ps1", "create_daily_report_task.ps1", "setup_automation.ps1"]
        results = []
        
        for script in ps_scripts:
            script_path = self.project_path / script
            if script_path.exists():
                results.append(f"{script}: 存在")
            else:
                results.append(f"{script}: 不存在")
        
        if all("存在" in r for r in results):
            return self.log_result(test_name, "PASS", "所有PowerShell脚本都存在")
        else:
            return self.log_result(test_name, "WARN", f"部分脚本缺失: {results}")
    
    def generate_summary_report(self):
        """生成测试总结报告"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "FAIL")
        warning_tests = sum(1 for r in self.test_results if r["status"] == "WARN")
        
        print("\n" + "="*60)
        print("📊 自动化系统测试总结报告")
        print("="*60)
        print(f"测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"项目路径: {self.project_path}")
        print(f"测试总数: {total_tests}")
        print(f"✅ 通过: {passed_tests}")
        print(f"❌ 失败: {failed_tests}")
        print(f"⚠️ 警告: {warning_tests}")
        
        if failed_tests == 0:
            print("\n🎉 恭喜！所有关键测试已通过！")
            print("系统已准备好进行自动化运行。")
        else:
            print("\n⚠️ 注意：有失败的测试需要修复。")
        
        # 保存详细报告
        report_file = self.project_path / f"automation_test_report_{self.today}.json"
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": warning_tests,
                "test_date": self.today
            },
            "detailed_results": self.test_results
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n📄 详细报告已保存: {report_file}")
            
        except Exception as e:
            print(f"\n⚠️ 报告保存失败: {e}")
        
        return report_data
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🔍 开始自动化系统测试...")
        print(f"项目目录: {self.project_path}")
        print(f"测试日期: {self.today}")
        print("-"*60)
        
        # 运行所有测试
        self.check_python_env()
        self.check_ruby_env()
        self.check_bundler()
        
        self.check_file_exists("daily_a_stock_analysis.py")
        self.check_file_exists("run_jekyll_service.ps1")
        self.check_file_exists("create_daily_report_task.ps1")
        self.check_file_exists("setup_automation.ps1")
        self.check_file_exists("_config.yml")
        self.check_file_exists("Gemfile")
        self.check_file_exists("README_AUTOMATION.md")
        
        self.test_daily_report_script()
        self.check_jekyll_config()
        self.test_powershell_scripts()
        
        # 生成总结报告
        return self.generate_summary_report()


def main():
    """主函数"""
    # 获取项目路径（当前目录）
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试器
    tester = AutomationTester(project_path)
    
    # 运行所有测试
    report = tester.run_all_tests()
    
    # 根据测试结果提供建议
    print("\n📋 下一步建议:")
    
    failed_tests = sum(1 for r in tester.test_results if r["status"] == "FAIL")
    warning_tests = sum(1 for r in tester.test_results if r["status"] == "WARN")
    
    if failed_tests == 0:
        print("1. ✅ 所有关键测试通过，可以开始使用自动化系统")
        print("2. 🔧 运行 ./setup_automation.ps1 进行一键安装")
        print("3. 🌐 访问 http://127.0.0.1:4001/ 查看网站")
    else:
        print("1. ⚠️ 请先修复失败的测试项目")
        print("2. 📖 查看 README_AUTOMATION.md 获取帮助")
        print("3. 🔧 运行失败的测试项查看详细错误信息")
    
    if warning_tests > 0:
        print("4. ⚠️ 注意：有警告信息，可能影响部分功能")
    
    print("\n🚀 快速启动命令:")
    print("  python daily_a_stock_analysis.py    # 生成今日报告")
    print("  ./setup_automation.ps1             # 一键安装")
    print("  ./run_jekyll_service.ps1          # 启动网站服务")


if __name__ == "__main__":
    main()