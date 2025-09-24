"""
用户服务
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.logging import get_logger
from app.core.exceptions import DatabaseException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserStatsResponse

logger = get_logger(__name__)


class UserService:
    """用户服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_create: UserCreate) -> User:
        """创建用户"""
        try:
            user = User(**user_create.model_dump())
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"创建用户成功: {user.id}")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"创建用户失败: {e}")
            raise DatabaseException(f"创建用户失败: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_openid(self, openid: str) -> Optional[User]:
        """根据openid获取用户"""
        return self.db.query(User).filter(User.openid == openid).first()
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"更新用户信息成功: {user.id}")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新用户信息失败: {e}")
            raise DatabaseException(f"更新用户信息失败: {str(e)}")
    
    def update_last_login(self, user_id: int) -> Optional[User]:
        """更新最后登录时间"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            user.last_login_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
            
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新登录时间失败: {e}")
            return None
    
    def get_users(
        self,
        page: int = 1,
        size: int = 10,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """获取用户列表"""
        query = self.db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        total = query.count()
        users = query.order_by(desc(User.created_at)).offset((page - 1) * size).limit(size).all()
        
        return {
            "items": users,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    
    def get_user_stats(self) -> UserStatsResponse:
        """获取用户统计信息"""
        try:
            # 总用户数
            total_users = self.db.query(User).count()
            
            # 活跃用户数
            active_users = self.db.query(User).filter(User.is_active == True).count()
            
            # 今日新用户数
            today = datetime.utcnow().date()
            new_users_today = self.db.query(User).filter(
                func.date(User.created_at) == today
            ).count()
            
            # 生成次数最多的用户
            top_generators = self.db.query(User).filter(
                User.total_generated > 0
            ).order_by(desc(User.total_generated)).limit(5).all()
            
            # 分享次数最多的用户
            top_sharers = self.db.query(User).filter(
                User.total_shared > 0
            ).order_by(desc(User.total_shared)).limit(5).all()
            
            return UserStatsResponse(
                total_users=total_users,
                active_users=active_users,
                new_users_today=new_users_today,
                top_generators=[
                    {
                        "id": user.id,
                        "nickname": user.nickname,
                        "total_generated": user.total_generated
                    }
                    for user in top_generators
                ],
                top_sharers=[
                    {
                        "id": user.id,
                        "nickname": user.nickname,
                        "total_shared": user.total_shared
                    }
                    for user in top_sharers
                ]
            )
            
        except Exception as e:
            logger.error(f"获取用户统计失败: {e}")
            return UserStatsResponse(
                total_users=0,
                active_users=0,
                new_users_today=0,
                top_generators=[],
                top_sharers=[]
            )
    
    def ban_user(self, user_id: int) -> bool:
        """封禁用户"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.is_banned = True
            user.is_active = False
            self.db.commit()
            
            logger.info(f"封禁用户成功: {user.id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"封禁用户失败: {e}")
            return False
    
    def unban_user(self, user_id: int) -> bool:
        """解封用户"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.is_banned = False
            user.is_active = True
            self.db.commit()
            
            logger.info(f"解封用户成功: {user.id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"解封用户失败: {e}")
            return False