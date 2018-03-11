import peewee_async

HOSTNAME = 'localhost'

PORT = '8080'

DATABASE = peewee_async.PooledPostgresqlDatabase(
    'test',
    user='',
    password='',
    host='localhost'
)
