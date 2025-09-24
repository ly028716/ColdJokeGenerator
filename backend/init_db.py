#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库初始化脚本
用于创建数据库表结构
"""

import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所有模型以确保它们被注册
from app.models.joke import Joke  # noqa
from app.models.user import User  # noqa
from app.models.share import Share  # noqa

from app.db.base import Base
from app.db.session import engine

def init_db():
    """初始化数据库，创建所有表"""
    print("开始初始化数据库...")
    print(f"将要创建的表: {list(Base.metadata.tables.keys())}")
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成！")

if __name__ == "__main__":
    init_db()