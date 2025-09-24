"""
项目初始化脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.session import create_tables
from app.services.ai_service import AIService

def init_project():
    """初始化项目"""
    print("开始初始化AI冷笑话生成器项目...")
    
    # 1. 设置日志
    setup_logging()
    logger = get_logger(__name__)
    logger.info("项目初始化开始")
    
    # 2. 创建必要的目录
    directories = ["logs", "data", "uploads"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"创建目录: {directory}")
    
    # 3. 创建数据库表
    try:
        create_tables()
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        return False
    
    # 4. 测试AI服务连接
    try:
        ai_service = AIService()
        result = ai_service.test_api_connection()
        if result["status"] == "success":
            logger.info("AI服务连接测试成功")
        else:
            logger.warning(f"AI服务连接测试失败: {result['message']}")
            logger.info("将使用备用笑话库")
    except Exception as e:
        logger.error(f"AI服务测试失败: {e}")
    
    # 5. 检查配置
    logger.info("检查项目配置...")
    logger.info(f"项目名称: {settings.PROJECT_NAME}")
    logger.info(f"版本: {settings.VERSION}")
    logger.info(f"环境: {settings.ENVIRONMENT}")
    logger.info(f"调试模式: {settings.DEBUG}")
    logger.info(f"数据库URL: {settings.DATABASE_URL}")
    
    if settings.QWEN_API_KEY and settings.QWEN_API_KEY != "your_qwen_api_key_here":
        logger.info("阿里千问API密钥已配置")
    else:
        logger.warning("阿里千问API密钥未配置，将使用备用笑话库")
    
    logger.info("项目初始化完成！")
    print("\n项目初始化完成！")
    print(f"服务将在 http://{settings.HOST}:{settings.PORT} 启动")
    print("使用以下命令启动服务:")
    print("  python run.py")
    print("或者:")
    print(f"  uvicorn app.main:app --host {settings.HOST} --port {settings.PORT} --reload")
    
    return True

if __name__ == "__main__":
    success = init_project()
    if not success:
        sys.exit(1)