"""
用户模型
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    openid: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment="微信openid")
    nickname: Mapped[Optional[str]] = mapped_column(String(100), comment="用户昵称")
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, comment="头像URL")
    gender: Mapped[Optional[int]] = mapped_column(comment="性别：0-未知，1-男，2-女")
    city: Mapped[Optional[str]] = mapped_column(String(50), comment="城市")
    province: Mapped[Optional[str]] = mapped_column(String(50), comment="省份")
    country: Mapped[Optional[str]] = mapped_column(String(50), comment="国家")
    language: Mapped[Optional[str]] = mapped_column(String(20), default="zh_CN", comment="语言")
    
    # 用户状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否被封禁")
    
    # 统计信息
    total_generated: Mapped[int] = mapped_column(default=0, comment="总生成次数")
    total_shared: Mapped[int] = mapped_column(default=0, comment="总分享次数")
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="最后登录时间"
    )

    # 关系
    jokes: Mapped[List["Joke"]] = relationship("Joke", back_populates="user")
    shares: Mapped[List["Share"]] = relationship("Share", back_populates="user")
    preferences: Mapped[Optional["UserPreference"]] = relationship(
        "UserPreference", 
        back_populates="user",
        uselist=False
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, openid='{self.openid}', nickname='{self.nickname}')>"