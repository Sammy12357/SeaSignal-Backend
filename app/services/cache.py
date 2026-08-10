import time
import functools


def ttl_cache(ttl_seconds):
    def decorator(func):
        store = {}

        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in store:
                timestamp, value = store[args]
                if now - timestamp < ttl_seconds:
                    return value          # fresh enough — reuse
            value = func(*args)           # stale or missing — recompute
            store[args] = (now, value)
            return value

        return wrapper
    return decorator