import os

from aioframe.secrets import get_secret_key
# from aioframe.sessions import get_session_setup


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS_REGISTRY = (
    'chat_app',
)

SECRET_KEY = get_secret_key()

HOSTNAME = 'localhost'

PORT = '8000'
