# 开发环境搭建

## 🛠️ 环境要求

### 系统要求
- **操作系统**: macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **Python版本**: 3.9.0 或更高版本
- **内存**: 至少 4GB RAM
- **磁盘空间**: 至少 2GB 可用空间

### 依赖工具
- **Git**: 版本控制
- **Docker**: (可选) 容器化开发环境
- **VS Code**: (推荐) 开发IDE
- **Postman**: (可选) API测试工具

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/vitoi/ai-daily-brief.git
cd ai-daily-brief
```

### 2. 创建虚拟环境
```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 使用 conda (可选)
conda create -n ai-daily-brief python=3.9
conda activate ai-daily-brief
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

### 5. 初始化数据库
```bash
# 如果使用SQLite (开发环境)
python -c "from src.database import init_db; init_db()"

# 如果使用PostgreSQL (生产环境)
# 请参考部署文档
```

### 6. 运行开发服务器
```bash
# 运行主程序
python src/main.py

# 或运行开发服务器
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 项目结构

```
ai-daily-brief/
├── docs/                    # 项目文档
├── src/                     # 源代码
│   ├── __init__.py
│   ├── main.py             # 应用入口
│   ├── config.py           # 配置管理
│   ├── database.py         # 数据库模型
│   ├── collectors/         # 数据收集器
│   ├── processors/         # 数据处理器
│   ├── publishers/         # 发布器
│   └── utils/              # 工具函数
├── tests/                   # 测试文件
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_processors.py
│   └── test_publishers.py
├── config/                  # 配置文件
│   ├── config.example.json
│   └── news_sources.json
├── scripts/                 # 脚本工具
│   ├── setup.py
│   └── deploy.py
├── requirements.txt         # Python依赖
├── requirements-dev.txt     # 开发依赖
├── Dockerfile               # Docker配置
├── docker-compose.yml       # Docker Compose
├── .env.example             # 环境变量示例
├── .gitignore              # Git忽略文件
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 🔧 开发工具配置

### VS Code 配置

创建 `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.associations": {
        "*.yml": "yaml",
        "*.yaml": "yaml"
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

创建 `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Python: Test",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/"],
            "console": "integratedTerminal"
        }
    ]
}
```

### Pre-commit Hooks

安装 pre-commit:
```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 🧪 测试环境

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_collectors.py

# 运行带覆盖率的测试
pytest --cov=src --cov-report=html

# 运行性能测试
pytest tests/ -k "performance"
```

### 测试配置
`pytest.ini`:
```ini
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
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## 📊 监控与调试

### 日志配置
```python
# src/config/logging.py
import logging
import sys
from pathlib import Path

def setup_logging(level=logging.INFO, log_file=None):
    """设置日志配置"""

    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 文件处理器 (如果指定)
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # 配置根日志器
    logging.basicConfig(
        level=level,
        handlers=handlers
    )

    # 设置第三方库日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
```

### 性能监控
```python
# src/utils/performance.py
import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def measure_performance(func: Callable) -> Callable:
    """性能测量装饰器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"{func.__name__} 执行时间: {execution_time:.2f}秒"
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func.__name__} 执行失败，耗时: {execution_time:.2f}秒，错误: {e}"
            )
            raise

    return wrapper
```

## 🚀 部署开发环境

### 使用 Docker
```bash
# 构建开发镜像
docker build -t ai-daily-brief:dev -f Dockerfile.dev .

# 运行开发容器
docker run -it --rm \
    -v $(pwd):/app \
    -p 8000:8000 \
    ai-daily-brief:dev

# 或使用 docker-compose
docker-compose -f docker-compose.dev.yml up
```

### 使用 VS Code Dev Containers
创建 `.devcontainer/devcontainer.json`:
```json
{
    "name": "AI Daily Brief Dev",
    "dockerFile": "../Dockerfile.dev",
    "extensions": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker"
    ],
    "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true
    },
    "forwardPorts": [8000],
    "postCreateCommand": "pip install -r requirements-dev.txt"
}
```

## 🔍 故障排除

### 常见问题

#### 依赖安装失败
```bash
# 清理缓存
pip cache purge

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 升级 pip
pip install --upgrade pip
```

#### 数据库连接问题
```bash
# 检查数据库服务状态
sudo systemctl status postgresql

# 检查连接配置
python -c "from src.database import test_connection; test_connection()"
```

#### 测试运行失败
```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 运行单个测试调试
pytest tests/test_example.py -v -s
```

## 📚 学习资源

- [Python官方文档](https://docs.python.org/3/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://sqlalchemy.org/)
- [pytest文档](https://docs.pytest.org/)
- [Docker文档](https://docs.docker.com/)

---

*本文档版本: v1.0 | 最后更新: 2025-01-17*
