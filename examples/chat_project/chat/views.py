import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session

from aioframe.auth.utils import login_required, get_user_by_session, get_identity
from aioframe.views import TemplateView, WebsocketView
from aioframe.clients import get_request

import random
import markovify

from chat_project.conf import HOSTNAME, PORT, APPS_DIR
from .app_conf import app


class ChatBot:

    def __init__(self, ws_group):
        self.ws_group = ws_group
        self.data = {}

    async def handle_msg(self, msg_data):
        # TODO: clean this up lol
        response = {'msg': None}
        data = msg_data[1:].split()
        try:
            command = data[0]
        except IndexError:
            response['msg'] = response['msg'] = 'Error: Not enough arguments.'
        args = data[1:]
        if command == 'markovify':
            try:
                src_url = args[0]
            except IndexError:
                response['msg'] = 'Error: Not enough arguments.'
            else:
                try:
                    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                        text = await get_request(session, src_url)
                        text_model = markovify.Text(text)
                        self.data['markov'] = text_model
                except aiohttp.client_exceptions.InvalidURL:
                    response['msg'] = 'Error: Invalid URL provided.'
                else:
                    response['msg'] = 'Loaded data from {}'.format(src_url)
        elif command == 'talk':
            markov = self.data.get('markov')
            if not markov:
                response['msg'] = 'Error: No data loaded, try !markovify <http://source.txt>'
            else:
                sentences = [markov.make_sentence() for i in range(10)]
                sentences = list(set([s for s in sentences if s]))
                markov_msg = random.choice(sentences)
                response['msg'] = markov_msg
        else:
            response['msg'] = 'Error: valid commands are "markovify" and "talk"'
        return response


class ChatRoom(WebsocketView, TemplateView):

    @classmethod
    async def get_bot_handler(cls, ws_group, msg_data):
        bot = ws_group['bot']
        if not bot:
            bot = ws_group['bot'] = ChatBot(ws_group)
        response = await bot.handle_msg(msg_data)
        return response

    @app.route('rooms/ws/{group_name}/')
    async def ws_handler(request, *args, **kwargs):
        response, ws_group = await __class__.get_ws_response(request)
        session = await get_session(request)
        async for msg in response:
            if msg.type == aiohttp.web.WSMsgType.TEXT:
                msg_data = msg.data 
                if msg_data and msg_data[0] == '!':
                    bot_res = await __class__.get_bot_handler(ws_group, msg_data)
                    msg_resp = bot_res['msg']
                else:
                    identity = await get_identity(session)
                    username = 'User ' + identity['_session_id'][:5]
                    msg_resp = '{}: {}'.format(username, msg.data)
                for ws in ws_group['sockets']:
                    await ws.send_str(msg_resp)
        return response

    @app.route('rooms/{group_name}/')
    async def room(request, *args, **kwargs):
        group_name = request._match_info['group_name']
        ws_route = '{}:{}/chat/rooms/ws/{}/'.format(HOSTNAME, PORT, group_name)
        session = await get_session(request)
        # user = await get_user_by_session(session)
        identity = await get_identity(session)
        # Temp
        username = 'User ' + identity['_session_id'][:5]
        context = {
            'ws_route': ws_route,
            'title': 'Chatroom {}'.format(group_name),
            'user': '<{}>'.format(username)
        }
        return render_template('chat/chat.html', request, context)

app_views = [ChatRoom]
