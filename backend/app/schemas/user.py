"""
用户相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """用户基础模型"""
    openid: str = Field(..., description="微信openid")
    nickname: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    gender: Optional[int] = Field(None, description="性别：0-未知，1-男，2-女")
    city: Optional[str] = Field(None, description="城市")
    province: Optional[str] = Field(None, description="省份")
    country: Optional[str] = Field(None, description="国家")
    language: Optional[str] = Field("zh_CN", description="语言")


class UserCreate(UserBase):
    """创建用户模型"""
    pass


class UserUpdate(BaseModel):
    """更新用户模型"""
    nickname: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    gender: Optional[int] = Field(None, description="性别")
    city: Optional[str] = Field(None, description="城市")
    province: Optional[str] = Field(None, description="省份")
    country: Optional[str] = Field(None, description="国家")
    language: Optional[str] = Field(None, description="语言")


class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int
    is_active: bool = True
    is_banned: bool = False
    total_generated: int = 0
    total_shared: int = 0
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """用户响应模型"""
    pass


class UserStatsResponse(BaseModel):
    """用户统计响应模型"""
    total_users: int
    active_users: int
    new_users_today: int
    top_generators: list
    top_sharers: list