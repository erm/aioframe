import aiohttp
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from aioframe.loaders import get_apps_enabled, load_apps_enabled
from aioframe.loaders import load_apps_enabled

from conf import APPS_REGISTRY, SECRET_KEY, HOSTNAME, PORT


webapp = aiohttp.web.Application()
aiohttp_session.setup(webapp, EncryptedCookieStorage(SECRET_KEY))
APPS_ENABLED = get_apps_enabled(APPS_REGISTRY)
load_apps_enabled(APPS_ENABLED, webapp)
aiohttp.web.run_app(webapp, host=HOSTNAME, port=PORT)
