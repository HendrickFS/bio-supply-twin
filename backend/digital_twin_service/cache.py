"""
Bio Supply Digital Twin Service - Redis Cache Manager
===================================================

Purpose:
    Redis-based caching layer for the Digital Twin service to improve
    performance by caching frequently accessed data and API responses.

Dependencies:
    - redis: Redis client library
    - json: Data serialization
    - logging: Error handling and monitoring

"""

import redis
import json
import logging
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, host: str = "redis", port: int = 6379, db: int = 0):
        """
        Initialize Redis cache manager with connection pooling.
        
        Args:
            host: Redis server hostname
            port: Redis server port
            db: Redis database number (0-15)
        """
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            self.redis_client.ping()
            self.connected = True
            logger.info(f"Redis cache connected to {host}:{port}")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Cache will be disabled.")
            self.redis_client = None
            self.connected = False

    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with consistent format."""
        return f"bio_supply:{prefix}:{identifier}"

    def get(self, key: str, prefix: str = "general") -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key identifier
            prefix: Cache key prefix for organization
            
        Returns:
            Cached value or None if not found/expired
        """
        if not self.connected:
            return None
            
        try:
            cache_key = self._generate_key(prefix, key)
            cached_value = self.redis_client.get(cache_key)
            
            if cached_value:
                logger.debug(f"Cache HIT: {cache_key}")
                return json.loads(cached_value)
            else:
                logger.debug(f"Cache MISS: {cache_key}")
                return None
                
        except Exception as e:
            logger.error(f"Cache GET error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300, prefix: str = "general") -> bool:
        """
        Set value in cache with TTL.
        
        Args:
            key: Cache key identifier
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 5 minutes)
            prefix: Cache key prefix for organization
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
            
        try:
            cache_key = self._generate_key(prefix, key)
            serialized_value = json.dumps(value, default=str)  # Handle datetime objects
            
            result = self.redis_client.setex(cache_key, ttl, serialized_value)
            logger.debug(f"Cache SET: {cache_key} (TTL: {ttl}s)")
            return result
            
        except Exception as e:
            logger.error(f"Cache SET error for key {key}: {e}")
            return False

    def delete(self, key: str, prefix: str = "general") -> bool:
        """Delete specific cache entry."""
        if not self.connected:
            return False
            
        try:
            cache_key = self._generate_key(prefix, key)
            result = self.redis_client.delete(cache_key)
            logger.debug(f"Cache DELETE: {cache_key}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"Cache DELETE error for key {key}: {e}")
            return False

    def clear_prefix(self, prefix: str) -> int:
        """
        Clear all cache entries with specific prefix.
        
        Args:
            prefix: Prefix to match for deletion
            
        Returns:
            Number of keys deleted
        """
        if not self.connected:
            return 0
            
        try:
            pattern = self._generate_key(prefix, "*")
            keys = self.redis_client.keys(pattern)
            
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Cache CLEAR: Deleted {deleted} keys with prefix '{prefix}'")
                return deleted
            return 0
            
        except Exception as e:
            logger.error(f"Cache CLEAR error for prefix {prefix}: {e}")
            return 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics and health info."""
        if not self.connected:
            return {"status": "disconnected", "error": "Redis not available"}
            
        try:
            info = self.redis_client.info()
            return {
                "status": "connected",
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"status": "error", "error": str(e)}

    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage."""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

    # Convenience methods for common cache patterns
    def cache_api_response(self, endpoint: str, data: Any) -> bool:
        """Cache API response with 30 second TTL."""
        return self.set(endpoint, data, ttl=30, prefix="api")

    def cache_db_query(self, query_id: str, data: Any) -> bool:
        """Cache database query result with 60 second TTL."""
        return self.set(query_id, data, ttl=60, prefix="db")

    def cache_analytics(self, analysis_id: str, data: Any) -> bool:
        """Cache analytics result with 120 second TTL."""
        return self.set(analysis_id, data, ttl=120, prefix="analytics")

    def get_api_cache(self, endpoint: str) -> Optional[Any]:
        """Get cached API response."""
        return self.get(endpoint, prefix="api")

    def get_db_cache(self, query_id: str) -> Optional[Any]:
        """Get cached database query result."""
        return self.get(query_id, prefix="db")

    def get_analytics_cache(self, analysis_id: str) -> Optional[Any]:
        """Get cached analytics result."""
        return self.get(analysis_id, prefix="analytics")

    def invalidate_box_cache(self, box_id: str):
        """Invalidate all cache entries related to a specific box."""
        self.clear_prefix(f"box_{box_id}")
        self.clear_prefix("api")  # Invalidate API caches that might include this box

    def invalidate_sample_cache(self, sample_id: str):
        """Invalidate all cache entries related to a specific sample."""
        self.clear_prefix(f"sample_{sample_id}")
        self.clear_prefix("api")  # Invalidate API caches that might include this sample


# Global cache instance
cache = CacheManager()