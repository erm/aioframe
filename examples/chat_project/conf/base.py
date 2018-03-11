import os
import asyncio

import peewee
import peewee_async


from aioframe.secrets import get_secret_key
from aioframe.sessions import get_session_storage
from aioframe.models import DATABASE_PROXY


# Project

APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Session
#   - simple_cookie
#   - encrypted_cookie : secret_key=None
#   - redis : redis_host=localhost, redis_port=6379

SECRET_KEY = get_secret_key()

SESSION_STORAGE = get_session_storage('encrypted_cookie', secret_key=SECRET_KEY)

# Apps

APPS_REGISTRY = (
    'chat_app',
    'auth',
)

# Server

HOSTNAME = 'localhost'

PORT = '8000'


# Database

DATABASE = peewee_async.PooledPostgresqlDatabase(
    'test',
    user='',
    password='',
    host='localhost'
)
DATABASE_PROXY.initialize(DATABASE)
OBJECTS = peewee_async.Manager(DATABASE_PROXY)
