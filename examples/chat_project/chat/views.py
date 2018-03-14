import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session

from aioframe.auth.utils import get_user_by_session, get_identity
from aioframe.views import TemplateView, WebsocketView, WebsocketBotView
from aioframe.clients import get_request
from aioframe.apps.routes import get_url

import random
import markovify

from chat_project.conf import HOSTNAME, PORT, APPS_DIR
from .apps import app


@app.route_class()
class ChatRoom(WebsocketView, TemplateView):

    @app.route('room/ws/{group_name}/', name='room_ws')
    async def ws_handler(self, *args, **kwargs):
        request = self._request
        response = await self.get_ws_response()
        session = await get_session(request)
        async for msg in response:
            if msg.type == aiohttp.web.WSMsgType.TEXT:
                msg_data = msg.data 
                identity = await get_identity(session)
                username = 'User ' + identity['_session_id'][:5]
                msg_resp = '{}: {}'.format(username, msg.data)
                for ws in self.ws_group['sockets']:
                    await ws.send_str(msg_resp)
        return response

    @app.route('room/{group_name}/', name='room')
    async def room(self, *args, **kwargs):
        request = self._request
        group_name = request._match_info['group_name']
        ws_url = get_url(request, 'room_ws', kwargs={'group_name': group_name}, is_ws=True)
        session = await get_session(request)
        # user = await get_user_by_session(session)
        identity = await get_identity(session)
        username = 'User ' + identity['_session_id'][:5]
        context = {
            'ws_url': ws_url,
            'title': 'Chatroom {}'.format(group_name),
            'user': '<{}>'.format(username)
        }
        return render_template('chat/chat.html', request, context)


@app.route_class()
class ChatBotRoom(WebsocketBotView, TemplateView):

    @app.route('botroom/ws/{group_name}/', name='botroom_ws')
    async def ws_handler(self, *args, **kwargs):
        request = self._request
        response = await self.get_ws_response()
        session = await get_session(request)
        async for msg in response:
            if msg.type == aiohttp.web.WSMsgType.TEXT:
                msg_data = msg.data 
                if msg_data and msg_data[0] == '!':
                    await self.ws_group['bot'].handle_msg(msg_data)
                else:
                    identity = await get_identity(session)
                    username = 'User ' + identity['_session_id'][:5]
                    msg_resp = '{}: {}'.format(username, msg.data)
                    for ws in self.ws_group['sockets']:
                        await ws.send_str(msg_resp)
        return response

    @app.route('botroom/{group_name}/', name='botroom')
    async def botroom(self, *args, **kwargs):
        request = self._request
        group_name = request._match_info['group_name']
        ws_url = get_url(request, 'botroom_ws', kwargs={'group_name': group_name}, is_ws=True)
        session = await get_session(request)
        # user = await get_user_by_session(session)
        identity = await get_identity(session)
        username = 'User ' + identity['_session_id'][:5]
        context = {
            'ws_url': ws_url,
            'title': 'Chatroom {}'.format(group_name),
            'user': '<{}>'.format(username)
        }
        return render_template('chat/chat.html', request, context)


# app_views = [ChatRoom, ChatBotRoom]
