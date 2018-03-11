from passlib.hash import sha256_crypt

from ..auth.models import User


def run_command(conf, username, password):
    password = sha256_crypt.hash(password)
    user = User.create(username=username, password=password, is_superuser=True, is_active=True)
    print(user)
