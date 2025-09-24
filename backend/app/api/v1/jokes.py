from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.core.middleware import limiter
from app.core.response import APIResponse

# 创建一个安全的限流装饰器
def safe_limit(rate_limit: str):
    """安全的限流装饰器，如果limiter不可用则跳过"""
    def decorator(func):
        if limiter is not None:
            return limiter.limit(rate_limit)(func)
        return func
    return decorator
from app.db.session import get_db
from app.schemas.joke import (
    JokeGenerateRequest,
    JokeBatchGenerateRequest,
    JokeResponse,
    JokeListResponse,
    ShareRequest,
    ShareResponse,
    ShareStatsResponse
)
from app.services.joke_service import JokeService
from app.services.share_service import ShareService

router = APIRouter()


@router.post("/generate")
@safe_limit("10/minute")
async def generate_joke(
    request: Request,
    generate_request: JokeGenerateRequest,
    db: Session = Depends(get_db)
):
    """生成单个冷笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    joke = await joke_service.generate_joke(generate_request)
    
    return APIResponse.success(
        data=JokeResponse.model_validate(joke),
        message="笑话生成成功",
        request_id=request_id
    )


@router.post("/batch")
@safe_limit("5/minute")
async def generate_batch_jokes(
    request: Request,
    generate_request: JokeBatchGenerateRequest,
    db: Session = Depends(get_db)
):
    """批量生成冷笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    jokes = await joke_service.generate_batch_jokes(generate_request)
    
    return APIResponse.success(
        data=[JokeResponse.model_validate(joke) for joke in jokes],
        message=f"成功生成{len(jokes)}个笑话",
        request_id=request_id
    )


@router.get("/category/{category}")
@safe_limit("20/minute")
async def generate_joke_by_category(
    request: Request,
    category: str,
    temperature: Optional[float] = Query(0.8, ge=0.1, le=2.0),
    db: Session = Depends(get_db)
):
    """按分类生成笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    generate_request = JokeGenerateRequest(
        category=category,
        temperature=temperature
    )
    
    joke_service = JokeService(db)
    joke = await joke_service.generate_joke(generate_request)
    
    return APIResponse.success(
        data=JokeResponse.model_validate(joke),
        message=f"成功生成{category}类笑话",
        request_id=request_id
    )


@router.get("/")
async def get_jokes(
    request: Request,
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=50, description="每页数量"),
    category: Optional[str] = Query(None, description="分类筛选"),
    is_featured: Optional[bool] = Query(None, description="是否精选"),
    db: Session = Depends(get_db)
):
    """获取笑话列表"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    result = joke_service.get_jokes(
        page=page,
        size=size,
        category=category,
        is_featured=is_featured
    )
    
    return APIResponse.success(
        data=result,
        message="获取笑话列表成功",
        request_id=request_id
    )


@router.get("/{joke_id}")
async def get_joke(
    request: Request,
    joke_id: int,
    db: Session = Depends(get_db)
):
    """获取单个笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    joke = joke_service.get_joke_by_id(joke_id)
    
    if not joke:
        return APIResponse.not_found(
            message="笑话不存在",
            request_id=request_id
        )
    
    # 增加查看次数
    joke_service.increment_view_count(joke_id)
    
    return APIResponse.success(
        data=JokeResponse.model_validate(joke),
        message="获取笑话成功",
        request_id=request_id
    )


@router.post("/{joke_id}/favorite")
@safe_limit("30/minute")
async def favorite_joke(
    request: Request,
    joke_id: int,
    db: Session = Depends(get_db)
):
    """收藏笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    success = joke_service.toggle_favorite(joke_id)
    
    if not success:
        return APIResponse.not_found(
            message="笑话不存在",
            request_id=request_id
        )
    
    return APIResponse.success(
        data={"favorited": True},
        message="收藏成功",
        request_id=request_id
    )


@router.get("/user/{user_id}/history")
async def get_user_joke_history(
    request: Request,
    user_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取用户笑话历史"""
    request_id = getattr(request.state, "request_id", None)
    
    joke_service = JokeService(db)
    result = joke_service.get_user_jokes(user_id, page, size)
    
    return APIResponse.success(
        data=result,
        message="获取用户笑话历史成功",
        request_id=request_id
    )


@router.post("/share")
@safe_limit("20/minute")
async def share_joke(
    request: Request,
    share_request: ShareRequest,
    db: Session = Depends(get_db)
):
    """分享笑话"""
    request_id = getattr(request.state, "request_id", None)
    
    # 获取客户端信息
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    share_service = ShareService(db)
    share = await share_service.create_share(
        share_request,
        ip_address=client_ip,
        user_agent=user_agent
    )
    
    return APIResponse.success(
        data=ShareResponse.model_validate(share),
        message="分享记录成功",
        request_id=request_id
    )


@router.get("/share/stats")
async def get_share_stats(
    request: Request,
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    db: Session = Depends(get_db)
):
    """获取分享统计"""
    request_id = getattr(request.state, "request_id", None)
    
    share_service = ShareService(db)
    stats = share_service.get_share_stats(days)
    
    return APIResponse.success(
        data=stats,
        message="获取分享统计成功",
        request_id=request_id
    )