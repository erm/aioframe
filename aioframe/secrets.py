import base64
from cryptography import fernet


def get_secret_key():
    return base64.urlsafe_b64decode(fernet.Fernet.generate_key())
