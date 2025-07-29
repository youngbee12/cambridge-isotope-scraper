#!/bin/bash
# Cambridge Isotope Scraper GitHub 推送脚本

set -e

echo "📡 Cambridge Isotope Scraper GitHub 推送工具"
echo "============================================"

# 检查参数
GITHUB_REPO=${1:-""}
GITHUB_USERNAME=${2:-""}

if [ -z "$GITHUB_REPO" ]; then
    echo "❌ 请提供 GitHub 仓库地址"
    echo ""
    echo "🚀 使用方法:"
    echo "   $0 <仓库地址> [用户名]"
    echo ""
    echo "📝 示例:"
    echo "   $0 https://github.com/username/cambridge-isotope-scraper.git"
    echo "   $0 git@github.com:username/cambridge-isotope-scraper.git username"
    echo ""
    exit 1
fi

echo "📋 配置信息:"
echo "   仓库地址: $GITHUB_REPO"
echo "   用户名: ${GITHUB_USERNAME:-'未指定'}"
echo ""

# 检查 Git 状态
echo "🔍 检查 Git 状态..."
if ! git status >/dev/null 2>&1; then
    echo "❌ 当前目录不是 Git 仓库"
    exit 1
fi

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  检测到未提交的更改"
    echo "📋 未提交的文件:"
    git status --porcelain
    echo ""
    read -p "是否继续推送? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 推送已取消"
        exit 1
    fi
fi

# 检查远程仓库
echo "🔗 配置远程仓库..."
if git remote get-url origin >/dev/null 2>&1; then
    CURRENT_ORIGIN=$(git remote get-url origin)
    echo "ℹ️  当前远程仓库: $CURRENT_ORIGIN"
    
    if [ "$CURRENT_ORIGIN" != "$GITHUB_REPO" ]; then
        echo "🔄 更新远程仓库地址..."
        git remote set-url origin "$GITHUB_REPO"
    fi
else
    echo "➕ 添加远程仓库..."
    git remote add origin "$GITHUB_REPO"
fi

# 检查分支
CURRENT_BRANCH=$(git branch --show-current)
echo "🌿 当前分支: $CURRENT_BRANCH"

# 推送代码
echo "📤 推送代码到 GitHub..."
if git push -u origin "$CURRENT_BRANCH"; then
    echo "✅ 代码推送成功"
else
    echo "❌ 代码推送失败"
    echo "💡 可能的解决方案:"
    echo "   1. 检查网络连接"
    echo "   2. 验证 GitHub 认证信息"
    echo "   3. 确认仓库权限"
    exit 1
fi

# 推送标签
echo "🏷️  推送标签..."
if git push origin --tags; then
    echo "✅ 标签推送成功"
else
    echo "⚠️  标签推送失败（可能没有标签）"
fi

# 检查是否有发布包
if [ -d "dist" ] && [ "$(ls -A dist/)" ]; then
    echo ""
    echo "📦 检测到发布包:"
    ls -la dist/*.tar.gz dist/*.zip 2>/dev/null || true
    echo ""
    echo "💡 下一步建议:"
    echo "   1. 访问 GitHub 仓库: $GITHUB_REPO"
    echo "   2. 创建新的 Release"
    echo "   3. 上传发布包文件"
    echo "   4. 添加发布说明"
    echo ""
    echo "🔗 GitHub Release 页面:"
    REPO_URL=$(echo "$GITHUB_REPO" | sed 's/\.git$//' | sed 's/git@github\.com:/https:\/\/github.com\//')
    echo "   ${REPO_URL}/releases/new"
    echo ""
    
    # 提供自动打开浏览器的选项
    read -p "是否打开 GitHub Release 页面? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v open >/dev/null 2>&1; then
            open "${REPO_URL}/releases/new"
        elif command -v xdg-open >/dev/null 2>&1; then
            xdg-open "${REPO_URL}/releases/new"
        else
            echo "请手动访问: ${REPO_URL}/releases/new"
        fi
    fi
fi

echo ""
echo "🎉 GitHub 推送完成！"
echo ""
echo "📊 仓库信息:"
echo "   🔗 仓库地址: $GITHUB_REPO"
echo "   🌿 分支: $CURRENT_BRANCH"
echo "   🏷️  最新标签: $(git describe --tags --abbrev=0 2>/dev/null || echo '无标签')"
echo "   📝 最新提交: $(git log -1 --pretty=format:'%h - %s')"
echo ""
echo "📚 后续步骤:"
echo "   1. 在 GitHub 上创建 Release"
echo "   2. 上传发布包文件"
echo "   3. 编写发布说明"
echo "   4. 更新项目文档"
echo "   5. 分享项目链接"
