import aiohttp
import aiohttp_session

# from ..contrib import auth
from ..loaders import load_apps_enabled


def run_command(conf):
    webapp = aiohttp.web.Application()
    aiohttp_session.setup(webapp, conf.SESSION_STORAGE)
    # auth.setup(webapp)
    load_apps_enabled(webapp, conf)
    aiohttp.web.run_app(webapp, host=conf.HOSTNAME, port=conf.PORT)
