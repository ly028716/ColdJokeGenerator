from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# 可选导入 prometheus_client
try:
    from prometheus_client import make_asgi_app
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import setup_middleware
from app.core.response import APIResponse
from app.core.exceptions import BaseCustomException


# 设置日志
setup_logging()
logger = get_logger(__name__)


# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI冷笑话生成器后端API服务",
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("应用启动中...")
    logger.info(f"环境: {settings.ENVIRONMENT}")
    logger.info(f"调试模式: {settings.DEBUG}")


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("应用关闭中...")

# 设置中间件
setup_middleware(app)

# 包含API路由
app.include_router(api_router, prefix="/api")

# 添加监控端点
if settings.ENABLE_METRICS and PROMETHEUS_AVAILABLE:
    metrics_app = make_asgi_app()
    app.mount(settings.METRICS_PATH, metrics_app)
elif settings.ENABLE_METRICS and not PROMETHEUS_AVAILABLE:
    logger.warning("Prometheus client 不可用，跳过监控端点设置")


# 异常处理器
@app.exception_handler(BaseCustomException)
async def custom_exception_handler(request: Request, exc: BaseCustomException):
    """自定义异常处理器"""
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"自定义异常: {exc.detail}")
    return APIResponse.error(
        message=exc.detail,
        code=exc.status_code,
        status_code=exc.status_code,
        request_id=request_id
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP异常处理器"""
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"HTTP异常: {exc.detail}")
    return APIResponse.error(
        message=exc.detail,
        code=exc.status_code,
        status_code=exc.status_code,
        request_id=request_id
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """数据验证异常处理器"""
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"数据验证异常: {exc.errors()}")
    return APIResponse.validation_error(
        message="请求数据验证失败",
        errors=exc.errors(),
        request_id=request_id
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    request_id = getattr(request.state, "request_id", None)
    logger.error(f"未处理异常: {str(exc)}", exc_info=True)
    return APIResponse.error(
        message="服务器内部错误",
        code=500,
        request_id=request_id
    )


# 根路由
@app.get("/")
async def root(request: Request):
    """根路由"""
    request_id = getattr(request.state, "request_id", None)
    return APIResponse.success(
        data={
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "docs_url": "/docs" if settings.DEBUG else None
        },
        message="欢迎使用AI冷笑话生成器API服务",
        request_id=request_id
    )


@app.get("/health")
async def health_check(request: Request):
    """健康检查"""
    request_id = getattr(request.state, "request_id", None)
    return APIResponse.success(
        data={
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        },
        message="服务运行正常",
        request_id=request_id
    )


@app.get("/info")
async def app_info(request: Request):
    """应用信息"""
    request_id = getattr(request.state, "request_id", None)
    return APIResponse.success(
        data={
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "api_version": settings.API_V1_STR
        },
        message="应用信息获取成功",
        request_id=request_id
    )