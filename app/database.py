import os
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Redis 连接
redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

# PostgreSQL 连接
DATABASE_URL = os.getenv("POSTGRES_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)