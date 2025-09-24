"""
笑话模型
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Joke(Base):
    """笑话模型"""
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, comment="笑话内容")
    category: Mapped[Optional[str]] = mapped_column(String(50), comment="笑话分类")
    tags: Mapped[Optional[str]] = mapped_column(String(200), comment="标签，逗号分隔")
    
    # 生成信息
    prompt: Mapped[Optional[str]] = mapped_column(Text, comment="生成提示词")
    model_name: Mapped[Optional[str]] = mapped_column(String(50), comment="使用的模型名称")
    temperature: Mapped[Optional[float]] = mapped_column(Float, comment="生成温度参数")
    
    # 用户关联
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        comment="生成用户ID"
    )
    
    # 统计信息
    view_count: Mapped[int] = mapped_column(default=0, comment="查看次数")
    share_count: Mapped[int] = mapped_column(default=0, comment="分享次数")
    like_count: Mapped[int] = mapped_column(default=0, comment="点赞次数")
    
    # 质量评分
    quality_score: Mapped[Optional[float]] = mapped_column(Float, comment="质量评分")
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否精选")
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否公开")
    
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
    user: Mapped[Optional["User"]] = relationship("User", back_populates="jokes")
    shares: Mapped[List["Share"]] = relationship("Share", back_populates="joke")

    def __repr__(self) -> str:
        return f"<Joke(id={self.id}, content='{self.content[:50]}...', category='{self.category}')>"