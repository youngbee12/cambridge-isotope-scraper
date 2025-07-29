#!/bin/bash
# Cambridge Isotope Scraper 一键部署脚本

set -e

echo "🚀 Cambridge Isotope Laboratories 多线程爬虫一键部署"
echo "=================================================="

# 检查参数
DEPLOY_TYPE=${1:-"local"}
GITHUB_REPO=${2:-""}

echo "📋 部署类型: $DEPLOY_TYPE"

case $DEPLOY_TYPE in
    "local")
        echo "🏠 本地部署模式"
        
        # 检查 Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ 未找到 Python3，请先安装"
            exit 1
        fi
        
        # 运行安装脚本
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            echo "🪟 检测到 Windows 系统"
            cmd //c install.bat
        else
            echo "🐧 检测到 Unix 系统"
            chmod +x install.sh
            ./install.sh
        fi
        
        echo "✅ 本地部署完成！"
        ;;
        
    "docker")
        echo "🐳 Docker 部署模式"
        
        # 检查 Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ 未找到 Docker，请先安装 Docker"
            exit 1
        fi
        
        # 构建镜像
        echo "🔨 构建 Docker 镜像..."
        docker build -t cambridge-isotope-scraper .
        
        # 创建必要目录
        mkdir -p output urls
        
        # 复制示例文件
        cp examples/sample_urls.json urls/
        
        echo "✅ Docker 部署完成！"
        echo ""
        echo "🚀 使用方法:"
        echo "   docker run --rm -v \$(pwd)/output:/app/output cambridge-isotope-scraper python optimized_multithreaded_scraper.py -t 2 --headless"
        ;;
        
    "github")
        echo "📡 GitHub 部署模式"
        
        if [ -z "$GITHUB_REPO" ]; then
            echo "❌ 请提供 GitHub 仓库地址"
            echo "用法: $0 github https://github.com/youngbee12/repo.git"
            exit 1
        fi
        
        # 检查 Git
        if ! command -v git &> /dev/null; then
            echo "❌ 未找到 Git，请先安装"
            exit 1
        fi
        
        # 添加远程仓库
        if git remote get-url origin &> /dev/null; then
            echo "ℹ️  更新现有远程仓库"
            git remote set-url origin "$GITHUB_REPO"
        else
            echo "➕ 添加远程仓库"
            git remote add origin "$GITHUB_REPO"
        fi
        
        # 推送到 GitHub
        echo "📤 推送到 GitHub..."
        git push -u origin main
        
        echo "✅ GitHub 部署完成！"
        echo "🌐 仓库地址: $GITHUB_REPO"
        ;;
        
    "cloud")
        echo "☁️  云端部署模式"
        echo "⚠️  云端部署需要额外配置，请参考文档"
        
        # 这里可以添加云端部署逻辑
        # 例如：AWS、Azure、GCP 等
        
        echo "📚 支持的云平台:"
        echo "   - AWS EC2 + Docker"
        echo "   - Google Cloud Run"
        echo "   - Azure Container Instances"
        echo "   - DigitalOcean Droplets"
        ;;
        
    *)
        echo "❌ 未知的部署类型: $DEPLOY_TYPE"
        echo ""
        echo "📖 支持的部署类型:"
        echo "   local   - 本地安装 (默认)"
        echo "   docker  - Docker 容器化部署"
        echo "   github  - 推送到 GitHub"
        echo "   cloud   - 云端部署指南"
        echo ""
        echo "🚀 使用示例:"
        echo "   $0 local"
        echo "   $0 docker"
        echo "   $0 github https://github.com/youngbee12/cambridge-isotope-scraper.git"
        echo "   $0 cloud"
        exit 1
        ;;
esac

echo ""
echo "🎉 部署完成！"
echo ""
echo "📖 下一步:"
echo "   1. 查看 README.md 了解详细使用方法"
echo "   2. 运行性能测试: python high_thread_test.py"
echo "   3. 开始爬取数据: python optimized_multithreaded_scraper.py"
echo ""
echo "🆘 需要帮助?"
echo "   - 查看文档: README.md"
echo "   - Docker 部署: DOCKER.md"
echo "   - 提交问题: GitHub Issues"
