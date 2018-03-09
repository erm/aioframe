from aiohttp_jinja2 import render_template

from aioframe.views import TemplateView, WebsocketView

from example_project.conf.settings import HOSTNAME, PORT
from .app_conf import app


class ChatView(TemplateView, WebsocketView):

    @app.route('room/{room_name}/')
    def chatroom(request, *args, **kwargs):
        room_name = request._match_info['room_name']
        ws_route = '{}:{}/chat/ws/{}/'.format(HOSTNAME, PORT, room_name)
        return render_template('chat.html', request, {'ws_route': ws_route})

app_views = [ChatView]
