from django.core.cache import cache
from .models import Property

from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    # Try to get the queryset from cache
    queryset = cache.get('all_properties')

    if not queryset:
        # If not in cache, fetch from DB
        queryset = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', queryset, 3600)

    return queryset


def get_redis_cache_metrics():
    try:
        # Connect to the default Redis cache
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")

        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

        # Log the metrics
        logger.error(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, Hit Ratio: {hit_ratio:.2f}"
        )

        return {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "hit_ratio": hit_ratio,
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0,
        }