#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最小化的服务器启动脚本，跳过数据库相关功能
"""

import sys
import os
from pathlib import Path

# 将项目根目录添加到Python路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    try:
        print("正在检查依赖...")
        
        # 检查 FastAPI
        try:
            import fastapi
            print(f"[OK] FastAPI 版本: {fastapi.__version__}")
        except ImportError as e:
            print(f"[ERROR] FastAPI 导入失败: {e}")
            sys.exit(1)
        
        # 检查 uvicorn
        try:
            import uvicorn
            print("[OK] Uvicorn 可用")
        except ImportError as e:
            print(f"[ERROR] Uvicorn 导入失败: {e}")
            sys.exit(1)
        
        print("\n创建最小化应用...")
        
        # 创建一个最小化的 FastAPI 应用
        from fastapi import FastAPI
        
        app = FastAPI(
            title="AI冷笑话生成器",
            version="1.0.0",
            description="AI冷笑话生成器后端API服务（最小化版本）"
        )
        
        @app.get("/")
        async def root():
            """根路由"""
            return {
                "name": "AI冷笑话生成器",
                "version": "1.0.0",
                "status": "running",
                "message": "欢迎使用AI冷笑话生成器API服务"
            }
        
        @app.get("/health")
        async def health_check():
            """健康检查"""
            return {
                "status": "healthy",
                "version": "1.0.0"
            }
        
        @app.get("/api/test")
        async def test_api():
            """测试API"""
            return {
                "message": "API测试成功",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        
        print("[OK] 应用创建成功")
        
        print("\n正在启动服务器...")
        print("服务地址: http://localhost:8000")
        print("API文档: http://localhost:8000/docs")
        print("健康检查: http://localhost:8000/health")
        print("按 Ctrl+C 停止服务")
        
        # 使用兼容 Python 3.6 的方式启动
        import asyncio
        config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
        server = uvicorn.Server(config)
        
        # 对于 Python 3.6，使用 asyncio.get_event_loop().run_until_complete
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.serve())
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)