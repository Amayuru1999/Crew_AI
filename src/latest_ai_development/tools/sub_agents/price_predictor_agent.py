import asyncio
import json
from nats.aio.client import Client as NATS

PRICE_PREDICTOR_TOPIC = "agent.price_predictor"
CREW_RESPONSES_TOPIC = "crew.responses"

async def price_predictor_agent():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    async def predictor_handler(msg):
        data = json.loads(msg.data.decode())
        task_id = data.get("task_id", "no-id")
        print(f"[PricePredictorAgent] Received: {data}")

        # Simulate AI-driven stock recommendation
        result = {
            "task_id": task_id,
            "agent": "PricePredictorAgent",
            "info": "Buy TSLA, NVDA, AAPL"
        }

        await nc.publish(CREW_RESPONSES_TOPIC, json.dumps(result).encode())

    await nc.subscribe(PRICE_PREDICTOR_TOPIC, cb=predictor_handler)
    print("[PricePredictorAgent] Listening for tasks...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(price_predictor_agent())
