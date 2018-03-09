import aiohttp_jinja2
from aiohttp import web, WSMsgType
import jinja2


class TemplateView:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self.webapp,
            loader=jinja2.PackageLoader(self.app.app_name, 'templates')
        )


class WebsocketView:

    ws_handler_route = 'ws/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app.route(self.ws_handler_route)(self.ws_handler)

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg)
                if msg.data == 'close':
                    await ws.close()
                else:
                    reply = 'You said: {}'.format(msg.data)
                    await ws.send_str(reply)
            elif msg.type == WSMsgType.ERROR:
                print(ws.exception())
        return ws
