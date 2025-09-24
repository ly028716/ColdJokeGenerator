#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的服务器启动脚本
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
        
        # 检查应用
        try:
            from app.main import app
            print("[OK] 应用导入成功")
        except ImportError as e:
            print(f"[ERROR] 应用导入失败: {e}")
            print("详细错误信息:")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        print("\n正在启动服务器...")
        print("服务地址: http://localhost:8000")
        print("API文档: http://localhost:8000/docs")
        print("按 Ctrl+C 停止服务")
        
        # 使用最简单的方式启动
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)