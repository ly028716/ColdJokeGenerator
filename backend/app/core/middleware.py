"""
中间件配置
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

# 可选导入 slowapi
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
    SLOWAPI_AVAILABLE = True
    # 创建限流器
    limiter = Limiter(key_func=get_remote_address)
except ImportError:
    SLOWAPI_AVAILABLE = False
    limiter = None

from app.core.config import settings


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"Request started - ID: {request_id} | "
            f"Method: {request.method} | "
            f"URL: {request.url} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(
            f"Request completed - ID: {request_id} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        
        # 添加响应头
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_middleware(app):
    """设置中间件"""
    
    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 受信任主机中间件
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )
    
    # 限流中间件（可选）
    if SLOWAPI_AVAILABLE:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
    else:
        logger.warning("SlowAPI 不可用，跳过限流中间件设置")
    
    # 日志中间件
    app.add_middleware(LoggingMiddleware)