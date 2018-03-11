import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session
from playhouse.shortcuts import model_to_dict
from passlib.hash import sha256_crypt

from aioframe.views import TemplateView
from aioframe.clients import get_request
from aioframe.auth.models import User, UserPermission
from aioframe.sessions import generate_session_id

from chat_project.conf import HOSTNAME, PORT, APPS_DIR, OBJECTS
from .app_conf import app


class Auth(TemplateView):

    @app.route('login/', methods=['GET', 'POST'])
    async def login(request, *args, **kwargs):
        session = await get_session(request)
        identity = session.get('AIOFRAME_AUTH_IDENTITY')
        if identity:
            raise aiohttp.web.HTTPFound('/auth/dashboard/')
        if request.method == 'POST':
            data = await request.post()
            try:
                user = await OBJECTS.get(User, username=data['username'])
            except User.DoesNotExist:
                session['form_errors'] = 'Invalid login.'
                raise aiohttp.web.HTTPFound('/auth/login/')
            else:
                password = data['password']
                is_verified = sha256_crypt.verify(password, user.password)
                if not is_verified:
                    session['form_errors'] = 'Invalid password'
                    raise aiohttp.web.HTTPFound('/auth/login/')
                session_id = generate_session_id()
                session['AIOFRAME_AUTH_IDENTITY'] = {
                    '_session_id': session_id.decode('utf-8').replace("'", '"'),
                    'user': model_to_dict(user),
                }
                raise aiohttp.web.HTTPFound('/auth/dashboard/')
        form_errors = session.pop('form_errors', None)
        context = {'form_errors': form_errors}
        return render_template('login.html', request, context)

    @app.route('dashboard/')
    async def dashboard(request, *args, **kwargs):
        session = await get_session(request)
        identity = session.get('AIOFRAME_AUTH_IDENTITY')
        if not identity:
            raise aiohttp.web.HTTPFound('/auth/dashboard/')
        context = {'user': identity['user']}
        return render_template('dashboard.html', request, context)

app_views = [Auth]
