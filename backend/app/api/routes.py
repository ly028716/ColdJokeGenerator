from fastapi import APIRouter, Request
from app.api.v1 import jokes, users, admin
from app.core.response import APIResponse

router = APIRouter()

# 添加测试端点
@router.get("/v1/test")
async def api_test(request: Request):
    """API测试端点"""
    request_id = getattr(request.state, "request_id", None)
    return APIResponse.success(
        data={"message": "API连接正常", "timestamp": "2025-09-24T11:42:50"},
        message="测试成功",
        request_id=request_id
    )

# 包含v1版本的API路由
router.include_router(jokes.router, prefix="/v1/jokes", tags=["jokes"])
router.include_router(users.router, prefix="/v1/users", tags=["users"])
router.include_router(admin.router, prefix="/v1/admin", tags=["admin"])