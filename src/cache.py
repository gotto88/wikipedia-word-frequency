from time import time

from pydantic import BaseModel
from typing import ClassVar, TypeVar, Generic

from src.models import WikiPageInfo

CachedDataTyep = TypeVar("CachedDataTyep")


class Cache(Generic[CachedDataTyep]):
    """
    A general cache class.
    """

    class CacheItem(BaseModel):
        data: CachedDataTyep
        timestamp: float

    _cache: ClassVar[dict[str, CacheItem]] = {}

    def __init__(self, ttl: int) -> None:
        self._ttl = ttl

    def get(self, key: str) -> CachedDataTyep | None:
        if key not in self._cache:
            return None
        entry = self._cache[key]
        if time() - entry.timestamp > self._ttl:
            del self._cache[key]
            return None
        return entry.data

    def set(self, key: str, data: CachedDataTyep) -> None:
        self._cache[key] = self.CacheItem(
            data=data,
            timestamp=time()
        )


class WikiPageCache(Cache[WikiPageInfo]):
    """
    A cache for Wikipedia pages.
    """

    def __init__(self, ttl: int) -> None:
        super().__init__(ttl)
