from gino.ext.sanic import Gino
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic

from blog.util import Upload
from blog.util.whoosh import SanicIndexSerivce

db = Gino()
photo = Upload()
jinja_env = Environment(
    loader=PackageLoader('blog'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=True)
index_service = SanicIndexSerivce()


def create_app(config):
    app = Sanic(name='blog')
    app.config.from_object(config)

    db.init_app(app)
    photo.init_app(app)
    index_service.init_app(app)

    from blog.tasks import open_redis_connection, close_redis_connection

    app.listeners['before_server_start'].append(open_redis_connection)
    app.listeners['before_server_stop'].append(close_redis_connection)

    return app
