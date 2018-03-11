import aiohttp
import aiohttp_session

from aioframe.loaders import load_apps_enabled

import conf


def get_webapp(conf):
    webapp = aiohttp.web.Application()
    aiohttp_session.setup(webapp, conf.SESSION_STORAGE)
    # auth.setup(webapp)
    load_apps_enabled(webapp, conf)
    #aiohttp.web.run_app(webapp, host=conf.HOSTNAME, port=conf.PORT)
    return webapp

webapp = get_webapp(conf)
# gunicorn webapp:webapp --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker