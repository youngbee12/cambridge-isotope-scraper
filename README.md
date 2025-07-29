# Cambridge Isotope Laboratories 多线程爬虫

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange.svg)](https://selenium-python.readthedocs.io/)

一个高效的多线程爬虫工具，用于提取 Cambridge Isotope Laboratories (isotope.com) 的产品信息，包括 CAS 号、分子式、产品图片等详细数据。

## ✨ 功能特点

- 🚀 **多线程并发处理** - 支持 2-128 个线程（推荐 2-8 个）
- 🔍 **智能 404 检测** - 快速跳过不存在的页面，提高效率
- 📊 **完整数据提取** - CAS 号、分子式、同义词、产品图片等
- 💾 **多种输出格式** - CSV 和 Excel 格式
- ⚙️ **灵活配置** - 丰富的命令行参数支持
- 🛡️ **错误处理** - 自动重试和详细的错误日志
- 📈 **性能监控** - 内置性能测试和资源监控

## 🎯 提取的数据字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `name` | 产品名称 | D-Glucose (1-¹³C, 99%; 6-¹³C, 97%; 6,6-D₂, 97%) |
| `product_number` | 产品编号 | DLM-4895 |
| `cas_labeled` | 标记化合物 CAS 号 | 157171-80-7 |
| `cas_unlabeled` | 未标记化合物 CAS 号 | 50-99-7 |
| `formula` | 分子式 | C4*C2H10D2O6 |
| `molecular_weight` | 分子量 | 184.15 |
| `synonyms` | 同义词 | D-Glucopyranose; Dextrose; D-GLC |
| `image_url` | 产品图片 URL | https://isotope.com/product/image/... |
| `chemical_purity` | 化学纯度 | 98% |

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Chrome 浏览器
- 4GB+ 可用内存（推荐 8GB+）

### 2. 安装

```bash
# 克隆项目
git clone https://github.com/youngbee12/cambridge-isotope-scraper.git
cd cambridge-isotope-scraper

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 基本使用

```bash
# 使用默认设置（2 个线程，内置测试 URL）
python optimized_multithreaded_scraper.py

# 指定线程数
python optimized_multithreaded_scraper.py -t 4

# 使用 headless 模式（推荐用于批量处理）
python optimized_multithreaded_scraper.py -t 4 --headless

# 限制爬取数量
python optimized_multithreaded_scraper.py -t 4 -n 100
```

## 📖 详细使用说明

### 命令行参数

```bash
python optimized_multithreaded_scraper.py [选项]
```

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--threads` | `-t` | 线程数量 | 2 |
| `--max-products` | `-n` | 最大爬取产品数量 | 无限制 |
| `--headless` | | 使用 headless 模式 | False |
| `--urls-file` | `-u` | URL 列表文件路径 | 内置测试 URL |
| `--output-prefix` | `-o` | 输出文件前缀 | optimized_products |
| `--verbose` | `-v` | 详细输出模式 | False |

### 使用示例

```bash
# 高效批量处理
python optimized_multithreaded_scraper.py -t 4 --headless -n 1000 -o batch1

# 从文件读取 URL 列表
python optimized_multithreaded_scraper.py -u product_urls.json -t 3

# 调试模式
python optimized_multithreaded_scraper.py -t 1 -v -n 10

# 性能测试
python high_thread_test.py
```

### URL 文件格式

支持 JSON 和文本格式：

**JSON 格式（推荐）：**
```json
[
  "https://isotope.com/product1",
  "https://isotope.com/product2"
]
```

**文本格式：**
```
https://isotope.com/product1
https://isotope.com/product2
```

## 📊 性能建议

### 推荐配置

| 使用场景 | 线程数 | 其他建议 |
|----------|--------|----------|
| 日常测试 | 2-4 | 非 headless 模式便于观察 |
| 批量处理 | 4-8 | headless 模式，分批处理 |
| 大规模爬取 | 8-16 | 监控系统资源，使用代理 |

### 系统资源需求

- **内存**: 每线程约 200MB
- **CPU**: 建议多核处理器
- **网络**: 稳定的网络连接

## ⚠️ 注意事项

1. **遵守网站条款**: 请遵守 isotope.com 的使用条款和 robots.txt
2. **合理使用**: 避免过于频繁的请求，建议使用 2-8 个线程
3. **IP 保护**: 大量爬取时考虑使用代理轮换
4. **数据用途**: 仅用于学术研究和合法用途

## 🔧 故障排除

### 常见问题

1. **ChromeDriver 错误**
   ```bash
   # 手动更新 ChromeDriver
   pip install --upgrade webdriver-manager
   ```

2. **内存不足**
   ```bash
   # 减少线程数
   python optimized_multithreaded_scraper.py -t 2
   ```

3. **网络错误**
   ```bash
   # 使用更少线程和详细模式
   python optimized_multithreaded_scraper.py -t 1 -v
   ```

### 调试技巧

- 使用 `-v` 参数查看详细日志
- 使用 `-t 1` 单线程模式便于调试
- 检查生成的 `failed_urls_*.txt` 文件

## 📁 项目结构

```
cambridge-isotope-scraper/
├── optimized_multithreaded_scraper.py  # 主爬虫程序
├── high_thread_test.py                 # 性能测试工具
├── requirements.txt                    # 依赖包列表
├── README.md                          # 项目说明
├── LICENSE                            # 开源协议
├── .gitignore                         # Git 忽略文件
└── examples/                          # 示例文件
    ├── sample_urls.json               # 示例 URL 文件
    └── sample_output.csv              # 示例输出文件
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Selenium](https://selenium-python.readthedocs.io/) - Web 自动化框架
- [pandas](https://pandas.pydata.org/) - 数据处理库
- [Cambridge Isotope Laboratories](https://isotope.com/) - 数据来源

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/youngbee12/cambridge-isotope-scraper/issues)
- 发送邮件至：yangzhicheng@simm.ac.cn

---

⭐ 如果这个项目对您有帮助，请给个 Star！
