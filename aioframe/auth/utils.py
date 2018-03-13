import aiohttp
from aiohttp_session import get_session
from passlib.hash import sha256_crypt

from .models import User
from ..sessions import generate_session_id


async def get_identity(session):
    identity = session.get('AIOFRAME_AUTH_IDENTITY')
    if not identity:
        session_id = generate_session_id()
        identity = {
            '_session_id': session_id.decode('utf-8').replace("'", '"'),
            'user_id': None 
        }
        session['AIOFRAME_AUTH_IDENTITY'] = identity
    return identity


async def get_user_by_session(session):
    identity = await get_identity(session)
    user = None
    if identity['user_id']:
        try:
            user = User.get(id=user_id)
        except User.DoesNotExist:
            user = None
    return user


async def authenticate(session, conf, username, password):
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


# def login_required(func):
#     async def _login_required(self, *args, **kwargs):
#         session = await get_session(self._request)
#         if not session.get('AIOFRAME_AUTH_IDENTITY'):
#             raise aiohttp.web.HTTPForbidden
#         response = await func(self, *args, **kwargs)
#         return response
#     return _login_required


def create_user(username, password):
    password = sha256_crypt.hash(password)
    user = User.create(username=username, password=password, is_superuser=False, is_active=True)
