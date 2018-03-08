from aiohttp import web

from conf.base import APPS_ENABLED

webapp = web.Application()
for app_name, app_module in APPS_ENABLED.items():
    app_module.views.app_views(app_name, webapp).router.get_routes(webapp)

web.run_app(webapp, host='127.0.0.1', port=8080)
