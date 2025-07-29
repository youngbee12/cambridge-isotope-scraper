# 📋 Release Notes

## 🎉 v1.0.0 - Initial Release (2025-07-29)

### ✨ 新功能

#### 🚀 核心爬虫功能
- **多线程并发处理**: 支持 2-128 个线程（推荐 2-8 个）
- **智能 404 检测**: 快速跳过不存在的页面，提高效率
- **完整数据提取**: 
  - 产品名称和编号
  - CAS 号（标记/未标记）
  - 分子式和分子量
  - 化学纯度和同位素富集度
  - 产品图片 URL
  - 同义词和描述

#### 🔧 配置和使用
- **丰富的命令行参数**: 线程数、输出格式、文件路径等
- **多种输入格式**: 支持 JSON 和文本格式的 URL 列表
- **多种输出格式**: CSV 和 Excel 格式
- **详细的日志记录**: 支持详细模式和调试信息

#### 📊 性能和监控
- **性能测试工具**: `high_thread_test.py` 用于测试不同线程配置
- **资源监控**: 实时监控 CPU 和内存使用情况
- **错误处理**: 自动重试和详细的错误日志

#### 🐳 容器化支持
- **Docker 支持**: 完整的 Dockerfile 和 docker-compose.yml
- **跨平台部署**: 支持 Linux、macOS、Windows
- **一键部署**: 自动化安装和部署脚本

### 📦 包含文件

#### 核心程序
- `optimized_multithreaded_scraper.py` - 主爬虫程序
- `high_thread_test.py` - 性能测试工具

#### 配置和文档
- `README.md` - 详细使用说明
- `DOCKER.md` - Docker 部署指南
- `requirements.txt` - Python 依赖包
- `setup.py` - 安装配置

#### 部署工具
- `install.sh` - Linux/macOS 安装脚本
- `install.bat` - Windows 安装脚本
- `deploy.sh` - 一键部署脚本
- `Dockerfile` - Docker 镜像配置
- `docker-compose.yml` - Docker 编排配置

#### 示例文件
- `examples/sample_urls.json` - 示例 URL 文件（JSON 格式）
- `examples/sample_urls.txt` - 示例 URL 文件（文本格式）
- `examples/sample_output.csv` - 示例输出文件

### 🎯 使用场景

#### 🔬 科研用途
- 化学品信息收集
- 同位素标记化合物研究
- 分子式和 CAS 号数据库构建

#### 📊 数据分析
- 产品价格和可用性分析
- 市场研究和竞品分析
- 化学品供应链分析

#### 🏭 工业应用
- 采购信息收集
- 供应商数据整理
- 产品目录管理

### 🚀 快速开始

#### 本地安装
```bash
# 克隆项目
git clone https://github.com/youngbee12/cambridge-isotope-scraper.git
cd cambridge-isotope-scraper

# 一键安装
./install.sh  # Linux/macOS
# 或
install.bat   # Windows

# 开始使用
python optimized_multithreaded_scraper.py -t 4 --headless
```

#### Docker 部署
```bash
# 构建并运行
docker build -t cambridge-isotope-scraper .
docker run --rm -v $(pwd)/output:/app/output cambridge-isotope-scraper \
  python optimized_multithreaded_scraper.py -t 4 --headless

# 或使用 Docker Compose
docker-compose up
```

### 📈 性能基准

基于测试环境（8核 CPU，8GB RAM）的性能数据：

| 线程数 | 处理速度 | 内存使用 | 推荐场景 |
|--------|----------|----------|----------|
| 2 | 0.04 产品/秒 | +0.3GB | 日常使用 |
| 4 | 0.07 产品/秒 | +0.3GB | 推荐配置 |
| 8 | 0.10 产品/秒 | +0.6GB | 高性能 |
| 16+ | 边际提升 | +1.2GB+ | 不推荐 |

### ⚠️ 注意事项

1. **合规使用**: 请遵守网站使用条款和 robots.txt
2. **合理频率**: 建议使用 2-8 个线程，避免过于频繁的请求
3. **IP 保护**: 大量爬取时考虑使用代理轮换
4. **数据用途**: 仅用于学术研究和合法用途

### 🐛 已知问题

1. **高线程数限制**: 超过 16 个线程可能导致系统资源不足
2. **网络依赖**: 需要稳定的网络连接
3. **Chrome 依赖**: 需要安装 Chrome 浏览器

### 🔮 未来计划

#### v1.1.0 计划功能
- [ ] 代理轮换支持
- [ ] 断点续传功能
- [ ] 数据去重和验证
- [ ] Web UI 界面
- [ ] API 接口支持

#### v1.2.0 计划功能
- [ ] 分布式爬取支持
- [ ] 数据库存储选项
- [ ] 实时监控面板
- [ ] 自动化调度

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 开启 Pull Request

### 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

### 🙏 致谢

感谢以下开源项目的支持：
- [Selenium](https://selenium-python.readthedocs.io/)
- [pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/)

---

**下载地址**: [GitHub Releases](https://github.com/yourusername/cambridge-isotope-scraper/releases)

**技术支持**: [GitHub Issues](https://github.com/yourusername/cambridge-isotope-scraper/issues)
