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

    def route(self, name, methods=['GET']):
        def _route(func):
            route_name = '/{}/{}'.format(self.namespace, name) if self.namespace else name
            self.views[route_name] = {'view_func': func, 'methods': methods}
            return func
        return _route

    def load_routes(self, webapp):
        for route_name, view in self.views.items():
            view_func = view['view_func']
            methods = view['methods']
            for method in methods:
                webapp.router.add_route(method, route_name, view_func)
