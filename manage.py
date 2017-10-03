# coding: utf-8
import os
import time

from flask import g
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_whooshalchemyplus import whoosh_index
from gevent import wsgi
# from werkzeug import 

from app import create_app, db, make_celery, celery as celery_worker
from app.models.comments import Comment
from app.models.users import User
from app.models.posts import Post
from app.models.roles import Role, Permission

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()
if os.path.exists('.env'):
    print('Importing environment from .env')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
whoosh_index(app, Post)
admin = Admin(app, name='Cong Blog', template_mode="bootstrap3")
celery = make_celery(app, celery_worker)


@app.teardown_appcontext
def shutdown_session(exception=None):
    return db.session.remove()


@app.before_request
def record_time():
    g.start_time = time.time()


@app.after_request
def com_time(response):
    app.logger.info(time.time() - g.start_time)
    return response


def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Comment=Comment,
        Permission=Permission,
        Post=Post)


manager.add_command("shell",
                    Shell(use_ipython=True, make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    # server = wsgi.WSGIServer(('localhost', 5000), app)
    # server.serve_forever()
    manager.run()
