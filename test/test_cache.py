from unittest.mock import patch
from time import time

from src.cache import Cache


class TestCache:
    """Test cases for the general Cache class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        Cache._cache.clear()
        self.cache = Cache[int](ttl=60)  # 60 seconds TTL

    def test_get_not_found_entry(self):
        """Test case: get returns None for non-existing cache entry."""
        result = self.cache.get("non_existent_key")
        assert result is None
        assert len(self.cache._cache) == 0

    def test_set_get_operation(self):
        """Test case: set and get operations work correctly."""
        key = "test_key"
        data = 42
        self.cache.set(key, data)
        assert len(self.cache._cache) == 1
        assert key in self.cache._cache
        result = self.cache.get(key)
        assert result == 42

    def test_outdated_entry_removal(self):
        """Test case: outdated entries are automatically removed on get."""
        key = "outdated_key"
        data = 100
        short_ttl_cache = Cache[int](ttl=1)
        short_ttl_cache.set(key, data)
        assert short_ttl_cache.get(key) == data
        with patch('src.cache.time') as mock_time:
            mock_time.return_value = time() + 2
            result = short_ttl_cache.get(key)
            assert result is None
            assert key not in short_ttl_cache._cache
            assert len(short_ttl_cache._cache) == 0

    def test_outdated_entry_removal_add_again(self):
        """Test case: outdated entries are automatically
           removed on get and can be added again.
        """
        key = "outdated_key"
        data = 100
        short_ttl_cache = Cache[int](ttl=1)
        short_ttl_cache.set(key, data)
        assert short_ttl_cache.get(key) == data
        with patch('src.cache.time') as mock_time:
            mock_time.return_value = time() + 2
            result = short_ttl_cache.get(key)
            assert result is None
            assert key not in short_ttl_cache._cache
            assert len(short_ttl_cache._cache) == 0
        short_ttl_cache.set(key, data)
        assert short_ttl_cache.get(key) == data
        assert len(short_ttl_cache._cache) == 1
        assert key in short_ttl_cache._cache

    def test_multiple_entries(self):
        """Test case: multiple entries can be stored and retrieved."""
        entries = {
            "key1": 10,
            "key2": 20,
            "key3": 30
        }
        for key, data in entries.items():
            self.cache.set(key, data)
        assert len(self.cache._cache) == 3
        for key, expected_data in entries.items():
            result = self.cache.get(key)
            assert result == expected_data
