#!/usr/bin/env python3
"""
AI Daily Brief - GitHub Pages 设置脚本

这个脚本帮助你快速设置GitHub Pages发布功能。
"""

import os
import json
import subprocess
from pathlib import Path

def setup_github_pages():
    """设置GitHub Pages发布功能"""

    print("🚀 AI Daily Brief - GitHub Pages 设置向导")
    print("=" * 50)

    # 检查配置文件
    config_path = Path("config/config.json")
    if not config_path.exists():
        print("❌ 配置文件不存在，请先复制 config.example.json 到 config.json")
        return

    # 读取当前配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 获取GitHub用户名
    username = input("请输入你的GitHub用户名: ").strip()
    if not username:
        print("❌ GitHub用户名不能为空")
        return

    repo_name = input("请输入GitHub Pages仓库名 (默认: ai-daily-brief-pages): ").strip()
    if not repo_name:
        repo_name = "ai-daily-brief-pages"

    # 更新配置
    config['github_pages'] = {
        "repo_url": f"https://github.com/{username}/{repo_name}.git",
        "branch": "gh-pages",
        "local_repo_path": "github_pages_repo"
    }

    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("✅ 配置已更新！"    print(f"📝 请手动创建GitHub仓库: https://github.com/{username}/{repo_name}")
    print("💡 确保仓库设置为公开，并且启用了GitHub Pages (Settings -> Pages -> Source: Deploy from a branch -> Branch: gh-pages)")

    print("\n🔧 接下来的步骤：")
    print("1. 在GitHub上创建仓库并启用Pages")
    print("2. 运行程序测试发布功能: python src/main.py")
    print("3. 访问你的站点: https://{username}.github.io/{repo_name}/")

if __name__ == "__main__":
    setup_github_pages()
