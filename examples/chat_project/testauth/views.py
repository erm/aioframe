import aiohttp
from aiohttp_jinja2 import render_template

from aioframe.auth.utils import authenticate, login_required
from aioframe.views import TemplateView

from .app_conf import app


class Auth(TemplateView):

    @app.route('login/', methods=['GET', 'POST'])
    async def login(request, *args, **kwargs):
        if request.method == 'POST':
            data = await request.post()
            username = data['username']
            password = data['password']
            await authenticate(request, username, password)
            raise aiohttp.web.HTTPFound('/testauth/dashboard/')

        context = {}
        return render_template('login.html', request, context)

    @app.route('dashboard/')
    @login_required
    async def dashboard(request, *args, **kwargs):
        context = {'user': 'test'}
        return render_template('dashboard.html', request, context)

app_views = [Auth]
