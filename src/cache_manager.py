"""
Cache Manager for Social Image Generator
Provides caching for processed images and generated content
"""
import hashlib
import os
import pickle
import time
from typing import Optional, Any
from functools import wraps
import json


class CacheManager:
    """
    Simple filesystem-based cache manager for image processing
    """

    def __init__(self, cache_dir: str = 'cache', ttl: int = 3600):
        """
        Initialize cache manager

        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.enabled = True

        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, key_data: Any) -> str:
        """
        Generate cache key from data

        Args:
            key_data: Data to hash (will be converted to JSON)

        Returns:
            Hash string to use as cache key
        """
        # Convert to JSON for consistent hashing
        if isinstance(key_data, (dict, list)):
            key_str = json.dumps(key_data, sort_keys=True)
        else:
            key_str = str(key_data)

        # Generate SHA256 hash
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> str:
        """Get full path for cache file"""
        return os.path.join(self.cache_dir, f"{cache_key}.cache")

    def get(self, key_data: Any) -> Optional[Any]:
        """
        Get item from cache

        Args:
            key_data: Key data to look up

        Returns:
            Cached value or None if not found/expired
        """
        if not self.enabled:
            return None

        try:
            cache_key = self._get_cache_key(key_data)
            cache_path = self._get_cache_path(cache_key)

            # Check if cache file exists
            if not os.path.exists(cache_path):
                return None

            # Check if cache is expired
            if self.ttl > 0:
                file_age = time.time() - os.path.getmtime(cache_path)
                if file_age > self.ttl:
                    # Cache expired, remove it
                    os.remove(cache_path)
                    return None

            # Load and return cached data
            with open(cache_path, 'rb') as f:
                cached_data = pickle.load(f)
                return cached_data

        except Exception as e:
            # If anything goes wrong, just return None (cache miss)
            print(f"Cache read error: {e}")
            return None

    def set(self, key_data: Any, value: Any) -> bool:
        """
        Store item in cache

        Args:
            key_data: Key data
            value: Value to cache

        Returns:
            True if successful
        """
        if not self.enabled:
            return False

        try:
            cache_key = self._get_cache_key(key_data)
            cache_path = self._get_cache_path(cache_key)

            # Store data
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f, protocol=pickle.HIGHEST_PROTOCOL)

            return True

        except Exception as e:
            print(f"Cache write error: {e}")
            return False

    def delete(self, key_data: Any) -> bool:
        """
        Delete item from cache

        Args:
            key_data: Key data

        Returns:
            True if deleted
        """
        try:
            cache_key = self._get_cache_key(key_data)
            cache_path = self._get_cache_path(cache_key)

            if os.path.exists(cache_path):
                os.remove(cache_path)
                return True

            return False

        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    def clear(self) -> int:
        """
        Clear all cache entries

        Returns:
            Number of entries deleted
        """
        try:
            count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    filepath = os.path.join(self.cache_dir, filename)
                    os.remove(filepath)
                    count += 1
            return count

        except Exception as e:
            print(f"Cache clear error: {e}")
            return 0

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries

        Returns:
            Number of entries removed
        """
        if self.ttl <= 0:
            return 0

        try:
            count = 0
            current_time = time.time()

            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    filepath = os.path.join(self.cache_dir, filename)
                    file_age = current_time - os.path.getmtime(filepath)

                    if file_age > self.ttl:
                        os.remove(filepath)
                        count += 1

            return count

        except Exception as e:
            print(f"Cache cleanup error: {e}")
            return 0

    def disable(self):
        """Disable caching"""
        self.enabled = False

    def enable(self):
        """Enable caching"""
        self.enabled = True


# Global cache instance
_cache_manager = None


def get_cache_manager(cache_dir: str = 'cache', ttl: int = 3600) -> CacheManager:
    """
    Get or create global cache manager instance

    Args:
        cache_dir: Cache directory
        ttl: Time to live in seconds

    Returns:
        CacheManager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(cache_dir, ttl)
    return _cache_manager


def cached(ttl: int = 3600, key_func=None):
    """
    Decorator to cache function results

    Args:
        ttl: Time to live in seconds
        key_func: Optional function to generate cache key from args

    Example:
        @cached(ttl=600)
        def expensive_operation(param1, param2):
            # ... expensive computation
            return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache_manager(ttl=ttl)

            # Generate cache key
            if key_func:
                cache_key_data = key_func(*args, **kwargs)
            else:
                # Default: use function name + args + kwargs
                cache_key_data = {
                    'function': func.__name__,
                    'args': args,
                    'kwargs': kwargs
                }

            # Try to get from cache
            cached_result = cache.get(cache_key_data)
            if cached_result is not None:
                return cached_result

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key_data, result)

            return result

        return wrapper
    return decorator
