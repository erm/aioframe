import aiohttp
from aiohttp_session import get_session
from passlib.hash import sha256_crypt

from .models import User
from ..sessions import generate_session_id


async def authenticate(request, username, password):
    session = await get_session(request)
    if session.get('AIOFRAME_AUTH_IDENTITY'):
        raise aiohttp.web.HTTPForbidden
    try:
        user = User.get(username=username)
    except User.DoesNotExist:
        raise aiohttp.web.HTTPForbidden
    is_verified = sha256_crypt.verify(password, user.password)
    if not is_verified:
        raise aiohttp.web.HTTPForbidden
    session_id = generate_session_id()
    session['AIOFRAME_AUTH_IDENTITY'] = {
        '_session_id': session_id.decode('utf-8').replace("'", '"'),
        'user_id': user.id
    }


def login_required(func):
    async def _login_required(request, *args, **kwargs):
        session = await get_session(request)
        if not session.get('AIOFRAME_AUTH_IDENTITY'):
            raise aiohttp.web.HTTPForbidden
        response = await func(request, *args, **kwargs)
        return response
    return _login_required
