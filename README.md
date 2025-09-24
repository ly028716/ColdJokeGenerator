# 🎭 冷笑话生成器 (Cold Joke Generator)

一个基于AI的冷笑话生成应用，包含微信小程序前端和FastAPI后端，支持多种笑话类型生成、历史记录管理和分享功能。

## ✨ 功能特性

### 🎯 核心功能
- **AI笑话生成**：基于阿里千问API生成各类冷笑话
- **多种类型**：支持随机、搞笑、冷笑话、脑筋急转弯等多种类型
- **历史记录**：自动保存生成的笑话，支持本地存储
- **分享功能**：支持笑话分享和收藏
- **网络检测**：智能检测网络状态，提供离线提示

### 🎨 用户体验
- **现代化UI**：简洁美观的界面设计
- **响应式布局**：适配不同屏幕尺寸
- **加载动画**：优雅的加载状态提示
- **错误处理**：完善的错误提示和重试机制
- **备用机制**：网络异常时提供本地备用笑话

## 🏗️ 技术架构

### 前端 (微信小程序)
- **框架**：微信小程序原生开发
- **语言**：JavaScript ES6+
- **样式**：WXSS + Flexbox布局
- **状态管理**：本地存储 + 页面状态管理
- **网络请求**：wx.request封装的API服务

### 后端 (FastAPI)
- **框架**：FastAPI + Python 3.8+
- **数据库**：SQLite + SQLAlchemy ORM
- **AI服务**：阿里千问API集成
- **缓存**：Redis (可选)
- **日志**：结构化日志系统
- **部署**：Uvicorn ASGI服务器

## 📦 项目结构

```
8_ColdJokeGenerator/
├── frontend/                 # 微信小程序前端
│   ├── components/          # 组件库
│   │   ├── joke-card/      # 笑话卡片组件
│   │   ├── loading/        # 加载组件
│   │   └── empty-state/    # 空状态组件
│   ├── pages/              # 页面
│   │   ├── index/          # 首页
│   │   ├── history/        # 历史记录
│   │   ├── category/       # 分类页面
│   │   └── profile/        # 个人中心
│   ├── utils/              # 工具库
│   │   └── api.js          # API封装
│   ├── images/             # 图片资源
│   └── app.js              # 应用入口
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   │   └── v1/         # API版本1
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── services/       # 业务服务
│   ├── alembic/            # 数据库迁移
│   ├── tests/              # 测试用例
│   └── requirements.txt    # Python依赖
└── README.md               # 项目说明
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 14+ (可选，用于开发工具)
- **微信开发者工具**: 最新版本
- **Redis**: 6.0+ (可选，用于缓存)

### 后端部署

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd 8_ColdJokeGenerator/backend
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   # 复制环境变量模板
   cp .env.example .env
   
   # 编辑 .env 文件，配置以下变量：
   # QWEN_API_KEY=your_qwen_api_key_here
   # DATABASE_URL=sqlite:///./test.db
   # REDIS_URL=redis://localhost:6379/0  # 可选
   ```

5. **初始化数据库**
   ```bash
   python init_db.py
   ```

6. **启动服务**
   ```bash
   # 开发环境
   python simple_start.py
   
   # 或使用uvicorn
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 前端部署

1. **打开微信开发者工具**

2. **导入项目**
   - 选择 `frontend` 目录作为项目根目录
   - 填入你的小程序AppID

3. **配置API地址**
   - 编辑 `app.js` 中的 `API_BASE_URL`
   - 开发环境：`http://localhost:8000/api/v1`
   - 生产环境：`https://your-domain.com/api/v1`

4. **编译运行**
   - 点击"编译"按钮
   - 在模拟器中预览效果

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `QWEN_API_KEY` | 阿里千问API密钥 | - | 否* |
| `DATABASE_URL` | 数据库连接URL | `sqlite:///./test.db` | 是 |
| `REDIS_URL` | Redis连接URL | - | 否 |
| `LOG_LEVEL` | 日志级别 | `INFO` | 否 |
| `CORS_ORIGINS` | 跨域允许源 | `["*"]` | 否 |

*注：没有API密钥时会使用内置的备用笑话

### API文档

启动后端服务后，访问以下地址查看API文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📱 功能截图

### 主要页面
- **首页**：笑话生成和展示
- **历史记录**：查看已生成的笑话
- **分类页面**：选择不同类型的笑话
- **个人中心**：用户设置和统计

### 核心功能
- **一键生成**：点击按钮即可生成新笑话
- **类型选择**：支持多种笑话类型
- **历史管理**：自动保存，支持删除和分享
- **网络状态**：实时显示连接状态

## 🛠️ 开发指南

### 添加新的笑话类型

1. **后端**：在 `app/services/ai_service.py` 中添加新的提示词
2. **前端**：在 `pages/category/category.js` 中添加新的分类选项

### 自定义AI服务

1. 实现 `app/services/ai_service.py` 中的 `AIService` 接口
2. 在 `app/core/config.py` 中添加相关配置
3. 更新环境变量模板

### 扩展数据模型

1. 在 `app/models/` 中定义新的SQLAlchemy模型
2. 在 `app/schemas/` 中定义对应的Pydantic模式
3. 使用Alembic生成数据库迁移文件

## 🧪 测试

### 后端测试
```bash
cd backend
pytest tests/ -v
```

### API测试
```bash
# 健康检查
curl http://localhost:8000/health

# 生成笑话
curl -X POST http://localhost:8000/api/v1/jokes/generate \
  -H "Content-Type: application/json" \
  -d '{"category": "random"}'
```

## 📈 性能优化

### 后端优化
- **数据库连接池**：使用SQLAlchemy连接池
- **Redis缓存**：缓存频繁请求的数据
- **异步处理**：使用FastAPI的异步特性
- **日志优化**：结构化日志，支持日志轮转

### 前端优化
- **图片优化**：使用WebP格式，压缩图片大小
- **请求缓存**：缓存API响应，减少网络请求
- **懒加载**：按需加载页面和组件
- **本地存储**：合理使用localStorage

## 🔒 安全考虑

- **API密钥保护**：使用环境变量，不在代码中硬编码
- **输入验证**：使用Pydantic进行数据验证
- **CORS配置**：合理配置跨域访问策略
- **日志脱敏**：避免在日志中记录敏感信息

## 🚀 部署建议

### 生产环境部署

1. **使用Docker**
   ```dockerfile
   # 参考 backend/Dockerfile
   FROM python:3.9-slim
   COPY . /app
   WORKDIR /app
   RUN pip install -r requirements.txt
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **使用Nginx反向代理**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **使用PM2管理进程**
   ```bash
   pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name cold-joke-api
   ```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [阿里千问](https://help.aliyun.com/zh/dashscope/) - AI对话服务
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 小程序开发框架

## 📞 联系方式

- **项目地址**: [GitHub Repository](https://github.com/your-username/cold-joke-generator)
- **问题反馈**: [Issues](https://github.com/your-username/cold-joke-generator/issues)
- **功能建议**: [Discussions](https://github.com/your-username/cold-joke-generator/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！