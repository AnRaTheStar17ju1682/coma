import redis.asyncio as redis


redis_files = redis.Redis(host="redis-images")
redis_text = redis.Redis(host="redis")