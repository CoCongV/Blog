import glob
import os
import sys
sys.path.insert(0, '.')
try:
    from config import Config as conf
except ImportError:
    from .config import config
    conf = config[os.getenv('LV_ENV') or 'default']

from flask import current_app
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_whooshalchemyplus import whoosh_index

from blog import create_app, db, make_celery, celery as celery_worker, migrate
from blog.models import (Comment, User, Post, Role, Permission, Author, Book,
                         AuthorBook, CategoryBook)

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

app = create_app(conf)
basedir = os.path.abspath(os.path.dirname(__file__))
manager = Manager(app)
whoosh_index(app, Post)
whoosh_index(app, Book)
whoosh_index(app, Author)
admin = Admin(app, name='Cong Blog', template_mode="bootstrap3")
celery = make_celery(app, celery_worker)

@app.teardown_appcontext
def shutdown_session(exception=None):
    return db.session.remove()


def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Comment=Comment,
        Permission=Permission,
        Post=Post,
        Book=Book,
        Author=Author)

manager.add_command("shell",
                    Shell(use_ipython=True, make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    Role.insert_roles()
    user = User(
        email='lv.cong@gmail.com',
        username='Lv Cong',
        password='5f4dcc3b5aa765d61d8327deb882cf99',
        confirmed=True)
    role = Role.query.filter_by(name='Administrator').first()
    user.role = role
    user.save()


@manager.command
def test(coverage=False):
    """Run the unit tests"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover(
        'blog/tests', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.option('-p', '--path', help='EBook dir path')
@manager.option('-c', '--creator', help="Creator for create ebook")
def load_ebook(path, creator):
    from sqlalchemy.exc import IntegrityError
    user = User.query.filter_by(email=creator).first()
    books_dest = current_app.config['UPLOADED_BOOKS_DEST']
    os.chdir(path)
    filetypes = ['txt', 'mobi', 'pdf', 'equb']
    for root, dirs, files in os.walk(path):
        for f in files:
            for t in filetypes:
                if f.endswith(t):
                    path = os.path.join(root, f)
                    filename = f.split('.')[0]
                    book = Book(name=filename, file=f, creator=user)
                    try:
                        book.save()
                    except IntegrityError:
                        continue
                    with open(path, 'rb') as origin_file:
                        data = origin_file.read()
                    write_path = os.path.join(books_dest, f)
                    with open(write_path, 'wb') as dest_file:
                        dest_file.write(data)
                                        


@manager.command
def del_ebooks():
    books = Book.query.filter()
    for b in books:
        b.delete()


def cli():
    manager.run()
