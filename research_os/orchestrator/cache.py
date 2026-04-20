from __future__ import annotations

from ..storage.redis_cache import RedisCache


class OrchestrationCache:
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self.cache = RedisCache(url=url)

    def get(self, key: str):
        return self.cache.get_json(key)

    def set(self, key: str, value, ttl_seconds: int = 3600) -> None:
        self.cache.set_json(key, value, ttl_seconds=ttl_seconds)
