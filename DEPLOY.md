# AI Daily Brief 部署指南

## 系统要求
- Python 3.9+
- pip (Python包管理器)
- Git

## 部署步骤

### 1. 克隆代码
```bash
git clone https://github.com/vitoi/ai-daily-brief.git
cd ai-daily-brief
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置
1. 复制配置文件模板：
```bash
cp config/config.example.json config/config.json
```

2. 编辑 `config/config.json`，填入您的配置信息：
```json
{
    "twitter": {
        "consumer_key": "你的Twitter API Key",
        "consumer_secret": "你的Twitter API Secret",
        "access_token": "你的Twitter Access Token",
        "access_token_secret": "你的Twitter Access Token Secret"
    }
}
```

### 4. 测试运行
```bash
python3 src/main.py
```

### 5. 设置定时任务
使用crontab设置每日自动运行：

1. 编辑crontab：
```bash
crontab -e
```

2. 添加以下行（例如，每天早上8点运行）：
```bash
0 8 * * * cd /path/to/ai-daily-brief && /usr/bin/python3 src/main.py >> /path/to/ai-daily-brief/logs/cron.log 2>&1
```

### 6. 日志管理
1. 创建日志目录：
```bash
mkdir -p logs
```

2. 日志文件：
- 程序日志：`ai_daily_brief.log`
- 定时任务日志：`logs/cron.log`

### 7. 监控和维护
1. 检查日志文件确保程序正常运行
2. 定期检查依赖包更新
3. 确保服务器有足够的磁盘空间存储日志和简报文件

## 故障排除

### 常见问题
1. 依赖安装失败
   - 确保使用正确的Python版本
   - 尝试使用 `pip install --upgrade pip` 更新pip

2. Twitter API错误
   - 检查API密钥是否正确
   - 确认Twitter开发者账号权限设置

3. 定时任务不运行
   - 检查crontab语法
   - 确认Python路径正确
   - 查看cron.log文件

### 日志位置
- 程序日志：`ai_daily_brief.log`
- 定时任务日志：`logs/cron.log`

## 安全建议
1. 确保配置文件权限正确：
```bash
chmod 600 config/config.json
```

2. 定期更新依赖包：
```bash
pip install --upgrade -r requirements.txt
```

3. 定期备份重要数据：
- 配置文件
- 日志文件
- 生成的简报文件

## 更新程序
当有新版本时，可以通过以下步骤更新：

1. 拉取最新代码：
```bash
git pull origin main
```

2. 更新依赖：
```bash
pip install -r requirements.txt
```

3. 重启定时任务：
```bash
crontab -e  # 编辑定时任务
```

## 联系支持
如有问题，请通过以下方式联系：
- GitHub Issues: https://github.com/vitoi/ai-daily-brief/issues
- Email: [您的联系邮箱] 