from typing import Any

from django.core.cache import cache


def store_temporary_data(key: str, value: Any):
    cache.set(key, value, timeout=60**2)


def retrieve_temporary_data(key):
    value = cache.get(key)
    return value


def delete_temporary_data(key):
    cache.delete(key)
