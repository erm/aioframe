from aiohttp import web, WSMsgType
from aiohttp_jinja2 import template

from aioframe.views import TemplateView
from aioframe.routes import Router


class WebsocketView(TemplateView):

    router = Router(namespace=None)

    @router.route('/ws')
    async def websocket_handler(request):
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

    @router.route('/chat')
    @template('chat.html')
    def chat(request, *args, **kwargs):
        return {}


app_views = WebsocketView
