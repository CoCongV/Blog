# coding: utf-8
import os
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models.comments import Comment
from app.models.users import User
from app.models.posts import Post
from app.models.roles import Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Comment=Comment, Permission=Permission, Post=Post)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main':
    manager.run()