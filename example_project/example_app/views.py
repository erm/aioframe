from aiohttp import web, WSMsgType
from aiohttp_jinja2 import render_template

from aioframe.views import TemplateView, WebsocketView
from aioframe.routes import Router


class ChatView(TemplateView, WebsocketView):

    router = Router(namespace='chat')

    @router.route('msg/')
    def chat(request, *args, **kwargs):
        ctx = __class__.get_context()
        ws_route = '{}{}'.format(ctx.get_app_route(), ctx.ws_handler_route)
        return render_template('chat.html', request, {'ws_route': ws_route})

app_views = ChatView
