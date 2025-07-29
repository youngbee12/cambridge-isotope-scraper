#!/usr/bin/env python3
"""
高线程数测试脚本
测试不同线程数的性能和稳定性
"""

import subprocess
import time
import psutil
import os
from datetime import datetime

def monitor_system_resources():
    """监控系统资源使用情况"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return {
        'cpu_percent': cpu_percent,
        'memory_used_gb': memory.used / (1024**3),
        'memory_percent': memory.percent,
        'available_memory_gb': memory.available / (1024**3)
    }

def test_thread_performance():
    """测试不同线程数的性能"""
    
    # 测试的线程数配置
    thread_configs = [
        {'threads': 2, 'products': 5, 'description': '基准测试 (推荐)'},
        {'threads': 4, 'products': 5, 'description': '中等负载'},
        {'threads': 8, 'products': 5, 'description': '高负载'},
        {'threads': 16, 'products': 5, 'description': '极高负载 (不推荐)'},
        # {'threads': 32, 'products': 5, 'description': '危险级别'},
        # {'threads': 64, 'products': 5, 'description': '系统极限'},
        # {'threads': 128, 'products': 5, 'description': '可能崩溃'},
    ]
    
    results = []
    
    print("=== Cambridge Isotope Laboratories 高线程数性能测试 ===\n")
    
    # 显示系统信息
    print("系统信息:")
    print(f"  CPU核心数: {psutil.cpu_count()}")
    print(f"  总内存: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print(f"  可用内存: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    print()
    
    for config in thread_configs:
        threads = config['threads']
        products = config['products']
        description = config['description']
        
        print(f"🧪 测试配置: {threads} 线程 - {description}")
        print(f"   处理产品数: {products}")
        
        # 测试前的系统状态
        before_resources = monitor_system_resources()
        print(f"   测试前 - CPU: {before_resources['cpu_percent']:.1f}%, 内存: {before_resources['memory_used_gb']:.1f}GB ({before_resources['memory_percent']:.1f}%)")
        
        # 检查是否有足够的内存
        estimated_memory_need = threads * 0.2  # 每个线程大约需要200MB
        if estimated_memory_need > before_resources['available_memory_gb']:
            print(f"   ⚠️  警告: 预计需要 {estimated_memory_need:.1f}GB 内存，但只有 {before_resources['available_memory_gb']:.1f}GB 可用")
            print(f"   ❌ 跳过此测试以避免系统崩溃\n")
            continue
        
        start_time = time.time()
        
        try:
            # 运行爬虫
            cmd = [
                'python', 'optimized_multithreaded_scraper.py',
                '-t', str(threads),
                '--headless',
                '-n', str(products),
                '-o', f'test_{threads}threads'
            ]
            
            print(f"   🚀 开始测试...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5分钟超时
            
            end_time = time.time()
            duration = end_time - start_time
            
            # 测试后的系统状态
            after_resources = monitor_system_resources()
            
            # 分析结果
            if result.returncode == 0:
                status = "✅ 成功"
                # 尝试解析输出中的统计信息
                output_lines = result.stdout.split('\n')
                success_count = 0
                for line in output_lines:
                    if '成功获取:' in line:
                        try:
                            success_count = int(line.split('成功获取:')[1].split()[0])
                        except:
                            pass
            else:
                status = "❌ 失败"
                success_count = 0
            
            test_result = {
                'threads': threads,
                'products': products,
                'duration': duration,
                'status': status,
                'success_count': success_count,
                'cpu_before': before_resources['cpu_percent'],
                'cpu_after': after_resources['cpu_percent'],
                'memory_before': before_resources['memory_used_gb'],
                'memory_after': after_resources['memory_used_gb'],
                'memory_peak': after_resources['memory_used_gb'] - before_resources['memory_used_gb']
            }
            
            results.append(test_result)
            
            print(f"   {status}")
            print(f"   耗时: {duration:.1f}秒")
            print(f"   成功产品: {success_count}/{products}")
            print(f"   内存使用: +{test_result['memory_peak']:.1f}GB")
            print(f"   CPU峰值: {after_resources['cpu_percent']:.1f}%")
            
            if result.returncode != 0:
                print(f"   错误信息: {result.stderr[:200]}...")
            
        except subprocess.TimeoutExpired:
            print(f"   ⏰ 测试超时 (5分钟)")
            test_result = {
                'threads': threads,
                'products': products,
                'duration': 300,
                'status': "⏰ 超时",
                'success_count': 0,
                'memory_peak': 'N/A'
            }
            results.append(test_result)
        
        except Exception as e:
            print(f"   💥 测试异常: {e}")
            test_result = {
                'threads': threads,
                'products': products,
                'duration': 0,
                'status': f"💥 异常: {e}",
                'success_count': 0,
                'memory_peak': 'N/A'
            }
            results.append(test_result)
        
        print()
        time.sleep(5)  # 让系统恢复
    
    # 生成测试报告
    print("=== 测试报告 ===")
    print(f"{'线程数':<8} {'状态':<12} {'耗时(秒)':<10} {'成功率':<8} {'内存增量':<10} {'效率':<10}")
    print("-" * 70)
    
    for result in results:
        if result['duration'] > 0 and result['success_count'] > 0:
            efficiency = result['success_count'] / result['duration']
        else:
            efficiency = 0
        
        success_rate = f"{result['success_count']}/{result['products']}" if result['success_count'] > 0 else "0"
        memory_info = f"{result['memory_peak']:.1f}GB" if isinstance(result['memory_peak'], float) else "N/A"
        
        print(f"{result['threads']:<8} {result['status']:<12} {result['duration']:<10.1f} {success_rate:<8} {memory_info:<10} {efficiency:<10.2f}")
    
    # 推荐配置
    print("\n=== 推荐配置 ===")
    successful_results = [r for r in results if '成功' in r['status'] and r['success_count'] > 0]
    
    if successful_results:
        # 找到效率最高的配置
        best_efficiency = max(successful_results, key=lambda x: x['success_count'] / x['duration'])
        print(f"🏆 最高效率: {best_efficiency['threads']} 线程 ({best_efficiency['success_count'] / best_efficiency['duration']:.2f} 产品/秒)")
        
        # 找到最稳定的配置
        stable_configs = [r for r in successful_results if r['memory_peak'] < 2.0]  # 内存增量小于2GB
        if stable_configs:
            best_stable = max(stable_configs, key=lambda x: x['threads'])
            print(f"🛡️  最稳定配置: {best_stable['threads']} 线程 (内存增量: {best_stable['memory_peak']:.1f}GB)")
    
    print(f"\n💡 建议:")
    print(f"   - 日常使用: 2-4 线程")
    print(f"   - 批量处理: 4-8 线程")
    print(f"   - 极限测试: 不超过 16 线程")
    print(f"   - 避免使用: 超过 32 线程")

if __name__ == "__main__":
    test_thread_performance()
