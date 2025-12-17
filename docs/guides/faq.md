# 常见问题解答 (FAQ)

## 🚀 快速开始

### Q: 如何快速开始使用 AI Daily Brief？

A: 按照以下步骤：

1. **安装项目**:
   ```bash
   git clone https://github.com/vitoi/ai-daily-brief.git
   cd ai-daily-brief
   pip install -r requirements.txt
   ```

2. **配置环境**:
   ```bash
   cp config/config.example.json config/config.json
   # 编辑配置文件，设置API密钥
   ```

3. **运行程序**:
   ```bash
   python src/main.py
   ```

4. **查看结果**: 简报会生成在项目根目录，文件名格式为 `daily_brief_YYYY-MM-DD.html`

### Q: 项目需要哪些外部服务？

A: 基本功能只需要网络连接。扩展功能需要：

- **Twitter API**: 发布到Twitter（可选）
- **邮件服务**: 发送邮件通知（可选）
- **GitHub**: 发布到GitHub Pages（可选）

### Q: 如何配置自动发布？

A: 支持多种发布方式：

```bash
# 运行配置向导
python setup_publishing.py

# 选择发布渠道：
# 1. Twitter 发布
# 2. 邮件推送
# 3. GitHub Pages 发布
```

## ⚙️ 配置问题

### Q: 配置文件在哪里？

A: 配置文件位于 `config/config.json`，示例配置在 `config/config.example.json`。

### Q: 如何获取 Twitter API 密钥？

A: 步骤如下：

1. 访问 [Twitter Developer Portal](https://developer.twitter.com/)
2. 创建新的应用或选择现有应用
3. 在应用设置中找到 "Keys and Tokens"
4. 复制以下信息到配置文件：
   - Consumer Key
   - Consumer Secret
   - Access Token
   - Access Token Secret

### Q: 邮件配置不工作怎么办？

A: 检查以下几点：

1. **Gmail 用户**: 使用应用密码而不是账户密码
2. **端口设置**:
   - Gmail: `smtp.gmail.com:587` (TLS)
   - Outlook: `smtp-mail.outlook.com:587` (TLS)
   - 163邮箱: `smtp.163.com:587` (TLS)

3. **安全设置**: 确保邮箱开启了SMTP访问

### Q: 如何添加新的新闻源？

A: 编辑 `config/news_sources.json`：

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

## 🏃‍♂️ 运行问题

### Q: 程序运行时显示"收集到 0 条新闻"？

A: 可能的原因：

1. **网络问题**: 检查网络连接
2. **RSS源失效**: 有些新闻源可能已更改URL
3. **频率限制**: 被网站限制访问频率
4. **解析错误**: 网站结构发生变化

**解决方法**:
```bash
# 测试网络连接
curl -I https://techcrunch.com/

# 检查日志详情
tail -50 ai_daily_brief.log
```

### Q: Twitter 发布失败？

A: 常见原因：

1. **API密钥错误**: 重新检查配置文件
2. **重复内容**: Twitter 不允许发布相同内容
3. **频率限制**: 超过API限制
4. **权限不足**: 应用没有发布权限

### Q: 邮件发送失败？

A: 检查：

1. **SMTP设置**: 服务器、端口、凭据
2. **网络连接**: 防火墙可能阻止SMTP端口
3. **邮箱设置**: 确认SMTP功能已开启

## 🔧 技术问题

### Q: 如何修改新闻分类规则？

A: 在 `src/brief_generator.py` 中修改关键词：

```python
categories = {
    'research': ['research', 'paper', 'study', 'algorithm', 'model'],
    'industry': ['company', 'product', 'launch', 'release', 'update'],
    'startups': ['startup', 'funding', 'raise', 'venture', 'seed'],
    'policy': ['regulation', 'policy', 'law', 'government', 'ethics']
}
```

### Q: 如何自定义简报模板？

A: 编辑 `config/templates/daily_brief.html`，使用Jinja2模板语法：

```html
<!-- 自定义标题 -->
<h1>{{ custom_title or "AI Daily Brief" }}</h1>

<!-- 自定义样式 -->
<style>
.custom-header {
    background: linear-gradient(135deg, {{ primary_color }}, {{ secondary_color }});
}
</style>
```

### Q: 如何添加新的发布渠道？

A: 在 `src/publisher.py` 中实现新的发布器：

```python
class NewPublisher:
    def publish_brief(self, content, summary):
        # 实现发布逻辑
        # 返回发布结果
        pass
```

然后在配置文件中添加配置项。

## 📊 数据与存储

### Q: 简报文件存储在哪里？

A: 简报文件存储在项目根目录，命名格式为 `daily_brief_YYYY-MM-DD.html`。

### Q: 如何清理旧的简报文件？

A: 使用以下命令：

```bash
# 删除30天前的简报
find . -name "daily_brief_*.html" -mtime +30 -delete

# 查看文件大小
du -sh daily_brief_*.html
```

### Q: 如何备份数据？

A: 手动备份：

```bash
# 创建备份目录
mkdir backup

# 备份配置文件
cp -r config backup/

# 备份简报文件
cp daily_brief_*.html backup/

# 压缩备份
tar -czf backup_$(date +%Y%m%d).tar.gz backup/
```

## 🧪 测试与调试

### Q: 如何运行测试？

A: 

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_collectors.py

# 运行带覆盖率的测试
pytest --cov=src --cov-report=html
```

### Q: 测试失败怎么办？

A: 

1. **检查依赖**: `pip install -r requirements-dev.txt`
2. **检查网络**: 有些测试需要网络连接
3. **查看错误详情**: `pytest -v`
4. **跳过网络测试**: `pytest -m "not network"`

### Q: 如何调试程序？

A: 

```bash
# 启用调试日志
export LOG_LEVEL=DEBUG
python src/main.py

# 或在代码中添加调试
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看详细日志
tail -f ai_daily_brief.log
```

## 🚀 部署问题

### Q: 如何设置定时运行？

A: 

**Linux/macOS**:
```bash
crontab -e
# 添加: 0 9 * * * cd /path/to/ai-daily-brief && python src/main.py
```

**Windows**:
使用任务计划程序，创建每日任务。

### Q: 如何部署到服务器？

A: 推荐使用Docker：

```bash
# 构建镜像
docker build -t ai-daily-brief .

# 运行容器
docker run -d --name ai-daily-brief \
  -v $(pwd)/config:/app/config \
  -p 8000:8000 \
  ai-daily-brief
```

### Q: 生产环境配置有什么不同？

A: 生产环境需要：

1. **数据库**: 使用PostgreSQL而不是SQLite
2. **缓存**: 配置Redis
3. **监控**: 设置Prometheus和Grafana
4. **日志**: 配置日志轮转和远程收集
5. **备份**: 设置自动备份策略

## 🔒 安全问题

### Q: 如何保护API密钥？

A: 

1. **环境变量**: 使用环境变量而不是硬编码
2. **文件权限**: 设置配置文件权限为600
3. **版本控制**: 不要提交密钥到Git
4. **轮换**: 定期更换API密钥

### Q: 如何处理敏感数据？

A: 

```bash
# 加密敏感配置文件
openssl enc -aes-256-cbc -salt -in config.json -out config.json.enc

# 解密使用
openssl enc -d -aes-256-cbc -in config.json.enc -out config.json
```

## 📈 性能优化

### Q: 如何提高收集速度？

A: 

1. **并发收集**: 启用多线程/异步收集
2. **缓存**: 使用Redis缓存已收集的内容
3. **优化数据库**: 添加合适的索引
4. **限制频率**: 避免过度请求

### Q: 内存使用过高怎么办？

A: 

1. **检查内存泄漏**: 使用 `memory_profiler`
2. **优化数据结构**: 使用生成器而不是列表
3. **限制缓存大小**: 配置Redis内存限制
4. **重启服务**: 定期重启释放内存

## 🤝 贡献相关

### Q: 如何报告Bug？

A: 在 [GitHub Issues](https://github.com/vitoi/ai-daily-brief/issues) 中创建Issue，包含：

- 错误描述
- 复现步骤
- 环境信息
- 错误日志

### Q: 如何提出功能建议？

A: 在 [GitHub Discussions](https://github.com/vitoi/ai-daily-brief/discussions) 中创建功能请求，说明：

- 功能描述
- 使用场景
- 预期效果

### Q: 如何贡献代码？

A: 

1. Fork 项目
2. 创建功能分支
3. 编写代码和测试
4. 提交 Pull Request

详细步骤请参考[贡献指南](contributing.md)。

## 📞 获取更多帮助

如果以上都没有解决你的问题：

1. 📖 查看完整[文档](../README.md)
2. 🐛 提交 [GitHub Issue](https://github.com/vitoi/ai-daily-brief/issues)
3. 💬 参与 [GitHub Discussions](https://github.com/vitoi/ai-daily-brief/discussions)
4. 📧 发送邮件至项目维护者

---

*最后更新: 2025-01-17*
