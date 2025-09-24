"""
分享服务
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.logging import get_logger
from app.core.exceptions import DatabaseException
from app.models.share import Share
from app.models.joke import Joke
from app.schemas.joke import ShareRequest, ShareCreate, ShareStatsResponse

logger = get_logger(__name__)


class ShareService:
    """分享服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_share(
        self,
        share_request: ShareRequest,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Share:
        """创建分享记录"""
        try:
            # 检查笑话是否存在
            joke = self.db.query(Joke).filter(Joke.id == share_request.joke_id).first()
            if not joke:
                raise DatabaseException("笑话不存在")
            
            # 生成分享链接
            share_url = self._generate_share_url(share_request.joke_id)
            
            # 创建分享记录
            share_create = ShareCreate(
                **share_request.model_dump(),
                user_id=user_id,
                share_url=share_url,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            share = Share(**share_create.model_dump())
            self.db.add(share)
            
            # 更新笑话分享次数
            joke.share_count += 1
            
            # 更新用户分享统计
            if user_id:
                self._update_user_share_stats(user_id)
            
            self.db.commit()
            self.db.refresh(share)
            
            logger.info(f"创建分享记录成功: {share.id}")
            return share
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"创建分享记录失败: {e}")
            raise DatabaseException(f"创建分享记录失败: {str(e)}")
    
    def get_share_stats(self, days: int = 7) -> ShareStatsResponse:
        """获取分享统计"""
        try:
            # 计算时间范围
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # 总分享次数
            total_shares = self.db.query(Share).filter(
                Share.created_at >= start_date
            ).count()
            
            # 按平台统计
            platform_stats = {}
            platform_query = self.db.query(
                Share.share_to,
                func.count(Share.id).label('count')
            ).filter(
                Share.created_at >= start_date
            ).group_by(Share.share_to).all()
            
            for platform, count in platform_query:
                platform_stats[platform] = count
            
            # 最近分享记录
            recent_shares = self.db.query(Share).filter(
                Share.created_at >= start_date
            ).order_by(desc(Share.created_at)).limit(10).all()
            
            # 最受欢迎的笑话
            top_shared_query = self.db.query(
                Joke,
                func.count(Share.id).label('share_count')
            ).join(Share).filter(
                Share.created_at >= start_date
            ).group_by(Joke.id).order_by(
                desc(func.count(Share.id))
            ).limit(5).all()
            
            top_shared_jokes = [joke for joke, _ in top_shared_query]
            
            return ShareStatsResponse(
                total_shares=total_shares,
                platform_stats=platform_stats,
                recent_shares=recent_shares,
                top_shared_jokes=top_shared_jokes
            )
            
        except Exception as e:
            logger.error(f"获取分享统计失败: {e}")
            return ShareStatsResponse(
                total_shares=0,
                platform_stats={},
                recent_shares=[],
                top_shared_jokes=[]
            )
    
    def increment_click_count(self, share_id: int) -> bool:
        """增加点击次数"""
        try:
            share = self.db.query(Share).filter(Share.id == share_id).first()
            if share:
                share.click_count += 1
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新点击次数失败: {e}")
            return False
    
    def get_share_by_url(self, share_url: str) -> Optional[Share]:
        """根据分享链接获取分享记录"""
        return self.db.query(Share).filter(Share.share_url == share_url).first()
    
    def get_user_shares(
        self,
        user_id: int,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """获取用户分享记录"""
        query = self.db.query(Share).filter(Share.user_id == user_id)
        
        total = query.count()
        shares = query.order_by(desc(Share.created_at)).offset((page - 1) * size).limit(size).all()
        
        return {
            "items": shares,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    
    def _generate_share_url(self, joke_id: int) -> str:
        """生成分享链接"""
        # 这里可以根据实际需求生成分享链接
        # 例如：https://your-domain.com/share/joke/{joke_id}
        return f"/share/joke/{joke_id}"
    
    def _update_user_share_stats(self, user_id: int):
        """更新用户分享统计"""
        try:
            from app.models.user import User
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                user.total_shared += 1
        except Exception as e:
            logger.error(f"更新用户分享统计失败: {e}")