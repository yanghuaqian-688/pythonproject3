import os
import asyncio
import asyncpg
from dotenv import load_dotenv
import aioredis

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")  # 包含 "postgresql+asyncpg://..."
REDIS_URL = os.getenv("REDIS_URL")

async def test_postgres():
    try:
        # 使用 asyncpg.connect 连接数据库（去掉 sslmode=...）
        conn = await asyncpg.connect(
            user="neondb_owner",
            password="npg_LhovGcZ8di7A",
            database="neondb",
            host="ep-noisy-lake-a1ec4l2q-pooler.ap-southeast-1.aws.neon.tech",
            port=5432,
            ssl="require"  # asyncpg 要用 ssl=True 或 ssl="require"
        )
        version = await conn.fetchval("SELECT version();")
        print("✅ PostgreSQL connection successful! Version:", version)
        await conn.close()
    except Exception as e:
        print("❌ PostgreSQL connection error:", e)

async def test_redis():
    try:
        redis = aioredis.from_url(REDIS_URL, decode_responses=True)
        pong = await redis.ping()
        print("✅ Redis connection successful!" if pong else "❌ Redis connection failed!")
    except Exception as e:
        print("❌ Redis connection error:", e)

async def main():
    await test_redis()
    await test_postgres()

asyncio.run(main())