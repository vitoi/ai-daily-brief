# 测试规范与策略

## 🎯 测试概述

### 测试目标
- **质量保证**: 确保代码功能正确，满足业务需求
- **缺陷预防**: 在开发早期发现和修复问题
- **回归保护**: 防止新功能破坏现有功能
- **文档作用**: 测试用例作为代码使用示例
- **重构保障**: 支持代码重构和优化

### 测试策略
采用**测试金字塔**模型，结合自动化测试：
- **单元测试**: 80% 覆盖率，核心业务逻辑
- **集成测试**: API接口和组件间交互
- **端到端测试**: 完整业务流程
- **性能测试**: 系统性能和稳定性

## 📊 测试类型详解

### 1. 单元测试 (Unit Tests)

#### 目标
测试单个函数、方法或类的行为，隔离外部依赖。

#### 适用场景
- 业务逻辑计算
- 数据转换和验证
- 工具函数
- 错误处理

#### 示例
```python
# tests/unit/test_news_processor.py
import pytest
from unittest.mock import Mock
from src.processors.news_processor import NewsProcessor

class TestNewsProcessor:

    @pytest.fixture
    def processor(self):
        return NewsProcessor()

    @pytest.fixture
    def sample_news(self):
        return {
            'title': 'AI Breakthrough in Machine Learning',
            'content': 'Researchers announce new ML technique...',
            'url': 'https://example.com/ai-news',
            'published_at': '2025-01-17T10:00:00Z'
        }

    def test_categorize_ai_news(self, processor, sample_news):
        """测试AI新闻分类"""
        category = processor.categorize_news(sample_news)

        assert category == 'research'
        assert 'AI' in processor.extract_keywords(sample_news['content'])

    def test_extract_keywords_success(self, processor, sample_news):
        """测试关键词提取"""
        keywords = processor.extract_keywords(sample_news['content'])

        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert 'AI' in keywords

    def test_categorize_empty_content(self, processor):
        """测试空内容处理"""
        with pytest.raises(ValueError, match="Content cannot be empty"):
            processor.categorize_news({'title': '', 'content': ''})

    @pytest.mark.parametrize("title,expected_category", [
        ("New AI Model Released", "research"),
        ("Company Launches AI Product", "industry"),
        ("AI Startup Raises Funding", "startups"),
        ("Government AI Regulations", "policy"),
    ])
    def test_categorize_different_types(self, processor, title, expected_category):
        """测试不同类型新闻分类"""
        news = {'title': title, 'content': f'Details about {title}'}
        category = processor.categorize_news(news)

        assert category == expected_category
```

### 2. 集成测试 (Integration Tests)

#### 目标
测试多个组件之间的交互，验证数据流和接口契约。

#### 适用场景
- 数据库操作
- 外部API调用
- 消息队列
- 文件系统操作

#### 示例
```python
# tests/integration/test_news_collection_flow.py
import pytest
from unittest.mock import patch, MagicMock
from src.collectors.news_collector import NewsCollector
from src.database import get_db_session

class TestNewsCollectionFlow:

    @pytest.fixture
    def db_session(self):
        """数据库会话fixture"""
        session = get_db_session()
        yield session
        session.rollback()  # 测试后回滚

    @pytest.fixture
    def mock_rss_response(self):
        """模拟RSS响应"""
        return {
            'entries': [
                {
                    'title': 'AI News Title',
                    'link': 'https://example.com/ai-news',
                    'summary': 'AI news summary',
                    'published': '2025-01-17T10:00:00Z'
                }
            ]
        }

    @patch('feedparser.parse')
    def test_full_collection_flow(self, mock_parse, db_session, mock_rss_response):
        """测试完整新闻收集流程"""
        # 准备模拟数据
        mock_parse.return_value = mock_rss_response

        # 执行收集
        collector = NewsCollector()
        news_items = collector.collect_from_rss('https://example.com/rss')

        # 验证收集结果
        assert len(news_items) == 1
        assert news_items[0]['title'] == 'AI News Title'

        # 验证数据库存储
        saved_news = db_session.query(News).filter_by(
            url='https://example.com/ai-news'
        ).first()
        assert saved_news is not None
        assert saved_news.title == 'AI News Title'

    @patch('requests.get')
    def test_api_collection_with_retries(self, mock_get, db_session):
        """测试API收集的重试机制"""
        # 模拟网络错误然后成功
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': []}
        mock_get.side_effect = [
            requests.ConnectionError("Network error"),
            mock_response
        ]

        collector = NewsCollector()
        with patch.object(collector, '_fetch_from_api') as mock_fetch:
            mock_fetch.return_value = []

            # 应该自动重试
            result = collector.collect_from_api('https://api.example.com/news')

            assert mock_fetch.call_count == 2  # 重试一次
            assert result == []
```

### 3. 端到端测试 (E2E Tests)

#### 目标
测试完整用户旅程，从前端到后端的全流程验证。

#### 适用场景
- 用户注册登录
- 新闻浏览和订阅
- 简报生成和发布
- 管理后台操作

#### 示例
```python
# tests/e2e/test_user_journey.py
import pytest
from playwright.sync_api import Page
from src.test_helpers import TestClient, create_test_user

class TestUserJourney:

    @pytest.fixture
    def test_client(self):
        """测试客户端"""
        return TestClient()

    @pytest.fixture
    def test_user(self, test_client):
        """测试用户"""
        return create_test_user(test_client, "test@example.com")

    def test_complete_news_workflow(self, test_client, test_user):
        """测试完整新闻工作流"""

        # 1. 用户登录
        response = test_client.login(test_user.email, "password")
        assert response.status_code == 200
        token = response.json()['token']

        # 2. 配置新闻源
        sources_config = {
            "name": "Test Source",
            "url": "https://example.com/rss",
            "type": "rss"
        }
        response = test_client.post(
            "/api/v1/sources",
            json=sources_config,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        source_id = response.json()['id']

        # 3. 触发新闻收集
        response = test_client.post(
            f"/api/v1/sources/{source_id}/collect",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

        # 4. 查看收集的新闻
        response = test_client.get(
            "/api/v1/news",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        news_data = response.json()
        assert len(news_data['data']['news']) > 0

        # 5. 生成简报
        response = test_client.post(
            "/api/v1/briefs",
            json={"date": "2025-01-17"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        brief_id = response.json()['id']

        # 6. 发布简报
        response = test_client.post(
            f"/api/v1/briefs/{brief_id}/publish",
            json={"channels": ["email"]},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

        # 7. 验证发布结果
        response = test_client.get(
            f"/api/v1/briefs/{brief_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        brief = response.json()
        assert brief['published'] is True
```

### 4. 性能测试 (Performance Tests)

#### 目标
验证系统在高负载下的性能表现和稳定性。

#### 指标
- **响应时间**: API响应时间 < 500ms
- **吞吐量**: 支持 1000+ 请求/分钟
- **并发用户**: 支持 100+ 并发用户
- **资源使用**: CPU < 80%, 内存 < 80%

#### 示例
```python
# tests/performance/test_api_performance.py
import pytest
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from src.test_helpers import PerformanceTestClient

class TestAPIPerformance:

    @pytest.fixture
    def perf_client(self):
        """性能测试客户端"""
        return PerformanceTestClient(base_url="http://localhost:8000")

    def test_news_api_response_time(self, perf_client):
        """测试新闻API响应时间"""
        start_time = time.time()

        response = perf_client.get("/api/v1/news?page=1&per_page=20")
        response_time = time.time() - start_time

        assert response.status_code == 200
        assert response_time < 0.5  # 500ms以内

    def test_concurrent_news_collection(self, perf_client):
        """测试并发新闻收集"""

        def collect_news():
            response = perf_client.post("/api/v1/collect")
            return response.status_code == 200

        # 模拟10个并发请求
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda _: collect_news(), range(10)))

        success_count = sum(results)
        assert success_count >= 8  # 至少80%成功率

    @pytest.mark.slow
    def test_sustained_load(self, perf_client):
        """测试持续负载"""
        import locust

        # 使用 Locust 进行负载测试
        # 这里可以配置更复杂的负载测试场景

        # 模拟持续10分钟的负载
        duration = 10 * 60  # 10分钟
        start_time = time.time()

        while time.time() - start_time < duration:
            response = perf_client.get("/api/v1/news")
            assert response.status_code == 200

            # 检查系统资源使用
            cpu_usage = perf_client.get_system_cpu()
            memory_usage = perf_client.get_system_memory()

            assert cpu_usage < 80
            assert memory_usage < 80

            time.sleep(1)  # 1秒间隔
```

## 🛠️ 测试工具与框架

### 核心工具
```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 主要测试工具
pytest==7.4.0          # 测试框架
pytest-cov==4.1.0      # 覆盖率报告
pytest-mock==3.11.1    # Mock工具
playwright==1.37.0     # E2E测试
locust==2.15.1         # 性能测试
```

### 测试配置
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml
markers =
    slow: 标记慢速测试
    integration: 标记集成测试
    e2e: 标记端到端测试
    performance: 标记性能测试
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### 测试数据管理
```python
# tests/conftest.py
import pytest
import os
from src.database import init_db, get_db_session
from src.config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """设置测试数据库"""
    # 使用测试数据库
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'

    # 初始化数据库
    init_db()

    yield

    # 清理测试数据
    os.remove('test.db')

@pytest.fixture
def db_session():
    """数据库会话fixture"""
    session = get_db_session()
    yield session
    session.rollback()

@pytest.fixture
def api_client():
    """API客户端fixture"""
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)

@pytest.fixture
def sample_news_data():
    """示例新闻数据"""
    return {
        'title': 'Test AI News',
        'content': 'This is a test news article about AI...',
        'url': 'https://example.com/test-news',
        'source': 'Test Source',
        'published_at': '2025-01-17T10:00:00Z'
    }
```

## 📊 测试覆盖率

### 覆盖率目标
- **整体覆盖率**: ≥ 80%
- **核心模块**: ≥ 90%
- **新功能**: 100%

### 覆盖率报告
```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html --cov-report=term-missing

# 查看HTML报告
open htmlcov/index.html

# 生成XML报告（CI/CD使用）
pytest --cov=src --cov-report=xml
```

### 覆盖率配置
```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

## 🔄 测试流程

### 开发阶段
1. **编写测试**: TDD/BDD 方式编写测试
2. **运行测试**: 本地运行相关测试
3. **代码审查**: 包含测试的代码审查
4. **持续集成**: 推送到 CI 后自动运行

### CI/CD 流程
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 发布检查
```bash
# 发布前检查脚本
#!/bin/bash

echo "=== 发布前检查 ==="

# 1. 运行所有测试
echo "运行测试..."
pytest --tb=short
if [ $? -ne 0 ]; then
    echo "❌ 测试失败，不能发布"
    exit 1
fi

# 2. 检查覆盖率
echo "检查覆盖率..."
pytest --cov=src --cov-report=term-missing | grep "TOTAL" | awk '{if ($4 < 80) exit 1}'
if [ $? -ne 0 ]; then
    echo "❌ 覆盖率不足，不能发布"
    exit 1
fi

# 3. 代码质量检查
echo "代码质量检查..."
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
if [ $? -ne 0 ]; then
    echo "❌ 代码质量问题，不能发布"
    exit 1
fi

echo "✅ 所有检查通过，可以发布"
```

## 🐛 调试与故障排除

### 调试技巧
```python
# 在测试中使用断点
import pdb; pdb.set_trace()

# 使用丰富的断言
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert "AI" in news.title, f"Title should contain 'AI': {news.title}"

# 记录详细的测试信息
def test_with_logging(caplog):
    caplog.set_level(logging.DEBUG)
    # 测试代码...
    assert "Expected message" in caplog.text
```

### Mock 策略
```python
# 外部API Mock
@patch('src.collectors.twitter_collector.TwitterAPI')
def test_twitter_publishing(mock_twitter):
    mock_twitter.post_tweet.return_value = {'id': '123', 'text': 'Test tweet'}

    publisher = TwitterPublisher()
    result = publisher.publish("Test content")

    assert result.success is True
    mock_twitter.post_tweet.assert_called_once_with("Test content")

# 数据库Mock
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    return session
```

### 测试数据管理
```python
# tests/fixtures/news_data.py
import json
from pathlib import Path

def load_test_news_data(filename):
    """加载测试新闻数据"""
    path = Path(__file__).parent / 'data' / filename
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# tests/fixtures/__init__.py
from .news_data import load_test_news_data

__all__ = ['load_test_news_data']
```

## 📈 测试指标监控

### 测试健康指标
- **测试通过率**: 目标 > 95%
- **测试执行时间**: 每次提交 < 10分钟
- **覆盖率变化**: 新代码覆盖率不下降
- **失败测试数**: < 5个

### 质量门禁
```python
# tests/quality_gate.py
def check_quality_gate():
    """质量门禁检查"""
    import subprocess
    import xml.etree.ElementTree as ET

    # 运行测试并生成报告
    result = subprocess.run(['pytest', '--junitxml=report.xml', '--cov=src', '--cov-report=xml'])

    if result.returncode != 0:
        raise Exception("测试失败")

    # 解析覆盖率报告
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    coverage = float(root.attrib['line-rate']) * 100

    if coverage < 80:
        raise Exception(f"覆盖率不足: {coverage}% < 80%")

    print(f"✅ 质量门禁通过 - 覆盖率: {coverage}%")
```

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
