class AppConf:

    def __init__(self, app_name, namespace=''):
        self.app_name = app_name
        self.namespace = namespace
        self.view_classes = {}

    def get_views(self, class_name):
        return self.view_classes[class_name]['views']

    def route_class(self):
        def _route_class(view_class):
            class_name = view_class.__qualname__
            view_class_dict = {'view_class': view_class}
            self.view_classes[class_name]['view_class'] = view_class
            return view_class
        return _route_class

    def route(self, path_, name=None, methods=['GET']):
        def _route(func):
            route_path = '/{}/{}'.format(self.namespace, path_)
            route_dict = {'view_func': func, 'methods': methods, 'name': name}
            class_name = func.__qualname__.split('.')[0]
            try:
                self.view_classes[class_name]['views'][route_path] = route_dict
            except KeyError:
                self.view_classes[class_name] = {'view_class': None, 'views': {route_path: route_dict}}
            return func
        return _route

    def setup(self, webapp):
        for name, _dict in self.view_classes.items():
            webapp['AIOFRAME_SETTINGS']['AIOFRAME_APPS'][name] = {'APP_CONF': self}
            view_class = _dict['view_class']
            _views = _dict['views']
            for route_path, route_dict in _views.items():
                print(route_path)
                route_name = route_dict['name']
                webapp.router.add_view(route_path, view_class, name=route_name)
