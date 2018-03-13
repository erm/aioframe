import os

from .apps.routes import get_reverse_match

import aiohttp_jinja2
from aiohttp import web
import jinja2


class View(web.View):

    """
    Class-based view that subclasses aiohttp.web.View to allow registering routes to functions
    within an aioframe app view.

    Looks up handlers by app view class and request path.
    """

    @property
    def view_class_name(self):
        return self.__class__.__qualname__

    async def __handle_request(self, method):
        request_path = self._request._rel_url.path
        match_info = self._request._match_info
        lookup_path = get_reverse_match(match_info) if match_info else request_path
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
            loader=jinja2.FileSystemLoader(os.path.join(
                self._request.app['AIOFRAME_SETTINGS']['conf'].APPS_DIR, 'templates'))
        )


class WebsocketView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws_group_name = self._request._match_info['group_name']
        try:
            self._request.app['socket_groups']
        except KeyError:
            self._request.app['socket_groups'] = {
                self.ws_group_name: {
                    'name': self.ws_group_name, 
                    'sockets': [], 
                    'data': {},
                    'bot': None
                }
            }
        self.ws_group = self._request.app['socket_groups'][self.ws_group_name]

    async def get_ws_response(self):
        response = web.WebSocketResponse()
        await response.prepare(self._request)
        self.ws_group['sockets'].append(response)
        return response


class WebsocketBot:

    def __init__(self, ws_group):
        self.ws_group = ws_group
        self.data = {}

    async def handle_msg(self, msg_data):
        print(msg_data)
        data = msg_data.split()
        print(data)
        for ws in self.ws_group['sockets']:
            msg_resp = 'lol'
            await ws.send_str(msg_resp)


class WebsocketBotView(WebsocketView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws_group['bot'] = WebsocketBot(self.ws_group)