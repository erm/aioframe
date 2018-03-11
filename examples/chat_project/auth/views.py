import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session
from playhouse.shortcuts import model_to_dict

from aioframe.auth.utils import authenticate, login_required, get_user_by_session, create_user
from aioframe.views import TemplateView

from chat_project import conf

from .app_conf import app


class Auth(TemplateView):

    @app.route('login/', methods=['GET', 'POST'])
    async def login(request, *args, **kwargs):
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
    async def signup(request, *args, **kwargs):
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
    @login_required
    async def dashboard(request, *args, **kwargs):
        session = await get_session(request)
        user = await get_user_by_session(session)
        context = {'user': model_to_dict(user)}
        return render_template('auth/dashboard.html', request, context)


app_views = [Auth]
