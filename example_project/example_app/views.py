from aiohttp import web

from aioframe.routes import Router


class MyAppView:

    router = Router(namespace='myappview')

    @router.route('somepath/')
    def somepath(request, *args, **kwargs):
        # GET = request.rel_url.query
        # print(GET)
        return web.Response(text="some app path")

    @router.route('somepath/otherpath/')
    def someotherpath(request, *args, **kwargs):
        return web.Response(text="some other app path")

# TODO: Change how this works to allow multiple app_views
app_views = MyAppView()
