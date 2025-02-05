import redis.asyncio as redis

from config import settings


redis_files = redis.Redis(host=settings.REDIS_FILES)
redis_text = redis.Redis(host=settings.REDIS)