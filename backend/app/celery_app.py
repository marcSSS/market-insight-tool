from celery import Celery
from app.core.config import settings

# 创建Celery实例
celery_app = Celery(
    "market_intelligence",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.services.market_analyzer", "app.services.user_analyzer", "app.services.competitor_analyzer"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟
    task_soft_time_limit=25 * 60,  # 25分钟
) 