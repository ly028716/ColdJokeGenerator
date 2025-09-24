#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
兼容 Python 3.6 的服务器启动脚本
"""

import sys
import asyncio
from pathlib import Path

# 将项目根目录添加到Python路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    try:
        import uvicorn
        from app.main import app
        from app.core.config import settings
        from app.core.logging import setup_logging, get_logger
        
        # 设置日志
        setup_logging()
        logger = get_logger(__name__)
        
        logger.info("启动AI冷笑话生成器后端服务...")
        logger.info(f"环境: {settings.ENVIRONMENT}")
        logger.info(f"调试模式: {settings.DEBUG}")
        logger.info(f"服务地址: http://{settings.HOST}:{settings.PORT}")
        
        # 使用兼容 Python 3.6 的方式启动服务
        config = uvicorn.Config(
            app,
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True,
        )
        server = uvicorn.Server(config)
        
        # 对于 Python 3.6，使用 asyncio.get_event_loop().run_until_complete
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.serve())
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()