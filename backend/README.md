# AI冷笑话生成器后端服务

## 项目介绍

AI冷笑话生成器后端服务基于FastAPI框架开发，提供笑话生成和分享功能的API接口。

## 技术栈

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- 阿里千问API

## 项目结构

```
backend/
├── app/                 # 应用核心代码
│   ├── api/            # API路由
│   ├── core/           # 核心配置
│   ├── db/             # 数据库相关
│   ├── models/         # 数据模型
│   ├── schemas/        # 数据验证模型
│   ├── services/       # 业务逻辑
│   └── main.py         # 应用入口
├── requirements.txt     # 依赖包
├── Dockerfile          # Docker配置
└── .env.example        # 环境变量示例
```

## 环境要求

- Python 3.8+
- pip包管理工具

## 安装步骤

1. 克隆项目代码
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   ```
   cp .env.example .env
   # 编辑.env文件，填入实际配置
   ```
4. 启动服务：
   ```
   uvicorn app.main:app --reload
   ```

## API接口

### 生成冷笑话
- **URL**: `/api/v1/jokes/generate`
- **方法**: GET
- **描述**: 调用阿里千问API生成冷笑话

### 分享记录
- **URL**: `/api/v1/jokes/share`
- **方法**: POST
- **描述**: 记录用户分享行为

## Docker部署

```
# 构建镜像
docker build -t ai-joke-generator .

# 运行容器
docker run -d -p 8000:8000 ai-joke-generator
```

## 开发指南

1. 安装开发依赖
2. 配置开发环境
3. 运行开发服务器
4. 编写单元测试

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。