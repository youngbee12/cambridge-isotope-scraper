#!/bin/bash
# Cambridge Isotope Scraper 项目打包脚本

set -e

VERSION="v1.0.0"
PROJECT_NAME="cambridge-isotope-scraper"
PACKAGE_NAME="${PROJECT_NAME}-${VERSION}"

echo "📦 Cambridge Isotope Scraper 项目打包工具"
echo "============================================"
echo "版本: $VERSION"
echo "项目: $PROJECT_NAME"
echo ""

# 创建打包目录
echo "📁 创建打包目录..."
rm -rf dist/
mkdir -p dist/

# 核心文件列表
CORE_FILES=(
    "README.md"
    "LICENSE"
    "requirements.txt"
    "setup.py"
    "optimized_multithreaded_scraper.py"
    "high_thread_test.py"
)

# 部署文件
DEPLOY_FILES=(
    "install.sh"
    "install.bat"
    "deploy.sh"
    "Dockerfile"
    "docker-compose.yml"
    "DOCKER.md"
)

# 文档文件
DOC_FILES=(
    "RELEASE_NOTES.md"
    ".gitignore"
)

# 示例文件
EXAMPLE_DIR="examples"

# 创建完整包
echo "📦 创建完整包..."
FULL_PACKAGE_DIR="dist/${PACKAGE_NAME}-full"
mkdir -p "$FULL_PACKAGE_DIR"

# 复制核心文件
echo "📋 复制核心文件..."
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$FULL_PACKAGE_DIR/"
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (未找到)"
    fi
done

# 复制部署文件
echo "🚀 复制部署文件..."
for file in "${DEPLOY_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$FULL_PACKAGE_DIR/"
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (未找到)"
    fi
done

# 复制文档文件
echo "📚 复制文档文件..."
for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$FULL_PACKAGE_DIR/"
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (未找到)"
    fi
done

# 复制示例目录
echo "📝 复制示例文件..."
if [ -d "$EXAMPLE_DIR" ]; then
    cp -r "$EXAMPLE_DIR" "$FULL_PACKAGE_DIR/"
    echo "  ✅ $EXAMPLE_DIR/"
else
    echo "  ⚠️  $EXAMPLE_DIR/ (未找到)"
fi

# 创建精简包（仅核心功能）
echo "📦 创建精简包..."
LITE_PACKAGE_DIR="dist/${PACKAGE_NAME}-lite"
mkdir -p "$LITE_PACKAGE_DIR"

# 复制核心文件到精简包
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$LITE_PACKAGE_DIR/"
    fi
done

# 复制基本安装脚本
cp "install.sh" "$LITE_PACKAGE_DIR/" 2>/dev/null || true
cp "install.bat" "$LITE_PACKAGE_DIR/" 2>/dev/null || true

# 创建 Docker 包
echo "🐳 创建 Docker 包..."
DOCKER_PACKAGE_DIR="dist/${PACKAGE_NAME}-docker"
mkdir -p "$DOCKER_PACKAGE_DIR"

# Docker 相关文件
DOCKER_SPECIFIC_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    "DOCKER.md"
    "requirements.txt"
    "optimized_multithreaded_scraper.py"
    "high_thread_test.py"
    "README.md"
    "LICENSE"
)

for file in "${DOCKER_SPECIFIC_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$DOCKER_PACKAGE_DIR/"
    fi
done

# 复制示例文件到 Docker 包
if [ -d "$EXAMPLE_DIR" ]; then
    cp -r "$EXAMPLE_DIR" "$DOCKER_PACKAGE_DIR/"
fi

# 创建压缩包
echo "🗜️  创建压缩包..."

# 完整包
cd dist/
tar -czf "${PACKAGE_NAME}-full.tar.gz" "${PACKAGE_NAME}-full/"
zip -r "${PACKAGE_NAME}-full.zip" "${PACKAGE_NAME}-full/" > /dev/null

# 精简包
tar -czf "${PACKAGE_NAME}-lite.tar.gz" "${PACKAGE_NAME}-lite/"
zip -r "${PACKAGE_NAME}-lite.zip" "${PACKAGE_NAME}-lite/" > /dev/null

# Docker 包
tar -czf "${PACKAGE_NAME}-docker.tar.gz" "${PACKAGE_NAME}-docker/"
zip -r "${PACKAGE_NAME}-docker.zip" "${PACKAGE_NAME}-docker/" > /dev/null

cd ..

# 生成校验和
echo "🔐 生成校验和..."
cd dist/
if command -v sha256sum >/dev/null 2>&1; then
    sha256sum *.tar.gz *.zip > checksums.sha256
elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 *.tar.gz *.zip > checksums.sha256
else
    echo "⚠️  未找到校验和工具，跳过校验和生成"
fi
cd ..

# 创建发布信息
echo "📋 创建发布信息..."
cat > dist/RELEASE_INFO.txt << EOF
Cambridge Isotope Laboratories 多线程爬虫 ${VERSION}
================================================

发布日期: $(date '+%Y-%m-%d %H:%M:%S')
Git 提交: $(git rev-parse HEAD)
Git 标签: $(git describe --tags --exact-match 2>/dev/null || echo "无标签")

📦 包含的文件包:

1. ${PACKAGE_NAME}-full.tar.gz / .zip
   - 完整功能包，包含所有文件和文档
   - 适合: 完整部署和开发

2. ${PACKAGE_NAME}-lite.tar.gz / .zip
   - 精简包，仅包含核心功能
   - 适合: 快速部署和生产环境

3. ${PACKAGE_NAME}-docker.tar.gz / .zip
   - Docker 容器化包
   - 适合: 容器化部署

🚀 快速开始:

1. 下载适合的包
2. 解压到目标目录
3. 运行安装脚本:
   - Linux/macOS: ./install.sh
   - Windows: install.bat
   - Docker: docker build -t cambridge-isotope-scraper .

📚 文档:
- README.md - 详细使用说明
- DOCKER.md - Docker 部署指南
- RELEASE_NOTES.md - 发布说明

🔐 校验和:
见 checksums.sha256 文件

EOF

# 显示结果
echo ""
echo "🎉 打包完成！"
echo ""
echo "📁 生成的文件:"
ls -la dist/
echo ""
echo "📊 文件大小:"
du -h dist/*.tar.gz dist/*.zip
echo ""
echo "🔐 校验和文件: dist/checksums.sha256"
echo "📋 发布信息: dist/RELEASE_INFO.txt"
echo ""
echo "🚀 下一步:"
echo "   1. 测试打包的文件"
echo "   2. 上传到 GitHub Releases"
echo "   3. 更新文档链接"
