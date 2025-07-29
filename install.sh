#!/bin/bash
# Cambridge Isotope Scraper 快速安装脚本

set -e

echo "🚀 Cambridge Isotope Laboratories 多线程爬虫安装脚本"
echo "=================================================="

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python 版本检查通过: $python_version"
else
    echo "❌ 需要 Python 3.8 或更高版本，当前版本: $python_version"
    exit 1
fi

# 检查 Chrome 浏览器
echo "📋 检查 Chrome 浏览器..."
if command -v google-chrome >/dev/null 2>&1 || command -v chromium-browser >/dev/null 2>&1 || [ -d "/Applications/Google Chrome.app" ]; then
    echo "✅ Chrome 浏览器检查通过"
else
    echo "⚠️  警告: 未检测到 Chrome 浏览器，请确保已安装 Chrome"
fi

# 创建虚拟环境
echo "📦 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "ℹ️  虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 验证安装
echo "🧪 验证安装..."
python3 -c "import selenium, pandas, requests; print('✅ 核心依赖包安装成功')"

# 测试 ChromeDriver
echo "🧪 测试 ChromeDriver..."
python3 -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

try:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com')
    driver.quit()
    print('✅ ChromeDriver 测试成功')
except Exception as e:
    print(f'❌ ChromeDriver 测试失败: {e}')
"

echo ""
echo "🎉 安装完成！"
echo ""
echo "📖 使用方法:"
echo "   # 激活虚拟环境"
echo "   source venv/bin/activate"
echo ""
echo "   # 基本使用"
echo "   python optimized_multithreaded_scraper.py"
echo ""
echo "   # 查看帮助"
echo "   python optimized_multithreaded_scraper.py --help"
echo ""
echo "   # 性能测试"
echo "   python high_thread_test.py"
echo ""
echo "📚 更多信息请查看 README.md"
