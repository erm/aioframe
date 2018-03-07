from aiohttp import web

from conf.base import APPS_ENABLED

webapp = web.Application()
for app_name, app_module in APPS_ENABLED.items():
    # See TODO in example_app.views
    print(app_module.views.app_views.router.routes)
    app_module.views.app_views.router.get_routes(webapp)

web.run_app(webapp, host='127.0.0.1', port=8080)
