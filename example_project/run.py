from aiohttp import web

from conf.base import webapp

web.run_app(webapp, host='localhost', port=8080)
