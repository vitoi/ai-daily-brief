# 配置参考

## 📋 配置文件概述

AI Daily Brief 支持多种配置方式，按优先级从高到低：

1. **环境变量** (最高优先级)
2. **配置文件** (`config/config.json`)
3. **默认值** (最低优先级)

## 🔧 核心配置

### 应用配置

```json
{
  "app": {
    "name": "AI Daily Brief",
    "version": "1.0.0",
    "debug": false,
    "log_level": "INFO",
    "secret_key": "your-secret-key-here"
  }
}
```

**环境变量**:
```bash
APP_NAME="AI Daily Brief"
APP_VERSION="1.0.0"
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY="your-secret-key-here"
```

### 数据库配置

```json
{
  "database": {
    "url": "postgresql://user:password@localhost:5432/ai_daily_brief",
    "pool_size": 10,
    "max_overflow": 20,
    "pool_timeout": 30,
    "pool_recycle": 3600
  }
}
```

**环境变量**:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/ai_daily_brief"
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

**支持的数据库**:
- PostgreSQL (推荐生产环境)
- MySQL
- SQLite (开发环境)

### Redis 配置

```json
{
  "redis": {
    "url": "redis://localhost:6379/0",
    "db": 0,
    "password": null,
    "socket_timeout": 5,
    "socket_connect_timeout": 5,
    "socket_keepalive": true,
    "socket_keepalive_options": {
      "TCP_KEEPIDLE": 60,
      "TCP_KEEPINTVL": 30,
      "TCP_KEEPCNT": 3
    },
    "health_check_interval": 30
  }
}
```

**环境变量**:
```bash
REDIS_URL="redis://localhost:6379/0"
REDIS_DB=0
REDIS_PASSWORD=""
```

## 📡 外部服务配置

### Twitter API 配置

```json
{
  "twitter": {
    "consumer_key": "your_consumer_key",
    "consumer_secret": "your_consumer_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret",
    "bearer_token": "your_bearer_token",
    "timeout": 30,
    "max_retries": 3,
    "rate_limit_wait": true
  }
}
```

**获取 Twitter API 密钥**:
1. 访问 [Twitter Developer Portal](https://developer.twitter.com/)
2. 创建应用或选择现有应用
3. 在 "Keys and Tokens" 页面获取凭据

**环境变量**:
```bash
TWITTER_CONSUMER_KEY="your_key"
TWITTER_CONSUMER_SECRET="your_secret"
TWITTER_ACCESS_TOKEN="your_token"
TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"
TWITTER_BEARER_TOKEN="your_bearer_token"
```

### 邮件服务配置

#### SMTP 配置
```json
{
  "email": {
    "provider": "smtp",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your_email@gmail.com",
    "password": "your_app_password",
    "use_tls": true,
    "use_ssl": false,
    "timeout": 30,
    "from_email": "noreply@yourdomain.com",
    "from_name": "AI Daily Brief"
  }
}
```

#### SendGrid 配置
```json
{
  "email": {
    "provider": "sendgrid",
    "api_key": "your_sendgrid_api_key",
    "from_email": "noreply@yourdomain.com",
    "from_name": "AI Daily Brief",
    "timeout": 30
  }
}
```

**环境变量**:
```bash
EMAIL_PROVIDER="smtp"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
EMAIL_FROM="noreply@yourdomain.com"
EMAIL_FROM_NAME="AI Daily Brief"
```

### GitHub 配置

```json
{
  "github": {
    "token": "your_github_token",
    "timeout": 30,
    "webhook_secret": "your_webhook_secret"
  }
}
```

**环境变量**:
```bash
GITHUB_TOKEN="your_token"
GITHUB_WEBHOOK_SECRET="your_secret"
```

## 📰 新闻源配置

### RSS 源配置

```json
{
  "news_sources": {
    "techcrunch": {
      "name": "TechCrunch AI",
      "type": "rss",
      "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
      "enabled": true,
      "priority": "high",
      "update_interval": 3600,
      "timeout": 30,
      "max_retries": 3,
      "headers": {
        "User-Agent": "AI Daily Brief/1.0"
      }
    }
  }
}
```

### API 源配置

```json
{
  "news_sources": {
    "arxiv": {
      "name": "arXiv AI",
      "type": "api",
      "base_url": "http://export.arxiv.org/api/query",
      "method": "GET",
      "params": {
        "search_query": "cat:cs.AI",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 100
      },
      "enabled": true,
      "priority": "high",
      "update_interval": 7200,
      "timeout": 60,
      "auth": {
        "type": "none"
      }
    }
  }
}
```

### 网页爬虫配置

```json
{
  "news_sources": {
    "zdnet": {
      "name": "ZDNet AI",
      "type": "scraper",
      "url": "https://www.zdnet.com/topic/artificial-intelligence/",
      "enabled": true,
      "priority": "medium",
      "update_interval": 1800,
      "selectors": {
        "article": "article",
        "title": "h3 a, h4 a",
        "link": "h3 a, h4 a",
        "date": "time",
        "summary": "p.summary, p"
      },
      "timeout": 30,
      "max_retries": 3,
      "respect_robots": true,
      "user_agent": "AI Daily Brief/1.0 (https://github.com/vitoi/ai-daily-brief)"
    }
  }
}
```

## ⚙️ 功能配置

### 简报生成配置

```json
{
  "brief": {
    "max_news_per_brief": 50,
    "min_news_per_brief": 5,
    "categories": {
      "research": {
        "enabled": true,
        "max_items": 15,
        "keywords": ["research", "paper", "study", "algorithm"]
      },
      "industry": {
        "enabled": true,
        "max_items": 15,
        "keywords": ["company", "product", "launch", "partnership"]
      },
      "startups": {
        "enabled": true,
        "max_items": 10,
        "keywords": ["startup", "funding", "raise", "venture"]
      },
      "policy": {
        "enabled": true,
        "max_items": 10,
        "keywords": ["regulation", "policy", "law", "government"]
      }
    },
    "summary_length": 200,
    "auto_publish": true,
    "publish_channels": ["email", "twitter"]
  }
}
```

### 缓存配置

```json
{
  "cache": {
    "enabled": true,
    "ttl": {
      "news": 3600,
      "brief": 7200,
      "stats": 1800
    },
    "max_memory": "256mb",
    "compression": true,
    "key_prefix": "aidb:"
  }
}
```

### 任务队列配置

```json
{
  "celery": {
    "broker_url": "redis://localhost:6379/1",
    "result_backend": "redis://localhost:6379/2",
    "timezone": "UTC",
    "enable_utc": true,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "result_expires": 3600,
    "worker_prefetch_multiplier": 1,
    "task_acks_late": true,
    "worker_max_tasks_per_child": 1000
  }
}
```

## 🔒 安全配置

### API 安全

```json
{
  "security": {
    "api_keys": {
      "enabled": true,
      "header_name": "X-API-Key",
      "rate_limit": "1000/hour"
    },
    "jwt": {
      "secret_key": "your-jwt-secret",
      "algorithm": "HS256",
      "access_token_expire_minutes": 30,
      "refresh_token_expire_days": 7
    },
    "cors": {
      "enabled": true,
      "origins": ["https://yourdomain.com"],
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "headers": ["*"],
      "credentials": true
    }
  }
}
```

### 数据加密

```json
{
  "encryption": {
    "enabled": true,
    "key": "your-32-byte-encryption-key",
    "algorithm": "AES-256-GCM",
    "sensitive_fields": [
      "password",
      "api_key",
      "secret_token"
    ]
  }
}
```

## 📊 监控配置

### Prometheus 监控

```json
{
  "monitoring": {
    "prometheus": {
      "enabled": true,
      "port": 9090,
      "metrics_path": "/metrics"
    },
    "metrics": {
      "collect_system_metrics": true,
      "collect_business_metrics": true,
      "histogram_buckets": [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
    }
  }
}
```

### 日志配置

```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": [
      {
        "type": "file",
        "filename": "logs/ai-daily-brief.log",
        "max_bytes": 10485760,
        "backup_count": 5
      },
      {
        "type": "console",
        "level": "WARNING"
      }
    ],
    "loggers": {
      "src.collectors": "DEBUG",
      "src.publishers": "INFO",
      "requests": "WARNING",
      "urllib3": "WARNING"
    }
  }
}
```

## 🚀 部署配置

### Docker 配置

```json
{
  "docker": {
    "image": "ai-daily-brief:latest",
    "build": {
      "context": ".",
      "dockerfile": "Dockerfile"
    },
    "ports": ["8000:8000"],
    "environment": {
      "DEBUG": "false",
      "LOG_LEVEL": "INFO"
    },
    "volumes": [
      "./config:/app/config",
      "./data:/app/data",
      "./logs:/app/logs"
    ],
    "restart": "unless-stopped"
  }
}
```

### Kubernetes 配置

```json
{
  "kubernetes": {
    "namespace": "ai-daily-brief",
    "replicas": 3,
    "resources": {
      "requests": {
        "cpu": "500m",
        "memory": "1Gi"
      },
      "limits": {
        "cpu": "1000m",
        "memory": "2Gi"
      }
    },
    "health_checks": {
      "readiness_probe": {
        "http_get": {
          "path": "/health",
          "port": 8000
        },
        "initial_delay_seconds": 30,
        "period_seconds": 10
      },
      "liveness_probe": {
        "http_get": {
          "path": "/health",
          "port": 8000
        },
        "initial_delay_seconds": 60,
        "period_seconds": 30,
        "failure_threshold": 3
      }
    }
  }
}
```

## 🔧 配置验证

### 配置验证脚本

```python
# config_validator.py
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError, validator

class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = 10
    max_overflow: int = 20

    @validator('url')
    def validate_db_url(cls, v):
        if not v.startswith(('postgresql://', 'mysql://', 'sqlite:///')):
            raise ValueError('Unsupported database URL')
        return v

class AppConfig(BaseModel):
    name: str
    version: str
    debug: bool = False
    database: DatabaseConfig

def validate_config(config_path: str) -> bool:
    """验证配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        # 验证应用配置
        app_config = AppConfig(**config_data)
        print("✅ 配置验证通过")

        return True

    except ValidationError as e:
        print(f"❌ 配置验证失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

if __name__ == "__main__":
    config_path = "config/config.json"
    validate_config(config_path)
```

### 配置热重载

```python
# src/config/manager.py
import json
import time
import threading
from pathlib import Path
from typing import Dict, Any, Callable

class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = {}
        self.callbacks = []
        self.last_modified = 0
        self.load_config()

    def load_config(self):
        """加载配置"""
        if not self.config_path.exists():
            return

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            self.last_modified = self.config_path.stat().st_mtime

    def watch_config(self, interval: int = 5):
        """监控配置文件变化"""
        def watcher():
            while True:
                try:
                    current_mtime = self.config_path.stat().st_mtime
                    if current_mtime > self.last_modified:
                        print("🔄 检测到配置变化，正在重载...")
                        self.load_config()
                        self._notify_callbacks()
                except Exception as e:
                    print(f"配置监控错误: {e}")

                time.sleep(interval)

        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()

    def add_callback(self, callback: Callable):
        """添加配置变化回调"""
        self.callbacks.append(callback)

    def _notify_callbacks(self):
        """通知所有回调"""
        for callback in self.callbacks:
            try:
                callback(self.config)
            except Exception as e:
                print(f"配置回调执行失败: {e}")

    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value
```

## 📋 配置模板

### 完整配置模板

```json
{
  "app": {
    "name": "AI Daily Brief",
    "version": "1.0.0",
    "debug": false,
    "log_level": "INFO",
    "secret_key": "change-this-in-production"
  },
  "database": {
    "url": "postgresql://user:password@localhost:5432/ai_daily_brief",
    "pool_size": 10,
    "max_overflow": 20
  },
  "redis": {
    "url": "redis://localhost:6379/0"
  },
  "twitter": {
    "consumer_key": "your_consumer_key",
    "consumer_secret": "your_consumer_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
  },
  "email": {
    "provider": "smtp",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your_email@gmail.com",
    "password": "your_app_password",
    "from_email": "noreply@yourdomain.com"
  },
  "brief": {
    "max_news_per_brief": 50,
    "categories": {
      "research": {"enabled": true, "max_items": 15},
      "industry": {"enabled": true, "max_items": 15},
      "startups": {"enabled": true, "max_items": 10},
      "policy": {"enabled": true, "max_items": 10}
    },
    "auto_publish": true,
    "publish_channels": ["email", "twitter"]
  },
  "cache": {
    "enabled": true,
    "ttl": {"news": 3600, "brief": 7200}
  },
  "security": {
    "api_keys": {"enabled": true},
    "cors": {"enabled": true, "origins": ["https://yourdomain.com"]}
  },
  "monitoring": {
    "prometheus": {"enabled": true, "port": 9090}
  }
}
```

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
