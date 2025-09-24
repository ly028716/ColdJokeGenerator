"""
日志配置
"""
import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """设置日志配置"""
    
    # 移除默认的日志处理器
    logger.remove()
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 控制台日志格式
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 文件日志格式
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # 添加控制台日志处理器
    logger.add(
        sys.stdout,
        format=console_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 添加文件日志处理器
    logger.add(
        settings.LOG_FILE,
        format=file_format,
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # 添加错误日志处理器
    logger.add(
        "logs/error.log",
        format=file_format,
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("日志系统初始化完成")


# 获取日志记录器
def get_logger(name: str = __name__):
    """获取日志记录器"""
    return logger.bind(name=name)