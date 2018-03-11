import os

import aiohttp_jinja2
from aiohttp import web
import jinja2


class TemplateView:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self.webapp,
            loader=jinja2.FileSystemLoader(os.path.join(self.conf.APPS_DIR, 'templates'))
        )


class WebsocketView:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.webapp['socket_groups']
        except KeyError:
            self.webapp['socket_groups'] = {}

    @classmethod
    def get_ws_group(cls, request, group_name):
        try:
            request.app['socket_groups'][group_name]
        except KeyError:
            request.app['socket_groups'][group_name] = {'sockets': [], 'data': {}}
        return request.app['socket_groups'][group_name]

    @classmethod
    async def get_ws_response(cls, request):
        response = web.WebSocketResponse()
        await response.prepare(request)
        group_name = request._match_info['group_name']
        ws_group = cls.get_ws_group(request, group_name)
        ws_group['sockets'].append(response)
        return response, ws_group
