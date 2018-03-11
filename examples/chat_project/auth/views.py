import aiohttp
from aiohttp_jinja2 import render_template
from aiohttp_session import get_session

from aioframe.views import TemplateView
from aioframe.clients import get_request

from chat_project.conf import HOSTNAME, PORT, APPS_DIR, OBJECTS
from .app_conf import app
from .models import User, UserPermission


class Login(TemplateView):

    @app.route('login/', methods=['GET', 'POST'])
    async def login(request, *args, **kwargs):
        if request.method == 'POST':
            data = await request.post()
            try:
                user = await OBJECTS.get(User, username=data['username'], password=data['password'])
            except User.DoesNotExist:
                raise aiohttp.web.HTTPFound('/auth/login/')
            print(user)
        context = {}
        return render_template('login.html', request, context)


app_views = [Login]
