#!/bin/bash

# AI冷笑话生成器后端服务部署脚本

set -e

echo "🚀 开始部署AI冷笑话生成器后端服务..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "📝 创建环境变量文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，配置必要的环境变量（特别是QWEN_API_KEY和SECRET_KEY）"
    echo "   然后重新运行此脚本"
    exit 1
fi

# 读取环境变量
source .env

# 检查必要的环境变量
if [ -z "$QWEN_API_KEY" ] || [ "$QWEN_API_KEY" = "your_qwen_api_key_here" ]; then
    echo "⚠️  警告: QWEN_API_KEY未配置，将使用备用笑话库"
fi

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-secret-key-here" ]; then
    echo "❌ 请在.env文件中配置SECRET_KEY"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs data uploads ssl

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose down

# 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 健康检查
echo "🏥 执行健康检查..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ 服务启动成功！"
        break
    else
        echo "⏳ 等待服务启动... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ 服务启动失败，请检查日志"
    docker-compose logs app
    exit 1
fi

# 显示服务信息
echo ""
echo "🎉 部署完成！"
echo ""
echo "📊 服务信息:"
echo "  - 应用地址: http://localhost:8000"
echo "  - API文档: http://localhost:8000/docs"
echo "  - 健康检查: http://localhost:8000/health"
echo "  - 数据库: PostgreSQL (localhost:5432)"
echo "  - 缓存: Redis (localhost:6379)"
echo "  - 监控: Prometheus (http://localhost:9090)"
echo ""
echo "📝 常用命令:"
echo "  - 查看日志: docker-compose logs -f app"
echo "  - 重启服务: docker-compose restart app"
echo "  - 停止服务: docker-compose down"
echo "  - 更新服务: ./deploy.sh"
echo ""
echo "📁 重要文件:"
echo "  - 配置文件: .env"
echo "  - 日志目录: ./logs/"
echo "  - 数据目录: ./data/"
echo ""

# 显示初始化建议
if [ "$QWEN_API_KEY" = "your_qwen_api_key_here" ]; then
    echo "💡 建议:"
    echo "  1. 配置阿里千问API密钥以启用AI生成功能"
    echo "  2. 配置SSL证书以启用HTTPS"
    echo "  3. 设置定期备份策略"
    echo ""
fi

echo "✨ 部署完成！服务已在后台运行。"