# 快速开始指南

## 🎯 5分钟上手 AI Daily Brief

本指南将帮助你在5分钟内完成AI Daily Brief的基本设置和运行。

## 📋 前置条件

- ✅ 已完成[安装指南](installation.md)的步骤
- ✅ Python 3.9+ 已安装
- ✅ 项目依赖已安装
- ✅ 基本配置文件已创建

## 🚀 第一步：基础配置

### 1.1 配置数据源

项目已经内置了主流AI新闻源，你可以查看默认配置：

```bash
# 查看新闻源配置
cat config/news_sources.json
```

默认包含的新闻源：
- **TechCrunch AI** - 科技新闻
- **MIT Technology Review** - 学术科技
- **VentureBeat AI** - 创业新闻
- **arXiv AI** - 学术论文
- 等等...

### 1.2 配置发布渠道（可选）

如果你想自动发布简报到社交媒体或邮箱：

```bash
# 运行配置向导
python setup_publishing.py
```

选择你想要的发布渠道：
1. **Twitter** - 发布简报摘要
2. **邮件** - 发送完整HTML简报
3. **GitHub Pages** - 创建在线简报归档

## 🏃‍♂️ 第二步：运行程序

### 2.1 手动运行一次

```bash
# 运行主程序
python src/main.py
```

你会看到类似输出：
```
2025-01-17 21:51:44,415 - __main__ - INFO - 开始收集新闻...
2025-01-17 21:51:44,417 - news_collector - INFO - 开始从arXiv API收集AI论文...
2025-01-17 21:53:10,000 - news_collector - INFO - 从arXiv收集到 8 条论文
2025-01-17 21:53:11,819 - news_collector - INFO - 开始从TechCrunch AI RSS收集新闻...
2025-01-17 21:53:22,720 - urllib3.connectionpool - WARNING - Retrying...
2025-01-17 21:53:32,439 - news_collector - INFO - 从TechCrunch RSS收集到 1 条新闻
2025-01-17 21:53:34,080 - __main__ - INFO - 收集到 9 条新闻
2025-01-17 21:53:34,083 - __main__ - INFO - 生成简报...
2025-01-17 21:53:34,100 - __main__ - INFO - 简报已保存到 daily_brief_2025-12-17.html
2025-01-17 21:53:34,100 - __main__ - INFO - 发布简报...
```

### 2.2 查看生成的简报

程序运行完成后，会生成一个HTML文件：

```bash
# 查看生成的简报文件
ls -la daily_brief_*.html

# 使用浏览器打开
open daily_brief_2025-12-17.html  # macOS
xdg-open daily_brief_2025-12-17.html  # Linux
start daily_brief_2025-12-17.html  # Windows
```

### 2.3 查看本地归档服务器（可选）

如果你想查看历史简报：

```bash
# 启动本地服务器
python local_server.py

# 打开浏览器访问
# http://localhost:8000
```

## 📊 第三步：理解输出

### 3.1 简报内容结构

生成的简报包含以下部分：

1. **标题区域** - 显示生成日期和总新闻数量
2. **分类新闻** - 按主题分类展示：
   - 🔬 **Research** - 学术研究和论文
   - 🏢 **Industry** - 产业新闻和产品发布
   - 🚀 **Startups** - 创业公司动态
   - 📋 **Policy** - 政策法规更新
   - ❓ **Other** - 其他相关新闻

3. **新闻条目** - 每个条目包含：
   - 标题和链接
   - 来源和发布时间
   - 内容摘要
   - 相关标签

### 3.2 发布状态

程序会显示发布结果：
```
2025-12-17 21:53:37,116 - publisher - INFO - 成功发布到Twitter
2025-12-17 21:53:37,117 - __main__ - INFO - 成功发布到 twitter
```

## 🔄 第四步：设置自动化

### 4.1 使用定时任务（推荐）

#### Linux/macOS (crontab)
```bash
# 编辑定时任务
crontab -e

# 添加每日早上9点运行（根据需要调整时间）
0 9 * * * cd /path/to/ai-daily-brief && python src/main.py >> logs/cron.log 2>&1
```

#### Windows (任务计划程序)
1. 打开任务计划程序
2. 创建基本任务
3. 设置触发器为"每日"
4. 设置动作为"启动程序"
5. 程序路径：`C:\path\to\python.exe`
6. 参数：`src/main.py`
7. 起始位置：`C:\path\to\ai-daily-brief`

### 4.2 使用 systemd 服务（Linux）

创建服务文件 `/etc/systemd/system/ai-daily-brief.service`：
```ini
[Unit]
Description=AI Daily Brief Service
After=network.target

[Service]
Type=oneshot
User=your_username
WorkingDirectory=/path/to/ai-daily-brief
ExecStart=/path/to/python src/main.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

启用和启动服务：
```bash
sudo systemctl enable ai-daily-brief
sudo systemctl start ai-daily-brief

# 设置定时运行
sudo systemctl edit ai-daily-brief
# 添加定时器配置...
```

### 4.3 使用 GitHub Actions（云端）

创建 `.github/workflows/daily-brief.yml`：
```yaml
name: Daily AI Brief

on:
  schedule:
    - cron: '0 9 * * *'  # 每天早上9点运行
  workflow_dispatch:     # 允许手动触发

jobs:
  generate-brief:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Generate brief
      run: python src/main.py
      env:
        TWITTER_CONSUMER_KEY: ${{ secrets.TWITTER_CONSUMER_KEY }}
        TWITTER_CONSUMER_SECRET: ${{ secrets.TWITTER_CONSUMER_SECRET }}
        # 添加其他环境变量...

    - name: Commit and push changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add daily_brief_*.html
        git commit -m "Update daily brief $(date +%Y-%m-%d)" || echo "No changes to commit"
        git push
```

## 🎨 第五步：自定义配置

### 5.1 添加新的新闻源

编辑 `config/news_sources.json`：
```json
{
  "sources": [
    {
      "name": "新新闻源",
      "url": "https://example.com/rss",
      "type": "rss"
    }
  ]
}
```

### 5.2 自定义发布模板

修改 `config/templates/daily_brief.html` 来自定义简报样式。

### 5.3 调整收集参数

在 `src/main.py` 中调整：
- 收集的新闻数量
- 分类阈值
- 发布渠道

## 📊 第六步：监控和维护

### 6.1 查看日志
```bash
# 查看最新日志
tail -50 ai_daily_brief.log

# 搜索错误
grep "ERROR" ai_daily_brief.log

# 实时监控
tail -f ai_daily_brief.log
```

### 6.2 清理旧文件
```bash
# 删除30天前的简报文件
find . -name "daily_brief_*.html" -mtime +30 -delete

# 查看磁盘使用情况
du -sh ./*
```

### 6.3 性能监控
```bash
# 运行性能测试
python -m pytest tests/ -k performance --durations=10

# 查看系统资源使用
top -p $(pgrep -f "python src/main.py")
```

## 🎉 恭喜！

你已经成功设置并运行了 AI Daily Brief！

### 接下来你可以：

1. **调整配置** - 自定义新闻源和发布设置
2. **设置自动化** - 让程序每日自动运行
3. **扩展功能** - 添加新的发布渠道或数据源
4. **监控运行** - 定期检查日志和性能

### 获取帮助

- 📖 [完整文档](../README.md)
- 🐛 [问题反馈](https://github.com/vitoi/ai-daily-brief/issues)
- 💬 [社区讨论](https://github.com/vitoi/ai-daily-brief/discussions)

享受你的 AI 新闻简报之旅！🚀

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
