class Router:

    def __init__(self, namespace=None):
        self.routes = {}
        self.namespace = namespace

    def route(self, name):
        def _route(func):
            route_name = '/{}/{}'.format(self.namespace, name) if self.namespace else name
            self.routes[route_name] = func
            return func
        return _route

    def get_routes(self, app):
        for route_name, view in self.routes.items():
            print(route_name)
            app.router.add_get(route_name, view)
