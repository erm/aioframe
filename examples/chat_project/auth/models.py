import peewee

from chat_project.conf import DATABASE


class User(peewee.Model):

    id = peewee.IntegerField()
    username = peewee.CharField()
    password = peewee.CharField()
    is_superuser = peewee.BooleanField()
    is_active = peewee.BooleanField()

    class Meta:
        database = DATABASE


class UserPermission(peewee.Model):

    id = peewee.IntegerField()
    user_id = peewee.IntegerField()
    permission_name = peewee.CharField()

    class Meta:
        database = DATABASE

User.create_table(True)
UserPermission.create_table(True)
