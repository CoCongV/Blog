# coding: utf-8
from datetime import datetime

import bleach
from flask import url_for, current_app
from whoosh.analysis import SimpleAnalyzer

from markdown import markdown
from sqlalchemy.dialects import postgresql

from app import db
from app.models.minixs import CRUDMixin, Serializer


class Post(CRUDMixin, db.Model, Serializer):
    __tablename__ = 'posts'
    __searchable__ = ['body', 'title']
    __analyzer__ = SimpleAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.utcnow(), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.Column(postgresql.ARRAY(db.String(32)))
    view = db.Column(db.Integer, default=0)

    def __repr__(self):
        return str(self.json()).replace(',', '\n')

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(
            markdown(value, output_format='html')
        )

    def to_json(self, split=False):
        json_data = {
            "post_id": self.id,
            'tags': self.tags,
            "url": url_for('post.postview', id=self.id),
            "title": self.title,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'author': self.author.username,
            'avatar': self.author.avatar,
            'view': self.view
        }
        if split:
            json_data.update({'body_html': self.body_html[:500]})
        else:
            pagination = self.comments.order_by(db.desc('timestamp')).paginate(
                1, per_page=current_app.config['BLOG_COMMENT_PAGE'],
                error_out=False
            )
            comments = pagination.items
            _next = None
            if pagination.has_next:
                _next = url_for('comment.commentview', post=self.id, page=2)
            json_data.update({'body_html': self.body_html,
                              'author_url': url_for('user.user_profile', uid=self.author_id),
                              'comments': [i.to_json() for i in comments],
                              'next': _next})
        return json_data


db.event.listen(Post.body, 'set', Post.on_change_body)
