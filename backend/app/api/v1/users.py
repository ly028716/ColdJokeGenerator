"""
用户相关API接口
"""
from typing import Optional
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
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserStatsResponse
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("/")
async def create_user(
    request: Request,
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """创建用户"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    
    # 检查用户是否已存在
    existing_user = user_service.get_user_by_openid(user_create.openid)
    if existing_user:
        return APIResponse.error(
            message="用户已存在",
            code=400,
            request_id=request_id
        )
    
    user = user_service.create_user(user_create)
    
    return APIResponse.success(
        data=UserResponse.model_validate(user),
        message="用户创建成功",
        request_id=request_id
    )


@router.get("/{user_id}")
async def get_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户信息"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.not_found(
            message="用户不存在",
            request_id=request_id
        )
    
    return APIResponse.success(
        data=UserResponse.model_validate(user),
        message="获取用户信息成功",
        request_id=request_id
    )


@router.get("/openid/{openid}")
async def get_user_by_openid(
    request: Request,
    openid: str,
    db: Session = Depends(get_db)
):
    """通过openid获取用户信息"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    user = user_service.get_user_by_openid(openid)
    
    if not user:
        return APIResponse.not_found(
            message="用户不存在",
            request_id=request_id
        )
    
    return APIResponse.success(
        data=UserResponse.model_validate(user),
        message="获取用户信息成功",
        request_id=request_id
    )


@router.put("/{user_id}")
async def update_user(
    request: Request,
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_update)
    
    if not user:
        return APIResponse.not_found(
            message="用户不存在",
            request_id=request_id
        )
    
    return APIResponse.success(
        data=UserResponse.model_validate(user),
        message="用户信息更新成功",
        request_id=request_id
    )


@router.post("/{user_id}/login")
@safe_limit("10/minute")
async def user_login(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    """用户登录"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    user = user_service.update_last_login(user_id)
    
    if not user:
        return APIResponse.not_found(
            message="用户不存在",
            request_id=request_id
        )
    
    return APIResponse.success(
        data=UserResponse.model_validate(user),
        message="登录成功",
        request_id=request_id
    )


@router.get("/")
async def get_users(
    request: Request,
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=50, description="每页数量"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    result = user_service.get_users(page, size, is_active)
    
    return APIResponse.success(
        data=result,
        message="获取用户列表成功",
        request_id=request_id
    )


@router.get("/stats/overview")
async def get_user_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """获取用户统计信息"""
    request_id = getattr(request.state, "request_id", None)
    
    user_service = UserService(db)
    stats = user_service.get_user_stats()
    
    return APIResponse.success(
        data=stats,
        message="获取用户统计成功",
        request_id=request_id
    )