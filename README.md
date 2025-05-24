# AI Daily Brief

一个自动化的AI行业动态简报平台，可以收集、整理和发布AI相关新闻和动态。

## 功能特点

- 自动抓取多个AI相关新闻源
- 智能内容聚合和分类
- 生成格式化的每日简报
- 支持邮件订阅
- 支持社交媒体发布（Twitter等）

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

1. 配置新闻源和发布渠道
2. 运行主程序：
```bash
python src/main.py
```

## 配置说明

在 `config` 目录下可以配置：
- 新闻源列表
- 邮件模板
- 社交媒体API密钥
- 发布计划

## 合规性

在使用本项目的过程中，请确保遵守以下合规性要求：

- **API 使用**：在使用 Twitter API 等外部 API 时，请确保遵守其服务条款和使用限制。
- **数据抓取**：在抓取数据时，请遵守目标网站的 robots.txt 规则，并控制请求频率以避免对目标网站造成负担。
- **隐私保护**：确保在收集和使用数据时，遵守相关隐私法规，保护用户隐私。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 