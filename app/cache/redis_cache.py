import os
import redis.asyncio as redis
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisCache:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        self.simulate_down = False

    async def get_json(self, key: str):
        if self.simulate_down:
            raise redis.ConnectionError("Simulated Redis down")
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_json(self, key: str, value, expire: int = 300):
        if self.simulate_down:
            raise redis.ConnectionError("Simulated Redis down")
        await self.redis.set(key, json.dumps(value), ex=expire)

redis_cache = RedisCache() 