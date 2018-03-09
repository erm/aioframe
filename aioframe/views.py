import aiohttp_jinja2
from aiohttp import web, WSMsgType
from aiohttp_session import get_session
import jinja2


class TemplateView:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self.webapp,
            loader=jinja2.PackageLoader(self.app.app_name, 'templates')
        )


class WebsocketView:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app.route('ws/{ws_group}/')(self.ws_handler)
        try:
            self.webapp['sockets']
        except KeyError:
            self.webapp['sockets'] = {}

    async def ws_handler(self, request):
        resp = web.WebSocketResponse()
        await resp.prepare(request)
        session = await get_session(request)
        ws_group = request._match_info['ws_group']
        try:
            request.app['sockets'][ws_group].append(resp)
        except KeyError:
            request.app['sockets'][ws_group] = [resp]
        async for msg in resp:
            if msg.type == web.WSMsgType.TEXT:
                for ws in request.app['sockets'][ws_group]:
                    if ws is not resp:
                        msg_data = '{}: {}'.format(session._created, msg.data)
                        await ws.send_str(msg_data)
            else:
                return resp
        return resp
