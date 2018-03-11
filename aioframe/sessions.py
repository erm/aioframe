import aiohttp_session

from .exceptions import SessionStorageDoesNotExist, SessionSecretKeyDoesNotExist


def get_simple_cookie_storage():
    from aiohttp_session.cookie_storage import SimpleCookieStorage
    return SimpleCookieStorage()


def get_encrypted_cookie_storage(secret_key):
    if not secret_key:
        raise SessionSecretKeyDoesNotExist
    from aiohttp_session.cookie_storage import EncryptedCookieStorage
    return EncryptedCookieStorage(secret_key)


def get_redis_storage(redis_host, redis_port):
    from aiohttp_session.redis_storage import RedisStorage
    import aioredis
    redis = yield from aioredis.create_pool((redis_host, redis_port))
    return RedisStorage(redis)


def get_session_storage(storage_name, secret_key=None, redis_host='localhost', redis_port=6379):
    if storage_name == 'simple_cookie':
        return get_simple_cookie_storage()
    if storage_name == 'encrypted_cookie':
        return get_encrypted_cookie_storage(secret_key)
    if storage_name == 'redis':
        return get_redis_storage(redis_host, redis_port)
    raise SessionStorageDoesNotExist(storage_name)

