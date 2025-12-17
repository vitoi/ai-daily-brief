# AI Daily Brief

一个自动化的AI行业动态简报平台，可以收集、整理和发布AI相关新闻和动态。

## 功能特点

- 自动抓取多个AI相关新闻源
- 智能内容聚合和分类
- 生成格式化的每日简报
- 支持多渠道自动发布：
  - 社交媒体（Twitter）
  - 邮件推送
  - GitHub Pages静态站点
- 个人使用友好，支持灵活配置

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd ai_daily_brief
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
复制 `.env.example` 到 `.env` 并填写必要的配置信息。

## 使用方法

### 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置发布渠道（可选）：
```bash
python setup_publishing.py
```

3. 运行主程序：
```bash
python src/main.py
```

### 个人使用配置

#### 邮件推送（推荐）
每天自动发送简报到你的邮箱：
```bash
python setup_publishing.py  # 选择选项2
```

#### GitHub Pages站点
创建个人简报归档站点：
```bash
python setup_publishing.py  # 选择选项3
```

#### Twitter发布
分享简报到社交媒体：
```bash
python setup_publishing.py  # 选择选项1
```

#### 本地归档服务器
启动本地Web服务器查看历史简报：
```bash
python local_server.py [端口号]
# 例如：python local_server.py 8080
# 然后访问: http://localhost:8080
```

### 定时运行
使用crontab设置每日自动运行：
```bash
# 编辑crontab
crontab -e

# 添加每日早上8点运行
0 8 * * * cd /path/to/ai-daily-brief && /usr/bin/python3 src/main.py >> logs/cron.log 2>&1
```

## 配置说明

在 `config` 目录下可以配置：
- 新闻源列表
- 邮件模板
- 社交媒体API密钥
- 发布计划

### 发布渠道配置

#### Twitter发布
```json
{
  "twitter": {
    "consumer_key": "your_consumer_key",
    "consumer_secret": "your_consumer_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
  }
}
```

#### 邮件发布
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",
    "recipient_email": "recipient@example.com"
  }
}
```

#### GitHub Pages发布
```json
{
  "github_pages": {
    "repo_url": "https://github.com/username/ai-daily-brief-pages.git",
    "branch": "gh-pages",
    "local_repo_path": "github_pages_repo"
  }
}
```

## 合规性

在使用本项目的过程中，请确保遵守以下合规性要求：

- **API 使用**：在使用 Twitter API 等外部 API 时，请确保遵守其服务条款和使用限制。
- **数据抓取**：在抓取数据时，请遵守目标网站的 robots.txt 规则，并控制请求频率以避免对目标网站造成负担。
- **隐私保护**：确保在收集和使用数据时，遵守相关隐私法规，保护用户隐私。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 