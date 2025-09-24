from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class JokeGenerateRequest(BaseModel):
    """笑话生成请求模型"""
    category: Optional[str] = Field(None, description="笑话分类")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    length: Optional[str] = Field("medium", description="长度偏好: short/medium/long")
    temperature: Optional[float] = Field(0.8, ge=0.1, le=2.0, description="生成温度")
    custom_prompt: Optional[str] = Field(None, description="自定义提示词")


class JokeBatchGenerateRequest(BaseModel):
    """批量生成笑话请求模型"""
    count: int = Field(1, ge=1, le=10, description="生成数量")
    category: Optional[str] = Field(None, description="笑话分类")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    length: Optional[str] = Field("medium", description="长度偏好")
    temperature: Optional[float] = Field(0.8, ge=0.1, le=2.0, description="生成温度")


class JokeBase(BaseModel):
    """笑话基础模型"""
    content: str = Field(..., description="笑话内容")
    category: Optional[str] = Field(None, description="笑话分类")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class JokeCreate(JokeBase):
    """创建笑话模型"""
    prompt: Optional[str] = Field(None, description="生成提示词")
    model_name: Optional[str] = Field(None, description="模型名称")
    temperature: Optional[float] = Field(None, description="生成温度")
    user_id: Optional[int] = Field(None, description="用户ID")


class JokeUpdate(BaseModel):
    """更新笑话模型"""
    content: Optional[str] = Field(None, description="笑话内容")
    category: Optional[str] = Field(None, description="笑话分类")
    tags: Optional[str] = Field(None, description="标签")
    is_featured: Optional[bool] = Field(None, description="是否精选")
    is_public: Optional[bool] = Field(None, description="是否公开")


class JokeInDB(JokeBase):
    """数据库中的笑话模型"""
    id: int
    user_id: Optional[int] = None
    view_count: int = 0
    share_count: int = 0
    like_count: int = 0
    quality_score: Optional[float] = None
    is_featured: bool = False
    is_public: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JokeResponse(JokeInDB):
    """笑话响应模型"""
    pass


class JokeListResponse(BaseModel):
    """笑话列表响应模型"""
    items: List[JokeResponse]
    total: int
    page: int
    size: int
    pages: int


class ShareRequest(BaseModel):
    """分享请求模型"""
    joke_id: int = Field(..., description="笑话ID")
    share_to: str = Field(..., description="分享平台")
    share_title: Optional[str] = Field(None, description="分享标题")
    share_desc: Optional[str] = Field(None, description="分享描述")
    device_info: Optional[str] = Field(None, description="设备信息")


class ShareCreate(ShareRequest):
    """创建分享记录模型"""
    user_id: Optional[int] = Field(None, description="用户ID")
    share_url: Optional[str] = Field(None, description="分享链接")
    ip_address: Optional[str] = Field(None, description="IP地址")
    user_agent: Optional[str] = Field(None, description="用户代理")


class ShareInDB(BaseModel):
    """数据库中的分享记录模型"""
    id: int
    user_id: Optional[int]
    joke_id: int
    share_to: str
    share_url: Optional[str]
    share_title: Optional[str]
    share_desc: Optional[str]
    click_count: int
    device_info: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShareResponse(ShareInDB):
    """分享响应模型"""
    pass


class ShareStatsResponse(BaseModel):
    """分享统计响应模型"""
    total_shares: int
    platform_stats: dict
    recent_shares: List[ShareResponse]
    top_shared_jokes: List[JokeResponse]