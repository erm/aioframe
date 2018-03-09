from aiohttp_jinja2 import render_template

from aioframe.views import TemplateView, WebsocketView

from .app_conf import app


class ChatView(TemplateView, WebsocketView):

    @app.route('msg/')
    def chat(request, *args, **kwargs):
        ws_route = 'localhost:8080/chat/ws/' # TODO: Get from context data
        return render_template('chat.html', request, {'ws_route': ws_route})


class OtherChatView(TemplateView, WebsocketView):

    @app.route('msg2/')
    def chat(request, *args, **kwargs):
        ws_route = 'localhost:8080/chat/ws/' # TODO: Get from context data
        return render_template('chat.html', request, {'ws_route': ws_route})


app_views = [ChatView, OtherChatView]
