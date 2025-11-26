from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from app.redis_client import init_redis
import uuid

app = FastAPI(title="AI Worker Demo")

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis()
    print("✅ Redis 已初始化")

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "").strip()
    if not question:
        return {"error": "请提供问题"}

    redis = app.state.redis
    task_id = str(uuid.uuid4())

    await redis.lpush("task_queue", task_id)
    await redis.hset(f"task:{task_id}", mapping={"question": question, "status": "pending"})

    return {"task_id": task_id, "status": "pending"}

@app.get("/task/{task_id}")
async def get_task(task_id: str):
    redis = app.state.redis
    task = await redis.hgetall(f"task:{task_id}")
    if not task:
        return {"error": "任务不存在"}
    return task