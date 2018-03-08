from aiohttp import web, WSMsgType
from aiohttp_jinja2 import template

from aioframe.views import TemplateView, WebsocketView
from aioframe.routes import Router


class ChatView(TemplateView, WebsocketView):

    router = Router(namespace=None)

    @router.route('/chat')
    @template('chat.html')
    def chat(request, *args, **kwargs):
        return {}

app_views = ChatView
