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


# def get_user_model(database):
#     database_proxy.initialize(database)
#     model_class.create_table(True)
#     return model_class


# def get_user_permission_model(database, model_class=UserPermissionModel):
#     database_proxy.initialize(database)
#     model_class.create_table(True)
#     return model_class
