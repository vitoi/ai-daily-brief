# 贡献指南

## 🤝 如何参与项目

欢迎所有形式的贡献！无论是修复bug、添加功能、改进文档，还是提出建议，我们都非常欢迎。以下是参与项目的指南。

## 📋 贡献流程

### 1. 准备工作

#### 环境设置
```bash
# 1. Fork 项目到你的 GitHub 账户
# 在 GitHub 上点击 "Fork" 按钮

# 2. 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/ai-daily-brief.git
cd ai-daily-brief

# 3. 添加上游仓库
git remote add upstream https://github.com/vitoi/ai-daily-brief.git

# 4. 创建功能分支
git checkout -b feature/your-feature-name
```

#### 开发环境
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试确保环境正常
pytest tests/

# 启动开发服务器
python src/main.py
```

### 2. 开发阶段

#### 代码规范
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 使用 [Black](https://black.readthedocs.io/) 格式化代码
- 添加类型注解
- 编写完整的文档字符串

#### 提交规范
```bash
# 提交信息格式
<type>(<scope>): <subject>

# 示例
feat(collector): add RSS feed parser
fix(publisher): resolve Twitter API timeout
docs(readme): update installation guide
test(collector): add RSS parsing tests

# 常用类型
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具更新
```

#### 测试要求
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_collectors.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 3. 提交贡献

#### 创建 Pull Request
```bash
# 1. 同步上游仓库
git fetch upstream
git rebase upstream/main

# 2. 推送分支
git push origin feature/your-feature-name

# 3. 创建 Pull Request
# 在 GitHub 上访问你的 fork，点击 "Compare & pull request"
```

#### PR 模板
创建 PR 时请填写以下信息：

**标题**: `[类型] 简洁描述`

**描述**:
```
## 问题描述
[清晰描述要解决的问题]

## 解决方案
[详细说明解决方案]

## 测试
[描述测试方法和结果]

## 相关 Issue
[关联的 Issue 编号，如: #123]

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 通过了所有测试
```

## 🐛 报告 Bug

### Bug 报告模板
```markdown
**Bug 描述**
[清晰简洁地描述问题]

**复现步骤**
1. 转到 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

**期望行为**
[描述期望发生什么]

**实际行为**
[描述实际发生什么]

**截图**
[如果适用，添加截图]

**环境信息**
- OS: [e.g. macOS 12.1]
- Python: [e.g. 3.9.7]
- 项目版本: [e.g. v1.0.0]

**额外信息**
[其他相关信息]
```

## 💡 提出新功能

### 功能请求模板
```markdown
**功能描述**
[清晰描述新功能]

**使用场景**
[说明这个功能在什么情况下使用]

**建议实现**
[如果有想法，描述实现方式]

**替代方案**
[考虑过的其他实现方式]

**额外信息**
[其他相关信息]
```

## 📝 文档贡献

### 文档改进
- 修复拼写错误
- 改进说明清晰度
- 添加缺失信息
- 更新过时内容

### 文档规范
- 使用 Markdown 格式
- 中英文对照（核心文档）
- 包含示例代码
- 保持结构清晰

## 🧪 测试贡献

### 添加测试用例
```python
# tests/test_your_feature.py
import pytest
from src.your_module import YourClass

class TestYourFeature:
    def test_basic_functionality(self):
        # 测试基本功能
        pass

    def test_edge_cases(self):
        # 测试边界情况
        pass

    def test_error_handling(self):
        # 测试错误处理
        pass
```

### 测试覆盖率
- 新代码需要 100% 测试覆盖
- 修改现有代码需要保持覆盖率
- 复杂逻辑需要全面测试

## 🔧 代码审查

### 审查清单
**功能完整性**
- [ ] 实现预期的功能
- [ ] 处理边界情况
- [ ] 错误处理完善

**代码质量**
- [ ] 遵循代码规范
- [ ] 有完整的类型注解
- [ ] 有详细的文档字符串
- [ ] 通过所有 linting 检查

**测试覆盖**
- [ ] 有对应的单元测试
- [ ] 测试覆盖边界条件
- [ ] 测试覆盖错误场景

**安全检查**
- [ ] 无敏感信息泄露
- [ ] 输入验证完善
- [ ] SQL 注入防护
- [ ] XSS 防护

### 审查意见
- **请求更改**: 需要修改后重新提交
- **批准**: 可以合并
- **评论**: 建议但不强制修改

## 🌟 贡献者认可

### 贡献者墙
所有贡献者都会被添加到项目贡献者列表中。

### 贡献等级
- **贡献者**: 首次成功合并 PR
- **活跃贡献者**: 多个有意义的贡献
- **维护者**: 核心代码贡献和审查

### 特别感谢
对重大贡献的贡献者，我们会提供：
- 项目署名
- 优先处理 Issue
- 技术支持优先级

## 📞 获取帮助

### 沟通渠道
- 💬 [GitHub Discussions](https://github.com/vitoi/ai-daily-brief/discussions) - 一般讨论
- 🐛 [GitHub Issues](https://github.com/vitoi/ai-daily-brief/issues) - 问题反馈
- 📧 [邮件列表](mailto:contributors@ai-daily-brief.dev) - 重要通知

### 常见问题

#### Q: 如何开始贡献？
A: 从查看 [Issues](https://github.com/vitoi/ai-daily-brief/issues) 开始，选择标有 "good first issue" 的问题。

#### Q: 代码风格检查失败怎么办？
A: 运行 `black .` 和 `flake8 src/` 来自动修复大部分问题。

#### Q: 测试失败怎么办？
A: 确保安装了所有依赖 `pip install -r requirements-dev.txt`，然后运行 `pytest` 查看详细错误信息。

#### Q: 如何撤销提交？
A: 使用 `git reset --soft HEAD~1` 撤销最后一次提交，但保留文件更改。

## 📜 行为准则

### 我们的承诺
在参与本项目的过程中，我们承诺：

- 🤝 **尊重**: 尊重不同背景和经验水平的贡献者
- 🏃‍♂️ **包容**: 欢迎各种形式的贡献
- 🚫 **无骚扰**: 零容忍骚扰和歧视行为
- 📢 **透明**: 公开、透明的决策过程

### 不可接受的行为
- 侮辱性、歧视性或排斥性言论
- 故意恐吓、跟踪或骚扰
- 发布他人私人信息
- 其他违反职业道德的行为

### 报告违规
如果遇到违规行为，请通过以下方式报告：
- 📧 发送邮件至 conduct@ai-daily-brief.dev
- 🐛 在相关 Issue 中 @maintainer
- 💬 在 Discord 私信管理员

## 🎉 贡献奖励

### 每月贡献者
每月评选出最活跃的贡献者，获得：
- 🏆 项目徽章
- 📜 贡献者证书
- 🎁 专属周边

### Hacktoberfest
10月参与开源贡献，获得：
- 🌟 专属 T-shirt
- 📊 贡献统计
- 🎯 成就徽章

---

**感谢你的贡献！每一次贡献都在让 AI Daily Brief 变得更好。** 🚀

*本文档版本: v1.0 | 最后更新: 2025-01-17*
