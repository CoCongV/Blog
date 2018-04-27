# coding: utf-8
from flask_admin.contrib.sqlamodel import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from ..models import User, Comment, Post, Role
from .. import db
from manage import admin

admin.add_views(ModelView(User, db.session),
                ModelView(Comment, db),
                ModelView(Post, db.session),
                ModelView(Role, db.session))