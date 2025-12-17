# 安装指南

## 🖥️ 系统要求

### 最低系统要求
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **内存**: 2GB RAM
- **存储空间**: 500MB 可用空间
- **网络**: 稳定的互联网连接

### 推荐系统配置
- **操作系统**: Ubuntu 20.04+ 或 macOS 12+
- **内存**: 4GB RAM 以上
- **存储空间**: 2GB 可用空间
- **网络**: 高速互联网连接

## 📦 安装方式

### 方式一：使用 pip 安装（推荐）

#### 1. 安装 Python
确保你有 Python 3.9 或更高版本：
```bash
python --version
# 应该显示 Python 3.9.x 或更高版本
```

如果没有安装 Python：
- **Windows**: 从 [python.org](https://python.org) 下载安装包
- **macOS**: 使用 Homebrew: `brew install python`
- **Ubuntu**: `sudo apt update && sudo apt install python3 python3-pip`

#### 2. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv ai-daily-brief-env

# 激活虚拟环境
# Windows:
ai-daily-brief-env\Scripts\activate
# macOS/Linux:
source ai-daily-brief-env/bin/activate
```

#### 3. 克隆项目
```bash
git clone https://github.com/vitoi/ai-daily-brief.git
cd ai-daily-brief
```

#### 4. 安装依赖
```bash
pip install -r requirements.txt
```

#### 5. 验证安装
```bash
python -c "import src.main; print('✅ 安装成功！')"
```

### 方式二：使用 Docker 安装

#### 1. 安装 Docker
- **Windows/macOS**: 下载 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Ubuntu**: 按照 [官方指南](https://docs.docker.com/engine/install/ubuntu/) 安装

#### 2. 克隆项目并构建镜像
```bash
git clone https://github.com/vitoi/ai-daily-brief.git
cd ai-daily-brief

# 构建Docker镜像
docker build -t ai-daily-brief .
```

#### 3. 运行容器
```bash
# 运行容器
docker run -it --rm ai-daily-brief

# 或者使用 docker-compose
docker-compose up
```

## ⚙️ 基本配置

### 1. 配置文件设置

复制示例配置文件：
```bash
cp config/config.example.json config/config.json
```

编辑配置文件：
```json
{
  "twitter": {
    "consumer_key": "your_twitter_consumer_key",
    "consumer_secret": "your_twitter_consumer_secret",
    "access_token": "your_twitter_access_token",
    "access_token_secret": "your_twitter_access_token_secret"
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",
    "recipient_email": "recipient@example.com"
  }
}
```

### 2. 环境变量设置（可选）

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=sqlite:///ai_daily_brief.db

# API密钥
TWITTER_CONSUMER_KEY=your_key_here
TWITTER_CONSUMER_SECRET=your_secret_here

# 邮件配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# 应用配置
LOG_LEVEL=INFO
DEBUG=false
```

### 3. Twitter API 设置

1. 访问 [Twitter Developer Portal](https://developer.twitter.com/)
2. 创建新的应用或使用现有应用
3. 在 "Keys and Tokens" 页面获取：
   - Consumer Key
   - Consumer Secret
   - Access Token
   - Access Token Secret
4. 将这些值填入 `config.json` 或 `.env` 文件

### 4. 邮件服务设置

#### Gmail 设置
1. 启用两步验证
2. 生成应用密码：[Google App Passwords](https://support.google.com/accounts/answer/185833)
3. 使用应用密码而不是账户密码

#### 其他邮件服务
```json
{
  "email": {
    "smtp_server": "smtp.163.com",  // 或其他SMTP服务器
    "smtp_port": 587,
    "sender_email": "your_email@163.com",
    "sender_password": "your_password",
    "recipient_email": "recipient@example.com"
  }
}
```

## 🚀 运行程序

### 基本运行
```bash
# 激活虚拟环境（如果使用）
source ai-daily-brief-env/bin/activate

# 运行主程序
python src/main.py
```

### Docker 运行
```bash
# 使用 Docker 运行
docker run -it --rm \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  ai-daily-brief
```

### 后台运行
```bash
# 使用 nohup 在后台运行
nohup python src/main.py > output.log 2>&1 &

# 查看进程
ps aux | grep python

# 停止进程
kill <process_id>
```

## 🧪 测试安装

### 运行测试
```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_collectors.py -v
```

### 手动测试功能
```bash
# 测试新闻收集
python -c "
from src.news_collector import NewsCollector
collector = NewsCollector()
news = collector.collect_all_news()
print(f'收集到 {len(news)} 条新闻')
"

# 测试简报生成功能
python -c "
from src.brief_generator import BriefGenerator
generator = BriefGenerator()
brief = generator.generate_brief([])
print('简报生成功能正常')
"
```

## 🔧 故障排除

### 常见安装问题

#### pip 安装失败
```bash
# 更新 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 清理缓存
pip cache purge
```

#### 虚拟环境问题
```bash
# 删除并重新创建虚拟环境
rm -rf ai-daily-brief-env
python -m venv ai-daily-brief-env
source ai-daily-brief-env/bin/activate
pip install -r requirements.txt
```

#### 权限问题 (macOS/Linux)
```bash
# 如果遇到权限错误，使用 --user 安装
pip install --user -r requirements.txt

# 或者使用 sudo（不推荐）
sudo pip install -r requirements.txt
```

### 运行时问题

#### 网络连接问题
```bash
# 测试网络连接
curl -I https://www.google.com

# 检查代理设置
echo $http_proxy $https_proxy

# 如果在公司网络后，配置代理
export http_proxy=http://proxy.company.com:8080
export https_proxy=http://proxy.company.com:8080
```

#### API 密钥问题
```bash
# 测试 Twitter API 连接
python -c "
import tweepy
# 尝试连接 Twitter API
try:
    client = tweepy.Client(
        consumer_key='your_key',
        consumer_secret='your_secret',
        access_token='your_token',
        access_token_secret='your_token_secret'
    )
    print('Twitter API 连接成功')
except Exception as e:
    print(f'Twitter API 连接失败: {e}')
"
```

#### 数据库问题
```bash
# 检查 SQLite 数据库
python -c "
import sqlite3
conn = sqlite3.connect('ai_daily_brief.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
tables = cursor.fetchall()
print('数据库表:', tables)
conn.close()
"
```

### 日志分析
```bash
# 查看错误日志
tail -50 ai_daily_brief.log

# 搜索特定错误
grep "ERROR" ai_daily_brief.log

# 查看最近的运行日志
tail -f ai_daily_brief.log
```

## 📞 获取帮助

如果在安装过程中遇到问题：

1. **查看文档**: [故障排除指南](../deployment/troubleshooting.md)
2. **检查日志**: 查看 `ai_daily_brief.log` 文件
3. **提交Issue**: [GitHub Issues](https://github.com/vitoi/ai-daily-brief/issues)
4. **社区讨论**: [GitHub Discussions](https://github.com/vitoi/ai-daily-brief/discussions)

## ✅ 验证安装成功

运行以下命令验证安装：
```bash
# 1. 检查 Python 版本
python --version

# 2. 检查依赖安装
python -c "import requests, bs4, tweepy; print('✅ 依赖安装成功')"

# 3. 测试基本功能
python src/main.py --help

# 4. 检查配置文件
python -c "
import json
with open('config/config.json') as f:
    config = json.load(f)
print('✅ 配置文件格式正确')
"
```

如果所有检查都通过，恭喜你！AI Daily Brief 已经成功安装并可以正常使用了。

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
