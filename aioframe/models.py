import peewee


DATABASE_PROXY = peewee.Proxy()


class BaseModel(peewee.Model):

    class Meta:
        database = DATABASE_PROXY
