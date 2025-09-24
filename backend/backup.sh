#!/bin/bash

# AI冷笑话生成器数据备份脚本

set -e

# 配置
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="ai-joke-db"
DB_NAME="jokes_db"
DB_USER="jokes_user"

echo "🗄️  开始数据备份..."

# 创建备份目录
mkdir -p $BACKUP_DIR

# 数据库备份
echo "📊 备份数据库..."
docker exec $CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME > "$BACKUP_DIR/db_backup_$DATE.sql"

# 压缩备份文件
echo "🗜️  压缩备份文件..."
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

# 备份应用数据
echo "📁 备份应用数据..."
tar -czf "$BACKUP_DIR/data_backup_$DATE.tar.gz" data/ logs/

# 清理旧备份（保留最近7天）
echo "🧹 清理旧备份..."
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "✅ 备份完成！"
echo "📁 备份文件:"
ls -la $BACKUP_DIR/*$DATE*

# 备份验证
echo "🔍 验证备份文件..."
if [ -f "$BACKUP_DIR/db_backup_$DATE.sql.gz" ] && [ -f "$BACKUP_DIR/data_backup_$DATE.tar.gz" ]; then
    echo "✅ 备份文件验证成功"
else
    echo "❌ 备份文件验证失败"
    exit 1
fi

echo "🎉 数据备份完成！"