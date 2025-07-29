# Cambridge Isotope Laboratories 多线程爬虫 Docker 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY optimized_multithreaded_scraper.py .
COPY high_thread_test.py .
COPY examples/ ./examples/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建非 root 用户
RUN useradd -m -u 1000 scraper && chown -R scraper:scraper /app
USER scraper

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# 暴露端口（如果需要）
# EXPOSE 8080

# 默认命令
CMD ["python", "optimized_multithreaded_scraper.py", "--help"]
