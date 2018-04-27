from gino import Gino
from sanic import Sanic

from blog.util import Upload

db = Gino()
photo = Upload()


def create_app(config):
    app = Sanic(name='blog')
    app.config.from_object(config)

    photo.init_app(app)

    from blog.tasks import open_redis_connection, close_redis_connection

    app.listeners['before_server_start'].append(open_redis_connection)
    app.listeners['before_server_stop'].append(close_redis_connection)

    return app
