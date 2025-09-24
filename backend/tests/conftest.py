"""
测试配置文件
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_engine():
    """数据库引擎fixture"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """数据库会话fixture"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """测试客户端fixture"""
    app.dependency_overrides[get_db] = lambda: db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_joke_data():
    """示例笑话数据"""
    return {
        "content": "为什么程序员喜欢冷笑话？因为它们像代码一样冷！",
        "category": "程序员",
        "tags": "程序员,冷笑话"
    }


@pytest.fixture
def sample_user_data():
    """示例用户数据"""
    return {
        "openid": "test_openid_123",
        "nickname": "测试用户",
        "avatar_url": "https://example.com/avatar.jpg",
        "gender": 1,
        "city": "北京",
        "province": "北京",
        "country": "中国"
    }