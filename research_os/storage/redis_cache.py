from __future__ import annotations

import json
from typing import Any


class RedisCache:
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self.url = url
        self.client = None
        try:
            import redis

            self.client = redis.Redis.from_url(url)
            self.client.ping()
        except Exception:
            self.client = None

    @property
    def available(self) -> bool:
        return self.client is not None

    def get_json(self, key: str) -> Any:
        if not self.client:
            return None
        value = self.client.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set_json(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        if not self.client:
            return
        self.client.setex(key, ttl_seconds, json.dumps(value, ensure_ascii=False))
