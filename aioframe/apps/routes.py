from ..exceptions import AppRouteURLKeyError


def get_url(request, name, kwargs={}, is_ws=False):
    resource = request.app.router[name]
    try:
        resource_path = resource.url_for(**kwargs) if kwargs else resource.url_for()
    except KeyError as e:
        raise AppRouteURLKeyError(e)
    conf = request.app['AIOFRAME_SETTINGS']['conf']
    if is_ws:
        url = '{}{}'.format(conf.WS_URL_ROOT, resource_path)
    else:
        url = '{}{}'.format(conf.URL_ROOT, resource_path)
    return url


def get_reverse_match(match_info):
    return match_info._route._resource._formatter
