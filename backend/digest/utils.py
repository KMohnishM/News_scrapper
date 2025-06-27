import hashlib
from django.core.cache import cache

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()

def is_article_seen(url):
    key = f"article_seen:{hash_url(url)}"
    return cache.get(key)

def mark_article_seen(url):
    key = f"article_seen:{hash_url(url)}"
    cache.set(key, 1, timeout=60*60*24)  # 24 hours 