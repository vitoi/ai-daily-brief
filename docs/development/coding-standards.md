# 代码规范与最佳实践

## 🎯 概述

良好的代码规范是团队协作和项目维护的基础。本文档定义了AI Daily Brief项目的编码标准、命名约定、最佳实践和代码审查准则。

## 📝 代码风格

### Python 代码风格

项目采用 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 作为基础代码风格指南，并使用以下工具进行代码格式化和检查：

- **代码格式化**: [Black](https://black.readthedocs.io/)
- **代码检查**: [flake8](https://flake8.pycqa.org/)
- **类型检查**: [mypy](https://mypy.readthedocs.io/)
- **导入排序**: [isort](https://pycqa.github.io/isort/)

#### Black 配置
```ini
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### flake8 配置
```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    build,
    dist,
    .venv,
    .tox,
    .eggs,
    *.egg
per-file-ignores =
    __init__.py:F401
```

### 代码结构规范

#### 文件结构
```
src/
├── __init__.py
├── main.py                 # 应用入口
├── config.py              # 配置管理
├── database.py            # 数据库相关
├── models/                # 数据模型
│   ├── __init__.py
│   ├── news.py
│   └── brief.py
├── collectors/            # 数据收集器
│   ├── __init__.py
│   ├── base.py
│   ├── rss_collector.py
│   └── api_collector.py
├── processors/            # 数据处理器
├── publishers/            # 发布器
└── utils/                 # 工具函数
    ├── __init__.py
    ├── helpers.py
    └── validators.py
```

#### 包导入
```python
# 标准库导入
import os
import sys
from typing import List, Dict, Optional

# 第三方库导入
import requests
from bs4 import BeautifulSoup
import sqlalchemy as sa

# 本地模块导入
from .base import BaseCollector
from ..models.news import NewsItem
from ..utils.helpers import clean_text
```

## 📏 命名约定

### 类命名
```python
# 正确
class NewsCollector:
class RSSFeedParser:
class ContentProcessor:

# 错误
class news_collector:  # 应使用 PascalCase
class News_Collector:  # 不使用下划线
```

### 函数和方法命名
```python
# 正确
def collect_news_items():
def parse_rss_feed():
def validate_news_item():

# 错误
def CollectNewsItems():  # 应使用 snake_case
def parseRSSFeed():      # 不使用驼峰式
```

### 变量命名
```python
# 正确
news_items = []
current_page = 1
max_retries = 3

# 错误
newsItems = []      # 不使用驼峰式
currentpage = 1     # 单词间应有下划线
MAX_RETRIES = 3     # 常量除外
```

### 常量命名
```python
# 正确
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# 错误
maxRetries = 3      # 应使用大写字母
default_timeout = 30 # 常量应大写
```

## 🔧 代码质量要求

### 类型注解

所有新代码必须使用类型注解：

```python
from typing import List, Dict, Optional, Union

def process_news_items(
    items: List[Dict[str, Union[str, int]]],
    max_items: Optional[int] = None
) -> List[Dict[str, str]]:
    """处理新闻条目列表"""
    pass
```

### 文档字符串

所有公共函数、类和方法必须有文档字符串：

```python
class NewsCollector:
    """新闻收集器基类

    负责从各种数据源收集新闻数据，并进行初步处理和验证。

    Attributes:
        timeout (int): 请求超时时间（秒）
        max_retries (int): 最大重试次数
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """初始化收集器

        Args:
            timeout: 请求超时时间
            max_retries: 最大重试次数
        """
        self.timeout = timeout
        self.max_retries = max_retries

    def collect_news(self, source_url: str) -> List[Dict[str, str]]:
        """从指定源收集新闻

        Args:
            source_url: 数据源URL

        Returns:
            新闻条目列表

        Raises:
            ConnectionError: 网络连接失败
            ValidationError: 数据验证失败
        """
        pass
```

### 错误处理

#### 异常处理原则
```python
# 正确：具体的异常类型
try:
    response = requests.get(url, timeout=self.timeout)
    response.raise_for_status()
except requests.Timeout:
    logger.warning(f"请求超时: {url}")
    raise ConnectionError(f"连接超时: {url}")
except requests.HTTPError as e:
    logger.error(f"HTTP错误: {e}")
    raise ValidationError(f"无效响应: {url}")
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise

# 错误：过于宽泛的异常处理
try:
    # 一些操作
    pass
except:
    pass  # 不记录错误信息
```

#### 自定义异常
```python
# exceptions.py
class AIDailyBriefError(Exception):
    """AI Daily Brief 基础异常"""
    pass

class CollectionError(AIDailyBriefError):
    """数据收集异常"""
    pass

class ProcessingError(AIDailyBriefError):
    """数据处理异常"""
    pass

class PublishingError(AIDailyBriefError):
    """发布异常"""
    pass
```

### 日志记录

#### 日志级别使用
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: 详细的调试信息
logger.debug("处理新闻条目: %s", item_id)

# INFO: 正常操作信息
logger.info("成功收集 %d 条新闻", count)

# WARNING: 警告信息
logger.warning("数据源 %s 响应缓慢", source_url)

# ERROR: 错误信息
logger.error("收集失败: %s", str(e))

# CRITICAL: 严重错误
logger.critical("数据库连接丢失")
```

#### 结构化日志
```python
# 推荐：结构化日志
logger.info("新闻收集完成", extra={
    "source": source_name,
    "count": item_count,
    "duration": duration,
    "status": "success"
})

# 不推荐：字符串格式化
logger.info(f"新闻收集完成: 源={source_name}, 数量={item_count}")
```

## 🧪 测试规范

### 测试文件结构
```
tests/
├── __init__.py
├── conftest.py              # pytest 配置和 fixtures
├── unit/                   # 单元测试
│   ├── test_collectors.py
│   ├── test_processors.py
│   └── test_publishers.py
├── integration/            # 集成测试
│   ├── test_full_pipeline.py
│   └── test_external_apis.py
└── fixtures/               # 测试数据
    ├── sample_news.json
    └── mock_responses.py
```

### 测试用例编写
```python
import pytest
from unittest.mock import Mock, patch
from src.collectors.rss_collector import RSSCollector

class TestRSSCollector:

    @pytest.fixture
    def collector(self):
        return RSSCollector()

    @pytest.fixture
    def mock_feed_data(self):
        return {
            "entries": [
                {
                    "title": "AI News Title",
                    "link": "https://example.com/ai-news",
                    "summary": "AI news summary",
                    "published": "2025-01-17T10:00:00Z"
                }
            ]
        }

    def test_collect_success(self, collector, mock_feed_data):
        """测试成功收集RSS数据"""
        with patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = mock_feed_data

            result = collector.collect("https://example.com/rss")

            assert len(result) == 1
            assert result[0]["title"] == "AI News Title"
            assert result[0]["url"] == "https://example.com/ai-news"

    def test_collect_network_error(self, collector):
        """测试网络错误处理"""
        with patch('feedparser.parse', side_effect=Exception("Network error")):
            with pytest.raises(CollectionError):
                collector.collect("https://example.com/rss")

    @pytest.mark.asyncio
    async def test_collect_with_retry(self, collector):
        """测试重试机制"""
        with patch.object(collector, '_fetch_feed') as mock_fetch:
            mock_fetch.side_effect = [Exception("Temp error"), Mock()]

            await collector.collect_with_retry("https://example.com/rss")

            assert mock_fetch.call_count == 2
```

### 测试覆盖率要求
- **单元测试**: ≥ 80% 覆盖率
- **集成测试**: 核心业务流程全覆盖
- **回归测试**: 所有已知bug的回归测试

## 🔒 安全编码实践

### 输入验证
```python
from pydantic import BaseModel, validator
import re

class NewsSource(BaseModel):
    """新闻源配置模型"""
    name: str
    url: str
    type: str

    @validator('url')
    def validate_url(cls, v):
        """验证URL格式"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(v):
            raise ValueError('Invalid URL format')
        return v

    @validator('type')
    def validate_type(cls, v):
        """验证类型"""
        allowed_types = ['rss', 'api', 'scrape']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of: {allowed_types}')
        return v
```

### 敏感数据处理
```python
import os
from cryptography.fernet import Fernet

class SecretManager:
    """敏感数据管理器"""

    def __init__(self):
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

## 🚀 性能优化

### 异步编程
```python
import asyncio
import aiohttp
from typing import List, Dict

class AsyncNewsCollector:
    """异步新闻收集器"""

    async def collect_multiple_sources(self, sources: List[Dict]) -> List[Dict]:
        """并发收集多个数据源"""

        async def collect_single_source(source):
            async with aiohttp.ClientSession() as session:
                return await self._collect_from_source(session, source)

        # 限制并发数量，避免过载
        semaphore = asyncio.Semaphore(10)

        async def limited_collect(source):
            async with semaphore:
                return await collect_single_source(source)

        tasks = [limited_collect(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果，过滤异常
        valid_results = []
        for result in results:
            if not isinstance(result, Exception):
                valid_results.extend(result)

        return valid_results
```

### 缓存策略
```python
from functools import lru_cache
import redis
import json

class CacheManager:
    """缓存管理器"""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    @lru_cache(maxsize=1000)
    def get_cached_news(self, source_url: str, ttl: int = 3600) -> List[Dict]:
        """获取缓存的新闻数据"""
        cache_key = f"news:{source_url}"

        # 先检查内存缓存（LRU）
        cached = self.get_cache(cache_key)
        if cached:
            return json.loads(cached)

        # 从Redis获取
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached.decode())

        # 缓存未命中，从源获取
        news_data = self._fetch_from_source(source_url)

        # 设置缓存
        self.redis.setex(cache_key, ttl, json.dumps(news_data))

        return news_data
```

## 📋 代码审查清单

### 功能完整性
- [ ] 代码实现预期的功能
- [ ] 错误处理完善
- [ ] 边界条件考虑充分
- [ ] 性能满足要求

### 代码质量
- [ ] 遵循代码规范
- [ ] 有完整的类型注解
- [ ] 有详细的文档字符串
- [ ] 通过所有linting检查

### 测试覆盖
- [ ] 有对应的单元测试
- [ ] 测试覆盖边界条件
- [ ] 测试覆盖错误场景
- [ ] 测试代码符合规范

### 安全检查
- [ ] 无敏感信息泄露
- [ ] 输入验证完善
- [ ] SQL注入防护
- [ ] XSS防护

### 性能考虑
- [ ] 无明显性能问题
- [ ] 合理使用缓存
- [ ] 异步处理合适
- [ ] 资源使用合理

## 📚 参考资料

- [PEP 8 - Python代码风格指南](https://www.python.org/dev/peps/pep-0008/)
- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Effective Python](https://effectivepython.com/)

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
