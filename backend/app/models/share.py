"""
分享记录模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Share(Base):
    """分享记录模型"""
    __tablename__ = "shares"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 关联信息
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        comment="分享用户ID"
    )
    joke_id: Mapped[int] = mapped_column(
        ForeignKey("jokes.id", ondelete="CASCADE"),
        comment="笑话ID"
    )
    
    # 分享信息
    share_to: Mapped[str] = mapped_column(String(50), comment="分享平台")
    share_url: Mapped[Optional[str]] = mapped_column(Text, comment="分享链接")
    share_title: Mapped[Optional[str]] = mapped_column(String(200), comment="分享标题")
    share_desc: Mapped[Optional[str]] = mapped_column(Text, comment="分享描述")
    
    # 统计信息
    click_count: Mapped[int] = mapped_column(default=0, comment="点击次数")
    
    # 设备信息
    device_info: Mapped[Optional[str]] = mapped_column(String(200), comment="设备信息")
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), comment="IP地址")
    user_agent: Mapped[Optional[str]] = mapped_column(Text, comment="用户代理")
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="分享时间"
    )

    # 关系
    user: Mapped[Optional["User"]] = relationship("User", back_populates="shares")
    joke: Mapped["Joke"] = relationship("Joke", back_populates="shares")

    def __repr__(self) -> str:
        return f"<Share(id={self.id}, joke_id={self.joke_id}, share_to='{self.share_to}')>"