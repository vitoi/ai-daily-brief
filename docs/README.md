# AI Daily Brief - 项目文档

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://github.com/vitoi/ai-daily-brief/workflows/CI/badge.svg)](https://github.com/vitoi/ai-daily-brief/actions)

**AI Daily Brief** 是一个智能化的AI行业新闻聚合与发布平台，自动收集、整理和发布AI相关新闻，帮助用户及时了解AI领域的最新动态。

## 📖 文档导航

### 🚀 快速开始
- [项目概述](overview.md) - 了解项目功能和架构
- [安装指南](user/installation.md) - 快速部署项目
- [使用指南](user/quickstart.md) - 开始使用项目

### 🏗️ 架构与设计
- [系统架构](architecture/system.md) - 整体架构设计
- [数据流](architecture/dataflow.md) - 数据处理流程
- [API设计](api/overview.md) - 接口规范

### 💻 开发指南
- [开发环境](development/environment.md) - 搭建开发环境
- [代码规范](development/coding-standards.md) - 编码标准和最佳实践
- [测试规范](development/testing.md) - 测试策略和规范
- [贡献指南](development/contributing.md) - 如何参与项目贡献

### 🚀 部署运维
- [部署指南](deployment/production.md) - 生产环境部署
- [监控告警](deployment/monitoring.md) - 系统监控和告警
- [故障排除](deployment/troubleshooting.md) - 常见问题解决

### 📚 参考资料
- [API参考](api/reference.md) - 完整的API文档
- [配置参考](guides/configuration.md) - 配置选项说明
- [FAQ](guides/faq.md) - 常见问题解答

## ✨ 核心特性

- 🤖 **智能新闻聚合**: 自动从多个AI新闻源收集最新资讯
- 🧠 **智能内容分类**: 基于AI的新闻内容智能分类和标签
- 📧 **多渠道发布**: 支持邮件、社交媒体、静态站点等多种发布方式
- 🎨 **个性化定制**: 灵活的配置系统，支持自定义新闻源和发布规则
- 📊 **数据可视化**: 内置简报归档和统计分析功能
- 🔒 **安全合规**: 遵循robots.txt和API使用规范

## 🏗️ 技术栈

### 后端
- **Python 3.9+**: 核心编程语言
- **FastAPI**: 高性能异步Web框架
- **SQLAlchemy**: 数据库ORM
- **Celery**: 分布式任务队列

### 数据处理
- **BeautifulSoup4**: HTML解析
- **feedparser**: RSS处理
- **NLTK**: 自然语言处理
- **pandas**: 数据分析

### 外部服务
- **Twitter API**: 社交媒体发布
- **SendGrid/Mailgun**: 邮件服务
- **GitHub Pages**: 静态站点托管

## 📊 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   News Sources  │───▶│  AI Daily Brief │───▶│   Publishing    │
│                 │    │                 │    │   Channels      │
│ • RSS Feeds     │    │ • News Collector │    │ • Email        │
│ • Web Scraping  │    │ • Content Filter │    │ • Twitter      │
│ • APIs          │    │ • Brief Generator│    │ • GitHub Pages │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Local Archive │
                       │                 │
                       │ • HTML Reports  │
                       │ • JSON Data     │
                       │ • Statistics    │
                       └─────────────────┘
```

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境
```bash
cp config/config.example.json config/config.json
# 编辑 config/config.json 配置你的API密钥
```

### 运行项目
```bash
python src/main.py
```

## 📈 项目状态

- ✅ 核心功能开发完成
- ✅ 基础测试覆盖
- ✅ 文档完善
- 🔄 性能优化进行中
- 📋 API接口开发待完成

## 🤝 贡献

欢迎参与项目贡献！请查看[贡献指南](development/contributing.md)了解详细信息。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 📞 联系方式

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/vitoi/ai-daily-brief/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/vitoi/ai-daily-brief/discussions)

---

*最后更新: 2025-01-17*
