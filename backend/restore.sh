#!/bin/bash

# AI冷笑话生成器数据恢复脚本

set -e

# 检查参数
if [ $# -ne 1 ]; then
    echo "使用方法: $0 <备份日期>"
    echo "示例: $0 20231222_143000"
    exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="./backups"
CONTAINER_NAME="ai-joke-db"
DB_NAME="jokes_db"
DB_USER="jokes_user"

echo "🔄 开始数据恢复..."

# 检查备份文件是否存在
DB_BACKUP_FILE="$BACKUP_DIR/db_backup_$BACKUP_DATE.sql.gz"
DATA_BACKUP_FILE="$BACKUP_DIR/data_backup_$BACKUP_DATE.tar.gz"

if [ ! -f "$DB_BACKUP_FILE" ]; then
    echo "❌ 数据库备份文件不存在: $DB_BACKUP_FILE"
    exit 1
fi

if [ ! -f "$DATA_BACKUP_FILE" ]; then
    echo "❌ 数据备份文件不存在: $DATA_BACKUP_FILE"
    exit 1
fi

# 确认恢复操作
echo "⚠️  警告: 此操作将覆盖现有数据！"
echo "📁 将恢复以下备份:"
echo "  - 数据库: $DB_BACKUP_FILE"
echo "  - 应用数据: $DATA_BACKUP_FILE"
echo ""
read -p "确认继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 恢复操作已取消"
    exit 1
fi

# 停止应用服务
echo "🛑 停止应用服务..."
docker-compose stop app

# 恢复数据库
echo "📊 恢复数据库..."
gunzip -c "$DB_BACKUP_FILE" | docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME

# 恢复应用数据
echo "📁 恢复应用数据..."
tar -xzf "$DATA_BACKUP_FILE"

# 重启服务
echo "🚀 重启服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🏥 执行健康检查..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ 服务恢复成功！"
        break
    else
        echo "⏳ 等待服务启动... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ 服务恢复失败，请检查日志"
    docker-compose logs app
    exit 1
fi

echo "🎉 数据恢复完成！"
echo "🌐 服务地址: http://localhost:8000"