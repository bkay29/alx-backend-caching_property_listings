from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get the queryset from cache
    queryset = cache.get('all_properties')

    if not queryset:
        # If not in cache, fetch from DB
        queryset = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', queryset, 3600)

    return queryset