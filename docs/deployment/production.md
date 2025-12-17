# 生产环境部署指南

## 🎯 部署概述

本指南介绍如何在生产环境中安全、稳定地部署AI Daily Brief系统。

## 🏗️ 部署架构

### 推荐架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Application   │    │   Database      │
│   (Nginx)       │────▶│   Server       │────▶│   (PostgreSQL)  │
│                 │    │   (Gunicorn)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Redis Cache   │    │   File Storage  │    │   Monitoring    │
│                 │    │   (S3/MinIO)    │    │   (Prometheus)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 组件说明

- **负载均衡器**: Nginx 反向代理和负载均衡
- **应用服务器**: Gunicorn WSGI服务器
- **数据库**: PostgreSQL 关系型数据库
- **缓存**: Redis 内存数据库
- **文件存储**: 对象存储服务
- **监控**: Prometheus + Grafana

## 📦 部署准备

### 系统要求

#### 服务器配置
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 50GB SSD
- **网络**: 10Mbps以上带宽
- **操作系统**: Ubuntu 20.04 LTS

#### 网络要求
- 域名和SSL证书
- 防火墙配置
- DNS解析

### 环境准备

#### 1. 服务器初始化
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git htop vim ufw

# 配置防火墙
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

#### 2. 安装 Python
```bash
# 安装 Python 3.9
sudo apt install -y python3.9 python3.9-venv python3-pip

# 验证安装
python3.9 --version
```

#### 3. 安装 PostgreSQL
```bash
# 安装 PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 启动服务
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 创建数据库和用户
sudo -u postgres psql
```

```sql
-- 在PostgreSQL shell中执行
CREATE DATABASE ai_daily_brief;
CREATE USER brief_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ai_daily_brief TO brief_user;
\q
```

#### 4. 安装 Redis
```bash
# 安装 Redis
sudo apt install -y redis-server

# 配置 Redis
sudo vim /etc/redis/redis.conf
# 修改: supervised systemd
# 修改: bind 127.0.0.1

# 启动 Redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### 5. 安装 Nginx
```bash
# 安装 Nginx
sudo apt install -y nginx

# 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 🚀 应用部署

### 1. 代码部署

#### 使用 Git 部署
```bash
# 创建应用目录
sudo mkdir -p /opt/ai-daily-brief
sudo chown $USER:$USER /opt/ai-daily-brief

# 克隆代码
cd /opt/ai-daily-brief
git clone https://github.com/vitoi/ai-daily-brief.git .
git checkout main  # 或指定标签
```

#### 使用 Docker 部署（推荐）
```bash
# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: .
    container_name: ai-daily-brief-app
    environment:
      - DATABASE_URL=postgresql://brief_user:password@db:5432/ai_daily_brief
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    restart: unless-stopped

  db:
    image: postgres:14
    container_name: ai-daily-brief-db
    environment:
      - POSTGRES_DB=ai_daily_brief
      - POSTGRES_USER=brief_user
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: ai-daily-brief-redis
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: ai-daily-brief-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
EOF

# 部署应用
docker-compose up -d
```

### 2. 配置管理

#### 环境变量配置
```bash
# 创建环境变量文件
cat > .env << 'EOF'
# 数据库配置
DATABASE_URL=postgresql://brief_user:secure_password@localhost:5432/ai_daily_brief

# Redis配置
REDIS_URL=redis://localhost:6379/0

# API密钥
TWITTER_CONSUMER_KEY=your_key
TWITTER_CONSUMER_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret

# 邮件配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SENDER_PASSWORD=your_app_password

# 应用配置
SECRET_KEY=your-secret-key-here
DEBUG=false
LOG_LEVEL=INFO

# 服务器配置
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

#### 配置文件
```bash
# 创建生产配置文件
cp config/config.example.json config/config.json

# 编辑配置文件（添加生产环境配置）
vim config/config.json
```

### 3. 数据库迁移

```bash
# 运行数据库迁移
python src/manage.py db upgrade

# 或者手动创建表
python -c "
from src.database import init_db
init_db()
"
```

## 🌐 Web服务器配置

### Nginx 配置

创建 `/etc/nginx/sites-available/ai-daily-brief`:
```nginx
upstream ai_daily_brief_app {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 配置
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # 静态文件缓存
    location /static/ {
        alias /opt/ai-daily-brief/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API 接口
    location /api/ {
        proxy_pass http://ai_daily_brief_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # API 缓存
        proxy_cache api_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
        add_header X-Cache-Status $upstream_cache_status;
    }

    # Webhook 接口（不缓存）
    location /webhook/ {
        proxy_pass http://ai_daily_brief_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}

# 缓存配置
proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m use_temp_path=off;
```

启用站点：
```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/ai-daily-brief /etc/nginx/sites-enabled/

# 删除默认站点
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重载配置
sudo systemctl reload nginx
```

## 🔒 安全配置

### SSL证书配置

#### 使用 Let's Encrypt
```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 设置自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 手动配置 SSL
```bash
# 创建 SSL 目录
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

# 上传证书文件
# /etc/ssl/certs/your-domain.crt
# /etc/ssl/private/your-domain.key

# 设置权限
sudo chmod 600 /etc/ssl/private/your-domain.key
sudo chown root:root /etc/ssl/private/your-domain.key
```

### 应用安全

#### 环境变量加密
```bash
# 安装 python-dotenv 和 cryptography
pip install python-dotenv cryptography

# 创建加密的密钥
python -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print('密钥:', key.decode())
"
```

#### 敏感数据处理
```python
# src/config/security.py
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

class SecurityManager:
    def __init__(self):
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY not set")
        self.fernet = Fernet(key.encode())

    def encrypt_sensitive_data(self, data: str) -> str:
        """加密敏感数据"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """解密敏感数据"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
```

## 📊 监控配置

### Prometheus 配置

创建 `/etc/prometheus/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'ai-daily-brief'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana 配置

```bash
# 安装 Grafana
sudo apt install -y apt-transport-https
sudo apt install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana

# 启动 Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 应用指标

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# 业务指标
NEWS_COLLECTED = Counter('news_collected_total', 'Total news items collected', ['source'])
BRIEFS_GENERATED = Counter('briefs_generated_total', 'Total briefs generated')
PUBLISH_SUCCESS = Counter('publish_success_total', 'Successful publishes', ['channel'])
PUBLISH_FAILURE = Counter('publish_failure_total', 'Failed publishes', ['channel'])

# 性能指标
COLLECTION_DURATION = Histogram('collection_duration_seconds', 'Time spent collecting news', ['source'])
PROCESSING_DURATION = Histogram('processing_duration_seconds', 'Time spent processing')
PUBLISH_DURATION = Histogram('publish_duration_seconds', 'Time spent publishing', ['channel'])

# 系统指标
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')

def get_metrics():
    """获取所有指标数据"""
    return generate_latest()
```

## 🔄 备份策略

### 数据库备份

```bash
# 创建备份脚本
cat > /opt/ai-daily-brief/backup.sh << 'EOF'
#!/bin/bash

# 数据库备份
BACKUP_DIR="/opt/ai-daily-brief/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# PostgreSQL 备份
pg_dump -U brief_user -h localhost ai_daily_brief > $BACKUP_DIR/db_$DATE.sql

# Redis 备份
redis-cli save
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# 文件备份
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /opt/ai-daily-brief/data/

# 清理7天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "备份完成: $DATE"
EOF

# 设置可执行权限
chmod +x /opt/ai-daily-brief/backup.sh

# 设置定时备份
crontab -e
# 添加: 0 2 * * * /opt/ai-daily-brief/backup.sh >> /opt/ai-daily-brief/logs/backup.log 2>&1
```

### 配置文件备份

```bash
# 备份重要配置
cat > /opt/ai-daily-brief/backup-config.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/ai-daily-brief/config-backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份配置文件
tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
    /opt/ai-daily-brief/config/ \
    /opt/ai-daily-brief/.env \
    /etc/nginx/sites-available/ai-daily-brief \
    /etc/systemd/system/ai-daily-brief.service

echo "配置备份完成: $DATE"
EOF

chmod +x /opt/ai-daily-brief/backup-config.sh
```

## 🚀 部署验证

### 健康检查

```bash
# 检查服务状态
sudo systemctl status ai-daily-brief
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis

# 检查端口监听
netstat -tlnp | grep :8000
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# 测试应用
curl -k https://your-domain.com/health
curl -k https://your-domain.com/api/v1/stats/overview
```

### 功能测试

```bash
# 测试新闻收集
curl -X POST https://your-domain.com/api/v1/collect \
  -H "Authorization: Bearer YOUR_API_KEY"

# 测试简报生成
curl -X POST https://your-domain.com/api/v1/briefs \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-01-17"}'
```

### 性能测试

```bash
# 使用 Apache Bench 进行压力测试
ab -n 1000 -c 10 https://your-domain.com/api/v1/news

# 使用 wrk 进行并发测试
wrk -t12 -c400 -d30s https://your-domain.com/api/v1/news
```

## 🔄 更新部署

### 滚动更新

```bash
# 创建更新脚本
cat > /opt/ai-daily-brief/update.sh << 'EOF'
#!/bin/bash

echo "开始更新 AI Daily Brief..."

# 备份当前版本
cp -r /opt/ai-daily-brief /opt/ai-daily-brief.backup.$(date +%s)

# 拉取最新代码
cd /opt/ai-daily-brief
git pull origin main

# 安装新依赖
source venv/bin/activate
pip install -r requirements.txt

# 运行数据库迁移
python src/manage.py db upgrade

# 重启应用
sudo systemctl restart ai-daily-brief

# 等待服务启动
sleep 10

# 健康检查
if curl -f https://your-domain.com/health; then
    echo "更新成功！"
    # 清理旧备份（保留最新的3个）
    ls -t /opt/ai-daily-brief.backup.* | tail -n +4 | xargs rm -rf
else
    echo "更新失败，正在回滚..."
    # 回滚逻辑
    sudo systemctl stop ai-daily-brief
    rm -rf /opt/ai-daily-brief
    mv /opt/ai-daily-brief.backup.* /opt/ai-daily-brief
    sudo systemctl start ai-daily-brief
    echo "已回滚到上一版本"
fi
EOF

chmod +x /opt/ai-daily-brief/update.sh
```

## 📞 故障排除

### 常见问题

#### 应用无法启动
```bash
# 检查日志
sudo journalctl -u ai-daily-brief -f

# 检查端口占用
lsof -i :8000

# 检查配置文件
python -c "import src.main; print('配置正确')"
```

#### 数据库连接问题
```bash
# 测试数据库连接
psql -U brief_user -d ai_daily_brief -h localhost -c "SELECT version();"

# 检查数据库日志
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### 内存不足
```bash
# 监控内存使用
free -h
htop

# 增加 swap 空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
