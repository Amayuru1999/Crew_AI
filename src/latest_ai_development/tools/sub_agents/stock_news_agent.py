import asyncio
import json
from nats.aio.client import Client as NATS

STOCK_NEWS_TOPIC = "agent.stock_news_agent"
CREW_RESPONSES_TOPIC = "crew.responses"

async def stock_news_agent():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    async def news_handler(msg):
        data = json.loads(msg.data.decode())
        task_id = data.get("task_id", "no-id")
        print(f"[StockNewsAgent] Received: {data}")

        # Simulate fetching news
        result = {
            "task_id": task_id,
            "agent": "StockNewsAgent",
            "info": "Weekly stock news retrieved..."
        }

        # Publish result to ExecutorSubAgent
        await nc.publish(CREW_RESPONSES_TOPIC, json.dumps(result).encode())

    await nc.subscribe(STOCK_NEWS_TOPIC, cb=news_handler)
    print("[StockNewsAgent] Listening for tasks...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(stock_news_agent())
