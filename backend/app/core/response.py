"""
统一响应格式
"""
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse


class DateTimeEncoder(json.JSONEncoder):
    """自定义JSON编码器，处理datetime对象"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ResponseModel(BaseModel):
    """统一响应模型"""
    code: int
    message: str
    data: Optional[Any] = None
    request_id: Optional[str] = None


class APIResponse:
    """API响应工具类"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "操作成功",
        code: int = 200,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """成功响应"""
        response_data = ResponseModel(
            code=code,
            message=message,
            data=data,
            request_id=request_id
        )
        # 使用自定义编码器处理datetime对象
        content = json.loads(json.dumps(response_data.model_dump(), cls=DateTimeEncoder))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=content
        )
    
    @staticmethod
    def error(
        message: str = "操作失败",
        code: int = 500,
        data: Any = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """错误响应"""
        response_data = ResponseModel(
            code=code,
            message=message,
            data=data,
            request_id=request_id
        )
        return JSONResponse(
            status_code=status_code,
            content=response_data.model_dump()
        )
    
    @staticmethod
    def validation_error(
        message: str = "数据验证失败",
        errors: Optional[Dict] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """验证错误响应"""
        return APIResponse.error(
            message=message,
            code=422,
            data={"errors": errors} if errors else None,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            request_id=request_id
        )
    
    @staticmethod
    def not_found(
        message: str = "资源未找到",
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """404响应"""
        return APIResponse.error(
            message=message,
            code=404,
            status_code=status.HTTP_404_NOT_FOUND,
            request_id=request_id
        )
    
    @staticmethod
    def unauthorized(
        message: str = "未授权访问",
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """401响应"""
        return APIResponse.error(
            message=message,
            code=401,
            status_code=status.HTTP_401_UNAUTHORIZED,
            request_id=request_id
        )
    
    @staticmethod
    def forbidden(
        message: str = "禁止访问",
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """403响应"""
        return APIResponse.error(
            message=message,
            code=403,
            status_code=status.HTTP_403_FORBIDDEN,
            request_id=request_id
        )
    
    @staticmethod
    def rate_limit(
        message: str = "请求过于频繁",
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """429响应"""
        return APIResponse.error(
            message=message,
            code=429,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            request_id=request_id
        )