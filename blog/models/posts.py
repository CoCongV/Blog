# coding: utf-8
from datetime import datetime

import bleach
from flask import url_for
from whoosh.analysis import SimpleAnalyzer

from markdown import markdown
from sqlalchemy.dialects import postgresql

from app import db, cache
from app.models.minixs import CRUDMixin, Serializer


class Post(CRUDMixin, db.Model, Serializer):
    __tablename__ = 'posts'
    __searchable__ = ['body', 'title']
    __analyzer__ = SimpleAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.utcnow(), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic',
        cascade='all, delete-orphan')
    tags = db.Column(postgresql.ARRAY(db.String(32)))
    view = db.Column(db.Integer, default=0)

    def __repr__(self):
        return str(self.json()).replace(',', '\n')

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(
            markdown(value, output_format='html')
        )

    @cache.memoize(timeout=300)
    def to_json(self, split=False):
        json_data = {
            "post_id": self.id,
            'tags': self.tags,
            "url": url_for('post.postview', post_id=self.id),
            "title": self.title,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'author': self.author.username,
            'avatar': self.author.avatar,
            'view': self.view
        }
        if split:
            json_data.update({'body_html': self.body_html[:500]})
        else:
            json_data.update({
                'body_html':
                self.body_html,
                'body':
                self.body,
                'author_url':
                url_for('user.user_profile', uid=self.author_id)
            })
        return json_data

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            Post.create(
                title='测试',
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                author_id=1,
                tags=['测试']
            )


db.event.listen(Post.body, 'set', Post.on_change_body)
