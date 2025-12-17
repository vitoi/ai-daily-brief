#!/usr/bin/env python3
"""
AI Daily Brief - GitHub同步脚本

快速同步本地更改到GitHub
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True, cwd=".")
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败:")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False

def sync_to_github():
    """同步到GitHub"""

    print("🚀 AI Daily Brief - GitHub同步工具")
    print("=" * 40)

    # 检查git状态
    if not run_command("git status --porcelain", "检查git状态"):
        print("❌ 请先初始化git仓库")
        return

    # 添加文件（自动忽略.gitignore中的文件）
    if not run_command("git add .", "添加文件到暂存区"):
        return

    # 检查是否有要提交的内容
    result = subprocess.run("git diff --cached --name-only", shell=True,
                          capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  没有需要提交的更改")
        return

    print(f"📝 准备提交的文件:")
    for file in result.stdout.strip().split('\n'):
        print(f"   - {file}")

    # 获取提交信息
    commit_msg = input("\n请输入提交信息 (默认: 'update'): ").strip()
    if not commit_msg:
        commit_msg = "update"

    # 提交
    if not run_command(f'git commit -m "{commit_msg}"', "提交更改"):
        return

    # 推送
    if not run_command("git push origin main", "推送到GitHub"):
        return

    print("\n🎉 同步完成！")
    print("🔗 查看你的仓库: https://github.com/vitoi/ai-daily-brief")

if __name__ == "__main__":
    sync_to_github()
