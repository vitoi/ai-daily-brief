# 故障排除指南

## 🔍 问题诊断流程

### 1. 快速诊断检查

运行以下命令进行基础诊断：
```bash
# 1. 检查服务状态
sudo systemctl status ai-daily-brief nginx postgresql redis

# 2. 检查端口监听
netstat -tlnp | grep -E ':(80|443|8000|5432|6379)'

# 3. 检查磁盘空间
df -h

# 4. 检查内存使用
free -h

# 5. 检查最近的日志
tail -50 /opt/ai-daily-brief/logs/ai-daily-brief.log
```

### 2. 日志分析

#### 应用日志位置
```bash
# 应用日志
/opt/ai-daily-brief/logs/ai-daily-brief.log

# 系统日志
sudo journalctl -u ai-daily-brief -f

# Nginx 错误日志
/var/log/nginx/error.log

# PostgreSQL 日志
/var/log/postgresql/postgresql-*.log
```

#### 日志分析命令
```bash
# 搜索错误
grep "ERROR" /opt/ai-daily-brief/logs/ai-daily-brief.log | tail -10

# 统计错误类型
grep "ERROR" /opt/ai-daily-brief/logs/ai-daily-brief.log | \
  sed 's/.*ERROR - //' | sort | uniq -c | sort -nr

# 查看最近1小时的日志
journalctl -u ai-daily-brief --since "1 hour ago"
```

## 🚨 常见问题及解决方案

### 启动问题

#### 问题：应用无法启动
**症状**: `systemctl status ai-daily-brief` 显示失败

**诊断**:
```bash
# 查看详细错误信息
sudo journalctl -u ai-daily-brief -n 50

# 检查 Python 环境
cd /opt/ai-daily-brief
source venv/bin/activate
python -c "import src.main; print('导入成功')"
```

**解决方案**:
```bash
# 1. 检查配置文件
python -c "
import json
with open('config/config.json') as f:
    config = json.load(f)
print('配置有效')
"

# 2. 检查依赖
pip check

# 3. 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 4. 重启服务
sudo systemctl restart ai-daily-brief
```

#### 问题：端口被占用
**症状**: `Address already in use`

**诊断**:
```bash
# 查找占用端口的进程
lsof -i :8000
netstat -tlnp | grep :8000

# 检查是否有其他实例运行
ps aux | grep python
```

**解决方案**:
```bash
# 杀死占用进程
sudo kill -9 <PID>

# 或者更改端口
vim config/config.json
# 修改 port 设置

# 重启服务
sudo systemctl restart ai-daily-brief
```

### 数据库问题

#### 问题：数据库连接失败
**症状**: `psycopg2.OperationalError: connection failed`

**诊断**:
```bash
# 检查 PostgreSQL 服务状态
sudo systemctl status postgresql

# 测试数据库连接
psql -U brief_user -d ai_daily_brief -h localhost -c "SELECT 1;"

# 检查连接配置
grep DATABASE_URL .env
```

**解决方案**:
```bash
# 1. 启动数据库服务
sudo systemctl start postgresql

# 2. 检查数据库是否存在
sudo -u postgres psql -c "SELECT datname FROM pg_database;"

# 3. 重新创建数据库
sudo -u postgres psql
DROP DATABASE IF EXISTS ai_daily_brief;
CREATE DATABASE ai_daily_brief;
GRANT ALL PRIVILEGES ON DATABASE ai_daily_brief TO brief_user;
\q

# 4. 运行迁移
cd /opt/ai-daily-brief
source venv/bin/activate
python src/manage.py db upgrade
```

#### 问题：数据库锁表
**症状**: 查询长时间无响应

**诊断**:
```bash
# 查看活跃查询
psql -U brief_user -d ai_daily_brief -c "SELECT * FROM pg_stat_activity;"

# 查看锁信息
psql -U brief_user -d ai_daily_brief -c "
SELECT
    activity.pid,
    activity.usename,
    activity.query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity AS activity
JOIN pg_stat_activity AS blocking ON blocking.pid = ANY(pg_blocking_pids(activity.pid));
"
```

**解决方案**:
```bash
# 终止阻塞查询
psql -U brief_user -d ai_daily_brief -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND now() - query_start > interval '5 minutes';
"

# 重启数据库（最后手段）
sudo systemctl restart postgresql
```

### 网络问题

#### 问题：无法访问网站
**症状**: HTTP 502/504 错误

**诊断**:
```bash
# 检查 Nginx 状态
sudo systemctl status nginx

# 检查 Nginx 配置
sudo nginx -t

# 检查应用响应
curl http://localhost:8000/health

# 检查防火墙
sudo ufw status
```

**解决方案**:
```bash
# 1. 重载 Nginx 配置
sudo nginx -s reload

# 2. 检查应用日志
sudo journalctl -u ai-daily-brief -n 20

# 3. 重启服务
sudo systemctl restart ai-daily-brief
sudo systemctl restart nginx
```

#### 问题：SSL证书问题
**症状**: HTTPS 证书错误

**诊断**:
```bash
# 检查证书文件
ls -la /etc/ssl/certs/
ls -la /etc/ssl/private/

# 检查证书到期时间
openssl x509 -in /etc/ssl/certs/your-domain.crt -text -noout | grep "Not After"

# 测试 SSL 配置
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

**解决方案**:
```bash
# 续期 Let's Encrypt 证书
sudo certbot renew

# 手动更新证书
sudo systemctl reload nginx

# 检查证书链
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/your-domain.crt
```

### 性能问题

#### 问题：响应缓慢
**症状**: API 响应时间 > 5秒

**诊断**:
```bash
# 检查系统负载
uptime
htop

# 检查数据库性能
psql -U brief_user -d ai_daily_brief -c "SELECT * FROM pg_stat_user_tables;"

# 检查缓存命中率
redis-cli info stats | grep keyspace_hits
redis-cli info stats | grep keyspace_misses

# 性能分析
python -c "
import cProfile
cProfile.run('from src.main import main; main()', 'profile.prof')
"
```

**解决方案**:
```bash
# 1. 增加工作进程
vim /etc/systemd/system/ai-daily-brief.service
# 修改 Environment=WORKERS=8

# 2. 优化数据库查询
# 添加适当的索引
psql -U brief_user -d ai_daily_brief -c "
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_news_published_at
ON news (published_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_news_category
ON news (category);
"

# 3. 增加缓存
# 调整 Redis 配置
vim /etc/redis/redis.conf
# maxmemory 256mb
# maxmemory-policy allkeys-lru

# 4. 重启服务
sudo systemctl daemon-reload
sudo systemctl restart ai-daily-brief
```

#### 问题：内存泄漏
**症状**: 内存使用持续增长

**诊断**:
```bash
# 监控内存使用
ps aux --sort=-%mem | head -10

# 检查 Python 内存使用
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"

# 分析内存泄漏
pip install memory_profiler
python -m memory_profiler src/main.py
```

**解决方案**:
```bash
# 1. 重启应用
sudo systemctl restart ai-daily-brief

# 2. 代码优化
# 使用弱引用
# 及时清理大对象
# 使用生成器而不是列表

# 3. 设置内存限制
vim /etc/systemd/system/ai-daily-brief.service
# 添加: MemoryLimit=512M
# 添加: MemorySwapMax=1G

sudo systemctl daemon-reload
sudo systemctl restart ai-daily-brief
```

### 外部服务问题

#### 问题：Twitter API 错误
**症状**: 发布失败，Twitter相关错误

**诊断**:
```bash
# 检查 API 密钥
grep TWITTER .env

# 测试 API 连接
python -c "
import tweepy
# 测试认证
"

# 检查 API 限制
curl -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
     "https://api.twitter.com/2/users/me"
```

**解决方案**:
```bash
# 1. 检查 API 密钥是否正确
# 访问 https://developer.twitter.com/en/portal/dashboard

# 2. 检查应用权限
# 确保有读写权限

# 3. 处理 API 限制
# 实现重试和退避策略
python -c "
import time
import tweepy

def post_with_retry(content, max_retries=3):
    for attempt in range(max_retries):
        try:
            # 发布推文
            return True
        except tweepy.TooManyRequests:
            wait_time = 2 ** attempt  # 指数退避
            time.sleep(wait_time)
        except Exception as e:
            logger.error(f'发布失败: {e}')
            break
    return False
"
```

#### 问题：邮件发送失败
**症状**: 邮件发布失败

**诊断**:
```bash
# 测试 SMTP 连接
python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('user@gmail.com', 'password')
print('SMTP 连接成功')
"

# 检查邮件配置
grep SMTP .env
```

**解决方案**:
```bash
# 1. 检查 SMTP 设置
# Gmail: smtp.gmail.com:587
# Outlook: smtp-mail.outlook.com:587

# 2. 使用应用密码（Gmail）
# https://support.google.com/accounts/answer/185833

# 3. 检查防火墙
sudo ufw allow out 587
sudo ufw allow out 465
```

### 数据问题

#### 问题：新闻收集失败
**症状**: 收集到的新闻数量为0

**诊断**:
```bash
# 检查网络连接
curl -I https://www.techcrunch.com/

# 测试 RSS 源
curl -s https://techcrunch.com/tag/artificial-intelligence/feed/ | head -20

# 检查新闻源配置
cat config/news_sources.json
```

**解决方案**:
```bash
# 1. 检查 RSS 源是否可访问
curl -I "https://techcrunch.com/tag/artificial-intelligence/feed/"

# 2. 更新新闻源 URL
# 有些网站可能更改了 RSS 地址

# 3. 添加请求头
# 一些网站需要 User-Agent
curl -H "User-Agent: Mozilla/5.0" \
     "https://techcrunch.com/tag/artificial-intelligence/feed/"
```

#### 问题：内容重复
**症状**: 收集到大量重复新闻

**诊断**:
```bash
# 检查去重逻辑
psql -U brief_user -d ai_daily_brief -c "
SELECT url, COUNT(*) as count
FROM news
GROUP BY url
HAVING COUNT(*) > 1
ORDER BY count DESC
LIMIT 10;
"
```

**解决方案**:
```bash
# 1. 改进去重算法
# 使用 URL 规范化
# 使用内容相似度检测

# 2. 清理重复数据
psql -U brief_user -d ai_daily_brief -c "
DELETE FROM news a USING (
    SELECT MIN(id) as id, url
    FROM news
    GROUP BY url HAVING COUNT(*) > 1
) b
WHERE a.url = b.url
AND a.id <> b.id;
"
```

## 🔧 高级故障排除

### 调试模式

#### 启用调试日志
```bash
# 修改环境变量
vim .env
# LOG_LEVEL=DEBUG

# 重启服务
sudo systemctl restart ai-daily-brief
```

#### 使用 Python 调试器
```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或者使用远程调试
pip install debugpy
```

### 系统监控

#### 实时监控脚本
```bash
cat > monitor.sh << 'EOF'
#!/bin/bash

echo "=== 系统状态监控 ==="
echo "时间: $(date)"

echo -e "\n=== 服务状态 ==="
sudo systemctl is-active ai-daily-brief && echo "✅ AI Daily Brief: 运行中" || echo "❌ AI Daily Brief: 停止"
sudo systemctl is-active nginx && echo "✅ Nginx: 运行中" || echo "❌ Nginx: 停止"
sudo systemctl is-active postgresql && echo "✅ PostgreSQL: 运行中" || echo "❌ PostgreSQL: 停止"
sudo systemctl is-active redis && echo "✅ Redis: 运行中" || echo "❌ Redis: 停止"

echo -e "\n=== 资源使用 ==="
echo "内存使用: $(free -h | grep '^Mem:' | awk '{print $3 "/" $2}')"
echo "磁盘使用: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"

echo -e "\n=== 应用指标 ==="
# 检查应用健康状态
curl -s http://localhost:8000/health && echo "✅ 应用健康检查通过" || echo "❌ 应用健康检查失败"

echo -e "\n=== 最近错误 ==="
tail -5 /opt/ai-daily-brief/logs/ai-daily-brief.log | grep ERROR || echo "最近无错误"

EOF

chmod +x monitor.sh
# 运行监控: ./monitor.sh
```

### 恢复策略

#### 数据恢复
```bash
# 从备份恢复数据库
pg_restore -U brief_user -d ai_daily_brief /path/to/backup.sql

# 恢复配置文件
tar -xzf /path/to/config-backup.tar.gz -C /

# 重启服务
sudo systemctl restart ai-daily-brief
```

#### 紧急回滚
```bash
# 停止服务
sudo systemctl stop ai-daily-brief

# 备份当前版本
mv /opt/ai-daily-brief /opt/ai-daily-brief.failed.$(date +%s)

# 恢复上一版本
cp -r /opt/ai-daily-brief.backup.latest /opt/ai-daily-brief

# 启动服务
sudo systemctl start ai-daily-brief
```

## 📞 获取帮助

### 内部资源
- 📖 [项目文档](../README.md)
- 🐛 [问题跟踪](https://github.com/vitoi/ai-daily-brief/issues)
- 💬 [开发讨论](https://github.com/vitoi/ai-daily-brief/discussions)

### 外部资源
- 🔍 [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- 📚 [PostgreSQL文档](https://www.postgresql.org/docs/)
- 🔧 [Nginx文档](https://nginx.org/en/docs/)

### 专业支持
如果以上方法都无法解决问题，请：
1. 收集完整的错误信息和日志
2. 描述问题发生的详细步骤
3. 说明你的环境配置
4. 提交详细的问题报告

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
