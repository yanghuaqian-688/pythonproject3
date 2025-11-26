import asyncio
import os
import redis.asyncio as aioredis
from dotenv import load_dotenv
import httpx

# 加载 .env
load_dotenv(override=True)
print("📂 当前工作目录:", os.getcwd())
print("📄 .env 文件路径:", os.path.abspath(".env"))
print("📄 是否存在 .env:", os.path.exists(".env"))

REDIS_URL = os.getenv("REDIS_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("DEBUG RAW KEY =", repr(OPENAI_API_KEY))

if not REDIS_URL:
    raise ValueError("REDIS_URL 未配置，请检查 .env 文件")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY 未配置，请检查 .env 文件")

print("🔑 REDIS_URL:", REDIS_URL)
print("🔑 OPENAI_API_KEY:", OPENAI_API_KEY[:8], "...")  # 只显示前8位防泄露

# Worker 主循环
async def worker():
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    print("🤖 Worker 已启动（后台 AI 就绪）")

    while True:
        task_id = await redis.rpop("task_queue")
        if task_id:
            task = await redis.hgetall(f"task:{task_id}")
            question = task.get("question", "")
            if question:
                # 调用 AI
                answer = await get_ai_reply(question)

                # 更新任务状态
                await redis.hset(f"task:{task_id}", mapping={
                    "status": "done",
                    "answer": answer
                })
                print(f"✅ 任务完成 {task_id}")
            else:
                print(f"⚠️ 任务 {task_id} 没有问题内容")
        else:
            await asyncio.sleep(0.2)

# 调用 OpenAI
# 调用 OpenAI
async def get_ai_reply(question: str) -> str:
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": question
            }
        ],
        "max_output_tokens": 200
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(url, headers=headers, json=data)
            resp.raise_for_status()
            result = resp.json()

            # 正常解析（新版 Responses API）
            return result["output"][0]["content"][0]["text"]

        except KeyError:
            # 返回结构异常
            return f"AI 返回结构异常: {result}"

        except httpx.HTTPStatusError as e:
            print("❌ OpenAI API 调用失败:", e.response.text)
            return "AI 调用失败"

        except Exception as e:
            print("❌ 调用 OpenAI 出现异常:", str(e))
            return "AI 调用异常"

if __name__ == "__main__":
    asyncio.run(worker())