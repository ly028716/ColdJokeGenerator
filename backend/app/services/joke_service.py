"""
笑话服务
"""
import json
import random
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import JokeGenerationException, DatabaseException
from app.models.joke import Joke
from app.schemas.joke import (
    JokeGenerateRequest,
    JokeBatchGenerateRequest,
    JokeCreate,
    JokeListResponse
)
from app.services.ai_service import AIService

logger = get_logger(__name__)


class JokeService:
    """笑话服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def generate_joke(self, request: JokeGenerateRequest, user_id: Optional[int] = None) -> Joke:
        """生成单个笑话"""
        try:
            # 构建提示词
            prompt = self._build_prompt(request)
            
            # 调用AI服务生成笑话
            content = await self.ai_service.generate_joke(
                prompt=prompt,
                temperature=request.temperature or 0.8,
                max_tokens=settings.QWEN_MAX_TOKENS
            )
            
            # 创建笑话记录
            joke_create = JokeCreate(
                content=content,
                category=request.category,
                tags=",".join(request.tags) if request.tags else None,
                prompt=prompt,
                model_name=settings.QWEN_MODEL,
                temperature=request.temperature,
                user_id=user_id
            )
            
            joke = self.create_joke(joke_create)
            logger.info(f"成功生成笑话: {joke.id}")
            
            return joke
            
        except Exception as e:
            logger.error(f"生成笑话失败: {e}")
            raise JokeGenerationException(f"生成笑话失败: {str(e)}")
    
    async def generate_batch_jokes(
        self, 
        request: JokeBatchGenerateRequest, 
        user_id: Optional[int] = None
    ) -> List[Joke]:
        """批量生成笑话"""
        jokes = []
        
        for i in range(request.count):
            try:
                single_request = JokeGenerateRequest(
                    category=request.category,
                    tags=request.tags,
                    length=request.length,
                    temperature=request.temperature
                )
                
                joke = await self.generate_joke(single_request, user_id)
                jokes.append(joke)
                
            except Exception as e:
                logger.error(f"批量生成第{i+1}个笑话失败: {e}")
                continue
        
        if not jokes:
            raise JokeGenerationException("批量生成笑话全部失败")
        
        return jokes
    
    def create_joke(self, joke_create: JokeCreate) -> Joke:
        """创建笑话记录"""
        try:
            joke = Joke(**joke_create.model_dump())
            self.db.add(joke)
            self.db.commit()
            self.db.refresh(joke)
            
            # 更新用户生成统计
            if joke.user_id:
                self._update_user_stats(joke.user_id, "generated")
            
            return joke
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"创建笑话记录失败: {e}")
            raise DatabaseException(f"创建笑话记录失败: {str(e)}")
    
    def get_joke_by_id(self, joke_id: int) -> Optional[Joke]:
        """根据ID获取笑话"""
        return self.db.query(Joke).filter(Joke.id == joke_id).first()
    
    def get_jokes(
        self,
        page: int = 1,
        size: int = 10,
        category: Optional[str] = None,
        is_featured: Optional[bool] = None,
        is_public: bool = True
    ) -> JokeListResponse:
        """获取笑话列表"""
        query = self.db.query(Joke).filter(Joke.is_public == is_public)
        
        if category:
            query = query.filter(Joke.category == category)
        
        if is_featured is not None:
            query = query.filter(Joke.is_featured == is_featured)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        jokes = query.order_by(desc(Joke.created_at)).offset((page - 1) * size).limit(size).all()
        
        return JokeListResponse(
            items=jokes,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    def get_user_jokes(self, user_id: int, page: int = 1, size: int = 10) -> JokeListResponse:
        """获取用户的笑话"""
        query = self.db.query(Joke).filter(Joke.user_id == user_id)
        
        total = query.count()
        jokes = query.order_by(desc(Joke.created_at)).offset((page - 1) * size).limit(size).all()
        
        return JokeListResponse(
            items=jokes,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    def increment_view_count(self, joke_id: int) -> bool:
        """增加查看次数"""
        try:
            joke = self.db.query(Joke).filter(Joke.id == joke_id).first()
            if joke:
                joke.view_count += 1
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新查看次数失败: {e}")
            return False
    
    def toggle_favorite(self, joke_id: int) -> bool:
        """切换收藏状态"""
        try:
            joke = self.db.query(Joke).filter(Joke.id == joke_id).first()
            if joke:
                joke.like_count += 1
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新收藏状态失败: {e}")
            return False
    
    def _build_prompt(self, request: JokeGenerateRequest) -> str:
        """构建生成提示词"""
        base_prompt = "请生成一个幽默的冷笑话"
        
        if request.category:
            base_prompt += f"，类型是{request.category}"
        
        if request.tags:
            base_prompt += f"，包含以下元素：{', '.join(request.tags)}"
        
        if request.length:
            length_map = {
                "short": "简短",
                "medium": "中等长度",
                "long": "较长"
            }
            base_prompt += f"，长度要求：{length_map.get(request.length, '中等长度')}"
        
        if request.custom_prompt:
            base_prompt += f"。额外要求：{request.custom_prompt}"
        
        base_prompt += "。请确保内容健康、积极向上，适合所有年龄段的用户。"
        
        return base_prompt
    
    def _update_user_stats(self, user_id: int, stat_type: str):
        """更新用户统计"""
        try:
            from app.models.user import User
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                if stat_type == "generated":
                    user.total_generated += 1
                elif stat_type == "shared":
                    user.total_shared += 1
                self.db.commit()
        except Exception as e:
            logger.error(f"更新用户统计失败: {e}")