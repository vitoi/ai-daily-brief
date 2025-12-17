# API 设计与接口规范

## 📋 概述

AI Daily Brief 提供 RESTful API 接口，支持外部系统集成、数据查询和自动化操作。本文档定义了API的设计原则、接口规范和使用指南。

## 🎯 设计原则

### RESTful 设计
- **资源导向**: 使用名词表示资源，HTTP方法表示操作
- **无状态**: 每个请求都是独立的，不依赖服务器端会话状态
- **统一接口**: 统一的资源标识和操作方法
- **超媒体驱动**: API响应包含相关资源的链接

### API 版本控制
- **URL路径版本控制**: `/api/v1/`
- **向后兼容**: 新版本API不会破坏现有集成
- **版本弃用**: 废弃版本提前通知，保留至少6个月

### 响应格式
```json
{
  "success": true,
  "data": {},
  "meta": {
    "timestamp": "2025-01-17T10:00:00Z",
    "version": "v1",
    "request_id": "req_123456"
  },
  "links": {
    "self": "/api/v1/news",
    "next": "/api/v1/news?page=2"
  }
}
```

## 🔐 认证授权

### API Key 认证
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.ai-daily-brief.com/v1/news
```

### 请求签名 (推荐用于生产环境)
```python
import hmac
import hashlib
import base64
from datetime import datetime

def generate_signature(api_secret, method, path, timestamp, body=""):
    """生成API请求签名"""
    message = f"{method}{path}{timestamp}{body}"
    signature = hmac.new(
        api_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

# 使用示例
timestamp = str(int(datetime.now().timestamp()))
signature = generate_signature(API_SECRET, "GET", "/v1/news", timestamp)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "X-Timestamp": timestamp,
    "X-Signature": signature
}
```

## 📊 核心API接口

### 新闻管理 API

#### 获取新闻列表
```http
GET /api/v1/news
```

**查询参数:**
- `page` (integer): 页码，默认1
- `per_page` (integer): 每页数量，默认20，最大100
- `category` (string): 分类筛选
- `source` (string): 来源筛选
- `start_date` (string): 开始日期，格式: YYYY-MM-DD
- `end_date` (string): 结束日期，格式: YYYY-MM-DD
- `keyword` (string): 关键词搜索
- `sort` (string): 排序字段，默认: published_at
- `order` (string): 排序方向，默认: desc

**响应示例:**
```json
{
  "success": true,
  "data": {
    "news": [
      {
        "id": "news_123456",
        "title": "Large Language Models Breakthrough",
        "content": "Researchers announce major breakthrough...",
        "summary": "Key findings include...",
        "url": "https://example.com/llm-breakthrough",
        "source": "TechCrunch",
        "category": "research",
        "tags": ["LLM", "AI", "Machine Learning"],
        "quality_score": 0.95,
        "published_at": "2025-01-17T09:00:00Z",
        "collected_at": "2025-01-17T09:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 156,
      "total_pages": 8
    }
  },
  "meta": {
    "timestamp": "2025-01-17T10:00:00Z",
    "version": "v1",
    "request_id": "req_abc123"
  },
  "links": {
    "self": "/api/v1/news?page=1",
    "next": "/api/v1/news?page=2",
    "prev": null
  }
}
```

#### 获取单条新闻
```http
GET /api/v1/news/{news_id}
```

#### 创建新闻 (管理员)
```http
POST /api/v1/news
Content-Type: application/json

{
  "title": "Custom News Title",
  "content": "News content...",
  "source": "manual",
  "category": "industry"
}
```

#### 更新新闻 (管理员)
```http
PUT /api/v1/news/{news_id}
Content-Type: application/json

{
  "category": "research",
  "tags": ["AI", "ML"]
}
```

#### 删除新闻 (管理员)
```http
DELETE /api/v1/news/{news_id}
```

### 简报管理 API

#### 获取简报列表
```http
GET /api/v1/briefs
```

**查询参数:**
- `date` (string): 指定日期，格式: YYYY-MM-DD
- `status` (string): 状态筛选 (draft, published, archived)

#### 获取最新简报
```http
GET /api/v1/briefs/latest
```

#### 创建简报 (管理员)
```http
POST /api/v1/briefs
Content-Type: application/json

{
  "title": "AI Daily Brief - 2025-01-17",
  "date": "2025-01-17",
  "news_ids": ["news_123", "news_456"],
  "custom_content": "Additional content..."
}
```

#### 发布简报
```http
POST /api/v1/briefs/{brief_id}/publish
Content-Type: application/json

{
  "channels": ["email", "twitter"],
  "recipients": ["user@example.com"]
}
```

### 数据源管理 API

#### 获取数据源列表
```http
GET /api/v1/sources
```

#### 获取数据源详情
```http
GET /api/v1/sources/{source_id}
```

#### 测试数据源连接
```http
POST /api/v1/sources/{source_id}/test
```

#### 更新数据源配置 (管理员)
```http
PUT /api/v1/sources/{source_id}
Content-Type: application/json

{
  "enabled": true,
  "frequency": "hourly",
  "config": {
    "timeout": 30,
    "max_retries": 3
  }
}
```

### 统计分析 API

#### 获取系统统计
```http
GET /api/v1/stats/overview
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "total_news": 15420,
    "news_today": 45,
    "briefs_published": 365,
    "active_sources": 12,
    "categories": {
      "research": 5230,
      "industry": 4560,
      "startups": 3210,
      "policy": 1420
    },
    "sources": {
      "TechCrunch": 2340,
      "MIT Technology Review": 1890,
      "VentureBeat": 1650
    }
  }
}
```

#### 获取趋势分析
```http
GET /api/v1/stats/trends
```

**查询参数:**
- `period` (string): 时间周期 (day, week, month)
- `metric` (string): 指标类型 (news_count, categories, sources)

## 🔄 Webhook 集成

### Webhook 配置
```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["brief.published", "news.collected"],
  "secret": "your_webhook_secret",
  "active": true
}
```

### Webhook 事件类型

#### 简报发布事件
```json
{
  "event": "brief.published",
  "timestamp": "2025-01-17T09:00:00Z",
  "data": {
    "brief_id": "brief_123",
    "title": "AI Daily Brief - 2025-01-17",
    "channels": ["email", "twitter"],
    "recipient_count": 150
  }
}
```

#### 新闻收集事件
```json
{
  "event": "news.collected",
  "timestamp": "2025-01-17T08:30:00Z",
  "data": {
    "source": "TechCrunch",
    "count": 12,
    "quality_score": 0.87,
    "categories": ["research", "industry"]
  }
}
```

### Webhook 安全验证
```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """验证Webhook签名"""
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)
```

## 📊 速率限制

### API 限制
- **免费计划**: 1000 请求/小时
- **专业计划**: 10000 请求/小时
- **企业计划**: 100000 请求/小时

### 响应头
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 3600
```

### 超出限制响应
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "retry_after": 3600
  }
}
```

## 🛡️ 错误处理

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "date",
      "reason": "Invalid date format"
    }
  },
  "meta": {
    "timestamp": "2025-01-17T10:00:00Z",
    "request_id": "req_123456"
  }
}
```

### 常见错误码

| 错误码 | HTTP状态码 | 描述 |
|--------|-----------|------|
| `VALIDATION_ERROR` | 400 | 请求参数无效 |
| `UNAUTHORIZED` | 401 | 未授权访问 |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `RATE_LIMIT_EXCEEDED` | 429 | 超出速率限制 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |

## 📚 SDK 和客户端

### Python SDK
```python
from ai_daily_brief import Client

client = Client(api_key="your_api_key")

# 获取最新新闻
news = client.news.list(page=1, per_page=10)

# 发布简报
brief = client.briefs.create(
    title="Custom Brief",
    news_ids=["news_123", "news_456"]
)
client.briefs.publish(brief.id, channels=["email"])
```

### JavaScript SDK
```javascript
import { AIDailyBrief } from 'ai-daily-brief-sdk';

const client = new AIDailyBrief({
  apiKey: 'your_api_key'
});

// 获取统计数据
const stats = await client.stats.overview();

// 监听Webhook
app.post('/webhook', (req, res) => {
  const event = client.webhooks.verify(req.body, req.headers['x-signature']);
  // 处理事件
});
```

## 🔍 API 调试工具

### 使用 cURL 测试
```bash
# 获取新闻列表
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.ai-daily-brief.com/v1/news?page=1&per_page=5"

# 创建新闻
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test News","content":"Test content"}' \
     https://api.ai-daily-brief.com/v1/news
```

### 使用 Postman
导入 [API Collection](./postman_collection.json) 到 Postman 中进行测试。

## 📈 性能优化

### 分页和限制
- 默认分页大小: 20
- 最大分页大小: 100
- 支持游标分页用于大数据集

### 缓存策略
- API响应缓存5分钟
- 静态资源缓存1小时
- CDN加速全球访问

### 压缩和优化
- Gzip压缩响应
- 图片WebP格式
- 懒加载列表数据

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
