import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session

from aioframe.views import TemplateView, WebsocketView
from aioframe.clients import get_request

import markovify

from chat_project.conf import HOSTNAME, PORT, APPS_DIR
from .app_conf import app


class ChatRoom(WebsocketView, TemplateView):

    @app.route('rooms/ws/{group_name}/')
    async def ws_handler(request, *args, **kwargs):
        response, ws_group = await __class__.get_ws_response(request)
        session = await get_session(request)
        # TODO: Implement sessions properly/user accounts
        async for msg in response:
            if msg.type == aiohttp.web.WSMsgType.TEXT:
                for ws in ws_group['sockets']:
                    name = '(You)' if ws is response else ''
                    msg_resp = 'User #{} {}: {}'.format(session.created, name, msg.data)
                    await ws.send_str(msg_resp)
        return response

    @app.route('rooms/{group_name}/')
    async def room(request, *args, **kwargs):
        group_name = request._match_info['group_name']
        ws_route = '{}:{}/chat_app/rooms/ws/{}/'.format(HOSTNAME, PORT, group_name)
        session = await get_session(request)
        context = {
            'ws_route': ws_route,
            'title': 'Chatroom {}'.format(group_name),
            'user': '(User #{}) '.format(session.created)
        }
        return render_template('chat.html', request, context)


class MarkovBot(WebsocketView, TemplateView):

    @classmethod
    async def get_data(cls, url):
        async with aiohttp.ClientSession() as session:
            text = await get_request(session, url)
            text_model = markovify.Text(text)
            return text_model

    @app.route('bots/markov/ws/{group_name}/')
    async def ws_handler(request, *args, **kwargs):
        response, ws_group = await __class__.get_ws_response(request)
        async for msg in response:
            ws_group_data = ws_group['data']
            # TODO: Properly implement command parsing/handling
            if msg.type == aiohttp.web.WSMsgType.TEXT:
                msg_data = msg.data.split()
                if msg_data[0] == 'getsrc' and ws_group_data:
                    src_url = ws_group_data['src_url']
                    msg_resp = 'This group already has data sourced from: {}'.format(src_url)
                elif msg_data[0] == 'getsrc':
                    ws_group_data = {}
                    src_url = msg_data[1]
                    try:
                        text_model = await __class__.get_data(src_url)
                    except aiohttp.client_exceptions.InvalidURL:
                        msg_resp = 'Invalid URL: {}'.format(src_url)
                    else:
                        ws_group_data['src_url'] = src_url
                        ws_group_data['text_model'] = text_model
                        ws_group['data'] = ws_group_data
                        msg_resp = 'Data sourced from: {}'.format(src_url)
                elif not ws_group_data:
                    msg_resp = 'No data source. Try "getsrc url.to.txt"'
                else:
                    text_model = ws_group['data']['text_model']
                    msg_resp = '{}'.format(text_model.make_sentence())
                await response.send_str(msg_resp)
        return response

    @app.route('bots/markov/{group_name}/')
    def markov(request, *args, **kwargs):
        group_name = request._match_info['group_name']
        # TODO: Implement method for building app routes
        ws_route = '{}:{}/chat_app/bots/markov/ws/{}/'.format(HOSTNAME, PORT, group_name)
        context = {
            'ws_route': ws_route,
            'title': 'MarkovBot {}'.format(group_name)
        }
        return render_template('chat.html', request, context)


app_views = [ChatRoom, MarkovBot]
