"""
自定义异常类
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class BaseCustomException(HTTPException):
    """基础自定义异常类"""
    
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class JokeGenerationException(BaseCustomException):
    """笑话生成异常"""
    
    def __init__(self, detail: str = "笑话生成失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class APIKeyException(BaseCustomException):
    """API密钥异常"""
    
    def __init__(self, detail: str = "API密钥无效或缺失"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class RateLimitException(BaseCustomException):
    """限流异常"""
    
    def __init__(self, detail: str = "请求过于频繁，请稍后再试"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        )


class DatabaseException(BaseCustomException):
    """数据库异常"""
    
    def __init__(self, detail: str = "数据库操作失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ValidationException(BaseCustomException):
    """数据验证异常"""
    
    def __init__(self, detail: str = "数据验证失败"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )