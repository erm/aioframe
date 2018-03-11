import aiohttp
import aiohttp_session

from aioframe.loaders import load_apps_enabled

from chat_project import conf


webapp = aiohttp.web.Application()
aiohttp_session.setup(webapp, conf.SESSION_STORAGE)
load_apps_enabled(webapp, conf)
# aiohttp.web.run_app(webapp, host=conf.HOSTNAME, port=conf.PORT)
