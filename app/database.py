import os
import asyncpg

# 严格从环境变量读取 PostgreSQL URL
POSTGRES_URL = os.environ["POSTGRES_URL"]

async def test_postgres_connection():
    """连接 PostgreSQL 测试并返回版本"""
    conn = await asyncpg.connect(POSTGRES_URL)
    version = await conn.fetchval("SELECT version()")
    await conn.close()
    return version