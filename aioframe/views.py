import aiohttp_jinja2
from aiohttp import web, WSMsgType
import jinja2

from aioframe.routes import Router


class View:

    def __init__(self, app_name, webapp):
        self.app_name = app_name
        self.webapp = webapp


class TemplateView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self.webapp, 
            loader=jinja2.PackageLoader(self.app_name, 'templates')
        )


class WebsocketView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        router = self.router
        router.route('/ws')(self.websocket_handler)

    async def websocket_handler(self, request):
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
