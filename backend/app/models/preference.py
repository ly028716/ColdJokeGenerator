"""
用户偏好模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserPreference(Base):
    """用户偏好模型"""
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 用户关联
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        comment="用户ID"
    )
    
    # 笑话偏好
    preferred_categories: Mapped[Optional[str]] = mapped_column(
        Text, 
        comment="偏好分类，JSON格式"
    )
    preferred_tags: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="偏好标签，JSON格式"
    )
    humor_level: Mapped[Optional[int]] = mapped_column(
        comment="幽默程度偏好：1-5"
    )
    content_length: Mapped[Optional[str]] = mapped_column(
        String(20),
        default="medium",
        comment="内容长度偏好：short/medium/long"
    )
    
    # 生成偏好
    generation_frequency: Mapped[Optional[int]] = mapped_column(
        default=5,
        comment="每日生成频率限制"
    )
    auto_share: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="是否自动分享"
    )
    
    # 通知偏好
    enable_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="是否启用通知"
    )
    notification_time: Mapped[Optional[str]] = mapped_column(
        String(10),
        comment="通知时间，格式：HH:MM"
    )
    
    # 隐私设置
    profile_public: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="个人资料是否公开"
    )
    share_history_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="分享历史是否公开"
    )
    
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

    # 关系
    user: Mapped["User"] = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, user_id={self.user_id})>"