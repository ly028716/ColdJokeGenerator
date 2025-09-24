"""
缓存服务
"""
import json
import pickle
from typing import Any, Optional, Union
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """缓存服务类"""
    
    def __init__(self):
        self.redis_client = None
        self.enabled = settings.ENABLE_CACHE
        
        if self.enabled:
            try:
                self.redis_client = Redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=False,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # 测试连接
                self.redis_client.ping()
                logger.info("Redis连接成功")
            except Exception as e:
                logger.warning(f"Redis连接失败: {e}，缓存功能将被禁用")
                self.enabled = False
                self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            data = self.redis_client.get(key)
            if data:
                return pickle.loads(data)
            return None
        except RedisError as e:
            logger.error(f"获取缓存失败: {e}")
            return None
        except Exception as e:
            logger.error(f"反序列化缓存数据失败: {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """设置缓存"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            data = pickle.dumps(value)
            expire_time = expire or settings.CACHE_EXPIRE_TIME
            
            result = self.redis_client.setex(key, expire_time, data)
            return bool(result)
        except RedisError as e:
            logger.error(f"设置缓存失败: {e}")
            return False
        except Exception as e:
            logger.error(f"序列化缓存数据失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            result = self.redis_client.delete(key)
            return bool(result)
        except RedisError as e:
            logger.error(f"删除缓存失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except RedisError as e:
            logger.error(f"检查缓存存在性失败: {e}")
            return False
    
    def get_json(self, key: str) -> Optional[dict]:
        """获取JSON格式缓存"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data.decode('utf-8'))
            return None
        except RedisError as e:
            logger.error(f"获取JSON缓存失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return None
    
    def set_json(
        self,
        key: str,
        value: dict,
        expire: Optional[int] = None
    ) -> bool:
        """设置JSON格式缓存"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            data = json.dumps(value, ensure_ascii=False)
            expire_time = expire or settings.CACHE_EXPIRE_TIME
            
            result = self.redis_client.setex(key, expire_time, data)
            return bool(result)
        except RedisError as e:
            logger.error(f"设置JSON缓存失败: {e}")
            return False
        except json.JSONEncodeError as e:
            logger.error(f"JSON序列化失败: {e}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """递增计数器"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            return self.redis_client.incrby(key, amount)
        except RedisError as e:
            logger.error(f"递增计数器失败: {e}")
            return None
    
    def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.expire(key, seconds))
        except RedisError as e:
            logger.error(f"设置过期时间失败: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """清除匹配模式的缓存"""
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except RedisError as e:
            logger.error(f"清除模式缓存失败: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        if not self.enabled or not self.redis_client:
            return {"enabled": False}
        
        try:
            info = self.redis_client.info()
            return {
                "enabled": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "total_commands_processed": info.get("total_commands_processed", 0)
            }
        except RedisError as e:
            logger.error(f"获取缓存统计失败: {e}")
            return {"enabled": True, "error": str(e)}


# 全局缓存实例
cache = CacheService()