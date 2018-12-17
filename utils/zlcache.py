import memcache

cache = memcache.Client(['129.204.31.108:11211'], debug=True)


def set(key, value, timeout=60):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)