def register(app, webapp):
    def wrapper(view_class):
        class ViewClass(view_class):
            def __init__(self, *args, **kwargs):
                self.app = app
                self.webapp = webapp
                super(ViewClass, self).__init__(*args, **kwargs)
        return ViewClass
    return wrapper


class AppConf:

    def __init__(self, app_name, namespace=None):
        self.app_name = app_name
        self.namespace = namespace
        self.views = {}

    def route(self, name):
        def _route(func):
            route_name = '/{}/{}'.format(self.namespace, name) if self.namespace else name
            self.views[route_name] = func
            return func
        return _route

    def load_routes(self, webapp):
        for route_name, view in self.views.items():
            webapp.router.add_get(route_name, view)
