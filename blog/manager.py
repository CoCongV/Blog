import asyncio
import os

import click
from IPython import embed

try:
    import config as conf
except ImportError:
    from .config import config
    conf = config[os.getenv('BLOG_ENV') or 'default']

from blog import create_app
from blog.models import Role, User

app = create_app(conf)


@click.group()
def cli():
    click.echo('START BLOG MANAGER CLI')


@cli.command()
@click.option('--host', default='localhost')
@click.option('-p', '--port', default=8000)
@click.option('-d', '--debug', default=True)
@click.option('-a', '--access', default=True)
@click.option('-w', '--workers', default=1)
def runserver(host, port, debug, access, workers):
    from aoiklivereload import LiveReloader
    reloader = LiveReloader()
    reloader.start_watcher_thread()
    app.run(host, port, debug, workers=workers, access_log=access)


@cli.command()
def shell():
    embed(app=app)


@cli.command()
def deploy():
    loop = asyncio.get_event_loop()

    async def insert():
        await Role.insert_roles()
        user = await User.create(
            email='lv.cong@gmail.com',
            username='VCong',
            password='root',
            confirmed=True)
        role = await Role.query.where(name='Administrator').gino.first()
        await user.update(role=role).apply()

    loop.run_until_complete(insert())
