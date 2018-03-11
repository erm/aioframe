import aiohttp
from aiohttp_session import get_session
from passlib.hash import sha256_crypt

from .models import User
from ..sessions import generate_session_id


async def get_user_by_session(session):
    identity = session.get('AIOFRAME_AUTH_IDENTITY')
    if not identity:
        raise aiohttp.web.HTTPForbidden
    user_id = identity['user_id']
    try:
        user = User.get(id=user_id)
    except User.DoesNotExist:
        raise aiohttp.web.HTTPForbidden
    return user


async def authenticate(session, conf, username, password):
    if session.get('AIOFRAME_AUTH_IDENTITY'):
        raise aiohttp.web.HTTPFound(conf.LOGIN_REDIRECT_URL)
    res = {'form_errors': None}
    try:
        user = User.get(username=username)
    except User.DoesNotExist:
        res['form_errors'] = 'User does not exist.'
        return res
    is_verified = sha256_crypt.verify(password, user.password)
    if not is_verified:
        res['form_errors'] = 'Invalid username or password'
        return res
    session_id = generate_session_id()
    session['AIOFRAME_AUTH_IDENTITY'] = {
        '_session_id': session_id.decode('utf-8').replace("'", '"'),
        'user_id': user.id
    }
    return res


def login_required(func):
    async def _login_required(request, *args, **kwargs):
        session = await get_session(request)
        if not session.get('AIOFRAME_AUTH_IDENTITY'):
            raise aiohttp.web.HTTPForbidden
        response = await func(request, *args, **kwargs)
        return response
    return _login_required
