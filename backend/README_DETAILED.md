# AI冷笑话生成器后端服务 - 详细文档

## 📋 项目概述

AI冷笑话生成器后端服务是一个基于FastAPI框架开发的现代化Web API服务，集成了阿里千问大模型，为微信小程序提供智能笑话生成功能。

## 🏗️ 系统架构

### 技术栈
- **Web框架**: FastAPI 0.104+
- **数据库**: SQLAlchemy 2.0 + SQLite/MySQL
- **缓存**: Redis
- **AI服务**: 阿里千问DashScope API
- **异步HTTP**: httpx
- **日志**: loguru
- **测试**: pytest + pytest-asyncio
- **代码质量**: black + isort + flake8 + mypy

### 项目结构
```
backend/
├── app/                    # 应用核心代码
│   ├── api/               # API路由层
│   │   └── v1/           # API v1版本
│   │       ├── jokes.py  # 笑话相关接口
│   │       ├── users.py  # 用户相关接口
│   │       └── admin.py  # 管理员接口
│   ├── core/             # 核心配置和工具
│   │   ├── config.py     # 配置管理
│   │   ├── exceptions.py # 自定义异常
│   │   ├── middleware.py # 中间件
│   │   ├── response.py   # 统一响应格式
│   │   └── logging.py    # 日志配置
│   ├── db/               # 数据库相关
│   │   ├── base.py       # 数据库基类
│   │   └── session.py    # 数据库会话
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── joke.py       # 笑话模型
│   │   ├── share.py      # 分享记录模型
│   │   └── preference.py # 用户偏好模型
│   ├── schemas/          # Pydantic数据验证模型
│   │   ├── user.py       # 用户相关模型
│   │   └── joke.py       # 笑话相关模型
│   ├── services/         # 业务逻辑层
│   │   ├── ai_service.py    # AI服务
│   │   ├── joke_service.py  # 笑话服务
│   │   ├── user_service.py  # 用户服务
│   │   ├── share_service.py # 分享服务
│   │   └── cache_service.py # 缓存服务
│   └── main.py           # 应用入口
├── tests/                # 测试代码
├── alembic/              # 数据库迁移
├── logs/                 # 日志文件
├── requirements.txt      # 依赖包
├── pyproject.toml        # 项目配置
├── .env.example          # 环境变量示例
├── Dockerfile            # Docker配置
├── run.py                # 启动脚本
└── init_project.py       # 项目初始化脚本
```

## 🚀 快速开始

### 1. 环境准备
```bash
# Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置
```bash
# 复制环境变量文件
cp .env.example .env

# 编辑配置文件
vim .env
```

### 3. 项目初始化
```bash
# 运行初始化脚本
python init_project.py
```

### 4. 启动服务
```bash
# 开发模式
python run.py

# 或使用uvicorn直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问文档
- API文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 📊 API接口文档

### 笑话相关接口

#### 生成单个笑话
```http
POST /api/v1/jokes/generate
Content-Type: application/json

{
    "category": "程序员",
    "tags": ["编程", "幽默"],
    "length": "medium",
    "temperature": 0.8,
    "custom_prompt": "关于Python的笑话"
}
```

#### 批量生成笑话
```http
POST /api/v1/jokes/batch
Content-Type: application/json

{
    "count": 3,
    "category": "程序员",
    "temperature": 0.8
}
```

#### 获取笑话列表
```http
GET /api/v1/jokes/?page=1&size=10&category=程序员&is_featured=true
```

#### 分享笑话
```http
POST /api/v1/jokes/share
Content-Type: application/json

{
    "joke_id": 1,
    "share_to": "wechat",
    "share_title": "分享一个笑话",
    "share_desc": "这个笑话很有趣"
}
```

### 用户相关接口

#### 创建用户
```http
POST /api/v1/users/
Content-Type: application/json

{
    "openid": "wx_openid_123",
    "nickname": "用户昵称",
    "avatar_url": "https://example.com/avatar.jpg",
    "gender": 1,
    "city": "北京",
    "province": "北京",
    "country": "中国"
}
```

#### 获取用户信息
```http
GET /api/v1/users/{user_id}
GET /api/v1/users/openid/{openid}
```

### 管理员接口

#### 系统健康检查
```http
GET /api/v1/admin/health
```

#### 获取系统统计
```http
GET /api/v1/admin/stats
```

## 🔧 配置说明

### 环境变量配置
```bash
# 项目配置
PROJECT_NAME=AI冷笑话生成器
VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# API配置
SECRET_KEY=your-super-secret-key-here-must-be-at-least-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 服务器配置
HOST=0.0.0.0
PORT=8000
ALLOWED_HOSTS=*

# 阿里千问API配置
QWEN_API_KEY=your_qwen_api_key_here
QWEN_MODEL=qwen-turbo
QWEN_MAX_TOKENS=200
QWEN_TEMPERATURE=0.8

# 数据库配置
DATABASE_URL=sqlite:///./test.db
DATABASE_ECHO=False

# Redis配置
REDIS_URL=redis://localhost:6379/0
REDIS_EXPIRE_TIME=3600

# 限流配置
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_ROTATION=1 day
LOG_RETENTION=30 days

# 缓存配置
CACHE_EXPIRE_TIME=300
ENABLE_CACHE=True

# 监控配置
ENABLE_METRICS=True
METRICS_PATH=/metrics
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python run_tests.py

# 或使用pytest直接运行
pytest tests/ -v --cov=app

# 运行特定测试文件
pytest tests/test_jokes.py -v

# 运行特定测试方法
pytest tests/test_jokes.py::TestJokeAPI::test_generate_joke -v
```

### 测试覆盖率
```bash
# 生成HTML覆盖率报告
pytest tests/ --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

## 📈 性能优化

### 缓存策略
- **笑话缓存**: 生成的笑话缓存5分钟
- **用户信息缓存**: 用户基本信息缓存1小时
- **统计数据缓存**: 统计数据缓存10分钟

### 限流配置
- **笑话生成**: 每分钟10次，每小时100次
- **用户登录**: 每分钟10次
- **分享功能**: 每分钟20次

### 数据库优化
- 使用索引优化查询性能
- 实现连接池管理
- 支持读写分离（生产环境）

## 🔒 安全措施

### API安全
- 请求限流防止滥用
- 输入验证和过滤
- CORS安全配置
- 统一错误处理

### 数据安全
- 敏感信息加密存储
- SQL注入防护
- XSS攻击防护
- 数据备份策略

## 📊 监控和日志

### 日志系统
- 结构化日志记录
- 日志轮转和压缩
- 错误日志单独记录
- 请求链路追踪

### 监控指标
- API响应时间
- 错误率统计
- 用户活跃度
- 系统资源使用

## 🐳 Docker部署

### 构建镜像
```bash
docker build -t ai-joke-generator:latest .
```

### 运行容器
```bash
docker run -d \
  --name ai-joke-generator \
  -p 8000:8000 \
  -e QWEN_API_KEY=your_api_key \
  -e DATABASE_URL=sqlite:///./data/app.db \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-joke-generator:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - QWEN_API_KEY=your_api_key
      - DATABASE_URL=postgresql://user:pass@db:5432/jokes
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=jokes
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔄 数据库迁移

### 创建迁移
```bash
alembic revision --autogenerate -m "Add new table"
```

### 执行迁移
```bash
alembic upgrade head
```

### 回滚迁移
```bash
alembic downgrade -1
```

## 🛠️ 开发指南

### 代码规范
```bash
# 格式化代码
black app/ tests/
isort app/ tests/

# 代码检查
flake8 app/ tests/
mypy app/

# 安装pre-commit钩子
pre-commit install
```

### 添加新功能
1. 在`models/`中定义数据模型
2. 在`schemas/`中定义API模型
3. 在`services/`中实现业务逻辑
4. 在`api/v1/`中添加API接口
5. 编写测试用例
6. 更新文档

## 🚨 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查数据库配置
echo $DATABASE_URL

# 测试数据库连接
python -c "from app.db.session import engine; print(engine.execute('SELECT 1').scalar())"
```

#### 2. Redis连接失败
```bash
# 检查Redis服务
redis-cli ping

# 检查Redis配置
echo $REDIS_URL
```

#### 3. AI API调用失败
```bash
# 检查API密钥
echo $QWEN_API_KEY

# 测试API连接
python -c "from app.services.ai_service import AIService; import asyncio; print(asyncio.run(AIService().test_api_connection()))"
```

### 日志分析
```bash
# 查看错误日志
tail -f logs/error.log

# 查看应用日志
tail -f logs/app.log

# 搜索特定错误
grep "ERROR" logs/app.log | tail -20
```

## 📞 技术支持

如有问题，请通过以下方式联系：
- 提交Issue到项目仓库
- 查看项目文档和FAQ
- 联系开发团队

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。