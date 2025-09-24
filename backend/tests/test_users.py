"""
用户相关测试
"""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


class TestUserAPI:
    """用户API测试类"""
    
    def test_create_user(self, client: TestClient, sample_user_data):
        """测试创建用户"""
        response = client.post("/api/v1/users/", json=sample_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["openid"] == sample_user_data["openid"]
        assert data["data"]["nickname"] == sample_user_data["nickname"]
    
    def test_create_duplicate_user(self, client: TestClient, db_session, sample_user_data):
        """测试创建重复用户"""
        # 先创建一个用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        
        # 尝试创建相同openid的用户
        response = client.post("/api/v1/users/", json=sample_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "已存在" in data["message"]
    
    def test_get_user_by_id(self, client: TestClient, db_session, sample_user_data):
        """测试根据ID获取用户"""
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        response = client.get(f"/api/v1/users/{user.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["id"] == user.id
        assert data["data"]["openid"] == sample_user_data["openid"]
    
    def test_get_user_by_openid(self, client: TestClient, db_session, sample_user_data):
        """测试根据openid获取用户"""
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        
        response = client.get(f"/api/v1/users/openid/{sample_user_data['openid']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["openid"] == sample_user_data["openid"]
    
    def test_update_user(self, client: TestClient, db_session, sample_user_data):
        """测试更新用户信息"""
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        update_data = {
            "nickname": "更新后的昵称",
            "city": "上海"
        }
        
        response = client.put(f"/api/v1/users/{user.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["nickname"] == update_data["nickname"]
        assert data["data"]["city"] == update_data["city"]
    
    def test_user_login(self, client: TestClient, db_session, sample_user_data):
        """测试用户登录"""
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        response = client.post(f"/api/v1/users/{user.id}/login")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["last_login_at"] is not None
    
    def test_get_users_list(self, client: TestClient, db_session, sample_user_data):
        """测试获取用户列表"""
        # 创建多个测试用户
        for i in range(5):
            user_data = sample_user_data.copy()
            user_data["openid"] = f"test_openid_{i}"
            user_data["nickname"] = f"测试用户{i}"
            user = User(**user_data)
            db_session.add(user)
        
        db_session.commit()
        
        response = client.get("/api/v1/users/?page=1&size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["items"]) == 5
        assert data["data"]["total"] == 5
    
    def test_get_user_stats(self, client: TestClient):
        """测试获取用户统计"""
        response = client.get("/api/v1/users/stats/overview")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "total_users" in data["data"]
        assert "active_users" in data["data"]


class TestUserService:
    """用户服务测试类"""
    
    def test_create_user_service(self, db_session, sample_user_data):
        """测试用户服务创建用户"""
        from app.services.user_service import UserService
        from app.schemas.user import UserCreate
        
        user_service = UserService(db_session)
        user_create = UserCreate(**sample_user_data)
        
        user = user_service.create_user(user_create)
        
        assert user.id is not None
        assert user.openid == sample_user_data["openid"]
        assert user.nickname == sample_user_data["nickname"]
        assert user.is_active == True
        assert user.is_banned == False
    
    def test_get_user_by_openid_service(self, db_session, sample_user_data):
        """测试通过openid获取用户"""
        from app.services.user_service import UserService
        
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        
        user_service = UserService(db_session)
        found_user = user_service.get_user_by_openid(sample_user_data["openid"])
        
        assert found_user is not None
        assert found_user.openid == sample_user_data["openid"]
    
    def test_update_user_service(self, db_session, sample_user_data):
        """测试用户服务更新用户"""
        from app.services.user_service import UserService
        from app.schemas.user import UserUpdate
        
        # 创建测试用户
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        user_service = UserService(db_session)
        user_update = UserUpdate(nickname="新昵称", city="深圳")
        
        updated_user = user_service.update_user(user.id, user_update)
        
        assert updated_user is not None
        assert updated_user.nickname == "新昵称"
        assert updated_user.city == "深圳"