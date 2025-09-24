"""
数据模型包
"""
from app.models.user import User
from app.models.joke import Joke
from app.models.share import Share
from app.models.preference import UserPreference

__all__ = ["User", "Joke", "Share", "UserPreference"]