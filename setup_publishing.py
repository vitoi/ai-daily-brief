#!/usr/bin/env python3
"""
AI Daily Brief - 发布渠道设置脚本

这个脚本帮助你快速配置各种自动发布功能。
"""

import os
import json
import getpass
from pathlib import Path

def setup_publishing():
    """设置发布渠道"""

    print("🚀 AI Daily Brief - 发布渠道设置向导")
    print("=" * 50)

    # 检查配置文件
    config_path = Path("config/config.json")
    if not config_path.exists():
        print("❌ 配置文件不存在，请先复制 config.example.json 到 config.json")
        return

    # 读取当前配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("\n📋 可用的发布渠道：")
    print("1. Twitter 发布")
    print("2. 邮件推送")
    print("3. GitHub Pages 静态站点")
    print("4. 本地文件（默认已启用）")

    choices = input("\n请选择要配置的渠道（用逗号分隔，如：1,2,3）: ").strip()

    if '1' in choices:
        setup_twitter(config)

    if '2' in choices:
        setup_email(config)

    if '3' in choices:
        setup_github_pages(config)

    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("\n✅ 配置已保存！")
    print("🎯 现在可以运行: python src/main.py 来测试发布功能")

def setup_twitter(config):
    """设置Twitter发布"""
    print("\n🐦 设置Twitter发布")
    print("💡 需要Twitter Developer账号: https://developer.twitter.com/")

    if 'twitter' not in config:
        config['twitter'] = {}

    config['twitter']['consumer_key'] = input("Twitter Consumer Key: ").strip()
    config['twitter']['consumer_secret'] = input("Twitter Consumer Secret: ").strip()
    config['twitter']['access_token'] = input("Twitter Access Token: ").strip()
    config['twitter']['access_token_secret'] = input("Twitter Access Token Secret: ").strip()

    print("✅ Twitter配置完成")

def setup_email(config):
    """设置邮件推送"""
    print("\n📧 设置邮件推送")
    print("💡 支持Gmail等SMTP服务")

    if 'email' not in config:
        config['email'] = {}

    config['email']['smtp_server'] = input("SMTP服务器 (默认: smtp.gmail.com): ").strip() or "smtp.gmail.com"
    config['email']['smtp_port'] = int(input("SMTP端口 (默认: 587): ").strip() or "587")
    config['email']['sender_email'] = input("发件人邮箱: ").strip()
    config['email']['sender_password'] = getpass.getpass("发件人密码/应用密码: ")
    config['email']['recipient_email'] = input("收件人邮箱: ").strip()

    print("✅ 邮件配置完成")

def setup_github_pages(config):
    """设置GitHub Pages"""
    print("\n🌐 设置GitHub Pages")
    print("💡 用于创建个人简报归档站点")

    if 'github_pages' not in config:
        config['github_pages'] = {}

    username = input("GitHub用户名: ").strip()
    repo_name = input("GitHub Pages仓库名 (默认: ai-daily-brief-pages): ").strip() or "ai-daily-brief-pages"

    config['github_pages']['repo_url'] = f"https://github.com/{username}/{repo_name}.git"
    config['github_pages']['branch'] = input("分支名 (默认: gh-pages): ").strip() or "gh-pages"
    config['github_pages']['local_repo_path'] = "github_pages_repo"

    print("✅ GitHub Pages配置完成")
    print(f"📝 请手动创建GitHub仓库: https://github.com/{username}/{repo_name}")
    print("🔧 确保启用GitHub Pages: Settings -> Pages -> Source: Deploy from a branch -> Branch: gh-pages")

if __name__ == "__main__":
    setup_publishing()
