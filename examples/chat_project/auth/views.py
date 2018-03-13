import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session
from playhouse.shortcuts import model_to_dict

from aioframe.auth.utils import authenticate, get_user_by_session, create_user
from aioframe.views import View, TemplateView

from chat_project import conf

from .app_conf import app


@app.route_class('auth/')
class Auth(TemplateView):

    @app.route('login/', methods=['GET', 'POST'])
    async def login(self):
        request = self._request
        session = await get_session(request)
        if request.method == 'POST':
            data = await request.post()
            username = data['username']
            password = data['password']
            res = await authenticate(session, conf, username, password)
            if not res['form_errors']:
                raise aiohttp.web.HTTPFound('/auth/dashboard/')
            session['form_errors'] = res['form_errors']
        context = {'form_errors': session.pop('form_errors', None)}
        return render_template('auth/login.html', request, context)

    @app.route('signup/', methods=['GET', 'POST'])
    async def signup(self):
        request = self._request
        session = await get_session(request)
        if request.method == 'POST':
            data = await request.post()
            username = data['username']
            password = data['password']
            user = create_user(username, password)
            res = await authenticate(session, conf, username, password)
            if not res['form_errors']:
                raise aiohttp.web.HTTPFound('/auth/dashboard/')
            session['form_errors'] = res['form_errors']
        context = {'form_errors': session.pop('form_errors', None)}
        return render_template('auth/signup.html', request, context)

    @app.route('dashboard/')
    async def dashboard(self):
        request = self._request
        session = await get_session(request)
        user = await get_user_by_session(session)
        context = {'user': None}
        return render_template('auth/dashboard.html', request, context)


app_views = [Auth]
