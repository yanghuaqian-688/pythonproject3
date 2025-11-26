import os
import aioredis

# 严格从环境变量读取 Redis URL
REDIS_URL = os.environ["REDIS_URL"]

async def init_redis():
    """初始化 Redis 客户端并返回对象"""
    return await aioredis.from_url(REDIS_URL, decode_responses=True)