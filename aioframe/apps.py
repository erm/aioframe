def register_view_class(app_conf):
    def wrapper(view_class):
        class ViewClass(view_class):
            def __init__(self, *args, **kwargs):
                self.app_conf = app_conf
                super(ViewClass, self).__init__(*args, **kwargs)
        return ViewClass
    return wrapper


class AppConf:

    def __init__(self, app_name, namespace=None):
        self.app_name = app_name
        self.namespace = namespace
        self.view_classes = {}

    def get_views(self, class_name):
        return self.view_classes[class_name]['views']

    def route_class(self, name):
        def _route_class(view_class):
            self.view_classes[view_class.__qualname__]['view_class'] = view_class
            return view_class
        return _route_class

    def route(self, name, methods=['GET']):
        def _route(func):
            route_name = '/' + name
            route_dict = {'view_func': func, 'methods': methods}
            class_name = func.__qualname__.split('.')[0]
            try:
                self.view_classes[class_name]['views'][route_name] = route_dict
            except KeyError:
                self.view_classes[class_name] = {'view_class': None, 'views': {route_name: route_dict}}
            return func
        return _route

    def load_routes(self, webapp):
        for _name, _dict in self.view_classes.items():
            webapp['AIOFRAME_SETTINGS']['app_views'][_name] = {'app_conf': self}
            _class = _dict['view_class']
            _views = _dict['views']
            #print(_views)
            for route_name in _views.keys():
                print(route_name)
                # print(_class)
                webapp.router.add_view(route_name, _class)
