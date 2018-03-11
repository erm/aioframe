import peewee

from ..models import BaseModel


class User(BaseModel):

    username = peewee.CharField()
    password = peewee.CharField()
    is_superuser = peewee.BooleanField()
    is_active = peewee.BooleanField()


class UserPermission(BaseModel):

    user_id = peewee.IntegerField()
    permission_name = peewee.CharField()
