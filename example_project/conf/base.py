import os
import asyncio
import time
import base64

from cryptography import fernet

import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

from aioframe.loaders import get_apps_enabled, load_apps_enabled


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS_REGISTRY = (
    'chatroom',
)

APPS_ENABLED = get_apps_enabled(APPS_REGISTRY)

SECRET_KEY = base64.urlsafe_b64decode(fernet.Fernet.generate_key())

webapp = web.Application()
aiohttp_session.setup(webapp, EncryptedCookieStorage(SECRET_KEY))
load_apps_enabled(APPS_ENABLED, webapp)
