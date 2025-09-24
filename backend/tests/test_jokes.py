"""
笑话相关测试
"""
import pytest
from fastapi.testclient import TestClient

from app.models.joke import Joke
from app.models.user import User


class TestJokeAPI:
    """笑话API测试类"""
    
    def test_generate_joke(self, client: TestClient):
        """测试生成笑话"""
        response = client.post(
            "/api/v1/jokes/generate",
            json={
                "category": "程序员",
                "temperature": 0.8
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert "content" in data["data"]
    
    def test_generate_batch_jokes(self, client: TestClient):
        """测试批量生成笑话"""
        response = client.post(
            "/api/v1/jokes/batch",
            json={
                "count": 3,
                "category": "程序员"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert isinstance(data["data"], list)
        assert len(data["data"]) <= 3
    
    def test_get_jokes_list(self, client: TestClient, db_session, sample_joke_data):
        """测试获取笑话列表"""
        # 创建测试笑话
        joke = Joke(**sample_joke_data)
        db_session.add(joke)
        db_session.commit()
        
        response = client.get("/api/v1/jokes/?page=1&size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "items" in data["data"]
        assert "total" in data["data"]
    
    def test_get_joke_by_id(self, client: TestClient, db_session, sample_joke_data):
        """测试根据ID获取笑话"""
        # 创建测试笑话
        joke = Joke(**sample_joke_data)
        db_session.add(joke)
        db_session.commit()
        db_session.refresh(joke)
        
        response = client.get(f"/api/v1/jokes/{joke.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["id"] == joke.id
        assert data["data"]["content"] == sample_joke_data["content"]
    
    def test_get_nonexistent_joke(self, client: TestClient):
        """测试获取不存在的笑话"""
        response = client.get("/api/v1/jokes/99999")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 404
    
    def test_favorite_joke(self, client: TestClient, db_session, sample_joke_data):
        """测试收藏笑话"""
        # 创建测试笑话
        joke = Joke(**sample_joke_data)
        db_session.add(joke)
        db_session.commit()
        db_session.refresh(joke)
        
        response = client.post(f"/api/v1/jokes/{joke.id}/favorite")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["favorited"] == True
    
    def test_share_joke(self, client: TestClient, db_session, sample_joke_data):
        """测试分享笑话"""
        # 创建测试笑话
        joke = Joke(**sample_joke_data)
        db_session.add(joke)
        db_session.commit()
        db_session.refresh(joke)
        
        response = client.post(
            "/api/v1/jokes/share",
            json={
                "joke_id": joke.id,
                "share_to": "wechat",
                "share_title": "分享一个笑话"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
    
    def test_get_share_stats(self, client: TestClient):
        """测试获取分享统计"""
        response = client.get("/api/v1/jokes/share/stats?days=7")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "total_shares" in data["data"]
        assert "platform_stats" in data["data"]


class TestJokeService:
    """笑话服务测试类"""
    
    def test_create_joke(self, db_session, sample_joke_data):
        """测试创建笑话"""
        from app.services.joke_service import JokeService
        from app.schemas.joke import JokeCreate
        
        joke_service = JokeService(db_session)
        joke_create = JokeCreate(**sample_joke_data)
        
        joke = joke_service.create_joke(joke_create)
        
        assert joke.id is not None
        assert joke.content == sample_joke_data["content"]
        assert joke.category == sample_joke_data["category"]
    
    def test_get_jokes_pagination(self, db_session, sample_joke_data):
        """测试笑话分页"""
        from app.services.joke_service import JokeService
        
        # 创建多个测试笑话
        for i in range(15):
            joke_data = sample_joke_data.copy()
            joke_data["content"] = f"测试笑话 {i+1}"
            joke = Joke(**joke_data)
            db_session.add(joke)
        
        db_session.commit()
        
        joke_service = JokeService(db_session)
        
        # 测试第一页
        result = joke_service.get_jokes(page=1, size=10)
        assert len(result.items) == 10
        assert result.total == 15
        assert result.pages == 2
        
        # 测试第二页
        result = joke_service.get_jokes(page=2, size=10)
        assert len(result.items) == 5
        assert result.total == 15