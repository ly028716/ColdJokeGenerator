"""
管理员API接口
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.response import APIResponse
from app.db.session import get_db
from app.services.ai_service import AIService
from app.services.cache_service import cache

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """系统健康检查"""
    request_id = getattr(request.state, "request_id", None)
    
    # 检查数据库连接
    db_status = "healthy"
    try:
        # 这里可以添加数据库连接检查
        pass
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # 检查AI服务
    ai_service = AIService()
    ai_status = await ai_service.test_api_connection()
    
    # 检查缓存服务
    cache_status = cache.get_stats()
    
    health_data = {
        "database": {"status": db_status},
        "ai_service": ai_status,
        "cache": cache_status,
        "overall": "healthy" if db_status == "healthy" and ai_status["status"] == "success" else "degraded"
    }
    
    return APIResponse.success(
        data=health_data,
        message="系统健康检查完成",
        request_id=request_id
    )


@router.post("/cache/clear")
async def clear_cache(
    request: Request,
    pattern: str = "*"
):
    """清除缓存"""
    request_id = getattr(request.state, "request_id", None)
    
    cleared_count = cache.clear_pattern(pattern)
    
    return APIResponse.success(
        data={"cleared_count": cleared_count},
        message=f"成功清除{cleared_count}个缓存项",
        request_id=request_id
    )


@router.get("/stats")
async def get_system_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """获取系统统计信息"""
    request_id = getattr(request.state, "request_id", None)
    
    from app.services.user_service import UserService
    from app.services.share_service import ShareService
    from app.models.joke import Joke
    
    user_service = UserService(db)
    share_service = ShareService(db)
    
    # 用户统计
    user_stats = user_service.get_user_stats()
    
    # 笑话统计
    total_jokes = db.query(Joke).count()
    featured_jokes = db.query(Joke).filter(Joke.is_featured == True).count()
    
    # 分享统计
    share_stats = share_service.get_share_stats(30)  # 30天统计
    
    # 缓存统计
    cache_stats = cache.get_stats()
    
    stats_data = {
        "users": user_stats.model_dump(),
        "jokes": {
            "total": total_jokes,
            "featured": featured_jokes
        },
        "shares": {
            "total": share_stats.total_shares,
            "platforms": share_stats.platform_stats
        },
        "cache": cache_stats
    }
    
    return APIResponse.success(
        data=stats_data,
        message="获取系统统计成功",
        request_id=request_id
    )