import asyncio
import time
import base64
import aiohttp_session
from cryptography import fernet

def get_secret_key():
    return base64.urlsafe_b64decode(fernet.Fernet.generate_key())
