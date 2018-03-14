import aiohttp
from .. import setup


def run_command(conf):
    webapp = aiohttp.web.Application()
    setup(webapp, conf)
    aiohttp.web.run_app(webapp, host=conf.HOSTNAME, port=conf.PORT)
