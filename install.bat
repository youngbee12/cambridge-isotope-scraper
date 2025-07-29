@echo off
REM Cambridge Isotope Scraper Windows 安装脚本

echo 🚀 Cambridge Isotope Laboratories 多线程爬虫安装脚本
echo ==================================================

REM 检查 Python
echo 📋 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ❌ 需要 Python 3.8 或更高版本
    python --version
    pause
    exit /b 1
)

echo ✅ Python 版本检查通过
python --version

REM 创建虚拟环境
echo 📦 创建虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo ✅ 虚拟环境创建成功
) else (
    echo ℹ️  虚拟环境已存在
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级 pip
echo ⬆️  升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 📥 安装依赖包...
pip install -r requirements.txt

REM 验证安装
echo 🧪 验证安装...
python -c "import selenium, pandas, requests; print('✅ 核心依赖包安装成功')"

REM 测试 ChromeDriver
echo 🧪 测试 ChromeDriver...
python -c "from selenium import webdriver; from selenium.webdriver.chrome.options import Options; from webdriver_manager.chrome import ChromeDriverManager; from selenium.webdriver.chrome.service import Service; options = Options(); options.add_argument('--headless'); options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage'); service = Service(ChromeDriverManager().install()); driver = webdriver.Chrome(service=service, options=options); driver.get('https://www.google.com'); driver.quit(); print('✅ ChromeDriver 测试成功')"

echo.
echo 🎉 安装完成！
echo.
echo 📖 使用方法:
echo    # 激活虚拟环境
echo    venv\Scripts\activate.bat
echo.
echo    # 基本使用
echo    python optimized_multithreaded_scraper.py
echo.
echo    # 查看帮助
echo    python optimized_multithreaded_scraper.py --help
echo.
echo    # 性能测试
echo    python high_thread_test.py
echo.
echo 📚 更多信息请查看 README.md

pause
