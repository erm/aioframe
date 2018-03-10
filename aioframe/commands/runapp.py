import aiohttp
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from ..loaders import get_apps_enabled, load_apps_enabled


def run_command(conf):
    webapp = aiohttp.web.Application()
    aiohttp_session.setup(webapp, EncryptedCookieStorage(conf.SECRET_KEY))
    apps_enabled = get_apps_enabled(conf.APPS_REGISTRY)
    load_apps_enabled(apps_enabled, webapp)
    aiohttp.web.run_app(webapp, host=conf.HOSTNAME, port=conf.PORT)
