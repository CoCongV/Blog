# coding: utf-8
import bleach
from markdown import markdown
from datetime import datetime

from app import db
from ..minixs import CRUDMixin


class Reply(db.Model, CRUDMixin):
    __tablename__ = 'replies'
    reply_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    replied_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Comment(db.Model, CRUDMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(length=1000))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    replied = db.relationship('Reply',
                              foreign_keys=[Reply.reply_id],
                              backref=db.backref('replies', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    replies = db.relationship('Reply',
                              foreign_keys=[Reply.replied_id],
                              backref=db.backref('replied', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

db.event.listen(Comment.body, 'set', Comment.on_change_body)