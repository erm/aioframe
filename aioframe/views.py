import os

from .apps.routes import get_reverse_match

import aiohttp_jinja2
from aiohttp import web
import jinja2


class View(web.View):

    @property
    def view_class_name(self):
        return self.__class__.__qualname__

    async def __handle_request(self, method):
        request_path = self._request._rel_url.path
        match_info = self._request._match_info
        lookup_path = get_reverse_match(match_info) if match_info else request_path
        print(lookup_path)
        app_conf = self._request.app['AIOFRAME_SETTINGS']['app_views'][self.view_class_name]['app_conf']
        try:
            view = app_conf.get_views(self.view_class_name)[lookup_path]
        except KeyError:
            raise web.HTTPNotFound
        if method not in view['methods']:
            raise web.HTTPMethodNotAllowed
        handler = view['view_func']
        response = await handler(self)
        return response

    async def get(self):
        response = await self.__handle_request('GET')
        return response

    async def post(self):
        response = await self.__handle_request('POST')
        return response


class TemplateView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self._request.app,
            loader=jinja2.FileSystemLoader(os.path.join(self._request.app['AIOFRAME_SETTINGS']['conf'].APPS_DIR, 'templates'))
        )


class WebsocketView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._request.app['socket_groups']
        except KeyError:
            self._request.app['socket_groups'] = {}

    def get_ws_group(self, group_name):
        try:
            self._request.app['socket_groups'][group_name]
        except KeyError:
            self._request.app['socket_groups'][group_name] = {'name': group_name, 'sockets': [], 'data': {}, 'bot': None}
        return self._request.app['socket_groups'][group_name]

    async def get_ws_response(self):
        response = web.WebSocketResponse()
        await response.prepare(self._request)
        group_name = self._request._match_info['group_name']
        ws_group = self.get_ws_group(group_name)
        ws_group['sockets'].append(response)
        return response, ws_group
