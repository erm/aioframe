import aiohttp
import aioframe
import conf


webapp = aiohttp.web.Application()
aioframe.setup(webapp, conf)

#gunicorn webapp:webapp --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker