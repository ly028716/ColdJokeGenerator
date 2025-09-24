from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# 创建数据库引擎
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    **engine_kwargs
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话异常: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """创建所有数据表"""
    from app.db.base import Base
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据表创建成功")
    except Exception as e:
        logger.error(f"数据表创建失败: {e}")
        raise