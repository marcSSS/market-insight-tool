from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基本配置
    APP_NAME: str = "北美市场洞察工具"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost/market_intelligence"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI配置
    OPENAI_API_KEY: str = ""
    
    # 外部API配置
    MARKET_DATA_API_KEY: Optional[str] = None
    SOCIAL_MEDIA_API_KEY: Optional[str] = None
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 分析配置
    MAX_ANALYSIS_DURATION: int = 300  # 秒
    MAX_CONTENT_LENGTH: int = 10000   # 字符
    
    # 缓存配置
    CACHE_TTL: int = 3600  # 秒
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置实例
settings = Settings()

# 从环境变量加载配置
def get_settings() -> Settings:
    return settings 