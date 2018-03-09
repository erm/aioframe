from aiohttp import web

from conf.base import webapp
from conf.settings import HOSTNAME, PORT

web.run_app(webapp, host=HOSTNAME, port=PORT)
