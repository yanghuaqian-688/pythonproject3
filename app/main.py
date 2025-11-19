from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import redis_client, SessionLocal

app = FastAPI()

# PostgreSQL 会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    redis_client.set("message", "Hello Redis + FastAPI!")
    value = redis_client.get("message")
    return {"redis_value": value}

@app.get("/increment")
def increment_counter():
    count = redis_client.incr("counter")
    return {"counter": count}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    # 简单测试 PostgreSQL 连接
    result = db.execute("SELECT version();").fetchone()
    return {"postgres_version": result[0]}