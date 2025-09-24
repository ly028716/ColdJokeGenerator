import os
from typing import List, Optional, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目配置
    PROJECT_NAME: str = "AI冷笑话生成器"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="your-secret-key-here-with-enough-characters-for-validation", min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 阿里千问API配置
    QWEN_API_KEY: Optional[str] = Field(default_factory=lambda: os.getenv("QWEN_API_KEY"))
    QWEN_API_URL: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    QWEN_MODEL: str = "qwen-turbo"
    QWEN_MAX_TOKENS: int = 200
    QWEN_TEMPERATURE: float = 0.8
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_ECHO: bool = False
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_EXPIRE_TIME: int = 3600  # 1小时
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_ROTATION: str = "1 day"
    LOG_RETENTION: str = "30 days"
    
    # 安全配置
    CORS_ORIGINS: List[str] = ["*"]
    ENABLE_HTTPS: bool = False
    
    # 缓存配置
    CACHE_EXPIRE_TIME: int = 300  # 5分钟
    ENABLE_CACHE: bool = True
    
    # 监控配置
    ENABLE_METRICS: bool = True
    METRICS_PATH: str = "/metrics"
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()