# Docker 部署指南

本项目支持 Docker 容器化部署，提供完全隔离的运行环境。

## 🐳 快速开始

### 1. 构建镜像

```bash
# 构建 Docker 镜像
docker build -t cambridge-isotope-scraper .

# 或使用 Docker Compose
docker-compose build
```

### 2. 运行容器

```bash
# 查看帮助信息
docker run --rm cambridge-isotope-scraper

# 运行基本爬取任务
docker run --rm -v $(pwd)/output:/app/output cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py -t 2 --headless -n 10 -o /app/output/test

# 使用 Docker Compose
docker-compose up isotope-scraper
```

## 📁 目录挂载

### 输出目录
```bash
# 创建输出目录
mkdir -p output

# 运行并保存结果到本地
docker run --rm -v $(pwd)/output:/app/output cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py -t 4 --headless -o /app/output/results
```

### URL 文件
```bash
# 创建 URL 目录并放入文件
mkdir -p urls
cp your_urls.json urls/

# 使用自定义 URL 文件
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/urls:/app/urls \
  cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py -u /app/urls/your_urls.json -o /app/output/results
```

## 🚀 常用命令

### 基本爬取
```bash
docker run --rm -v $(pwd)/output:/app/output cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py \
  --threads 4 \
  --headless \
  --max-products 100 \
  --output-prefix /app/output/batch1
```

### 性能测试
```bash
# 运行性能测试
docker-compose --profile testing up performance-test

# 或直接运行
docker run --rm -v $(pwd)/output:/app/output cambridge-isotope-scraper \
  python high_thread_test.py
```

### 交互式调试
```bash
# 进入容器进行调试
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  cambridge-isotope-scraper \
  /bin/bash
```

## 🔧 环境变量

可以通过环境变量配置容器行为：

```bash
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -e DISPLAY=:99 \
  -v $(pwd)/output:/app/output \
  cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py
```

## 📊 Docker Compose 配置

### 基本使用
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  isotope-scraper:
    command: ["python", "optimized_multithreaded_scraper.py", "-t", "4", "--headless", "-n", "100"]
    volumes:
      - ./my_urls:/app/urls
      - ./my_output:/app/output
```

### 批量处理
```bash
# 创建自定义配置
cat > docker-compose.override.yml << EOF
version: '3.8'
services:
  isotope-scraper:
    command: [
      "python", "optimized_multithreaded_scraper.py",
      "--threads", "6",
      "--headless",
      "--urls-file", "/app/urls/product_urls.json",
      "--output-prefix", "/app/output/full_catalog",
      "--max-products", "1000"
    ]
EOF

# 运行批量处理
docker-compose up
```

## 🛠️ 故障排除

### Chrome 相关问题
```bash
# 如果遇到 Chrome 启动问题，尝试添加更多参数
docker run --rm \
  --shm-size=2g \
  -v $(pwd)/output:/app/output \
  cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py --headless
```

### 权限问题
```bash
# 确保输出目录有正确的权限
sudo chown -R $USER:$USER output/
chmod 755 output/
```

### 内存限制
```bash
# 限制容器内存使用
docker run --rm \
  --memory=4g \
  --memory-swap=4g \
  -v $(pwd)/output:/app/output \
  cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py -t 2
```

## 📈 性能优化

### 多容器并行
```yaml
# docker-compose.parallel.yml
version: '3.8'
services:
  scraper-1:
    build: .
    command: ["python", "optimized_multithreaded_scraper.py", "-u", "/app/urls/batch1.json", "-o", "/app/output/batch1"]
    volumes:
      - ./output:/app/output
      - ./urls:/app/urls

  scraper-2:
    build: .
    command: ["python", "optimized_multithreaded_scraper.py", "-u", "/app/urls/batch2.json", "-o", "/app/output/batch2"]
    volumes:
      - ./output:/app/output
      - ./urls:/app/urls
```

```bash
# 运行多个并行容器
docker-compose -f docker-compose.parallel.yml up
```

## 🔒 安全考虑

1. **网络隔离**: 容器默认在隔离网络中运行
2. **非 root 用户**: 容器内使用非特权用户运行
3. **只读挂载**: 可以将某些目录设为只读

```bash
# 只读挂载 URL 文件
docker run --rm \
  -v $(pwd)/urls:/app/urls:ro \
  -v $(pwd)/output:/app/output \
  cambridge-isotope-scraper
```

## 📦 镜像管理

### 构建优化镜像
```bash
# 多阶段构建（如果需要）
docker build --target production -t cambridge-isotope-scraper:prod .

# 压缩镜像
docker build --squash -t cambridge-isotope-scraper:compressed .
```

### 推送到仓库
```bash
# 标记镜像
docker tag cambridge-isotope-scraper your-registry/cambridge-isotope-scraper:v1.0.0

# 推送镜像
docker push your-registry/cambridge-isotope-scraper:v1.0.0
```

---

更多信息请参考主 [README.md](README.md) 文件。
